import json
import sys
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.config import Settings  # noqa: E402
from app.services import ai, groq, openai_compat, openrouter  # noqa: E402

MATERIAL = (
    "Binary search halves the search space with each step, giving O(log n) "
    "time complexity. A hash table maps keys to values with average O(1) "
    "lookups. HTTPS adds TLS encryption to web communication."
)

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


class FakeResponse:
    def __init__(self, status_code: int, payload):
        self.status_code = status_code
        if isinstance(payload, str):
            self._text = payload
            self.text = payload
        else:
            self._text = json.dumps(payload)
            self.text = self._text

    def json(self):
        return json.loads(self._text)


def ok_completion(content: str) -> FakeResponse:
    return FakeResponse(
        200,
        {"choices": [{"message": {"content": content}}]},
    )


QUIZ_JSON = json.dumps(
    {
        "questions": [
            {
                "question": "What does binary search do each step?",
                "options": ["Halves the space", "Doubles", "Linear scan", "Sorts"],
                "correct_answer": 0,
                "explanation": "It halves the search space each step.",
            }
        ]
    }
)


class ProviderRoutingTests(unittest.TestCase):
    def _mock_post(self, content: str = QUIZ_JSON, status: int = 200):
        patcher = mock.patch.object(openai_compat.httpx, "post")
        mock_post = patcher.start()
        self.addCleanup(patcher.stop)
        if status == 200:
            mock_post.return_value = ok_completion(content)
        else:
            mock_post.return_value = FakeResponse(
                status, {"error": {"message": content}}
            )
        return mock_post

    @mock.patch.object(groq.settings, "groq_api_key", "groq-test-key")
    def test_groq_quiz_routes_to_groq_url_and_model(self):
        mock_post = self._mock_post()
        generated_by, questions, error_detail = ai.generate_quiz(
            MATERIAL, "medium", 1, provider="groq", model_name="openai/gpt-oss-20b"
        )
        self.assertEqual(generated_by, "ai")
        self.assertEqual(error_detail, "")
        self.assertEqual(questions[0]["correct_answer"], 0)
        self.assertEqual(len(questions[0]["options"]), 4)

        call = mock_post.call_args
        self.assertEqual(call.args[0], GROQ_URL)
        self.assertEqual(call.kwargs["headers"]["Authorization"], "Bearer groq-test-key")
        self.assertEqual(call.kwargs["json"]["model"], "openai/gpt-oss-20b")
        self.assertEqual(call.kwargs["json"]["response_format"], {"type": "json_object"})

    @mock.patch.object(openrouter.settings, "openrouter_api_key", "or-test-key")
    def test_openrouter_uses_free_default_model(self):
        mock_post = self._mock_post()
        generated_by, _, error_detail = ai.generate_quiz(
            MATERIAL, "easy", 1, provider="openrouter"
        )
        self.assertEqual(generated_by, "ai")
        self.assertEqual(error_detail, "")
        call = mock_post.call_args
        self.assertEqual(call.args[0], OPENROUTER_URL)
        self.assertEqual(call.kwargs["json"]["model"], "openrouter/free")

    @mock.patch.object(groq.settings, "groq_api_key", "groq-test-key")
    def test_flashcards_and_notes_use_groq(self):
        cards_resp = ok_completion(
            '{"flashcards": [{"front": "What is a hash table?", "back": "Maps keys to values."}]}'
        )
        notes_resp = ok_completion(
            '{"title": "T", "summary": "S", '
            '"sections": [{"heading": "H", "content": "C", "bullet_points": []}], '
            '"key_concepts": [{"term": "Hash table", "definition": "Maps keys."}]}'
        )
        with mock.patch.object(openai_compat.httpx, "post") as mock_post:
            mock_post.side_effect = [cards_resp, notes_resp]
            generated_by, cards, _ = ai.generate_flashcards(
                MATERIAL, count=1, provider="groq"
            )
            _, notes, _ = ai.generate_study_notes(MATERIAL, provider="groq")
        self.assertEqual(generated_by, "ai")
        self.assertEqual(cards[0]["front"], "What is a hash table?")
        self.assertEqual(notes["key_concepts"][0]["term"], "Hash table")
        self.assertEqual(mock_post.call_args_list[0].args[0], GROQ_URL)

    @mock.patch.object(groq.settings, "groq_api_key", "groq-test-key")
    def test_openai_compat_parses_fenced_json(self):
        self._mock_post(content="```json\n" + QUIZ_JSON + "\n```")
        generated_by, questions, _ = ai.generate_quiz(
            MATERIAL, "medium", 1, provider="groq"
        )
        self.assertEqual(generated_by, "ai")
        self.assertEqual(len(questions), 1)

    @mock.patch.object(openrouter.settings, "openrouter_api_key", "or-test-key")
    def test_openrouter_retries_without_json_mode_when_unsupported(self):
        reject = FakeResponse(
            400,
            {"error": {"message": "model does not support response_format json_object"}},
        )
        ok = ok_completion(QUIZ_JSON)
        mock_post = mock.Mock(side_effect=[reject, ok])
        with mock.patch.object(openai_compat.httpx, "post", mock_post):
            generated_by, questions, error_detail = ai.generate_quiz(
                MATERIAL, "medium", 1, provider="openrouter"
            )
        self.assertEqual(generated_by, "ai")
        self.assertEqual(error_detail, "")
        self.assertEqual(len(questions), 1)
        self.assertEqual(mock_post.call_count, 2)
        self.assertNotIn("response_format", mock_post.call_args_list[1].kwargs["json"])

    @mock.patch.object(groq.settings, "groq_api_key", "groq-test-key")
    def test_malformed_completion_falls_back(self):
        self._mock_post(
            content=json.dumps({"choices": [{"message": {}}]})
        )
        generated_by, questions, error_detail = ai.generate_quiz(
            MATERIAL, "medium", 1, provider="groq"
        )
        self.assertEqual(generated_by, "mock")
        self.assertTrue(error_detail)
        self.assertEqual(len(questions), 1)


