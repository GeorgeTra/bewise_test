from __future__ import annotations
from flask_sqlalchemy import SQLAlchemy
from typing import Optional, List


db = SQLAlchemy()


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question_id = db.Column(db.Integer, nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    answer_text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'Question({self.id})'

    @classmethod
    def get_latest(cls) -> Optional[Question]:
        max_id = db.session.query(db.func.max(cls.id)).scalar()
        return cls.query.filter_by(id=max_id).first()

    @classmethod
    def get_duplicates(cls, questions_ids: List[int]) -> List[int]:
        existing_questions = cls.query.filter(cls.question_id.in_(questions_ids)).all()
        return [q.question_id for q in existing_questions]



