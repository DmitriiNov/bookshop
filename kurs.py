from app import app, db
from app.models import User, Book
from flask import session

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Book': Book, 'session': session}
