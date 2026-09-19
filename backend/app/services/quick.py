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


# Study Podcast ----------------------------------------------------------------
# Deterministic two-host podcast scripts. Every factual line is drawn verbatim
# (or near-verbatim) from the material's sentences; host reactions are short
# spoken fillers that never introduce facts. The script stays inside the
# caller's word budget for the requested duration.

PODCAST_MODE_TITLES = {
    "learn": "Learn",
    "revise": "Revise",
    "exam_prep": "Exam Prep",
    "weak_topics": "Weak Topics",
}

PODCAST_WPM_CEILING = 165

_MODE_INTROS = {
    "learn": (
        "Welcome back to Study Sesh! Today we're taking a proper deep dive "
        "into the material — real explanations, not a recap."
    ),
    "revise": (
        "Hey, quick episode today. This is a fast Revise run — the definitions "
        "and facts you need to remember, straight from the material."
    ),
    "exam_prep": (
        "Welcome to Exam Prep. We're hitting the highest-value concepts and "
        "pointing out what's most likely to show up, with a self-check or two."
    ),
    "weak_topics": (
        "Welcome back! Your recent results flagged a few topics worth "
        "strengthening, so today's episode is built around exactly those."
    ),
}


def _podcast_focus_terms(text: str, n: int = 6) -> list[str]:
    return [term for term, _ in _term_counts(text)][:n]


def _podcast_reorder(
    pairs: list[tuple[str, str]], keywords: list[str]
) -> list[tuple[str, str]]:
    """Move sentences touching the given keywords to the front (stable)."""
    if not keywords:
        return pairs
    priority, rest = [], []
    for sentence, term in pairs:
        lowered = sentence.lower()
        hit = any(kw in lowered for kw in keywords) or any(
            kw in term.lower() for kw in keywords
        )
        (priority if hit else rest).append((sentence, term))
    return priority + rest


def generate_podcast_script(
    material_text: str,
    mode: str = "learn",
    duration_minutes: int = 5,
    focus_topic: str = "",
    weak_topics: list[dict] | None = None,
) -> dict:
    """Build a deterministic, material-grounded two-host podcast script.

    Returns the same raw dict shape the LLM providers return so the shared
    validation in ``services/podcast.py`` can run unchanged::

        {"title": str, "lines": [{"speaker": str, "text": str}]}
    """
    sentences = _split_sentences(material_text)
    ranked = [term for term, _ in _term_counts(material_text)]
    pairs = _pairs(sentences, ranked)
    terms = _podcast_focus_terms(material_text)
    title_topic = (
        focus_topic.strip()
        or (terms[0].capitalize() if terms else "This Material")
    )
    title = f"{PODCAST_MODE_TITLES.get(mode, 'Learn')}: {title_topic}"
    budget = max(60, int(duration_minutes) * PODCAST_WPM_CEILING)

    lines: list[dict] = [
        {
            "speaker": "host_one",
            "text": _MODE_INTROS.get(mode, _MODE_INTROS["learn"]),
        },
        {
            "speaker": "host_two",
            "text": (
                f"Let's get into it. {title_topic} — what does the "
                "material actually say about it first?"
            ),
        },
    ]

    if focus_topic:
        keywords = [
            w for w in _tokens(focus_topic) if w not in _STOPWORDS and len(w) > 2
        ]
        pairs = _podcast_reorder(pairs, keywords)
    if mode == "weak_topics" and weak_topics:
        weak_keywords: list[str] = []
        for topic in weak_topics:
            name = str(topic.get("title", ""))
            weak_keywords += [
                w for w in _tokens(name) if w not in _STOPWORDS and len(w) > 2
            ]
        pairs = _podcast_reorder(pairs, weak_keywords)

    outro_words = 45
    spent = _count_words(lines)
    idx = 0
    used = 0
    while idx < len(pairs) and spent < budget - outro_words:
        remaining = budget - outro_words - spent
        if remaining < 25:
            break
        sentence, term = pairs[idx]
        idx += 1
        sentence_next, term_next = (
            pairs[idx] if idx < len(pairs) else (None, None)
        )
        if sentence_next is not None:
            idx += 1
        else:
            sentence_next, term_next = sentence, term

        used += 1
        if mode == "exam_prep" and used % 3 == 0:
            pair_lines = [
                {
                    "speaker": "host_two",
                    "text": (
                        "Quick self-check from the material: which term fits "
                        f"here? {_cloze(sentence, term)}"
                    ),
                },
                {
                    "speaker": "host_one",
                    "text": (
                        f"That's {term} — the material brings it up in exactly "
                        "that context."
                    ),
                },
            ]
        elif mode == "revise":
            pair_lines = [
                {"speaker": "host_one", "text": f"Quick point: {sentence}."},
                {"speaker": "host_two", "text": f"{term} — noted."},
                {"speaker": "host_one", "text": f"Next: {sentence_next}."},
                {
                    "speaker": "host_two",
                    "text": f"Right, and that's the essence of {term_next}.",
                },
            ]
        elif mode == "weak_topics":
            pair_lines = [
                {
                    "speaker": "host_one",
                    "text": f"Let's slow down here — this one needs attention: {sentence}.",
                },
                {
                    "speaker": "host_two",
                    "text": f"So {term} is really about that. How does it tie to another idea?",
                },
                {"speaker": "host_one", "text": f"Sure — {sentence_next}."},
                {
                    "speaker": "host_two",
                    "text": f"Got it. One more angle: {term_next}.",
                },
            ]
        else:  # learn
            pair_lines = [
                {
                    "speaker": "host_one",
                    "text": f"Here's the core idea as the material frames it: {sentence}.",
                },
                {
                    "speaker": "host_two",
                    "text": f"That connects to {term} — what else does it tie into?",
                },
                {
                    "speaker": "host_one",
                    "text": f"It also relates to this: {sentence_next}.",
                },
                {
                    "speaker": "host_two",
                    "text": f"So the thread running through is {term} and {term_next}. Keep going.",
                },
            ]

        pair_words = _count_words(pair_lines)
        if spent + pair_words > budget - outro_words:
            break
        lines.extend(pair_lines)
        spent += pair_words

    recap_terms = ", ".join(dict.fromkeys(terms[:4])) or "the material's key ideas"
    lines += [
        {
            "speaker": "host_one",
            "text": f"Quick recap before we go: {recap_terms} — those are today's takeaways.",
        },
        {
            "speaker": "host_two",
            "text": "And remember, the details live in the material — review it for the depth. See you next episode!",
        },
    ]
    return {"title": title, "lines": lines}


