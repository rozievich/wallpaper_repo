from .connect import cur, conn

class User:
    def create_user(self, telegram_id: str, username: str, first_name: str):
        try:
            cur.execute("INSERT INTO users(telegram_id, username, first_name) VALUES(%s, %s, %s)", (telegram_id, username, first_name))
            conn.commit()
        except:
            pass
    
    def get_user(self, telegram_id: str):
        try:
            cur.execute("SELECT * FROM users WHERE telegram_id = %s", (telegram_id, ))
            return cur.fetchone()
        except:
            pass
    
    def all_users(self):
        try:
            cur.execute("SELECT * FROM users")
            return cur.fetchall()
        except:
            pass
