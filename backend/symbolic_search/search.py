
def statistic_by_year(cur, year):
    cur.execute("""
        SELECT COUNT(*) AS total_papers,
               AVG(n_citation) AS avg_citation,
               MAX(n_citation) AS max_citation
        FROM paper
        WHERE year = %s;
    """, (year,))
    row = cur.fetchone()
    return row

def high_citation(cur):
    cur.execute("""
        CREATE OR REPLACE VIEW high_citation_papers AS
        SELECT title, author, n_citation
        FROM paper
        WHERE n_citation = (SELECT MAX(n_citation) FROM paper);
    """)
    cur.connection.commit()
    cur.execute("SELECT * FROM high_citation_papers;")
    rows = cur.fetchall()
    return rows

def get_followed_authors_papers_by_year(cur, user_id):
    cur.execute("""
    SELECT author, year, ARRAY_AGG(title) AS papers
    FROM paper
    WHERE author IN (
        SELECT DISTINCT author
        FROM paper
        WHERE author IN (
            SELECT follower_id
            FROM follow
            WHERE user_id = %s
        )
    )
    GROUP BY author, year
    ORDER BY author, year DESC;
    """, (user_id,))
    results = cur.fetchall()
    papers_by_author_year = {}
    for row in results:
        author = row[0]
        year = row[1]
        papers = row[2]
        if author not in papers_by_author_year:
            papers_by_author_year[author] = {}
        papers_by_author_year[author][year] = papers
    return papers_by_author_year

def search_by_author(cur, author_name):
    cur.execute('''
        SELECT paper.paper_id, paper.title, paper.venue, paper.year, paper.n_citation, abstract.abstract, paper.reference, paper.author
        FROM paper
        INNER JOIN abstract ON paper.paper_id = abstract.paper_id
        WHERE paper.author ILIKE %s
        ORDER BY paper.n_citation DESC, paper.year DESC
        LIMIT 5;
    ''', ('%' + author_name + '%',))
    papers = cur.fetchall()

    return papers
