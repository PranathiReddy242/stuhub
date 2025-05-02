from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from .db import get_db
import uuid
from datetime import datetime
import sqlite3

class User(UserMixin):
    def __init__(self, id_, username, email, password):
        self.id = id_
        self.username = username
        self.email = email
        self.password = password

    @staticmethod
    def get(user_id):
        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE id = ?", (user_id,)
        ).fetchone()
        if not user:
            return None
        return User(id_=user['id'], username=user['username'], 
                   email=user['email'], password=user['password'])

    @staticmethod
    def create(username, email, password):
        db = get_db()
        try:
            db.execute(
                "INSERT INTO users (id, username, email, password) VALUES (?, ?, ?, ?)",
                (str(uuid.uuid4()), username, email, generate_password_hash(password))
            )
            db.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    @staticmethod
    def find_by_email(email):
        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE email = ?", (email,)
        ).fetchone()
        if not user:
            return None
        return User(id_=user['id'], username=user['username'], 
                   email=user['email'], password=user['password'])

class Post:
    @staticmethod
    def create(content, user_id):
        db = get_db()
        db.execute(
            "INSERT INTO posts (id, content, user_id) VALUES (?, ?, ?)",
            (str(uuid.uuid4()), content, user_id)
        )
        db.commit()

    @staticmethod
    def get_all():
        db = get_db()
        return db.execute('''
            SELECT posts.*, users.username 
            FROM posts LEFT JOIN users ON posts.user_id = users.id
            ORDER BY created_at DESC
        ''').fetchall()

    @staticmethod
    def get_by_user(user_id):
        db = get_db()
        return db.execute('''
            SELECT * FROM posts WHERE user_id = ? 
            ORDER BY created_at DESC
        ''', (user_id,)).fetchall()