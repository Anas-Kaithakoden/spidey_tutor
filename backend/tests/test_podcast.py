import base64
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.config import settings  # noqa: E402
from app.database import Base, get_db  # noqa: E402
from app.main import app  # noqa: E402
from app.models import (  # noqa: E402
    Material,
    PodcastEpisode,
    Quiz,
    QuizResult,
)
from app.schemas import (  # noqa: E402
    PODCAST_MAX_DURATION_MINUTES,
    PODCAST_MODES,
    CreatePodcast,
)
from app.services import audio as audio_service  # noqa: E402
from app.services import podcast as podcast_service  # noqa: E402
from app.services.quick import generate_podcast_script as quick_script  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

BASE_MATERIAL = (
    "Binary search halves the search space with each step, giving O(log n) "
    "time complexity. A hash table maps keys to values with average O(1) "
    "lookups. A stack follows LIFO ordering: the last element pushed is the "
    "first to be popped. DNS translates domain names into IP addresses. "
    "HTTPS adds TLS encryption to web communication. The OS scheduler "
    "allocates CPU time to processes. Normalization reduces database "
    "redundancy. HTTP requests are sent over TCP connections."
)

RICH_MATERIAL = " ".join(
    BASE_MATERIAL
    + (
        " A binary tree stores nodes in hierarchical order. A queue is FIFO. "
        "Graph algorithms rely on adjacency lists. Recursion calls a function "
        "from within itself. A database index speeds up lookups. Transactions "
        "guarantee atomicity. A deadlock stalls concurrent processes. "
        "Quicksort partitions an array around a pivot. Heaps implement priority "
    )
    for _ in range(8)
)

TTS_WAV = audio_service._wav_bytes_from_pcm(b"\x00\x00" * 6000, 24000)
TTS_MOCK_RETURN = ("audio/wav", base64.b64encode(TTS_WAV).decode(), "mock-tts")


def _assert_alternation(testcase, lines):
    speakers = [line["speaker"] for line in lines]
    testcase.assertEqual(set(speakers), {"host_one", "host_two"})
    run = 1
    for prev, curr in zip(speakers, speakers[1:]):
        run = run + 1 if prev == curr else 1
        testcase.assertLessEqual(run, 2, "a host held 3+ consecutive turns")


class BudgetTests(unittest.TestCase):
    def test_max_words_scales_with_duration(self):
        self.assertEqual(podcast_service.max_words_for(5), 5 * 165)
        self.assertEqual(podcast_service.max_words_for(10), 10 * 165)
        self.assertGreater(
            podcast_service.max_words_for(10), podcast_service.max_words_for(2)
        )

    def test_word_target_sits_below_cap(self):
        for m in (1, 2, 5, 10):
            self.assertLess(
                podcast_service.target_word_count(m),
                podcast_service.max_words_for(m),
            )

    def test_min_words_and_lines_stay_sane(self):
        self.assertEqual(podcast_service.min_lines_for(1), 6)
        self.assertGreaterEqual(podcast_service.min_lines_for(10), 30)
        self.assertLess(
            podcast_service.min_words_for(2), podcast_service.max_words_for(2)
        )

    def test_modes_are_covered_by_labels(self):
        for mode in PODCAST_MODES:
            self.assertTrue(podcast_service.MODE_LABELS[mode])