def _count_words(lines: list[dict]) -> int:
    return sum(len(str(line["text"]).split()) for line in lines)


# Exam Mode -------------------------------------------------------------------
# Deterministic mixed-type exams. The caller passes an ordered ``distribution``
# (one question type per slot); quick mode fills each slot strictly from the
# material so questions never reach outside the uploaded text.

EXAM_TYPE_PHRASINGS = {
    "mcq": "Which term best completes this sentence?\n\n\"{cloze}\"",
    "fill_blank": "Fill in the blank:\n\n\"{cloze}\"",
    "short_answer": "In one or two sentences, define \"{term}\" as covered in the study material.",
    "paragraph": (
        "Based only on the study material, explain the role and meaning of "
        "\"{term}\" in a short paragraph."
    ),
    "essay": (
        "Write a short essay about \"{term}\" using ONLY the study material. "
        "Cover the key points the material makes and stay grounded in the text."
    ),
}


def _default_exam_distribution(question_count: int) -> list[str]:
    """A sensible deterministic mix; same logic as the AI planner."""
    order = ["mcq", "mcq", "short_answer", "fill_blank", "paragraph", "essay"]
    distribution: list[str] = []
    idx = 0
    while len(distribution) < question_count:
        distribution.append(order[idx % len(order)])
        idx += 1
    return distribution[:question_count]


def _mcq_from(
    sentence: str, term: str, distractors: list[str], offset: int
) -> dict:
    options = list(dict.fromkeys([term] + distractors))
    if len(options) < 2:
        raise ValueError("Not enough terms for an MCQ exam question.")
    correct_idx = offset % len(options)
    rotated = options[correct_idx:] + options[:correct_idx]
    return {
        "question_type": "mcq",
        "question": (
            "Which term best completes this sentence?\n\n"
            f"\"{_cloze(sentence, term)}\""
        ),
        "options": rotated,
        "correct_answer": correct_idx,
        "accepted_answer": term,
        "explanation": (
            f"The answer is \"{term}\", which appears in the study "
            f"material: \"{sentence}\""
        ),
    }


def _from_sentence(qtype: str, term: str, sentences: list[str]) -> dict:
    sentence = _sentence_with(sentences, term)
    if sentence is None:
        raise ValueError(f"No sentence covering \"{term}\"")
    return {
        "question_type": qtype,
        "question": EXAM_TYPE_PHRASINGS[qtype].format(
            term=term, cloze=_cloze(sentence, term) if qtype == "fill_blank" else sentence
        ),
        "accepted_answer": sentence,
        "key_points": [term],
        "explanation": (
            f"Based on the study material: \"{sentence}\""
        ),
    }


def generate_exam(
    material_text: str,
    difficulty: str = "medium",
    question_count: int = 10,
    distribution: list[str] | None = None,
) -> list[dict]:
    """Deterministically build a mixed-type exam from the material.

    The returned questions mirror the raw dicts the LLM providers return so
    the shared normalizer in ``services/exam.py`` can validate them unchanged.
    Returns fewer questions than requested when the material is too short.
    """
    filled = distribution if distribution else _default_exam_distribution(question_count)
    filled = filled[:question_count]
    if not filled:
        return []

    sentences = _split_sentences(material_text)
    ranked = [term for term, _ in _term_counts(material_text)]
    pairs = _band(_pairs(sentences, ranked), difficulty)
    distractors_pool = [term for _, term in _pairs(sentences, ranked)]

    questions: list[dict] = []
    slot = 0
    for qtype in filled:
        if qtype == "mcq":
            if len(pairs) < 2:
                break
            sentence, term = pairs[slot % len(pairs)]
            distractors = [
                t for t in distractors_pool if t != term
            ][:3]
            try:
                questions.append(
                    _mcq_from(sentence, term, distractors, slot)
                )
            except ValueError:
                break
        else:
            if not pairs:
                break
            _, term = pairs[slot % len(pairs)]
            try:
                questions.append(_from_sentence(qtype, term, sentences))
            except ValueError:
                continue
        slot += 1

    if not questions and filled:
        # Material too short for even one question — fall back to cloze quiz
        for term in [t for _, t in pairs[:2]]:
            sentence = _sentence_with(sentences, term)
            if sentence is not None:
                questions.append(
                    _from_sentence("fill_blank", term, sentences)
                )
    return questions[:question_count]