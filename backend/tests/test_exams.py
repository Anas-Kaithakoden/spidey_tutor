import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.database import Base, get_db  # noqa: E402
from app.main import app  # noqa: E402
from app.models import Material  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from app.services import exam as exam_service  # noqa: E402
from app.services.exam import (  # noqa: E402
    MAX_SCORE,
    _validate_eval,
    evaluate_exam,
    grade_deterministic,
    normalize_question,
    plan_exam_distribution,
)

MATERIAL = (
    "Binary search halves the search space with each step, giving O(log n) "
    "time complexity. A hash table maps keys to values with average O(1) "
    "lookups. A stack follows LIFO ordering: the last element pushed is the "
    "first to be popped. DNS translates domain names into IP addresses. "
    "HTTPS adds TLS encryption to web communication. The OS scheduler "
    "allocates CPU time to processes. Normalization reduces database "
    "redundancy. HTTP requests are sent over TCP connections."
)


def _question(qtype, text, **extra):
    base = {
        "question_type": qtype,
        "question": text,
        "accepted_answer": "The material states " + text,
    }
    return normalize_question({**base, **extra})


class DistributionTests(unittest.TestCase):
    def test_sums_to_count(self):
        for count in range(1, 31):
            self.assertEqual(len(plan_exam_distribution(count)), count)

    def test_never_single_type_for_larger_exams(self):
        for count in (4, 5, 8, 15):
            types = set(plan_exam_distribution(count))
            self.assertGreaterEqual(len(types), 3)

    def test_small_counts_have_expected_variety(self):
        self.assertEqual(len(plan_exam_distribution(1)), 1)
        self.assertEqual(len(set(plan_exam_distribution(2))), 2)

    def test_returns_empty_for_zero(self):
        self.assertEqual(plan_exam_distribution(0), [])


class GenerationTests(unittest.TestCase):
    def test_quick_is_deterministic_and_counts(self):
        a = exam_service.generate_exam(MATERIAL, "medium", 6, provider="quick")
        b = exam_service.generate_exam(MATERIAL, "medium", 6, provider="quick")
        self.assertEqual(a[1], b[1])
        generated_by, questions, error_detail = a
        self.assertEqual(generated_by, "quick")
        self.assertEqual(error_detail, "")
        self.assertEqual(len(questions), 6)

    def test_quick_questions_are_mixed_and_valid(self):
        _, questions, _ = exam_service.generate_exam(
            MATERIAL, "hard", 8, provider="quick"
        )
        self.assertGreaterEqual(len({q["question_type"] for q in questions}), 3)
        for q in questions:
            self.assertIn(q["question_type"], exam_service.QUESTION_TYPES)
            if q["question_type"] == "mcq":
                self.assertGreaterEqual(len(q["options"]), 2)
                self.assertIn(q["correct_answer"], range(len(q["options"])))
            else:
                self.assertTrue(q["accepted_answer"])
            self.assertEqual(q["max_score"], MAX_SCORE[q["question_type"]])

    def test_quick_fill_blank_has_blank_marker(self):
        _, questions, _ = exam_service.generate_exam(
            MATERIAL, "medium", 10, provider="quick"
        )
        blanks = [q for q in questions if q["question_type"] == "fill_blank"]
        self.assertTrue(blanks, "expected at least one fill-blank question")
        for q in blanks:
            self.assertIn("______", q["question"])

    def test_unknown_provider_falls_back_to_mock(self):
        generated_by, questions, error_detail = exam_service.generate_exam(
            MATERIAL, "medium", 3, provider="bogus"
        )
        self.assertEqual(generated_by, "mock")
        self.assertTrue(error_detail)
        self.assertGreaterEqual(len(questions), 1)

    def test_empty_material_falls_back_to_mock(self):
        generated_by, _, error_detail = exam_service.generate_exam(
            "", "medium", 3, provider="quick"
        )
        self.assertEqual(generated_by, "mock")
        self.assertTrue(error_detail)


