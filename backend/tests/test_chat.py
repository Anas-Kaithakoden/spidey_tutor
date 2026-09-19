import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.services import quick  # noqa: E402
from app.services.ai import generate_chat_reply  # noqa: E402

MATERIAL = (
    "Binary search halves the search space with each step, giving O(log n) "
    "time complexity. A hash table maps keys to values with average O(1) "
    "lookups. A stack follows LIFO ordering: the last element pushed is the "
    "first to be popped. DNS translates domain names into IP addresses. "
    "HTTPS adds TLS encryption to web communication. The OS scheduler "
    "allocates CPU time to processes. Normalization reduces database "
    "redundancy."
)


class QuickChatReplyTests(unittest.TestCase):
    def test_answers_from_material(self):
        history = [{"role": "user", "content": "How does binary search work?"}]
        reply = quick.generate_chat_reply(MATERIAL, history)
        self.assertTrue(reply)
        self.assertIn("binary search", reply.lower())

    def test_answer_is_grounded_in_material(self):
        for question in (
            "What does DNS do?",
            "Explain HTTPS.",
            "What is a stack?",
        ):
            reply = quick.generate_chat_reply(
                MATERIAL, [{"role": "user", "content": question}]
            )
            self.assertTrue(reply)
            self.assertIn(reply.lower().rstrip("."), MATERIAL.lower())

    def test_says_unavailable_when_material_lacks_answer(self):
        history = [{"role": "user", "content": "What is the capital of France?"}]
        reply = quick.generate_chat_reply(MATERIAL, history)
        self.assertIn("not", reply.lower())
        self.assertIn("uploaded material", reply.lower())

    def test_follow_up_uses_conversation_context(self):
        history = [
            {"role": "user", "content": "What does DNS do?"},
            {"role": "assistant", "content": "It translates domain names into IP addresses."},
            {"role": "user", "content": "And what does HTTPS add to it?"},
        ]
        reply = quick.generate_chat_reply(MATERIAL, history)
        self.assertIn("tls", reply.lower())

    def test_latest_question_supersedes_earlier_context(self):
        history = [
            {"role": "user", "content": "How does binary search work?"},
            {"role": "assistant", "content": "It halves the search space each step."},
            {"role": "user", "content": "What does HTTPS add to web communication?"},
        ]
        reply = quick.generate_chat_reply(MATERIAL, history)
        self.assertIn("tls", reply.lower())

    def test_foreign_topic_after_context_is_not_answered(self):
        history = [
            {"role": "user", "content": "How does binary search work?"},
            {"role": "assistant", "content": "It halves the search space each step."},
            {"role": "user", "content": "Who wrote the novel Hamlet?"},
        ]
        reply = quick.generate_chat_reply(MATERIAL, history)
        self.assertIn("uploaded material", reply.lower())
        self.assertIn("not", reply.lower())

    def test_empty_material_is_handled(self):
        reply = quick.generate_chat_reply("", [{"role": "user", "content": "Hello?"}])
        self.assertIn("material", reply.lower())

    def test_deterministic_same_input_same_output(self):
        history = [{"role": "user", "content": "How does binary search work?"}]
        self.assertEqual(
            quick.generate_chat_reply(MATERIAL, history),
            quick.generate_chat_reply(MATERIAL, history),
        )


class ChatDispatchTests(unittest.TestCase):
    def test_quick_stamps_and_grounded(self):
        generated_by, reply, error_detail = generate_chat_reply(
            MATERIAL,
            [{"role": "user", "content": "What is a hash table?"}],
            provider="quick",
        )
        self.assertEqual(generated_by, "quick")
        self.assertEqual(error_detail, "")
        self.assertIn("hash table", reply.lower())

    def test_unknown_provider_falls_back_to_mock_still_grounded(self):
        generated_by, reply, error_detail = generate_chat_reply(
            MATERIAL,
            [{"role": "user", "content": "What is binary search?"}],
            provider="bogus",
        )
        self.assertEqual(generated_by, "mock")
        self.assertTrue(error_detail)
        self.assertIn("binary search", reply.lower())

    def test_mock_fallback_says_unavailable_for_foreign_topic(self):
        generated_by, reply, _ = generate_chat_reply(
            MATERIAL,
            [{"role": "user", "content": "Who wrote Hamlet?"}],
            provider="bogus",
        )
        self.assertEqual(generated_by, "mock")
        self.assertIn("uploaded material", reply.lower())

    def test_empty_material_is_handled_gracefully(self):
        generated_by, reply, _ = generate_chat_reply(
            "", [{"role": "user", "content": "Hello?"}], provider="quick"
        )
        self.assertEqual(generated_by, "quick")
        self.assertIn("material", reply.lower())


if __name__ == "__main__":
    unittest.main()