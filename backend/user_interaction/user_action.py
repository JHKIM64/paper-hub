import numpy as np
def add_paper(conn, cur, user_id, title, venue, year, abstract_text, abstract_text_vector):
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
    conn.commit()

    # abstract 테이블에 초록 정보 삽입
    abstract_text_vector_str = np.array2string(abstract_text_vector, separator=',')
    cur.execute('''
        INSERT INTO abstract (paper_id, abstract, abstract_vector)
        VALUES (%s, %s, %s);
    ''', (new_paper_id, abstract_text, abstract_text_vector_str))

    conn.commit()
    return "논문 정보와 초록이 성공적으로 저장되었습니다."
