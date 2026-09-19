import sys
import unittest
from contextlib import ExitStack, contextmanager
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient  # noqa: E402
from sqlalchemy import create_engine  # noqa: E402
from sqlalchemy.orm import sessionmaker  # noqa: E402
from sqlalchemy.pool import StaticPool  # noqa: E402
from youtube_transcript_api import (  # noqa: E402
    NoTranscriptFound,
    TranscriptsDisabled,
    VideoUnavailable,
)

from app.database import Base, get_db  # noqa: E402
from app.main import app  # noqa: E402
from app.services import transcript, youtube  # noqa: E402

VIDEO_ID = "dQw4w9WgXcQ"


class FakeSnippet:
    def __init__(self, text: str):
        self.text = text


class FakeTranscript:
    def __init__(self, language_code="en", is_generated=False, snippets=None):
        self.language_code = language_code
        self.is_generated = is_generated
        self.snippets = snippets if snippets is not None else []

    def fetch(self):
        return self.snippets


class FakeTranscriptList:
    def __init__(self, transcripts=None):
        self.transcripts = transcripts or []

    def find_transcript(self, languages):
        for t in self.transcripts:
            if t.language_code in languages:
                return t
        raise NoTranscriptFound(VIDEO_ID, languages, self)

    def __iter__(self):
        return iter(self.transcripts)


class UrlValidationTests(unittest.TestCase):
    def test_watch_url(self):
        self.assertEqual(
            youtube.parse_youtube_url(
                f"https://www.youtube.com/watch?v={VIDEO_ID}"
            ),
            VIDEO_ID,
        )

    def test_youtu_be_url(self):
        self.assertEqual(
            youtube.parse_youtube_url(f"https://youtu.be/{VIDEO_ID}"), VIDEO_ID
        )

    def test_shorts_url(self):
        self.assertEqual(
            youtube.parse_youtube_url(
                f"https://www.youtube.com/shorts/{VIDEO_ID}"
            ),
            VIDEO_ID,
        )

    def test_embed_url(self):
        self.assertEqual(
            youtube.parse_youtube_url(
                f"https://www.youtube.com/embed/{VIDEO_ID}?start=10"
            ),
            VIDEO_ID,
        )

    def test_live_url(self):
        self.assertEqual(
            youtube.parse_youtube_url(f"https://www.youtube.com/live/{VIDEO_ID}"),
            VIDEO_ID,
        )

    def test_mobile_and_music_hosts(self):
        self.assertEqual(
            youtube.parse_youtube_url(f"https://m.youtube.com/watch?v={VIDEO_ID}"),
            VIDEO_ID,
        )
        self.assertEqual(
            youtube.parse_youtube_url(
                f"https://music.youtube.com/watch?v={VIDEO_ID}"
            ),
            VIDEO_ID,
        )

    def test_extra_query_params_and_fragment(self):
        self.assertEqual(
            youtube.parse_youtube_url(
                f"https://www.youtube.com/watch?v={VIDEO_ID}&t=30s&feature=share"
            ),
            VIDEO_ID,
        )

    def test_scheme_is_optional(self):
        self.assertEqual(
            youtube.parse_youtube_url(f"www.youtube.com/watch?v={VIDEO_ID}"),
            VIDEO_ID,
        )

    def test_rejects_non_youtube_host(self):
        with self.assertRaises(ValueError):
            youtube.parse_youtube_url(
                f"https://example.com/watch?v={VIDEO_ID}"
            )

    def test_rejects_playlist_url(self):
        with self.assertRaises(ValueError):
            youtube.parse_youtube_url(
                "https://www.youtube.com/playlist?list=PL1234567890"
            )

    def test_rejects_missing_video_id(self):
        with self.assertRaises(ValueError):
            youtube.parse_youtube_url("https://www.youtube.com")

    def test_rejects_short_video_id(self):
        with self.assertRaises(ValueError):
            youtube.parse_youtube_url("https://www.youtube.com/watch?v=short")

    def test_rejects_invalid_characters(self):
        with self.assertRaises(ValueError):
            youtube.parse_youtube_url(
                "https://www.youtube.com/watch?v=bad id with spaces!"
            )

    def test_rejects_blank(self):
        with self.assertRaises(ValueError):
            youtube.parse_youtube_url("   ")