class ScriptSchemaTests(unittest.TestCase):
    def _valid_raw(self, title="My Episode", line_count=16, words_per_line=15):
        lines = [
            {
                "speaker": "host_one" if i % 2 == 0 else "host_two",
                "text": ("study words " * words_per_line).strip(),
            }
            for i in range(line_count)
        ]
        return {"title": title, "lines": lines}

    def test_valid_script_passes(self):
        script = podcast_service._validate_script(self._valid_raw(), 5)
        self.assertEqual(script.title, "My Episode")
        self.assertEqual(len(script.lines), 16)

    def test_missing_title_uses_fallback(self):
        raw = self._valid_raw(line_count=10, words_per_line=4)
        del raw["title"]
        script = podcast_service._validate_script(raw, 1, fallback_title="Fallback 1")
        self.assertEqual(script.title, "Fallback 1")

    def test_missing_title_and_fallback_rejected(self):
        raw = self._valid_raw(line_count=10)
        del raw["title"]
        with self.assertRaises(ValueError):
            podcast_service._validate_script(raw, 1)

    def test_not_an_object_rejected(self):
        with self.assertRaises(ValueError):
            podcast_service._validate_script(["lines"], 5)
        with self.assertRaises(ValueError):
            podcast_service._validate_script(None, 5)

    def test_blank_line_rejected(self):
        raw = self._valid_raw()
        raw["lines"][0]["text"] = "   "
        with self.assertRaises(ValueError):
            podcast_service._validate_script(raw, 5)

    def test_missing_host_rejected(self):
        raw = self._valid_raw()
        for i, line in enumerate(raw["lines"]):
            line["speaker"] = "host_one"
        with self.assertRaises(ValueError):
            podcast_service._validate_script(raw, 5)

    def test_three_consecutive_speaker_rejected(self):
        raw = self._valid_raw()
        raw["lines"][0]["speaker"] = "host_one"
        raw["lines"][1]["speaker"] = "host_one"
        raw["lines"][2]["speaker"] = "host_one"
        with self.assertRaises(ValueError):
            podcast_service._validate_script(raw, 5)

    def test_too_short_for_duration_rejected(self):
        raw = self._valid_raw(line_count=8, words_per_line=5)
        with self.assertRaises(ValueError):
            podcast_service._validate_script(raw, 10)

    def test_over_budget_rejected(self):
        raw = {
            "title": "Long",
            "lines": [
                {"speaker": ("host_one" if i % 2 == 0 else "host_two"),
                 "text": ("word " * 60).strip()}
                for i in range(20)
            ],
        }
        with self.assertRaises(ValueError):
            podcast_service._validate_script(raw, 5)

    def test_line_over_cap_rejected(self):
        raw = self._valid_raw(words_per_line=150)
        with self.assertRaises(ValueError):
            podcast_service._validate_script(raw, 10)