class NormalizeQuestionTests(unittest.TestCase):
    def test_mcq_alias_and_validation(self):
        norm = normalize_question(
            {
                "question_type": "multiple_choice",
                "question": "Pick one",
                "options": ["A", "B", "C", "D"],
                "correct_answer": 2,
            }
        )
        self.assertEqual(norm["question_type"], "mcq")
        self.assertEqual(norm["correct_answer"], 2)

        with self.assertRaises(ValueError):
            normalize_question(
                {
                    "question_type": "mcq",
                    "question": "Pick one",
                    "options": ["A"],
                    "correct_answer": 0,
                }
            )
        with self.assertRaises(ValueError):
            normalize_question(
                {
                    "question_type": "mcq",
                    "question": "Pick one",
                    "options": ["A", "B", "C", "D"],
                    "correct_answer": 7,
                }
            )

    def test_unknown_and_missing_answer_rejected(self):
        with self.assertRaises(ValueError):
            normalize_question({"question_type": "essay", "question": "Go"})
        with self.assertRaises(ValueError):
            normalize_question({"question_type": "mystery", "question": "Go"})

    def test_essay_key_points_fallback(self):
        norm = normalize_question(
            {
                "question_type": "essay",
                "question": "Explain DNS",
                "accepted_answer": "DNS translates domain names into IP addresses.",
            }
        )
        self.assertTrue(norm["key_points"])


class DeterministicGradingTests(unittest.TestCase):
    def _mcq(self, correct=1):
        return normalize_question(
            {
                "question_type": "mcq",
                "question": "Pick one",
                "options": ["Wrong", "Right", "A", "B"],
                "correct_answer": correct,
            }
        )

    def test_mcq_correct_incorrect_unanswered(self):
        q = self._mcq()
        self.assertEqual(
            grade_deterministic(q, {"option": 1})["status"], "correct"
        )
        self.assertEqual(
            grade_deterministic(q, {"option": 0})["status"], "incorrect"
        )
        self.assertEqual(
            grade_deterministic(q, {})["status"], "unanswered"
        )

    def test_fill_blank_overlap(self):
        q = _question("fill_blank", "DNS ______ names.", accepted_answer="translates")
        good = grade_deterministic(q, {"text": "translates domain names"})
        self.assertEqual(good["status"], "correct")
        none = grade_deterministic(q, {"text": ""})
        self.assertEqual(none["status"], "unanswered")

    def test_short_answer_partial_credit(self):
        q = _question(
            "short_answer",
            "What is binary search?",
            accepted_answer="Binary search halves the search space each step.",
        )
        partial = grade_deterministic(q, {"text": "Binary search"})
        self.assertIn(partial["status"], ("partial", "incorrect"))
        self.assertGreaterEqual(partial["score"], 0)


