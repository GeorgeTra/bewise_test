import main
import pytest
from models import Question
from datetime import datetime


@pytest.fixture()
def app():
    app = main.app
    app.config['TESTING'] = True
    app.config['QUIZ_SERVICE_URL'] = 'http://test'
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


def test_process_questions_invalid_schema(client):
    response = client.post('/question', json={'questions_num': 'abcd'})
    assert response.status_code == 400
    response = client.post('/question', json={'questions_num': -1})
    assert response.status_code == 400


def test_process_questions_invalid_json(client):
    response = client.post('/question', data={'questions_num': 'abcd'})
    assert response.status_code == 415
    response = client.post('/question', data='abcd', headers={'Content-Type': 'application/json'})
    assert response.status_code == 400


def test_process_questions_no_question(client, mocker):
    m = mocker.patch('main.save_new_questions')
    m.return_value = None
    response = client.post('/question', json={'questions_num': 2})
    assert response.status_code == 200
    assert response.json == {}
    m.assert_called_once_with(2, 'http://test')


def test_process_questions_with_question(client, mocker):
    m = mocker.patch('main.save_new_questions')
    dt = datetime(2023, 8, 25, 8, 37, 11)
    m.return_value = Question(id=100,
                              question_id=5,
                              question_text='abracadabra',
                              answer_text='no',
                              created_at=dt)
    response = client.post('/question', json={'questions_num': 10})
    assert response.status_code == 200
    assert response.json == {'question_id': 100, 'question_text': 'abracadabra', 'answer_text': 'no'}
    m.assert_called_once_with(10, 'http://test')
