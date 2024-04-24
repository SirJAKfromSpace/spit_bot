import pandas as pd
import json
import os
pd.set_option('display.max_columns', None)

def get_empty_df_x3():
    df_1, df_2, df_3 = pd.DataFrame({'A' : []}), pd.DataFrame({'A' : []}), pd.DataFrame({'A' : []})
    return df_1, df_2, df_3

def check_default_json_files_exists():
    file_path = os.path.join('./', 'songs.json')
    if not os.path.exists(file_path) and not os.path.isfile(file_path):
        return False
    file_path = os.path.join('./', 'playlists.json')
    if not os.path.exists(file_path) and not os.path.isfile(file_path):
        return False
    file_path = os.path.join('./', 'artists.json')
    if not os.path.exists(file_path) and not os.path.isfile(file_path):
        return False
    return True

def read_save_df(data):
    # Read into df
    df = pd.DataFrame(data)
    print('Data snapshot of index 0:')
    row = df.iloc[0].to_dict()
    print(json.dumps(row, indent=2, default=str))

    # Save df to file
    inp = input('Do you wish to save the dataframe? (Y/N): ')
    if str.lower(inp) == 'y':
        inp_jc = input('Save as JSON or CSV or cancel? (1.json 2.csv 3.cancel): ')
        # save as json
        if inp_jc == '1':
            filename = input('Enter filename (including extension) to save as (eg. filename.json): ')
            df.to_json(filename, orient='records', lines=True)
            print('JSON file saved in working directory!')
        # save as csv
        elif inp_jc == '2':
            filename = input('Enter filename (including extension) to save as (eg. filename.csv): ')
            df.to_csv(filename, index=False)
            print('CSV file saved in working directory!')
        else:
            print('Dataframe not saved.')
    else:
        print('Dataframe not saved.')
    return df

def read_jsonfile(b):
    if check_default_json_files_exists():
        print('Default JSON file exists in directory. Using that.')
        df = pd.read_json(f'{b}.json', orient='records', lines=True)
        print(f'JSON for {b} Loaded')
        return df
    filename = input(f'Enter {b} filename with ext of json file to read: ')
    try:
        # Read the JSON file into a DataFrame
        df = pd.read_json(filename or f'{b}.json', orient='records', lines=True)
        print(f'JSON for {b} Loaded')
        return df
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        return None
    except ValueError as e:
        print(f"Error reading {filename}: {e}")
        return None

def print_df(df):
    print('Columns:' ,df.columns)
    print('Shape:', df.shape)
    # print('Index 0:')
    # row = df.iloc[0].to_dict()
    # print(json.dumps(row, indent=2, default=str), '\n')

# CLEAN TO CSV

