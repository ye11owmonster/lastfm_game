import requests
import random
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("API_KEY")
shared_secret = os.environ.get("SHARED_SECRET")
app_name = os.environ.get("APP_NAME")

def get_artist_info(mbid: str, name: str = '') -> dict:

    """
    Get information about an artist from the Last.fm API.

    Parameters:
    - mbid (str): The MusicBrainz Identifier (MBID) of the artist.
    - name (str): The name of the artist (optional, used if MBID is not provided).

    Returns:
    dict: Artist information as provided by the Last.fm API.
    If there is an error in the API response, an empty dictionary is returned.
    """

    if mbid != '':
        info = requests.get(f"http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&mbid={mbid}&api_key={api_key}&format=json").json()
    else:
        info = requests.get(f"http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist={name}&api_key={api_key}&format=json").json()
    
    if 'error' in info.keys():
        info = {}
    
    return info

def get_random_artists(user_name: str, n_artists: int = 5) -> dict:

    """
    Retrieves a random selection of artists from the user's Last.fm scrobbling history.

    Parameters:
    - user_name (str): Last.fm username.
    - n_artists (int, optional): Number of random artists to retrieve. Defaults to 5.

    Returns:
    dict: A dictionary containing information about the random artists.
          - 'random_page' (int): Randomly selected page from the user's scrobbling history.
          - 'positions' (str): Range of positions of the selected artists on the page.
          - 'artists' (list of dict): List of dictionaries, each containing information about a random artist.
              - 'name' (str): Artist name.
              - 'playcount' (str): Number of times the user has played the artist's tracks.
              - 'url' (str): Last.fm URL of the artist.
              - 'youtube_url' (str): YouTube search URL for the artist's name.

    """
    
    result = {}

    get_stats = requests.get(f"http://ws.audioscrobbler.com/2.0/?method=library.getartists&api_key={api_key}&user={user_name}&format=json").json()
    max_page = int(get_stats['artists']['@attr']['totalPages'])

    lucky_page = random.randint(1, max_page)

    get_lucky_page = requests.get(f"http://ws.audioscrobbler.com/2.0/?method=library.getartists&api_key={api_key}&user={user_name}&page={lucky_page}&format=json").json()

    max_artist_on_page = len(get_lucky_page['artists']['artist'])

    lower_bound = random.randint(1, max_artist_on_page)
    upper_bound = lower_bound + n_artists
    
    lucky_artists = get_lucky_page['artists']['artist'][lower_bound:upper_bound]

    result['random_page'] = lucky_page
    result['positions'] = f"{lucky_page * 50 + lower_bound} - {lucky_page * 50 + upper_bound}"
    result['artists'] = []

    for a in lucky_artists:

        additional_info = get_artist_info(a['mbid'], a['name'])

        artist_info = {
            'name': a['name'],
            'tags': ', '.join([f"#{x['name']}" for x in additional_info.get('artist', {}).get('tags', {}).get('tag','')]),
            'playcount': a['playcount'],
            'url': a['url'],
            'youtube_url': f"https://www.youtube.com/results?search_query={a['name'].lower().replace(' ', '+')}"
        }

        result['artists'].append(artist_info)

    return result

get_random_artists('ChaoticDots')
