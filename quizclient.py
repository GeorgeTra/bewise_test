from flask import Flask, request, Response
import json
from requests import exceptions
from datetime import datetime
import requests
from models import Question
from typing import List


class QuizAccessError(Exception):
    pass


def load_questions(url: str, questions_number: int) -> List:
    request_url = f'{url}?count={questions_number}'
    try:
        r = requests.get(request_url)
    except exceptions.ConnectionError as e:
        raise QuizAccessError('Вопросы недоступны.') from e
    if r.status_code != 200:
        raise QuizAccessError('Ошибка при обращении к вопросам.')
    answers = r.text
    answers = json.loads(answers)
    return answers


def get_questions(url: str, questions_number: int) -> List[Question]:
    questions_list = load_questions(url, questions_number)
    result = []
    for question_dict in questions_list:
        question = Question()
        question.question_id = question_dict['id']
        question.question_text = question_dict['question']
        question.answer_text = question_dict['answer']
        question.created_at = datetime.strptime(question_dict['created_at'], "%Y-%m-%dT%H:%M:%S.%fZ")
        result.append(question)
    return result