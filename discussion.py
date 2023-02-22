from main import create_flask_app, db
import os
from main.models import User, Topic, Post

DISCUSSION_OPT_MODE = os.environ.get('DISCUSSION_OPT_MODE') or 'default'

app = create_flask_app(DISCUSSION_OPT_MODE)

with app.app_context():
    db.create_all()
    db.session.commit()

