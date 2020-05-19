from app import app, db
from app.models import Building, StudySpace, User, Post

@app.shell_context_processor
def make_shell_context():
    return {'db':db, 'Building':Building, 'StudySpace':StudySpace,\
            'User':User, 'Post':Post}