class QuickGenerationTests(unittest.TestCase):
    def test_deterministic_and_tagged(self):
        a = podcast_service.generate_podcast_script(
            RICH_MATERIAL, mode="learn", duration_minutes=5, provider="quick"
        )
        b = podcast_service.generate_podcast_script(
            RICH_MATERIAL, mode="learn", duration_minutes=5, provider="quick"
        )
        self.assertEqual(a[1], b[1])
        self.assertEqual(a[0], "quick")
        self.assertEqual(a[2], "")

    def test_both_hosts_alternate(self):
        for mode in PODCAST_MODES:
            _, script, _ = podcast_service.generate_podcast_script(
                RICH_MATERIAL, mode=mode, duration_minutes=5, provider="quick"
            )
            _assert_alternation(self, script["lines"])

    def test_grounded_in_material_only(self):
        material = (
            "Quasiparticles emerge in condensed matter physics. "
            "Ultrasonography uses sound waves for imaging. "
            "The Hall effect deflects charge carriers sideways."
        )
        generated_by, script, _ = podcast_service.generate_podcast_script(
            material, mode="learn", duration_minutes=2, provider="quick"
        )
        self.assertEqual(generated_by, "quick")
        joined = " ".join(line["text"] for line in script["lines"]).lower()
        self.assertIn("quasiparticle", joined)
        self.assertIn("ultrasonography", joined)
        self.assertNotIn("thoractometer", joined)

    def test_focus_topic_appears_in_title(self):
        _, script, _ = podcast_service.generate_podcast_script(
            RICH_MATERIAL,
            mode="learn",
            duration_minutes=2,
            provider="quick",
            focus_topic="hash table",
        )
        self.assertIn("hash table", script["title"].lower())

    def test_word_budget_respected(self):
        for minutes in (2, 5, 10):
            _, script, _ = podcast_service.generate_podcast_script(
                RICH_MATERIAL, mode="learn", duration_minutes=minutes,
                provider="quick",
            )
            words = sum(len(line["text"].split()) for line in script["lines"])
            self.assertLessEqual(
                words, podcast_service.max_words_for(minutes), f"{minutes} min over budget"
            )
            self.assertGreaterEqual(
                words, podcast_service.min_words_for(minutes), f"{minutes} min too short"
            )

    def test_weak_topics_reorders_discussion(self):
        weak = [{"title": "deadlock", "average_score": 30, "questions_answered": 4}]
        _, script, _ = podcast_service.generate_podcast_script(
            RICH_MATERIAL,
            mode="weak_topics",
            duration_minutes=3,
            provider="quick",
            weak_topics=weak,
        )
        joined = " ".join(line["text"] for line in script["lines"]).lower()
        self.assertIn("deadlock", joined)

    def test_unknown_provider_falls_back_to_mock(self):
        generated_by, script, error_detail = podcast_service.generate_podcast_script(
            RICH_MATERIAL, mode="learn", duration_minutes=2, provider="bogus"
        )
        self.assertEqual(generated_by, "mock")
        self.assertTrue(error_detail)
        self.assertGreaterEqual(len(script["lines"]), 2)
        _assert_alternation(self, script["lines"])

    @mock.patch.object(podcast_service, "_provider_generate_json")
    def test_invalid_ai_script_falls_back_to_mock(self, mock_gen):
        mock_gen.return_value = {"title": "Bad", "lines": []}
        generated_by, script, error_detail = podcast_service.generate_podcast_script(
            RICH_MATERIAL, mode="learn", duration_minutes=2, provider="gemini"
        )
        self.assertEqual(generated_by, "mock")
        self.assertTrue(error_detail)
        self.assertTrue(script["lines"])


class SynthesizePodcastAudioTests(unittest.TestCase):
    def test_uses_two_voices_and_builds_wav(self):
        lines = [
            {"speaker": "host_one", "text": "Welcome to the show."},
            {"speaker": "host_two", "text": "Glad to be here."},
            {"speaker": "host_one", "text": "Let's begin."},
        ]
        with mock.patch.object(
            audio_service, "generate_tts_audio", return_value=TTS_MOCK_RETURN
        ) as tts:
            mime, wav = audio_service.synthesize_podcast_audio(
                lines, voice_one="Kore", voice_two="Puck"
            )
        self.assertEqual(mime, "audio/wav")
        self.assertTrue(wav.startswith(b"RIFF"))
        self.assertGreater(audio_service.podcast_duration_seconds(wav), 0.0)
        self.assertEqual(tts.call_count, 3)
        kwargs_one = [c.kwargs for c in tts.call_args_list if c.kwargs.get("voice_name") == "Kore"]
        kwargs_two = [c.kwargs for c in tts.call_args_list if c.kwargs.get("voice_name") == "Puck"]
        self.assertEqual(len(kwargs_one), 2)
        self.assertEqual(len(kwargs_two), 1)

    def test_empty_lines_raise(self):
        with self.assertRaises(ValueError):
            audio_service.synthesize_podcast_audio([])


class CreatePodcastSchemaTests(unittest.TestCase):
    def test_duration_limits(self):
        self.assertEqual(CreatePodcast(material_id=1).duration_minutes, 5)
        self.assertEqual(
            1, CreatePodcast(material_id=1, duration_minutes=1).duration_minutes
        )
        self.assertEqual(
            PODCAST_MAX_DURATION_MINUTES,
            CreatePodcast(material_id=1, duration_minutes=PODCAST_MAX_DURATION_MINUTES).duration_minutes,
        )
        for bad in (0, -3, 11, 100):
            with self.assertRaises(Exception):
                CreatePodcast(material_id=1, duration_minutes=bad)
        with self.assertRaises(Exception):
            CreatePodcast(
                material_id=1,
                duration_minutes=1,
                mode="nonsense",
            )


class PodcastApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmpdir = tempfile.TemporaryDirectory()
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker

        cls.engine = create_engine(
            f"sqlite:///{Path(cls.tmpdir.name) / 'podcast_test.db'}",
            connect_args={"check_same_thread": False},
        )
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)

        def override_get_db():
            db = cls.Session()
            try:
                yield db
            finally:
                db.close()

        app.dependency_overrides[get_db] = override_get_db
        cls.old_media_dir = settings.podcast_media_dir
        settings.podcast_media_dir = str(Path(cls.tmpdir.name) / "media")

    @classmethod
    def tearDownClass(cls):
        app.dependency_overrides.pop(get_db, None)
        settings.podcast_media_dir = cls.old_media_dir
        cls.engine.dispose()
        cls.tmpdir.cleanup()

    def setUp(self):
        from sqlalchemy import delete

        with self.Session() as db:
            db.execute(delete(PodcastEpisode))
            db.execute(delete(QuizResult))
            db.execute(delete(Quiz))
            db.execute(delete(Material))
            db.commit()
        db = self.Session()
        self.material = Material(
            title="Algorithms", content=RICH_MATERIAL, source_type="text"
        )
        db.add(self.material)
        db.commit()
        self.material_id = self.material.id
        db.close()

    def _tts_ok(self):
        return mock.patch.object(
            audio_service, "generate_tts_audio", return_value=TTS_MOCK_RETURN
        )

    def test_create_quick_podcast_with_audio(self):
        with self._tts_ok() as tts:
            resp = self._client().post(
                "/api/podcasts",
                json={
                    "material_id": self.material_id,
                    "mode": "learn",
                    "duration_minutes": 3,
                    "provider": "quick",
                    "model_name": "quick",
                },
            )
        self.assertEqual(resp.status_code, 201, resp.text)
        body = resp.json()
        self.assertEqual(body["generated_by"], "quick")
        self.assertEqual(body["mode"], "learn")
        self.assertEqual(body["duration_minutes"], 3)
        self.assertTrue(body["title"])
        self.assertTrue(body["lines"])
        self.assertEqual(body["audio_status"], "ready")
        self.assertTrue(body["has_audio"])
        self.assertTrue(body["audio_url"].endswith("/audio"))

        audio = self._client().get(body["audio_url"])
        self.assertEqual(audio.status_code, 200)
        self.assertEqual(audio.headers["content-type"], "audio/wav")
        self.assertTrue(audio.content.startswith(b"RIFF"))
        self.assertGreater(tts.call_count, 0)

        fetched = self._client().get(f"/api/podcasts/{body['id']}")
        self.assertEqual(fetched.status_code, 200)
        self.assertEqual(fetched.json()["id"], body["id"])

    def test_list_by_material_and_missing_404(self):
        with self._tts_ok():
            first = self._client().post(
                "/api/podcasts",
                json={
                    "material_id": self.material_id,
                    "duration_minutes": 2,
                    "provider": "quick",
                },
            )
        listing = self._client().get(f"/api/podcasts?material_id={self.material_id}")
        self.assertEqual(listing.status_code, 200)
        self.assertEqual(len(listing.json()), 1)
        self.assertEqual(listing.json()[0]["id"], first.json()["id"])
        self.assertTrue(listing.json()[0]["material_title"])
        self.assertEqual(
            self._client().get("/api/podcasts/999999").status_code, 404
        )
        self.assertEqual(
            self._client().get("/api/podcasts/999999/audio").status_code, 404
        )

    def test_duration_and_mode_validation(self):
        client = self._client()
        base = {"material_id": self.material_id, "provider": "quick"}
        for duration in (0, -3, 11, 999):
            resp = client.post("/api/podcasts", json={**base, "duration_minutes": duration})
            self.assertEqual(resp.status_code, 422, f"duration {duration}")
        resp = client.post("/api/podcasts", json={**base, "mode": "bogus"})
        self.assertEqual(resp.status_code, 422)

    def test_missing_material_404(self):
        resp = self._client().post(
            "/api/podcasts",
            json={"material_id": 424242, "provider": "quick"},
        )
        self.assertEqual(resp.status_code, 404)

    def test_tts_failure_keeps_script(self):
        with mock.patch.object(
            audio_service, "generate_tts_audio", side_effect=RuntimeError("no tts")
        ):
            resp = self._client().post(
                "/api/podcasts",
                json={
                    "material_id": self.material_id,
                    "provider": "quick",
                    "duration_minutes": 2,
                },
            )
        self.assertEqual(resp.status_code, 201, resp.text)
        body = resp.json()
        self.assertEqual(body["audio_status"], "error")
        self.assertFalse(body["has_audio"])
        self.assertIsNone(body["audio_url"])
        self.assertTrue(body["warning"])
        self.assertTrue(body["lines"])

    def test_missing_gemini_key_yields_unavailable(self):
        with mock.patch.object(settings, "gemini_api_key", ""), self._tts_ok() as tts:
            resp = self._client().post(
                "/api/podcasts",
                json={"material_id": self.material_id, "provider": "quick"},
            )
        self.assertEqual(resp.status_code, 201, resp.text)
        body = resp.json()
        self.assertEqual(body["audio_status"], "unavailable")
        self.assertFalse(body["has_audio"])
        self.assertIn("GEMINI_API_KEY", body["warning"])
        tts.assert_not_called()

    def test_regenerate_audio_after_failure(self):
        with mock.patch.object(
            audio_service, "generate_tts_audio", side_effect=RuntimeError("boom")
        ):
            created = self._client().post(
                "/api/podcasts",
                json={"material_id": self.material_id, "provider": "quick",
                      "duration_minutes": 2},
            ).json()
        self.assertEqual(created["audio_status"], "error")

        with self._tts_ok() as tts:
            resp = self._client().post(f"/api/podcasts/{created['id']}/audio")
        self.assertEqual(resp.status_code, 200, resp.text)
        self.assertEqual(resp.json()["audio_status"], "ready")
        self.assertTrue(resp.json()["has_audio"])
        self.assertGreater(tts.call_count, 0)

        audio = self._client().get(f"/api/podcasts/{created['id']}/audio")
        self.assertEqual(audio.status_code, 200)
        self.assertTrue(audio.content.startswith(b"RIFF"))

    def test_weak_topics_uses_performance_snapshot(self):
        with self.Session() as db:
            quiz = Quiz(
                material_id=self.material_id,
                difficulty="medium",
                question_count=4,
                generated_by="quick",
                provider="quick",
            )
            db.add(quiz)
            db.flush()
            db.add(
                QuizResult(
                    quiz_id=quiz.id,
                    answers=[{"q": "scored"}],
                    score=2,
                    total=4,
                    percentage=50,
                )
            )
            db.commit()
        with self._tts_ok():
            resp = self._client().post(
                "/api/podcasts",
                json={
                    "material_id": self.material_id,
                    "mode": "weak_topics",
                    "duration_minutes": 2,
                    "provider": "quick",
                },
            )
        self.assertEqual(resp.status_code, 201, resp.text)
        self.assertTrue("Weak Topics" in resp.json()["title"])

    def test_delete_removes_episode_and_audio(self):
        with self._tts_ok():
            created = self._client().post(
                "/api/podcasts",
                json={"material_id": self.material_id, "provider": "quick",
                      "duration_minutes": 2},
            ).json()
        audio_path = Path(settings.podcast_media_dir) / f"podcast_{created['id']}.wav"
        self.assertTrue(audio_path.is_file())
        resp = self._client().delete(f"/api/podcasts/{created['id']}")
        self.assertEqual(resp.status_code, 204)
        self.assertFalse(audio_path.exists())
        listing = self._client().get(f"/api/podcasts?material_id={self.material_id}")
        self.assertEqual(listing.json(), [])

    def _client(self):
        return TestClient(app)


if __name__ == "__main__":
    unittest.main()