def clean_json_df(df_s, df_a, df_p):
    print('Cleaning Songs List')
    list_clean_rows = []
    tot = len(df_s)
    for i in range(tot):
        row = df_s.iloc[i].to_dict()
        # print(f'Index 0:\n{row}\n')
        clean_row = {
            'time_added_at': row['added_at'],
            'track_name': row['track']['name'],
            'artist_name': row['track']['artists'][0]['name'],
            'artist_uri': row['track']['artists'][0]['uri'],
            'track_number': row['track']['track_number'],
            'track_uri': row['track']['uri'],
            'track_popularity': row['track']['popularity'],
            'track_explicity': row['track']['explicit'],
            'track_duration_ms': row['track']['duration_ms'],
            'album_name': row['track']['album']['name'],
            'album_image_url': row['track']['album']['images'][0]['url'],
            'album_release_date': row['track']['album']['release_date'],
            'album_uri': row['track']['album']['uri'],
            'count_available_markets': len(row['track']['available_markets'])
        }
        list_clean_rows.append(clean_row)
        print(f'Rows cleaned [{i}/{tot}]', end='\r')
        # print('Cleaned Index 0:\n', clean_row, '\n')
    print(f'Total rows cleaned [{len(list_clean_rows)}/{tot}]')
    df_s_clean = pd.DataFrame(list_clean_rows)
    print('Songs Attributes:' ,df_s_clean.columns)

    print('Cleaning Artists List')
    list_clean_rows = []
    tot = len(df_a)
    for i in range(tot):
        row = df_a.iloc[i].to_dict()
        # print(f'Index 0:\n{row}\n')
        clean_row = {
            'artist_name': row['name'],
            'followers': row['followers']['total'],
            'artist_uri': row['uri'],
            'popularity': row['popularity'],
            'image_url': row['images'][0]['url'] if row['images'] else None,
            'genres': ', '.join(row['genres'])
        }
        list_clean_rows.append(clean_row)
        print(f'Rows cleaned [{i}/{tot}]', end='\r')
        # print('Cleaned Index 0:\n', clean_row, '\n')
    print(f'Total rows cleaned [{len(list_clean_rows)}/{tot}]')
    df_a_clean = pd.DataFrame(list_clean_rows)
    print('Artists Attributes:' ,df_a_clean.columns)

    print('Cleaning Playlists List and Adding Tracklist')
    from .api import spotipy_auth, get_playlist_tracks
    sp = spotipy_auth()
    list_clean_rows = []
    tot = len(df_p)
    for i in range(tot):
        row = df_p.iloc[i].to_dict()
        
        # getting tracklist from web api
        tracklist = get_playlist_tracks(sp, row)
        tracks_clean = []
        for t in tracklist:
            t_row = {
            'track_name': t['track']['name'],
            'artist_name': t['track']['artists'][0]['name'],
            'artist_uri': t['track']['artists'][0]['uri'],
            'track_uri': t['track']['uri'],
            'track_duration_ms': t['track']['duration_ms'],
            'album_name': t['track']['album']['name'],
            'album_image_url': t['track']['album']['images'][0]['url'],
            'album_release_date': t['track']['album']['release_date'],
            'album_uri': t['track']['album']['uri']
            }
            tracks_clean.append(t_row)

        clean_row = {
            'playlist_name': row['name'],
            'total_tracks': row['tracks']['total'],
            'description': row['description'],
            'owner_name': row['owner']['display_name'],
            'owner_uri': row['owner']['uri'],
            'image_url': row['images'][0]['url'],
            'is_public': row['public'],
            'tracklist': tracks_clean,
        }
        list_clean_rows.append(clean_row)
        print(f'Rows cleaned [{i}/{tot}]', end='\r')
        # print('Cleaned Index 0:\n', clean_row, '\n')
    print(f'Total rows cleaned [{len(list_clean_rows)}/{tot}]')
    df_p_clean = pd.DataFrame(list_clean_rows)
    print('Playlist Attributes:' ,df_p_clean.columns)
    return df_s_clean, df_a_clean, df_p_clean

def save_cleaned_csv_files(df_s, df_a, df_p):
    print('Save these cleaned flattened dataframes as CSV?')
    print(f'Songs:\n{df_s.head()}\n\nArtists:{df_a.head()}\n\nPlaylists:{df_p.head()}')
    inp = input('Save? (y/n): ')
    if str.lower(inp) == 'y':
        df_s.to_csv('SPIT_MyLikedSongs.csv')
        df_a.to_csv('SPIT_MyFollowedArtists.csv')
        df_p.to_csv('SPIT_MyPlaylists.csv')

        print('Cleaned CSVs saved to directory!')
    else:
        # consider saving. cleaned csv may prove easier to handle. json from api is bloated
        print('CSV Save Cancelled.') 

def read_clean_csv_files():
    try:
        dfs = pd.read_csv('SPIT_MyLikedSongs.csv')
        dfa = pd.read_csv('SPIT_MyFollowedArtists.csv')
        dfp = pd.read_csv('SPIT_MyPlaylists.csv')
        return dfs, dfa, dfp
    except FileNotFoundError:
        print(f"Error: CSV files not found.")
        return get_empty_df_x3()
    except ValueError as e:
        print(f"Error reading CSV file: {e}")
        return get_empty_df_x3()