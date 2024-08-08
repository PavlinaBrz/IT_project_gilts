from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from db import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

def add_user(username, hashed_password):
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    print(f"User added: ID={new_user.id}, Username={new_user.username}, Password Hash={new_user.password}")

def get_user(username):
    user = User.query.filter_by(username=username).first()
    if user:
        print(f"User found in database: {user.username}")
    else:
        print("User not found in database.")
    return user