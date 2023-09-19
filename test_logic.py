from models import Question
from datetime import datetime
from logic import save_new_questions
from main import db, app


def setup_function():
    with app.app_context():
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        db.init_app(app)
        db.create_all()


def teardown_function():
    with app.app_context():
        db.drop_all()


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


def test_save_new_questions(mocker):
    create_questions()
    d = datetime(2022, 12, 30, 18, 37, 50, 624000)
    m = mocker.patch('logic.get_questions')
    m.side_effect = [
        [
            Question(question_id=3, question_text='a, b, c', answer_text='123', created_at=d),
            Question(question_id=10, question_text='lalala', answer_text='bridge', created_at=d)
        ],
        [
            Question(question_id=3, question_text='lalala', answer_text='bridge', created_at=d)
        ],
        [
            Question(question_id=11, question_text='lesson', answer_text='seminar', created_at=d)
        ]
    ]
    with app.app_context():
        s = save_new_questions(2, 'https://test')
        assert s is not None
        assert s.question_id == 5

    with app.app_context():
        s = Question.query.all()
        assert isinstance(s, list)
        assert len(s) == 4
        assert s[0].question_id == 10
        assert s[1].question_id == 5
        assert s[2].question_id == 3
        assert s[3].question_id == 11

