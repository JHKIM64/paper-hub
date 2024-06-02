from backend.db_connection import get_db_connection, close_db_connection

def create_tables():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id VARCHAR PRIMARY KEY,
        email VARCHAR
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS paper (
        paper_id INT PRIMARY KEY,
        title VARCHAR,
        reference INT,
        venue VARCHAR,
        year INT,
        n_citation INT,
        author VARCHAR
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS abstract (
        paper_id INT PRIMARY KEY,
        abstract TEXT,
        abstract_vector TEXT,
        FOREIGN KEY (paper_id) REFERENCES paper(paper_id)
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS follow (
        user_id VARCHAR,
        follower_id VARCHAR,
        PRIMARY KEY (user_id, follower_id),
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        FOREIGN KEY (follower_id) REFERENCES users(user_id)
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS user_keyword (
        user_id VARCHAR,
        keyword TEXT,
        PRIMARY KEY (user_id, keyword),
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );
    """)

    conn.commit()
    cur.close()
    close_db_connection()
