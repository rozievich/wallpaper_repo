import psycopg2
from psycopg2.extras import DictCursor
from data.config import DB_NAME, DB_PASSWORD

conn = psycopg2.connect(
    user="postgres",
    database=DB_NAME,
    password=DB_PASSWORD,
    host="localhost",
    port=5432,
    cursor_factory=DictCursor
)
cur = conn.cursor()

def create_db():
    user_query = '''
    CREATE TABLE IF NOT EXISTS users(
        id BIGSERIAL PRIMARY KEY,
        telegram_id VARCHAR(60) UNIQUE,
        username VARCHAR(50),
        first_name VARCHAR(128) NOT NULL,
        created_at TIMESTAMP DEFAULT now()
    );'''
    cur.execute(user_query)
    conn.commit()