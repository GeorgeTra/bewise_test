from quizclient import get_questions
from models import Question
from models import db
from typing import List


def save_new_questions(questions_number: int, url: str) -> Question:
    remaining = questions_number
    latest = Question.get_latest()
    while remaining > 0:
        new_questions = get_questions(url, remaining)
        new_ids = [q.question_id for q in new_questions]
        existing_ids = Question.get_duplicates(new_ids)
        new_questions = [q for q in new_questions if q.question_id not in existing_ids]
        if len(new_questions) > 0:
            db.session.add_all(new_questions)
            db.session.commit()
        remaining = len(existing_ids)
    return latest