class TranscriptRetrievalTests(unittest.TestCase):
    def _patch_api(self, transcript_list):
        patcher = mock.patch.object(transcript, "YouTubeTranscriptApi")
        api_cls = patcher.start()
        self.addCleanup(patcher.stop)
        api_cls.return_value.list.return_value = transcript_list
        return api_cls

    def test_joins_segments_into_text(self):
        api = self._patch_api(
            FakeTranscriptList(
                [
                    FakeTranscript(
                        snippets=[
                            FakeSnippet("Binary search halves the space."),
                            FakeSnippet("This gives O(log n) time."),
                        ]
                    )
                ]
            )
        )
        text = transcript.fetch_transcript(VIDEO_ID)
        api.return_value.list.assert_called_once_with(VIDEO_ID)
        self.assertEqual(
            text, "Binary search halves the space. This gives O(log n) time."
        )

    def test_prefers_manual_english_transcript(self):
        generated_fr = FakeTranscript("fr", is_generated=True, snippets=[FakeSnippet("fr")])
        manual_en = FakeTranscript("en", is_generated=False, snippets=[FakeSnippet("english")])
        transcript_list = FakeTranscriptList([generated_fr, manual_en])
        self._patch_api(transcript_list)
        self.assertEqual(transcript.fetch_transcript(VIDEO_ID), "english")

    def test_falls_back_to_generated_when_no_manual(self):
        generated_en = FakeTranscript("en", is_generated=True, snippets=[FakeSnippet("auto")])
        generated_fr = FakeTranscript("fr", is_generated=True, snippets=[FakeSnippet("fr auto")])
        self._patch_api(FakeTranscriptList([generated_fr, generated_en]))
        self.assertEqual(transcript.fetch_transcript(VIDEO_ID), "auto")

    def test_raises_when_transcripts_disabled(self):
        def _list(video_id):
            raise TranscriptsDisabled(video_id)

        with mock.patch.object(transcript, "YouTubeTranscriptApi") as api_cls:
            api_cls.return_value.list.side_effect = _list
            with self.assertRaises(transcript.TranscriptError) as ctx:
                transcript.fetch_transcript(VIDEO_ID)
        self.assertIn("disabled", str(ctx.exception).lower())

    def test_raises_when_no_transcript_found(self):
        self._patch_api(FakeTranscriptList([]))
        with self.assertRaises(transcript.TranscriptError) as ctx:
            transcript.fetch_transcript(VIDEO_ID)
        self.assertIn("no transcript", str(ctx.exception).lower())

    def test_raises_when_video_unavailable(self):
        def _list(video_id):
            raise VideoUnavailable(video_id)

        with mock.patch.object(transcript, "YouTubeTranscriptApi") as api_cls:
            api_cls.return_value.list.side_effect = _list
            with self.assertRaises(transcript.TranscriptError) as ctx:
                transcript.fetch_transcript(VIDEO_ID)
        self.assertIn("unavailable", str(ctx.exception).lower())

    def test_raises_when_request_blocked(self):
        from youtube_transcript_api._errors import RequestBlocked

        def _list(video_id):
            raise RequestBlocked(video_id)

        with mock.patch.object(transcript, "YouTubeTranscriptApi") as api_cls:
            api_cls.return_value.list.side_effect = _list
            with self.assertRaises(transcript.TranscriptError) as ctx:
                transcript.fetch_transcript(VIDEO_ID)
        self.assertIn("blocking", str(ctx.exception).lower())

    def test_raises_when_transcript_is_empty(self):
        self._patch_api(
            FakeTranscriptList(
                [FakeTranscript(snippets=[FakeSnippet("   "), FakeSnippet("")])]
            )
        )
        with self.assertRaises(transcript.TranscriptError) as ctx:
            transcript.fetch_transcript(VIDEO_ID)
        self.assertIn("empty", str(ctx.exception).lower())


