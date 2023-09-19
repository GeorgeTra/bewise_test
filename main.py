from flask import Flask, request, make_response
from models import db
import requestschemas
import jsonschema
from logic import save_new_questions
import os


PGHOST = os.getenv('PGHOST')
PGPORT = os.getenv('PGPORT')
PGDB = os.getenv('PGDB')
PGUSER = os.getenv('PGUSER')
PGPASS = os.getenv('PGPASS')
SQLITE_FILE = os.getenv('SQLITE_FILE')
USE_SQLITE = os.getenv('USE_SQLITE')


def create_app():
    pg_uri = f'postgresql://{PGUSER}:{PGPASS}@{PGHOST}:{PGPORT}/{PGDB}'
    sqlite_uri = f'sqlite:///{SQLITE_FILE}'
    if USE_SQLITE == 'Y':
        db_uri = sqlite_uri
    else:
        db_uri = pg_uri
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['QUIZ_SERVICE_URL'] = 'https://jservice.io/api/random'
    return app


app = create_app()


@app.route('/')
def hello():
    return 'Hello!'


@app.route('/question', methods=['POST'])
def process_questions():
    json_data = request.json
    try:
        jsonschema.validate(json_data, schema=requestschemas.PROCESS_QUESTIONS)
    except jsonschema.ValidationError:
        return make_response('invalid schema', 400)
    quiz_url = app.config['QUIZ_SERVICE_URL']
    questions_num = json_data['questions_num']
    last_question = save_new_questions(questions_num, quiz_url)
    if last_question is None:
        result = {}
    else:
        result = {
            'question_id': last_question.id,
            'question_text': last_question.question_text,
            'answer_text': last_question.answer_text
        }
    return result


@app.cli.command('init-db')
def init_db():
    db.init_app(app)
    db.create_all()
    print('OK!')


if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0")




