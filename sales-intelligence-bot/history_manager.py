import json
from pathlib import Path


HISTORY_FILE = Path(__file__).parent / "search_history.json"

MAX_ITEMS = 7


def _load_all() -> list:

    if not HISTORY_FILE.exists():
        return []

    try:

        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    except (json.JSONDecodeError, OSError):
        return []


def _save_all(questions: list):

    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)


def save_question(question: str):
    """Add a question to the top of history (dedup + capped at MAX_ITEMS)."""

    questions = _load_all()

    if question in questions:
        questions.remove(question)

    questions.insert(0, question)

    questions = questions[:MAX_ITEMS]

    _save_all(questions)


def get_recent_questions(limit: int = MAX_ITEMS) -> list:
    """Return the most recent questions, newest first."""

    return _load_all()[:limit]


def clear_history():

    _save_all([])