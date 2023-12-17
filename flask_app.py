# Install Flask if you haven't already: pip install Flask

from flask import Flask, render_template, request, session
from last_fm_api import get_random_artists
from flask_session import Session

app = Flask(__name__, static_folder='static')

# # Configure session to use the filesystem
# app.config['SESSION_TYPE'] = 'filesystem'
# Session(app)

@app.route('/')
def index():

    username = session.get('username', '')

    return render_template('index.html', username=username)

@app.route('/about')
def about():

    return render_template('about.html')

@app.route('/', methods=['POST'])
def render_random_artists():

    username = request.form['username']

    # Store the username in the session
    #session['username'] = username
    
    # Call your last.fm API code here
    # Replace the following line with the actual function call from your code
    random_artists = get_random_artists(username)
    
    return render_template('index.html', username=username, random_artists=random_artists)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