class FailureFallbackTests(unittest.TestCase):
    def _mock_error(self, status: int, message: str):
        patcher = mock.patch.object(openai_compat.httpx, "post")
        mock_post = patcher.start()
        self.addCleanup(patcher.stop)
        mock_post.return_value = FakeResponse(status, {"error": {"message": message}})
        return mock_post

    def test_missing_groq_key_falls_back_with_hint(self):
        with mock.patch.object(groq.settings, "groq_api_key", ""):
            generated_by, questions, error_detail = ai.generate_quiz(
                MATERIAL, "medium", 2, provider="groq"
            )
        self.assertEqual(generated_by, "mock")
        self.assertIn("GROQ_API_KEY", error_detail)
        self.assertIn("backend/.env", error_detail)
        self.assertEqual(len(questions), 2)

    def test_missing_openrouter_key_falls_back_with_hint(self):
        with mock.patch.object(openrouter.settings, "openrouter_api_key", ""):
            generated_by, _, error_detail = ai.generate_flashcards(
                MATERIAL, count=2, provider="openrouter"
            )
        self.assertEqual(generated_by, "mock")
        self.assertIn("OPENROUTER_API_KEY", error_detail)

    @mock.patch.object(openrouter.settings, "openrouter_api_key", "or-key")
    def test_unavailable_free_model_falls_back(self):
        self._mock_error(404, "The free model is no longer available.")
        generated_by, questions, error_detail = ai.generate_quiz(
            MATERIAL, "medium", 2, provider="openrouter", model_name="openrouter/free"
        )
        self.assertEqual(generated_by, "mock")
        self.assertIn("unavailable", error_detail.lower())
        self.assertEqual(len(questions), 2)

    @mock.patch.object(groq.settings, "groq_api_key", "groq-test-key")
    def test_unsupported_model_falls_back(self):
        self._mock_error(404, "model_not_found")
        generated_by, _, error_detail = ai.generate_quiz(
            MATERIAL, "medium", 2, provider="groq", model_name="openai/gpt-oss-does-not-exist"
        )
        self.assertEqual(generated_by, "mock")
        self.assertIn("openai/gpt-oss-does-not-exist", error_detail)

    @mock.patch.object(groq.settings, "groq_api_key", "groq-test-key")
    def test_rate_limit_falls_back(self):
        self._mock_error(429, "Rate limit reached")
        generated_by, _, error_detail = ai.generate_quiz(
            MATERIAL, "medium", 2, provider="groq"
        )
        self.assertEqual(generated_by, "mock")
        self.assertIn("rate", error_detail.lower())

    @mock.patch.object(groq.settings, "groq_api_key", "groq-test-key")
    def test_invalid_api_key_falls_back(self):
        self._mock_error(401, "Invalid API key")
        generated_by, _, error_detail = ai.generate_quiz(
            MATERIAL, "medium", 2, provider="groq"
        )
        self.assertEqual(generated_by, "mock")
        self.assertIn("api key", error_detail.lower())

    @mock.patch.object(groq.settings, "groq_api_key", "groq-test-key")
    def test_provider_5xx_falls_back(self):
        self._mock_error(500, "internal error")
        generated_by, _, error_detail = ai.generate_quiz(
            MATERIAL, "medium", 2, provider="groq"
        )
        self.assertEqual(generated_by, "mock")
        self.assertIn("500", error_detail)

    @mock.patch.object(groq.settings, "groq_api_key", "groq-test-key")
    def test_network_timeout_falls_back(self):
        patcher = mock.patch.object(openai_compat.httpx, "post")
        mock_post = patcher.start()
        self.addCleanup(patcher.stop)
        mock_post.side_effect = openai_compat.httpx.TimeoutException("timed out")
        generated_by, _, error_detail = ai.generate_chat_reply(
            MATERIAL, [{"role": "user", "content": "hi"}], provider="groq"
        )
        self.assertEqual(generated_by, "mock")
        self.assertTrue(error_detail)


