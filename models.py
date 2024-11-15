from flask_login import UserMixin
import psycopg2


class User(UserMixin):
    def __init__(self, id, email, password, name):
        self.id = id
        self.email = email
        self.password = password
        self.name = name

    @staticmethod
    def get_user_by_email(email):
        conn = psycopg2.connect("dbname='lab5pad' user='web_rgz' password='123' host='localhost'")
        cursor = conn.cursor()
        cursor.execute("SELECT id, email, password, name FROM users WHERE email = %s", (email,))
        user_data = cursor.fetchone()
        conn.close()
        if user_data:
            return User(*user_data)
        return None

    @staticmethod
    def get_user_by_id(user_id):
        conn = psycopg2.connect("dbname='lab5pad' user='web_rgz' password='123' host='localhost'")
        cursor = conn.cursor()
        cursor.execute("SELECT id, email, password, name FROM users WHERE id = %s", (user_id,))
        user_data = cursor.fetchone()
        conn.close()
        if user_data:
            return User(*user_data)
        return None

    @staticmethod
    def create_user(name, email, hashed_password):
        conn = psycopg2.connect("dbname='lab5pad' user='web_rgz' password='123' host='localhost'")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
            (name, email, hashed_password)
        )
        conn.commit()
        conn.close()
        return True
