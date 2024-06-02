def add_paper(conn, cur, user_id, title, venue, year, abstract_text):
    # 현재 paper 테이블의 최대 paper_id 가져오기
    cur.execute('SELECT COALESCE(MAX(paper_id), 0) FROM paper')
    max_paper_id = cur.fetchone()[0]

    # 새로운 paper_id 설정
    new_paper_id = max_paper_id + 1

    # 논문 정보 삽입
    cur.execute('''
        INSERT INTO paper (paper_id, title, reference, venue, year, n_citation, author)
        VALUES (%s, %s, -1, %s, %s, 0, %s);
    ''', (new_paper_id, title, venue, year, user_id))

    # abstract 테이블에 초록 정보 삽입
    cur.execute('''
        INSERT INTO abstract (paper_id, abstract)
        VALUES (%s, %s);
    ''', (new_paper_id, abstract_text))

    conn.commit()
    return "논문 정보와 초록이 성공적으로 저장되었습니다."
