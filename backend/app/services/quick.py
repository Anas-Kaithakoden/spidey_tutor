"""Deterministic, non-LLM generation ("Quick Mode").

Pure local generation that never calls an external AI API. Given the same
material text and configuration, it always produces the same output. The
content is always derived from the study material itself (never invented):

- quizzes: cloze-deletion questions on key terms found in the material,
- flashcards: term -> defining sentence pairs from the material,
- study notes: sentences grouped into sections plus key concepts.

The output shapes mirror the raw dicts returned by the LLM providers so the
existing normalizers in ``services/ai.py`` can validate them unchanged.
"""

import re
from collections import Counter

_STOPWORDS = {
    "a", "about", "after", "again", "all", "also", "an", "and", "any", "are",
    "as", "at", "be", "because", "been", "before", "being", "between", "both",
    "but", "by", "can", "could", "did", "do", "does", "each", "else", "etc",
    "every", "for", "from", "had", "has", "have", "he", "her", "here", "hers",
    "him", "his", "how", "i", "if", "in", "into", "is", "it", "its", "may",
    "me", "more", "most", "my", "not", "of", "on", "one", "only", "or",
    "other", "our", "per", "so", "some", "such", "than", "that", "the",
    "their", "them", "then", "there", "these", "they", "this", "those",
    "through", "to", "two", "under", "until", "us", "using", "via", "was",
    "we", "were", "what", "when", "where", "which", "while", "who", "whom",
    "why", "will", "with", "would", "you", "your", "itself", "themselves",
    "ourselves", "yourselves",
}

_SENTENCE_SPLIT_RE = re.compile(r"[.!?]+\s+|\n+")
_WORD_RE = re.compile(r"[A-Za-z][A-Za-z0-9_-]{1,}")

SECTIONS_MAX = 4
KEY_CONCEPTS_MAX = 8


def _split_sentences(text: str) -> list[str]:
    """Split material into reasonably long, deterministic sentences."""
    sentences = []
    for part in _SENTENCE_SPLIT_RE.split(text.strip()):
        sentence = re.sub(r"\s+", " ", part).strip()
        if len(sentence) >= 15:
            sentences.append(sentence)
    return sentences


def _tokens(text: str) -> list[str]:
    return [w.lower() for w in _WORD_RE.findall(text.lower())]


def _term_counts(text: str) -> list[tuple[str, int]]:
    counts = Counter(w for w in _tokens(text) if w not in _STOPWORDS)
    return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))


def _contains_term(sentence: str, term: str) -> bool:
    return bool(re.search(r"\b" + re.escape(term) + r"\b", sentence, re.IGNORECASE))


def _sentence_with(sentences: list[str], term: str) -> str | None:
    for sentence in sentences:
        if _contains_term(sentence, term):
            return sentence
    return None


_INFLECT_SUFFIXES = ("s", "es", "ed", "d", "ing")


def _term_matches_sentence(sentence: str, term: str) -> bool:
    """Match a term as a word, or a common inflection of it (e.g. add ~ adds).

    Used by the deterministic chat reply so follow-up questions can resolve
    short-term inflections without reaching outside the material. The check
    is deliberately narrow (whole suffix words only) so "add" matches "adds"
    but not "addresses".
    """
    if _contains_term(sentence, term):
        return True
    if len(term) < 3:
        return False
    return any(_contains_term(sentence, term + suffix) for suffix in _INFLECT_SUFFIXES)


def _pairs(
    sentences: list[str], ranked: list[str]
) -> list[tuple[str, str]]:
    """(sentence, term) pairs for unique terms, in importance order."""
    pairs: list[tuple[str, str]] = []
    seen: set[str] = set()
    for term in ranked:
        if term in seen:
            continue
        sentence = _sentence_with(sentences, term)
        if sentence is None:
            continue
        seen.add(term)
        pairs.append((sentence, term))
        if len(pairs) >= 64:
            break
    return pairs


def _cloze(sentence: str, term: str) -> str:
    pattern = re.compile(r"\b" + re.escape(term) + r"\b", re.IGNORECASE)
    return pattern.sub("______", sentence)


