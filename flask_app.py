# Install Flask if you haven't already: pip install Flask

from flask import Flask, render_template, request, session
from last_fm_api import get_random_artists
import secrets
import sqlite3

app = Flask(__name__, static_folder='static')
app.secret_key = secrets.token_hex(nbytes=16)

@app.route('/')
def index():

    username = session.get('username', '')

    return render_template('index.html', username=username)

@app.route('/about')
def about():

    return render_template('about.html')

@app.route('/how_to_play')
def how_to_play():

    return render_template('how_to_play.html')

@app.route('/', methods=['POST'])
def render_random_artists():

    username = request.form['username']

    # Store the username in the session
    session['username'] = username
    
    # Call your last.fm API code here
    # Replace the following line with the actual function call from your code
    random_artists = get_random_artists(username)
    if 'error' in random_artists.keys():
        session.clear()
        return render_template('error.html', username=username, random_artists=random_artists)
    else:
        return render_template('generation.html', username=username, random_artists=random_artists)

@app.route('/clear', methods=['POST'])
def clear_session():
    session.clear()
    return render_template('index.html')

def get_db_connection():
    conn = sqlite3.connect('static/databases/db_lastfm_persistent.db')
    conn.row_factory = sqlite3.Row  # This allows us to use row['column_name']
    return conn

@app.route('/history', methods=['GET', 'POST'])
def get_history():

    username = session.get('username', '')
    # Get the page number from the query string (default is 1)
    page = request.args.get('page', 1, type=int)
    per_page = 5  # Number of entries per page
    total_pages_to_display = 10

    conn = get_db_connection()
    # Calculate the offset for the SQL query
    offset = (page - 1) * per_page
    # Fetch data with limit and offset for pagination
    rows = conn.execute("SELECT strftime('%Y-%m-%d', timestamp) as date, artist, tags FROM generation_history WHERE username=? ORDER BY date desc LIMIT ? OFFSET ?", (username, per_page, offset)).fetchall()
    total_rows = conn.execute('SELECT COUNT(*) FROM generation_history WHERE username=?', (username, )).fetchone()[0]
    conn.close()

    # Calculate total number of pages
    total_pages = (total_rows + per_page - 1) // per_page

    start_page = max(1, page - total_pages_to_display // 2)
    end_page = min(start_page + total_pages_to_display - 1, total_pages)

    return render_template('history.html', rows=rows, page=page, total_pages=total_pages, username=username, start_page=start_page, end_page=end_page)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
