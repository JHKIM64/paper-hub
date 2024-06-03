from flask import session
from backend.db_connection import get_db_connection, close_db_connection
import numpy as np
def login(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE user_id = %s;', (user_id,))
    exists = cur.fetchone()

    if exists or user_id == "postgres":
        print("로그인 성공!")
    else:
        print("해당 아이디가 존재하지 않습니다. 회원가입을 진행합니다.")

    return conn, cur, exists


def signup(user_id, email, keywords, keywords_vector):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO users (user_id, email) VALUES (%s, %s);', (user_id, email))
    for keyword, keyword_vector in zip(keywords, keywords_vector):
        keyword_vector_str = np.array2string(keyword_vector, separator=',')
        cur.execute('INSERT INTO user_keyword (user_id, keyword, keyword_vector) VALUES (%s, %s, %s);', (user_id, keyword.strip(), keyword_vector_str))
    conn.commit()
    cur.close()
    conn.close()


def logout(conn, cur):
    if conn and cur:
        cur.close()
        conn.close()
        print("로그아웃 되었습니다.")
    close_db_connection()
