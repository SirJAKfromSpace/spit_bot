import spotipy
import spotipy.util as util
import os
from dotenv import load_dotenv
load_dotenv()

# print('SPIT Initializing')
# print(f'{client_id} {client_secret}')
def spotipy_auth():
    print('Connect using Spotipy Web API')
    client_id = os.getenv('cid')
    client_secret = os.getenv('csecret')
    redirect_uri = 'https://jakfromspace.me/404'
    scope = 'user-top-read user-library-read user-follow-read'
    print('Note: the script will prompt you to log into your spotify account')
    username = input('Enter Spotify username (not email, no spaces): ')
    # username = 'jakfromspace' 
    token = util.prompt_for_user_token(username, scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)
    sp = spotipy.Spotify(auth=token)
    return sp


def getmostlistenedsongs(sp):
    results = sp.current_user_top_tracks(limit=20, time_range='long_term')
    print('\nMost Listened\n-')
    for i, item in enumerate(results['items']):
        # print(item)
        track = item['name']
        artists = item['artists'][0]['name']
        print(f'{i+1:>02}: {track} - {artists}')

def gettoplikedsongs(sp):
    results = sp.current_user_saved_tracks(limit=20)
    print('\nTop Liked\n-')
    for i, item in enumerate(results['items']):
        # print(json.dumps(item, indent=2))
        track = item['track']['name']
        artists = item['track']['artists'][0]['name']
        print(f'{i+1:>02}: {track} - {artists}')

def get_count_of_liked_songs(sp):
    # We only need the total, not all the items hence limit=1
    results = sp.current_user_saved_tracks(limit=1) 
    return results['total']

# API Get --------------------------------------------------------

def get_all_liked_songs(sp):
    print('Getting all Liked Songs')
    songs = []
    results = sp.current_user_saved_tracks()
    tot = results['total']
    print(f'Songs parsed [0/{tot}]', end='\r')
    while results:
        songs.extend(results['items'])
        results = sp.next(results)
        print(f'Songs parsed [{len(songs)}/{tot}]', end='\r')
    print(f'Total songs parsed [{len(songs)}/{tot}]')
    return songs

def get_all_followed_artists(sp):
    artists = []
    results = sp.current_user_followed_artists()
    # tot = results['total']
    tot = 'NULL'
    print(f'Artists parsed [0/{tot}]', end='\r')
    while results:
        artists.extend(results['artists']['items'])
        if results['artists']['next']:
            results = sp.next(results['artists'])
        else:
            results = None
        print(f'Artists parsed [{len(artists)}/{tot}]', end='\r')
    print(f'Total artists parsed [{len(artists)}/{tot}]')
    return artists

def get_all_playlists(sp):
    playlists = []
    results = sp.current_user_playlists(limit=50)
    playlists.extend(results['items'])
    print(f'Playlists parsed {len(playlists)}', end='\r')
    while results['next']:
        results = sp.next(results)
        playlists.extend(results['items'])
        print(f'Playlists parsed {len(playlists)}', end='\r')
    print(f'Playlists parsed {len(playlists)}')
    return playlists