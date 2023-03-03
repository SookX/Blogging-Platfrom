from flask_sqlalchemy import SQLAlchemy
from main import db, Account, app, Message

with app.app_context():
    db.create_all()