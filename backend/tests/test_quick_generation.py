import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.services import quick  # noqa: E402
from app.services.ai import (  # noqa: E402
    generate_flashcards,
    generate_quiz,
    generate_study_notes,
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


class QuickQuizTests(unittest.TestCase):
    def test_deterministic_same_input_same_output(self):
        a = quick.generate_quiz(MATERIAL, "medium", 5)
        b = quick.generate_quiz(MATERIAL, "medium", 5)
        self.assertEqual(a, b)

    def test_count_respected(self):
        for count in (1, 3, 5):
            questions = quick.generate_quiz(MATERIAL, "easy", count)
            self.assertLessEqual(len(questions), count)
            self.assertGreaterEqual(len(questions), 1)

    def test_question_structure_valid(self):
        for q in quick.generate_quiz(MATERIAL, "hard", 5):
            self.assertIn("question", q)
            self.assertIn("______", q["question"])
            self.assertGreaterEqual(len(q["options"]), 2)
            self.assertIn(q["correct_answer"], range(len(q["options"])))
            self.assertTrue(q["explanation"])

    def test_correct_answer_is_grounded_in_material(self):
        for q in quick.generate_quiz(MATERIAL, "medium", 5):
            answer = q["options"][q["correct_answer"]]
            self.assertIn(answer.lower(), MATERIAL.lower())


class QuickFlashcardTests(unittest.TestCase):
    def test_deterministic_and_count(self):
        self.assertEqual(
            quick.generate_flashcards(MATERIAL, 4),
            quick.generate_flashcards(MATERIAL, 4),
        )
        cards = quick.generate_flashcards(MATERIAL, 4)
        self.assertLessEqual(len(cards), 4)
        self.assertTrue(all(c["front"] and c["back"] for c in cards))
        self.assertTrue(all(c["front"].endswith("?") for c in cards))


class QuickStudyNotesTests(unittest.TestCase):
    def test_deterministic_structure(self):
        notes = quick.generate_study_notes(MATERIAL)
        self.assertEqual(notes, quick.generate_study_notes(MATERIAL))
        self.assertTrue(notes["title"])
        self.assertTrue(notes["summary"])
        self.assertIsInstance(notes["sections"], list)
        self.assertIsInstance(notes["key_concepts"], list)
        for section in notes["sections"]:
            self.assertIn("heading", section)
            self.assertTrue(section["content"])
            self.assertIsInstance(section["bullet_points"], list)
        for concept in notes["key_concepts"]:
            self.assertTrue(concept["term"])
            self.assertTrue(concept["definition"])

    def test_key_concepts_grounded_in_material(self):
        notes = quick.generate_study_notes(MATERIAL)
        for concept in notes["key_concepts"]:
            self.assertIn(concept["term"].lower(), MATERIAL.lower())
            self.assertIn(concept["term"].lower(), concept["definition"].lower())


class QuickDispatchTests(unittest.TestCase):
    def test_generate_quiz_quick_stamps(self):
        generated_by, questions = generate_quiz(
            MATERIAL, "medium", 5, provider="quick"
        )
        self.assertEqual(generated_by, "quick")
        self.assertEqual(
            questions, quick.generate_quiz(MATERIAL, "medium", 5)
        )

    def test_generate_flashcards_quick_stamps(self):
        generated_by, cards = generate_flashcards(
            MATERIAL, count=4, provider="quick"
        )
        self.assertEqual(generated_by, "quick")
        self.assertEqual(cards, quick.generate_flashcards(MATERIAL, 4))

    def test_generate_study_notes_quick_stamps(self):
        generated_by, notes = generate_study_notes(
            MATERIAL, provider="quick"
        )
        self.assertEqual(generated_by, "quick")
        self.assertEqual(notes, quick.generate_study_notes(MATERIAL))

    def test_unknown_provider_falls_back_to_mock(self):
        generated_by, _ = generate_quiz(
            MATERIAL, "medium", 5, provider="bogus"
        )
        self.assertEqual(generated_by, "mock")

    def test_empty_material_falls_back_to_mock(self):
        generated_by, _ = generate_quiz("", "medium", 5, provider="quick")
        self.assertEqual(generated_by, "mock")


if __name__ == "__main__":
    unittest.main()