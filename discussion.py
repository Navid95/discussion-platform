from main import create_flask_app, db
from main.models import User, Topic, Post
import os
from flask_migrate import Migrate

DISCUSSION_OPT_MODE = os.environ.get('DISCUSSION_OPT_MODE') or 'default'

app = create_flask_app(DISCUSSION_OPT_MODE)
migrate = Migrate(app=app, db=db)

with app.app_context():
    db.create_all()
    db.session.commit()


@app.shell_context_processor
def init_shell_context():
    return dict(db=db)
