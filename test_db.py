from main import db, app
import os.path
import os
from models import Question
from datetime import datetime


def setup_function():
    with app.app_context():
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        db.init_app(app)
        db.create_all()


def teardown_function():
    with app.app_context():
        db.drop_all()


def test_read_empty():
    with app.app_context():
        questions = Question.query.all()
        assert isinstance(questions, list)
        assert len(questions) == 0


def test_create():
    with app.app_context():
        question = Question(
            question_id=10,
            question_text='to be or not to be',
            answer_text='123',
            created_at=datetime(2022, 12, 30, 18, 37, 50, 624000),
        )
        db.session.add(question)
        db.session.commit()
        question2 = Question.query.filter_by(question_id=10).first()
        assert question2 is not None
        assert question2.question_id == 10
        assert question2.question_text == 'to be or not to be'
        assert question2.answer_text == '123'
        assert question2.created_at == datetime(2022, 12, 30, 18, 37, 50, 624000)
        assert isinstance(question2.id, int)


def test_get_latest_empty():
    with app.app_context():
        q = Question.get_latest()
        assert q is None


def test_get_latest_several():
    create_questions()
    with app.app_context():
        q = Question.get_latest()
        assert q is not None
        assert isinstance(q, Question)
        assert q.question_id == 5


def test_get_duplicates_exist():
    create_questions()
    with app.app_context():
        ids = Question.get_duplicates([1, 2, 3, 4, 5])
        assert ids == [5]


def test_get_duplicates_not_exist():
    create_questions()
    with app.app_context():
        ids = Question.get_duplicates([1, 2, 3, 4])
        assert ids == []


def create_questions():
    with app.app_context():
        question = Question(
            question_id=10,
            question_text='to be or not to be',
            answer_text='123',
            created_at=datetime(2022, 12, 30, 18, 37, 50, 624000),
        )
        db.session.add(question)
        db.session.commit()
        question = Question(
            question_id=5,
            question_text='some text',
            answer_text='some answer',
            created_at=datetime(2023, 5, 18, 18, 37, 50, 624000),
        )
        db.session.add(question)
        db.session.commit()






