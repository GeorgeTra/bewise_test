from main import app


@app.route('/hi')
def hi():
    return 'Text'