class YoutubeMaterialEndpointTests(unittest.TestCase):
    def setUp(self):
        engine = create_engine(
            "sqlite://",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        self.TestingSession = sessionmaker(
            bind=engine, autoflush=False, autocommit=False
        )
        Base.metadata.create_all(bind=engine)

        def override_get_db():
            db = self.TestingSession()
            try:
                yield db
            finally:
                db.close()

        app.dependency_overrides[get_db] = override_get_db
        self.client = TestClient(app)

    def tearDown(self):
        app.dependency_overrides.clear()

    @contextmanager
    def _mock_services(self, transcript_text="Hello world transcript.", meta=None):
        with ExitStack() as stack:
            stack.enter_context(
                mock.patch(
                    "app.routers.youtube_materials.transcript.fetch_transcript",
                    return_value=transcript_text,
                )
            )
            stack.enter_context(
                mock.patch(
                    "app.routers.youtube_materials.youtube.fetch_video_metadata",
                    return_value=meta or {},
                )
            )
            yield

    def test_success_creates_youtube_material(self):
        with self._mock_services(
            transcript_text="First sentence. Second sentence.",
            meta={"title": "Learn OS", "author_name": "CS Dept"},
        ):
            res = self.client.post(
                "/api/materials/youtube",
                json={"url": f"https://youtu.be/{VIDEO_ID}"},
            )
        self.assertEqual(res.status_code, 201)
        data = res.json()
        self.assertEqual(data["source_type"], "youtube")
        self.assertEqual(data["title"], "Learn OS")
        self.assertIn(VIDEO_ID, data["source_url"])
        self.assertEqual(data["word_count"], 4)
        self.assertGreater(data["id"], 0)

    def test_custom_title_overrides_video_title(self):
        with self._mock_services(
            transcript_text="Some content.", meta={"title": "Original Title"}
        ):
            res = self.client.post(
                "/api/materials/youtube",
                json={
                    "url": f"https://www.youtube.com/watch?v={VIDEO_ID}",
                    "title": "My Custom Title",
                },
            )
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.json()["title"], "My Custom Title")

    def test_title_falls_back_when_no_metadata(self):
        with self._mock_services(transcript_text="Some content.", meta={}):
            res = self.client.post(
                "/api/materials/youtube",
                json={"url": f"https://youtu.be/{VIDEO_ID}"},
            )
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.json()["title"], f"YouTube Video {VIDEO_ID}")

    def test_invalid_url_returns_400(self):
        res = self.client.post(
            "/api/materials/youtube",
            json={"url": "https://example.com/not-a-video"},
        )
        self.assertEqual(res.status_code, 400)
        self.assertIn("YouTube", res.json()["detail"])

    def test_transcript_unavailable_returns_422(self):
        patcher = mock.patch(
            "app.routers.youtube_materials.transcript.fetch_transcript",
            side_effect=transcript.TranscriptError(
                "No transcript or captions are available for this video."
            ),
        )
        patcher.start()
        self.addCleanup(patcher.stop)
        res = self.client.post(
            "/api/materials/youtube",
            json={"url": f"https://youtu.be/{VIDEO_ID}"},
        )
        self.assertEqual(res.status_code, 422)
        self.assertIn("transcript", res.json()["detail"].lower())

    def test_get_material_preserves_source_url(self):
        with self._mock_services(transcript_text="Some content.", meta={"title": "T"}):
            created = self.client.post(
                "/api/materials/youtube",
                json={"url": f"https://youtu.be/{VIDEO_ID}"},
            ).json()
        fetched = self.client.get(f"/api/materials/{created['id']}")
        self.assertEqual(fetched.status_code, 200)
        data = fetched.json()
        self.assertEqual(data["source_type"], "youtube")
        self.assertEqual(data["source_url"], created["source_url"])


class MetadataTests(unittest.TestCase):
    def test_metadata_none_on_http_error(self):
        class FakeResponse:
            status_code = 404

            def json(self):
                return {}

        with mock.patch.object(youtube.httpx, "get", return_value=FakeResponse()) as m:
            meta = youtube.fetch_video_metadata(VIDEO_ID)
        m.assert_called_once()
        self.assertEqual(meta, {})

    def test_metadata_parses_oembed(self):
        class FakeResponse:
            status_code = 200

            def json(self):
                return {
                    "title": "A Title",
                    "author_name": "Channel",
                    "author_url": "https://www.youtube.com/@channel",
                    "thumbnail_url": "https://img.youtube.com/vi/abc/0.jpg",
                }

        with mock.patch.object(
            youtube.httpx, "get", return_value=FakeResponse()
        ):
            meta = youtube.fetch_video_metadata(VIDEO_ID)
        self.assertEqual(meta["title"], "A Title")
        self.assertEqual(meta["author_name"], "Channel")

    def test_metadata_none_on_network_error(self):
        with mock.patch.object(
            youtube.httpx, "get", side_effect=youtube.httpx.TimeoutException("slow")
        ):
            self.assertEqual(youtube.fetch_video_metadata(VIDEO_ID), {})


if __name__ == "__main__":
    unittest.main()