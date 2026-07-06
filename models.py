from flask_login import UserMixin
from db import get_db

class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

def get_user_by_username(username):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE username = %s", (username,))
    return cursor.fetchone()

def get_user_by_id(user_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE id = %s", (user_id,))
    return cursor.fetchone()