class ModelRegistrationTests(unittest.TestCase):
    def test_groq_models_listed(self):
        with mock.patch.object(
            groq.settings,
            "groq_model",
            "openai/gpt-oss-20b",
        ), mock.patch.object(
            groq.settings,
            "groq_model_strong",
            "openai/gpt-oss-120b",
        ):
            models = groq.list_models()
        self.assertEqual(len(models), 2)
        self.assertEqual(models[0]["name"], "openai/gpt-oss-20b")
        self.assertEqual(models[1]["name"], "openai/gpt-oss-120b")
        self.assertTrue(all(m["provider"] == "groq" for m in models))

    def test_openrouter_free_models_configurable(self):
        with mock.patch.object(
            openrouter.settings,
            "openrouter_model",
            "openrouter/free",
        ), mock.patch.object(
            openrouter.settings,
            "openrouter_free_models",
            "meta-llama/llama-3.3-70b-instruct:free, deepseek/deepseek-chat-v3-0324:free",
        ):
            models = openrouter.list_models()
        names = [m["name"] for m in models]
        self.assertEqual(names[0], "openrouter/free")
        self.assertIn("meta-llama/llama-3.3-70b-instruct:free", names)
        self.assertIn("deepseek/deepseek-chat-v3-0324:free", names)
        self.assertTrue(all(m["provider"] == "openrouter" for m in models))

    def test_openai_compat_json_mode_fallback_detector(self):
        exc = openai_compat.ProviderError(
            "400: model does not support response_format json_object"
        )
        self.assertTrue(openai_compat._unsupported_json_mode(exc))
        exc2 = openai_compat.ProviderError("500: broken")
        self.assertFalse(openai_compat._unsupported_json_mode(exc2))


class EnvConfigTests(unittest.TestCase):
    def test_provider_settings_read_env_defaults(self):
        with mock.patch.dict(
            "os.environ",
            {
                "GROQ_API_KEY": "env-groq",
                "GROQ_MODEL": "openai/gpt-oss-20b",
                "GROQ_MODEL_STRONG": "openai/gpt-oss-120b",
                "OPENROUTER_API_KEY": "env-or",
                "OPENROUTER_MODEL": "openrouter/free",
                "OPENROUTER_FREE_MODELS": "meta-llama/llama-3.3-70b-instruct:free",
            },
            clear=False,
        ):
            s = Settings(_env_file=None)
        self.assertEqual(s.groq_api_key, "env-groq")
        self.assertEqual(s.groq_model, "openai/gpt-oss-20b")
        self.assertEqual(s.groq_model_strong, "openai/gpt-oss-120b")
        self.assertEqual(s.openrouter_api_key, "env-or")
        self.assertEqual(s.openrouter_model, "openrouter/free")
        self.assertEqual(
            s.openrouter_free_models, "meta-llama/llama-3.3-70b-instruct:free"
        )


if __name__ == "__main__":
    unittest.main()