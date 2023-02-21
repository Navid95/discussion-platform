from flask import Flask
from main import create_flask_app
import os


DISCUSSION_OPT_MODE = os.environ.get('DISCUSSION_OPT_MODE') or 'default'

app = create_flask_app(DISCUSSION_OPT_MODE)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
