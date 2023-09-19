import requests
from requests.exceptions import ConnectionError
from quizclient import load_questions, QuizAccessError, get_questions
import pytest
import json
from models import Question
from datetime import datetime


class ResponseStub:
    def __init__(self, status: int, content: str):
        self.status_code = status
        self.text = content


def test_load_questions_empty_list(mocker):
    m = mocker.patch('requests.get')
    m.return_value = ResponseStub(200, '[]')
    questions = load_questions('https://test', 10)
    assert isinstance(questions, list)
    assert len(questions) == 0
    requests.get.assert_called_once_with('https://test?count=10')


def test_load_questions_unavailable(mocker):
    m = mocker.patch('requests.get')
    m.side_effect = ConnectionError()
    with pytest.raises(QuizAccessError):
        load_questions('https://test', 10)
    requests.get.assert_called_once_with('https://test?count=10')


def test_load_questions_data(mocker):
    with open('test_data\\quiz_response.json', 'rt', encoding='utf-8') as f:
        response_text = f.read()
    m = mocker.patch('requests.get')
    m.return_value = ResponseStub(200, response_text)
    questions = load_questions('https://test', 10)
    assert isinstance(questions, list)
    assert len(questions) == 2
    question = questions[0]
    assert isinstance(question, dict)
    assert 'id' in question
    assert question['id'] == 566
    question1 = questions[1]
    assert isinstance(question1, dict)
    assert 'id' in question1
    assert question1['id'] == 567
    requests.get.assert_called_once_with('https://test?count=10')


def test_get_questions(mocker):
    with open('test_data\\quiz_response.json', 'rt', encoding='utf-8') as f:
        response_text = f.read()
    response_json = json.loads(response_text)
    m = mocker.patch('quizclient.load_questions')
    m.return_value = response_json
    questions = get_questions('https://test', 10)
    assert isinstance(questions, list)
    assert len(questions) == 2
    m.assert_called_once_with('https://test', 10)
    x = questions[0]
    assert isinstance(x, Question)
    assert x.question_id == 566
    assert x.question_text == 'Worlds 3rd largest, some of its inhabitants are "wild men"'
    assert x.answer_text == 'Borneo'
    assert x.created_at == datetime(2022, 12, 30, 18, 37, 50, 624000)
    assert x.id is None



