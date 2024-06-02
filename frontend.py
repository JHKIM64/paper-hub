from flask import Flask, render_template, request, redirect, url_for, session, g, jsonify
from backend import create_tables, close_db_connection
from backend.user_interaction import follow_user, unfollow_user, get_follower, add_paper
from backend.symbolic_search import statistic_by_year, high_citation, get_followed_authors_papers_by_year, \
    search_by_author
from backend.vector_search import find_relevant_papers, recommend_papers_by_keywords, model_select
from backend.authentication import login, signup, logout

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Initialize the model and tokenizer
model, tokenizer = model_select()

# Initialize the database
conn, cur = None, None


@app.before_request
def clear():
    if not conn:
        session.clear()


@app.route('/')
def home():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
def login_view():
    if request.method == 'POST':
        user_id = request.form['user_id']
        global conn, cur
        conn, cur, exist = login(user_id)
        if exist:
            session['username'] = user_id  # 세션에 사용자 이름 설정
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'message': 'User ID not found.'})
    session.clear()
    return render_template('login.html')

@app.route('/logout')
def logout_view():
    logout(conn, cur)
    session.pop('username', None)
    session.clear()
    return redirect(url_for('home'))


@app.route('/signup', methods=['GET', 'POST'])
def signup_view():
    if request.method == 'POST':
        user_id = request.form['user_id']
        email = request.form['email']
        keywords = request.form['keywords'].split(',')

        signup(cur, user_id, email, keywords)
        return redirect(url_for('login_view'))
    return render_template('signup.html')


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login_view'))

    if request.method == 'POST':
        action = request.form['action']
        if action == 'search_by_author':
            return redirect(url_for('search_by_author_view'))
        elif action == 'high_citation':
            return redirect(url_for('high_citation_view'))
        elif action == 'statistic_by_year':
            return redirect(url_for('statistic_by_year_view'))
        elif action == 'add_paper':
            return redirect(url_for('add_paper_view'))
        elif action == 'follow_user':
            return redirect(url_for('follow_user_view'))
        elif action == 'unfollow_user':
            return redirect(url_for('unfollow_user_view'))
        elif action == 'get_follower':
            return redirect(url_for('get_follower_view'))
        elif action == 'get_followed_authors_papers_by_year':
            return redirect(url_for('get_followed_authors_papers_by_year_view'))
        elif action == 'find_relevant_papers':
            return redirect(url_for('find_relevant_papers_view'))
        elif action == 'recommend_papers_by_keywords':
            return redirect(url_for('recommend_papers_by_keywords_view'))

    return render_template('dashboard.html', username=session['username'])


@app.route('/find_relevant_papers', methods=['GET', 'POST'])
def find_relevant_papers_view():
    if request.method == 'POST':
        query = request.form['query']

        relevant_papers = find_relevant_papers(cur, query, model, tokenizer)
        return render_template('result.html', result=relevant_papers)
    return render_template('find_relevant_papers.html')


@app.route('/recommend_papers_by_keywords', methods=['GET'])
def recommend_papers_by_keywords_view():
    print("recommend_papers_by_keywords_view")

    user_id = session['username']
    papers = recommend_papers_by_keywords(cur, user_id)
    return render_template('result.html', result=papers)



@app.route('/search_by_author', methods=['GET'])
def search_by_author_view():
    if request.method == 'POST':
        author_name = request.form['author_name']

        papers = search_by_author(cur, author_name)
        return render_template('result.html', result=papers)
    return render_template('search_by_author.html')


@app.route('/high_citation', methods=['GET'])
def high_citation_view():
    papers = high_citation(cur)
    return render_template('result.html', result=papers)


@app.route('/statistic_by_year', methods=['GET', 'POST'])
def statistic_by_year_view():
    if request.method == 'POST':
        year = request.form['year']

        stats = statistic_by_year(cur, year)
        return render_template('result.html', result=[stats])
    return render_template('statistic_by_year.html')


@app.route('/add_paper', methods=['GET', 'POST'])
def add_paper_view():
    if request.method == 'POST':
        user_id = session['username']
        title = request.form['title']
        venue = request.form['venue']
        year = request.form['year']
        abstract_text = request.form['abstract_text']
        result = add_paper(conn, cur, user_id, title, venue, year, abstract_text)
        return render_template('result.html', result=[result])
    return render_template('add_paper.html')


@app.route('/follow_user', methods=['GET', 'POST'])
def follow_user_view():
    if request.method == 'POST':
        user_id = session['username']
        follower_id = request.form['follower_id']

        result = follow_user(cur, user_id, follower_id)
        return render_template('result.html', result=[result])
    return render_template('follow_user.html')


@app.route('/unfollow_user', methods=['GET', 'POST'])
def unfollow_user_view():
    if request.method == 'POST':
        user_id = session['username']
        follower_id = request.form['follower_id']

        result = unfollow_user(cur, user_id, follower_id)
        return render_template('result.html', result=[result])
    return render_template('unfollow_user.html')


@app.route('/get_follower', methods=['GET'])
def get_follower_view():
    user_id = session['username']

    followers = get_follower(cur, user_id)
    return render_template('result.html', result=followers)


@app.route('/get_followed_authors_papers_by_year', methods=['GET'])
def get_followed_authors_papers_by_year_view():
    user_id = session['username']

    papers = get_followed_authors_papers_by_year(cur, user_id)
    return render_template('result.html', result=papers)


@app.teardown_appcontext
def teardown_db(Exception):
    print("wait for response...")


if __name__ == '__main__':
    app.run(debug=True)
