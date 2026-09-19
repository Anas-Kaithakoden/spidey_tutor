import sys
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient  # noqa: E402

from app.database import get_db  # noqa: E402
from app.main import app  # noqa: E402
from app.models import Base  # noqa: E402

SYLLABUS = (
    "Module 1: Search algorithms\n"
    "Module 2: Sorting algorithms\n"
    "Module 3: Data structures\n"
    "Module 4: Dynamic programming\n"
    "Module 5: Graph algorithms"
)


def _future_date(days: int = 15) -> str:
    return (date.today() + timedelta(days=days)).isoformat()


class StudyPlanApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmpdir = tempfile.TemporaryDirectory()
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker

        cls.engine = create_engine(
            f"sqlite:///{Path(cls.tmpdir.name) / 'plan_test.db'}",
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

    @classmethod
    def tearDownClass(cls):
        app.dependency_overrides.pop(get_db, None)
        cls.engine.dispose()
        cls.tmpdir.cleanup()

    def _client(self):
        return TestClient(app)

    def _make_pdf_bytes(self) -> bytes:
        import pymupdf

        doc = pymupdf.open()
        page = doc.new_page()
        page.insert_text((72, 72), SYLLABUS.replace("\n", "\n"))
        data = doc.tobytes()
        doc.close()
        return data

    def test_generate_quick_plan(self):
        client = self._client()
        exam_date = _future_date(15)
        resp = client.post(
            "/api/study-plan",
            json={
                "syllabus": SYLLABUS,
                "exam_date": exam_date,
                "daily_hours": 3,
                "provider": "quick",
                "model_name": "quick",
                "language": "en",
            },
        )
        self.assertEqual(resp.status_code, 200, resp.text)
        plan = resp.json()
        self.assertEqual(plan["generated_by"], "quick")
        expected_days = (date.fromisoformat(exam_date) - date.today()).days
        self.assertEqual(plan["total_topics"], expected_days)
        self.assertEqual(len(plan["plan"]), plan["total_topics"])
        self.assertGreater(plan["days_left"], 0)
        self.assertTrue(plan["tips"])

    def test_generate_plan_from_pdf(self):
        client = self._client()
        exam_date = _future_date(15)
        resp = client.post(
            "/api/study-plan/pdf",
            data={
                "exam_date": exam_date,
                "daily_hours": 2,
                "provider": "quick",
                "model_name": "quick",
                "language": "en",
            },
            files={"file": ("syllabus.pdf", self._make_pdf_bytes(), "application/pdf")},
        )
        self.assertEqual(resp.status_code, 200, resp.text)
        plan = resp.json()
        self.assertEqual(plan["generated_by"], "quick")
        expected_days = (date.fromisoformat(exam_date) - date.today()).days
        self.assertEqual(plan["total_topics"], expected_days)
        self.assertEqual(len(plan["plan"]), plan["total_topics"])
        self.assertEqual(plan["daily_hours"], 2)

    def test_rejects_non_pdf(self):
        client = self._client()
        resp = client.post(
            "/api/study-plan/pdf",
            data={"exam_date": _future_date(), "provider": "quick"},
            files={"file": ("notes.txt", b"hello", "text/plain")},
        )
        self.assertEqual(resp.status_code, 400)

    def test_rejects_past_exam_date(self):
        client = self._client()
        resp = client.post(
            "/api/study-plan",
            json={
                "syllabus": SYLLABUS,
                "exam_date": (date.today() - timedelta(days=1)).isoformat(),
                "provider": "quick",
            },
        )
        self.assertEqual(resp.status_code, 422)

    def test_rejects_short_syllabus(self):
        client = self._client()
        resp = client.post(
            "/api/study-plan",
            json={
                "syllabus": "x",
                "exam_date": _future_date(),
                "provider": "quick",
            },
        )
        self.assertEqual(resp.status_code, 422)


if __name__ == "__main__":
    unittest.main()