class EvaluationTests(unittest.TestCase):
    def _questions(self):
        mcq = normalize_question(
            {
                "question_type": "mcq",
                "question": "Which data structure maps keys to values?",
                "options": ["Stack", "Hash table", "Queue", "Array"],
                "correct_answer": 1,
            }
        )
        short = _question(
            "short_answer",
            "What does DNS do?",
            accepted_answer="DNS translates domain names into IP addresses.",
        )
        essay = _question(
            "essay",
            "Explain how a stack works.",
            accepted_answer="A stack follows LIFO ordering: last in, first out.",
            key_points=["LIFO", "last element popped first"],
        )
        mcq["id"], short["id"], essay["id"] = 1, 2, 3
        return [mcq, short, essay]

    def _answers(self):
        return {
            1: {"option": 1},
            2: {"text": "DNS translates names into IP addresses."},
            3: {"text": "A stack is LIFO: the last pushed element is popped first."},
        }

    def _llm_eval(self):
        return {
            "summary": "Strong, well-grounded answers.",
            "strengths": ["Good use of the material"],
            "weak_areas": [],
            "topics_to_improve": [],
            "recommendations": ["Keep practicing"],
            "reviews": [
                {
                    "question_id": 2,
                    "score": 2.0,
                    "status": "correct",
                    "feedback": "Accurate.",
                    "improved_answer": None,
                },
                {
                    "question_id": 3,
                    "score": 3.0,
                    "status": "partial",
                    "feedback": "Partially covered.",
                    "improved_answer": "A complete answer mentions LIFO.",
                },
            ],
        }

    @mock.patch.object(exam_service, "_provider_generate_json")
    def test_hybrid_grading_uses_llm_for_subjective(self, mock_gen):
        mock_gen.return_value = self._llm_eval()
        method, result, error_detail = evaluate_exam(
            self._questions(), self._answers(), MATERIAL, provider="gemini"
        )
        self.assertEqual(method, "hybrid")
        self.assertEqual(error_detail, "")
        by_id = {r["question_id"]: r for r in result["reviews"]}
        self.assertEqual(by_id[1]["status"], "correct")  # mcq deterministic
        self.assertEqual(by_id[2]["status"], "correct")  # short via LLM
        self.assertEqual(by_id[3]["status"], "partial")  # essay via LLM
        total = result["total_score"]
        self.assertEqual(total, 1.0 + 2.0 + 3.0)
        self.assertEqual(result["summary"], "Strong, well-grounded answers.")

    @mock.patch.object(exam_service, "_provider_generate_json")
    def test_llm_failure_switches_to_keyword_fallback(self, mock_gen):
        mock_gen.side_effect = RuntimeError("boom")
        method, result, error_detail = evaluate_exam(
            self._questions(), self._answers(), MATERIAL, provider="gemini"
        )
        self.assertEqual(method, "fallback")
        self.assertTrue(error_detail)
        self.assertTrue(result["strengths"])
        self.assertTrue(result["recommendations"])

    @mock.patch.object(exam_service, "_provider_generate_json")
    def test_ai_subjective_disabled_is_deterministic(self, mock_gen):
        method, result, _ = evaluate_exam(
            self._questions(),
            self._answers(),
            MATERIAL,
            provider="gemini",
            criteria={"ai_subjective": False},
        )
        self.assertEqual(method, "deterministic")
        mock_gen.assert_not_called()
        self.assertEqual(result["grading_method"], "deterministic")

    def test_validate_eval_rejects_missing_reviews(self):
        with self.assertRaises(ValueError):
            _validate_eval(self._llm_eval(), {2, 3, 99})

    @mock.patch.object(exam_service, "_provider_generate_json")
    def test_missing_review_triggers_fallback(self, mock_gen):
        bad = self._llm_eval()
        bad["reviews"] = [r for r in bad["reviews"] if r["question_id"] != 3]
        mock_gen.return_value = bad
        method, _, _ = evaluate_exam(
            self._questions(), self._answers(), MATERIAL, provider="gemini"
        )
        self.assertEqual(method, "fallback")

    def test_evaluation_criteria_snapshot(self):
        criteria = exam_service.evaluation_criteria()
        for key in (
            "ai_subjective",
            "strictness",
            "partial_credit",
            "penalize_unsupported",
        ):
            self.assertIn(key, criteria)


class ExamApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmpdir = tempfile.TemporaryDirectory()
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker

        cls.engine = create_engine(
            f"sqlite:///{Path(cls.tmpdir.name) / 'exam_test.db'}",
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

    def setUp(self):
        from sqlalchemy import delete

        with self.Session() as db:
            db.execute(delete(Material))
            db.commit()
        db = self.Session()
        self.material = Material(
            title="Algorithms", content=MATERIAL, source_type="text"
        )
        db.add(self.material)
        db.commit()
        self.material_id = self.material.id
        db.close()

    def _client(self):
        return TestClient(app)

    def test_create_and_submit_full_flow(self):
        client = self._client()
        resp = client.post(
            "/api/exams",
            json={
                "material_id": self.material_id,
                "title": "Unit 1 Exam",
                "difficulty": "medium",
                "question_count": 6,
                "duration_minutes": 20,
                "provider": "quick",
                "model_name": "quick",
            },
        )
        self.assertEqual(resp.status_code, 201, resp.text)
        exam = resp.json()
        self.assertEqual(exam["material_id"], self.material_id)
        self.assertEqual(exam["title"], "Unit 1 Exam")
        self.assertEqual(exam["generated_by"], "quick")
        self.assertEqual(exam["duration_minutes"], 20)
        self.assertEqual(len(exam["questions"]), 6)
        for q in exam["questions"]:
            self.assertIn("options" in q, (True,))
            self.assertGreaterEqual(q["max_score"], 1)

        fetched = client.get(f"/api/exams/{exam['id']}")
        self.assertEqual(fetched.status_code, 200)
        self.assertEqual(fetched.json()["id"], exam["id"])

        answers = []
        for idx, q in enumerate(exam["questions"]):
            if q["question_type"] == "mcq":
                answers.append({"question_id": q["id"], "option": 0})
            else:
                answers.append(
                    {"question_id": q["id"], "text": "A reasonable answer."}
                )

        result = client.post(
            f"/api/exams/{exam['id']}/submit",
            json={"answers": answers, "time_taken_seconds": 300},
        )
        self.assertEqual(result.status_code, 200, result.text)
        body = result.json()
        self.assertEqual(body["exam_id"], exam["id"])
        self.assertGreater(body["percentage"], 0)
        self.assertEqual(len(body["reviews"]), 6)
        self.assertIn("criteria_used", body)
        self.assertIn("strictness", body["criteria_used"])
        self.assertTrue(body["summary"])

        latest = client.get(f"/api/exams/{exam['id']}/result")
        self.assertEqual(latest.status_code, 200)
        self.assertEqual(latest.json()["result_id"], body["result_id"])

    def test_get_missing_exam_is_404(self):
        client = self._client()
        self.assertEqual(client.get("/api/exams/9999").status_code, 404)
        self.assertEqual(
            client.get("/api/exams/9999/result").status_code, 404
        )

    def test_submit_invalid_option_is_ignored_as_unanswered(self):
        client = self._client()
        resp = client.post(
            "/api/exams",
            json={
                "material_id": self.material_id,
                "difficulty": "easy",
                "question_count": 4,
                "duration_minutes": 10,
                "provider": "quick",
                "model_name": "quick",
            },
        )
        exam = resp.json()
        mcq = next(
            q for q in exam["questions"] if q["question_type"] == "mcq"
        )
        result = client.post(
            f"/api/exams/{exam['id']}/submit",
            json={
                "answers": [
                    {"question_id": mcq["id"], "option": 99},
                    {"question_id": mcq["id"], "option": 1},
                ]
            },
        )
        body = result.json()
        by_id = {
            r["question_id"]: r for r in body["reviews"]
        }
        # The out-of-range option 99 must be ignored; the valid option 1 is kept.
        self.assertNotEqual(by_id[mcq["id"]]["status"], "unanswered")
        unanswered = [
            r for r in body["reviews"] if r["status"] == "unanswered"
        ]
        self.assertGreaterEqual(len(unanswered), 1)


class ExamOutSchemaTests(unittest.TestCase):
    def test_exam_result_out_has_all_fields(self):
        from app.schemas import ExamResultOut

        payload = {
            "result_id": 1,
            "exam_id": 1,
            "attempt_id": 1,
            "total_score": 5.0,
            "max_score": 10,
            "percentage": 50.0,
            "summary": "S",
            "strengths": [],
            "weak_areas": [],
            "topics_to_improve": [],
            "recommendations": [],
            "reviews": [
                {
                    "question_id": 1,
                    "question": "Q",
                    "question_type": "mcq",
                    "user_answer": "A",
                    "expected_answer": "B",
                    "status": "correct",
                    "score": 1,
                    "max_score": 1,
                    "feedback": "f",
                    "improved_answer": None,
                }
            ],
            "grading_method": "hybrid",
            "generated_by": "quick",
            "criteria_used": {"strictness": "balanced"},
        }
        out = ExamResultOut.model_validate(payload)
        self.assertEqual(out.max_score, 10)


if __name__ == "__main__":
    unittest.main()