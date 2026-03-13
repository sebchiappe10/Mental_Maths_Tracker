import csv
import os

QUESTIONS_FILE = "questions.csv"
QUESTIONS_HEADERS = [
    "session_id", "date", "operator", "number_1", "number_2",
    "correct_answer", "my_answer", "is_correct", "response_time_ms", "difficulty_level"
]

SESSIONS_FILE = "sessions.csv"
SESSIONS_HEADERS = [
    "session_id", "date", "level", "total_questions",
    "correct", "score_percent", "operator_focus"
]


def write_question(row: dict) -> None:
    """Append one question result row to questions.csv."""
    file_exists = os.path.isfile(QUESTIONS_FILE)
    with open(QUESTIONS_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=QUESTIONS_HEADERS)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


def write_session(summary: dict) -> None:
    """Append one session summary row to sessions.csv."""
    file_exists = os.path.isfile(SESSIONS_FILE)
    with open(SESSIONS_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=SESSIONS_HEADERS)
        if not file_exists:
            writer.writeheader()
        writer.writerow(summary)