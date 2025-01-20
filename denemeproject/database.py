import sqlite3

class Database:
    @staticmethod
    def create_db():
        conn = sqlite3.connect("quiz.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                best_score INTEGER
            )
        """)
        conn.commit()
        conn.close()

    @staticmethod
    def get_user_best_score(username):
        conn = sqlite3.connect("quiz.db")
        cursor = conn.cursor()
        cursor.execute("SELECT best_score FROM users WHERE name=?", (username,))
        result = cursor.fetchone()
        conn.close()
        if result:
            return result[0]
        else:
            return None

    @staticmethod
    def update_user_score(username, score):
        conn = sqlite3.connect("quiz.db")
        cursor = conn.cursor()
        existing_score = Database.get_user_best_score(username)
        if existing_score is None:
            cursor.execute("INSERT INTO users (name, best_score) VALUES (?, ?)", (username, score))
        elif score > existing_score:
            cursor.execute("UPDATE users SET best_score=? WHERE name=?", (score, username))
        conn.commit()
        conn.close()
