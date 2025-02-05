"""
database_users.py
-----------------
Obsahuje SQLAlchemy model 'User' pro ukládání uživatelů (autentizace),
spolu s pomocnými funkcemi pro vytváření a vyhledávání uživatelů.
"""

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from db import db


class User(db.Model, UserMixin):
    """
    SQLAlchemy model reprezentující tabulku 'users'.
    Využívá Flask-Login (UserMixin) pro snadnou správu přihlášení.

    Sloupce:
      - id (int, PK)
      - username (str, unikátní, nepovolené nulové hodnoty)
      - password (str): heslo uložené jako hash
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)


def add_user(username, hashed_password):
    """
    Vytvoří nového uživatele v tabulce 'users' a uloží ho do DB.

    :param username: Jedinečné uživatelské jméno
    :param hashed_password: Hash hesla (např. z generate_password_hash)
    :return: None, ale do DB se zapíše nový řádek.
    """
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    print(f"User added: ID={new_user.id}, Username={new_user.username}, Password Hash={new_user.password}")


def get_user(username):
    """
    Vyhledá uživatele v DB podle username.

    :param username: Uživatelské jméno (string)
    :return: Objekt User, pokud existuje; jinak None.
    """
    user = User.query.filter_by(username=username).first()
    if user:
        print(f"User found in database: {user.username}")
    else:
        print("User not found in database.")
    return user