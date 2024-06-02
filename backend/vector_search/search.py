from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from backend.vector_search.embedding import get_embedding
from collections import defaultdict
def find_relevant_papers(cur, query, model, tokenizer, top_n=5):
    # Get the query embedding
    query_vector = get_embedding(query, model, tokenizer)

    # Retrieve all abstract vectors from the database
    cur.execute("SELECT paper_id, abstract_vector FROM abstract")
    rows = cur.fetchall()

    # Convert database vectors to numpy array
    paper_ids = []
    vectors = []
    for row in rows:
        paper_id, vector_str = row
        vector = np.fromstring(vector_str[1:-1], sep=',')
        paper_ids.append(paper_id)
        vectors.append(vector)

    vectors = np.array(vectors)

    # Compute cosine similarity between query vector and abstract vectors
    similarities = cosine_similarity([query_vector], vectors)[0]

    # Get the top_n most similar papers
    top_indices = similarities.argsort()[-top_n:][::-1]

    # Fetch the details of the top_n papers
    relevant_papers = []
    for idx in top_indices:
        paper_id = paper_ids[idx]
        cur.execute("SELECT title FROM paper WHERE paper_id = %s", (paper_id,))
        paper = cur.fetchone()
        relevant_papers.append({
            "paper_id": paper_id,
            "title": paper[0],
            "similarity_score": similarities[idx]
        })

    return relevant_papers


def recommend_papers_by_keywords(cur, user_id, top_n=3):
    # 특정 유저의 키워드 벡터들을 가져옵니다.
    cur.execute('SELECT keyword, keyword_vector FROM user_keyword WHERE user_id = %s', (user_id,))
    keywords = cur.fetchall()

    if not keywords:
        return []

    # 모든 논문 초록 벡터를 가져옵니다.
    cur.execute('SELECT paper_id, abstract_vector FROM abstract')
    abstracts = cur.fetchall()

    recommendations = defaultdict(list)

    for keyword, keyword_vector in keywords:
        keyword_vector = np.fromstring(keyword_vector[1:-1], sep=',')
        keyword_recommendations = []

        for paper_id, abstract_vector in abstracts:
            abstract_vector = np.fromstring(abstract_vector[1:-1], sep=',')
            similarity = cosine_similarity([keyword_vector], [abstract_vector])[0][0]
            keyword_recommendations.append((paper_id, similarity))

        keyword_recommendations.sort(key=lambda x: x[1], reverse=True)
        recommendations[keyword] = keyword_recommendations[:top_n]

    result = []
    for keyword, papers in recommendations.items():
        result.append('keyword : ' + keyword)
        for paper_id, similarity in papers:
            cur.execute('SELECT title FROM paper WHERE paper_id = %s', (paper_id,))
            title = cur.fetchone()[0]
            result.append({
                'paper_id': paper_id,
                'title': title,
            })
        result.append('=' * 100)
    return result


# if __name__ == '__main__':
#     # Load HuggingFace model and tokenizer
#     import psycopg2
#     from transformers import AutoTokenizer, AutoModel
#     import torch
#     import numpy as np
#     from sklearn.metrics.pairwise import cosine_similarity
#
#     model_name = "sentence-transformers/all-MiniLM-L6-v2"
#     tokenizer = AutoTokenizer.from_pretrained(model_name)
#     model = AutoModel.from_pretrained(model_name)
#
#     # Example usage
#     query = "Find papers related to neural network."
#     print("=" * 50)
#     print(f"Query: {query}")
#     print("=" * 50)
#     print("\nRelevant Papers:")
#     print("-" * 50)
#     relevant_papers = find_relevant_papers(query, top_n=3, model=model, tokenizer=tokenizer)
#     for paper in relevant_papers:
#         print(f"Paper ID: {paper['paper_id']}")
#         print(f"Title: {paper['title']}")
#         print(f"Similarity Score: {paper['similarity_score']}")
#         print("-" * 50)
