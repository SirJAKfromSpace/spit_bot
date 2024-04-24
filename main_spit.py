import spit.api as api

import pandas as pd
import seaborn as sb
import json

pd.set_option('display.max_columns', None)

# DataFrame --------------------------------------------------------

def read_save_df(data):
    # Read into df
    df = pd.DataFrame(data)
    print('HEAD:')
    print(df.head())
    # print('Index 0:')
    # row = df.iloc[0].to_dict()
    # print(json.dumps(row, indent=2))

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
    filename = input(f'Enter {b} filename with ext of json file to read: ')
    try:
        # Read the JSON file into a DataFrame
        df = pd.read_json(filename or f'{b}.json', orient='records', lines=True)
        print('Loaded')
        return df
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        return None
    except ValueError as e:
        print(f"Error reading {filename}: {e}")
        return None

def print_df(df):
    print(f'Data Attributes: {df.columns}')
    print('Index 0:')
    row = df.iloc[0]
    print(row, '\n')

def clean_json_df(df_s, df_a, df_p):
    print('HEAD:')
    print(df_s.head())
    print('Index 0:')
    row = df_s.iloc[0].to_dict()
    print(json.dumps(row, indent=2))


# MAIN RUNNER --------------------------------------------------------

inp = 'w'
df_songs, df_artists, df_playlists = pd.DataFrame({'A' : []}), pd.DataFrame({'A' : []}), pd.DataFrame({'A' : []})
while inp != 'q':
    print('\nSPIT - Spotify Playlist Import Tool')
    print(f'Loaded Data - Songs:{len(df_songs) or "Empty"}, Artists:{len(df_artists) or "Empty"}, Playlists:{len(df_playlists) or "Empty"}\n----')
    inp = input('1.Get Data using Web API request \n2.Read from json file in working directory \n3.View Loaded Data\nQ.Exit program\n\n(1/2/3/q or anything else to quit)?\n:> ')
    if inp == '1':
        sp = api.spotipy_auth()
        # Getting api data
        my_songs = api.get_all_liked_songs(sp)
        my_artists = api.get_all_followed_artists(sp)
        my_playlists = api.get_all_playlists(sp)
        # save to dataframe
        print('Reading Liked Songs into dataframe')
        df_songs = read_save_df(my_songs)
        print('Reading Followed Artists into dataframe')
        df_artists = read_save_df(my_artists)
        print('Reading Playlists into dataframe')
        df_playlists = read_save_df(my_playlists)

        # getmostlistenedsongs(sp)
        # gettoplikedsongs(sp)
    elif inp == '2':
        # read from json file
        print('Read Liked Songs from JSON file')
        df_songs = read_jsonfile('songs')
        print('Read Followed Artists from JSON file')
        df_artists = read_jsonfile('artists')
        print('Read Playlists from JSON file')
        df_playlists = read_jsonfile('playlists')
    elif inp == '3':
        print('Loaded Songs')
        print_df(df_songs)
        print('Loaded Artists')
        print_df(df_artists)
        print('Loaded Playlists')
        print_df(df_playlists)
    elif inp == '4':
        print('Extract relevant tuples from JSON data into clean CSV dataframe')
        if not df_songs.empty and not df_artists.empty and not df_playlists.empty:
            print('Dataframes OK')
            # df_songs_c, df_artists_c, df_playlists_c = 
            clean_json_df(df_songs, df_artists, df_playlists)
        else:
            print('Invalid Dataframes Error')
    elif inp == 'q':
        print('Quitting...')
        break
    else:
        print('Invalid option input. Try again!') 
        
print('Thanks\n_END_')
