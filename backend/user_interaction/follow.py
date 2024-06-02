
def get_follower(cur, user_id):
    cur.execute('SELECT follower_id FROM follow WHERE user_id = %s;', (user_id,))
    follower = cur.fetchall()
    return follower

def follow_user(cur, user_id, follower_id):
    try:
        cur.execute('SELECT 1 FROM users WHERE user_id = %s;', (user_id,))
        user_exists = cur.fetchone()
        if not user_exists:
            return f"User {user_id} does not exist."

        cur.execute('SELECT 1 FROM users WHERE user_id = %s;', (follower_id,))
        follower_exists = cur.fetchone()
        if not follower_exists:
            return f"{follower_id} 저자는 데이터베이스에 존재하지 않습니다."

        cur.execute('SELECT 1 FROM follow WHERE user_id = %s AND follower_id = %s;', (user_id, follower_id))
        already_following = cur.fetchone()
        if already_following:
            return f"{follower_id}를 이미 팔로우하고 있습니다."

        cur.execute('INSERT INTO follow (user_id, follower_id) VALUES (%s, %s);', (user_id, follower_id))
        cur.connection.commit()
        return f"{follower_id} 팔로우를 시작했습니다."
    except Exception as e:
        cur.connection.rollback()
        return f"An error occurred: {e}"

def unfollow_user(cur, user_id, follower_id):
    try:
        cur.execute('SELECT 1 FROM users WHERE user_id = %s;', (user_id,))
        user_exists = cur.fetchone()
        if not user_exists:
            return f"User {user_id} does not exist."

        cur.execute('SELECT 1 FROM users WHERE user_id = %s;', (follower_id,))
        follower_exists = cur.fetchone()
        if not follower_exists:
            return f"{follower_id}는 데이터베이스에 존재하지 않습니다."

        cur.execute('SELECT 1 FROM follow WHERE user_id = %s AND follower_id = %s;', (user_id, follower_id))
        follow_exists = cur.fetchone()
        if not follow_exists:
            return f"{follower_id}는 팔로우 목록에 없습니다."

        cur.execute('DELETE FROM follow WHERE user_id = %s AND follower_id = %s;', (user_id, follower_id))
        cur.connection.commit()
        return f"{follower_id} 팔로우를 취소했습니다."
    except Exception as e:
        cur.connection.rollback()
        return f"An error occurred: {e}"