def _band(
    pairs: list[tuple[str, str]], difficulty: str
) -> list[tuple[str, str]]:
    """Pick a deterministic importance band for the quiz difficulty."""
    n = len(pairs)
    if n == 0:
        return []
    if difficulty == "easy":
        start, end = 0, max(1, n // 3)
    elif difficulty == "hard":
        start, end = max(0, n - n // 3), n
    else:
        start, end = max(0, n // 3), max(1, n - n // 3)
    return pairs[start:end] or pairs[:]


def generate_quiz(
    material_text: str,
    difficulty: str = "medium",
    question_count: int = 5,
) -> list[dict]:
    """Deterministically build cloze quiz questions from the material."""
    sentences = _split_sentences(material_text)
    ranked = [term for term, _ in _term_counts(material_text)]
    pairs = _band(_pairs(sentences, ranked), difficulty)
    chosen = pairs[:question_count]
    used_terms = {term for _, term in chosen}
    distractors_pool = [t for t in ranked if t not in used_terms]

    questions: list[dict] = []
    for qi, (sentence, term) in enumerate(chosen):
        options_all = [term] + distractors_pool[:3]
        if len(options_all) < 2:
            break
        correct_idx = qi % len(options_all)
        options = options_all[correct_idx:] + options_all[:correct_idx]
        questions.append(
            {
                "question": (
                    f"Which term best completes this sentence?\n\n"
                    f"\"{_cloze(sentence, term)}\""
                ),
                "options": options,
                "correct_answer": correct_idx,
                "explanation": (
                    f"The answer is \"{term}\", which appears in the "
                    f"study material: \"{sentence}\""
                ),
            }
        )
    return questions


def generate_flashcards(
    material_text: str,
    count: int = 8,
) -> list[dict]:
    """Deterministically build term-definition flashcards from the material."""
    sentences = _split_sentences(material_text)
    ranked = [term for term, _ in _term_counts(material_text)]
    pairs = _pairs(sentences, ranked)[:count]
    return [
        {"front": f"What does \"{term}\" mean?", "back": sentence}
        for sentence, term in pairs
    ]


def _heading_for(group: list[str], ranked_group: list[tuple[str, int]]) -> str:
    if ranked_group:
        return f"About {ranked_group[0][0].capitalize()}"
    return group[0][:48]


def generate_study_notes(material_text: str) -> dict:
    """Deterministically structure the material into study notes."""
    sentences = _split_sentences(material_text)
    ranked = [term for term, _ in _term_counts(material_text)]
    pairs = _pairs(sentences, ranked)

    title = sentences[0][:80] if sentences else "Study Notes"
    summary = " ".join(sentences[:3])

    sections: list[dict] = []
    body = sentences[3:]
    if body:
        n_sections = min(SECTIONS_MAX, len(body))
        section_size = -(-len(body) // n_sections)
        for i in range(n_sections):
            group = body[i * section_size : (i + 1) * section_size]
            if not group:
                continue
            ranked_group = _term_counts(" ".join(group))
            sections.append(
                {
                    "heading": _heading_for(group, ranked_group),
                    "content": group[0],
                    "bullet_points": group[1:],
                }
            )

    key_concepts = [
        {"term": term, "definition": sentence}
        for sentence, term in pairs[:KEY_CONCEPTS_MAX]
    ]

    return {
        "title": title,
        "summary": summary,
        "sections": sections,
        "key_concepts": key_concepts,
    }


def generate_chat_reply(
    material_text: str,
    history: list[dict] | None = None,
    max_answer_chars: int = 600,
) -> str:
    """Deterministically answer a question using only the material text.

    ``history`` is the conversation so far (oldest first, ending with the
    current user question) as ``{"role": ..., "content": ...}`` dicts. The
    current question drives the keyword match; earlier user turns only provide
    context when the latest question has no keywords (e.g. a pronoun follow-up
    like "What about that?"). If nothing in the material matches, the answer
    says the information is not in the uploaded material — it never invents
    content that is not there.
    """
    history = history or []

    if not material_text.strip():
        return (
            "There is no study material uploaded yet, so I can't answer from "
            "it. Add a material first."
        )

    user_msgs = [
        m["content"] for m in history if m.get("role") == "user"
    ]
    if not user_msgs:
        return "Please ask a question about the uploaded material."

    def _keywords(text: str) -> list[str]:
        return list(
            dict.fromkeys(
                w for w in _tokens(text) if w not in _STOPWORDS and len(w) > 2
            )
        )

    question = user_msgs[-1].strip()
    primary = _keywords(question)
    if not primary:
        for q in reversed(user_msgs[:-1]):
            primary = _keywords(q)
            if primary:
                break

    if not primary:
        return (
            f"The uploaded material doesn't contain enough information to "
            f"answer \"{question}\". Try asking about a specific concept, "
            "term, or section in the notes."
        )

    sentences = _split_sentences(material_text)
    scored = [
        (sum(1 for k in primary if _term_matches_sentence(s, k)), s)
        for s in sentences
    ]
    scored.sort(key=lambda item: item[0], reverse=True)

    if not scored or scored[0][0] == 0:
        return (
            f"The uploaded material doesn't contain enough information to "
            f"answer \"{question}\". Try asking about something that is "
            "covered in the notes."
        )

    answer = scored[0][1]
    if len(answer) > max_answer_chars:
        answer = answer[:max_answer_chars].rsplit(" ", 1)[0] + "..."
    return answer