import spit_bot.api as bot_api
import spit_bot.data as bot_data

# MAIN RUNNER --------------------------------------------------------

inp = 'w'
bool_files = bot_data.check_default_json_files_exists()
df_songs, df_artists, df_playlists = bot_data.get_empty_df_x3()
df_songs_c, df_artists_c, df_playlists_c = bot_data.get_empty_df_x3()
while inp != 'q':
    print('\nSPIT - Spotify Playlist Import Tool')
    print(f'Web API JSON loaded [songs:{"✅" if df_songs.size>0 else "❌"}, artists:{"✅" if df_artists.size>0 else "❌"}, playlists:{"✅" if df_playlists.size>0 else "❌"}')
    print(f'Cleaned CSVs loaded [songs:{"✅" if df_songs_c.size>0 else "❌"}, artists:{"✅" if df_artists_c.size>0 else "❌"}, playlists:{"✅" if df_playlists_c.size>0 else "❌"}\n----')
    print('1.Get Data using Web API request \n2.Load from json file in working directory \n3.View JSON loaded data\n4.Clean data and Save to CSV\n5.Load Clean CSV Data\n6.View clean CSV dataframes\nQ.Exit program\n')
    inp = input('Select (1/2/3/4/5/6/q)? :> ')
    if inp == '1':
        sp = bot_api.spotipy_auth()
        # Getting api data
        my_songs = bot_api.get_all_liked_songs(sp)
        my_artists = bot_api.get_all_followed_artists(sp)
        my_playlists = bot_api.get_all_playlists(sp)
        # save to dataframe
        print('Reading Liked Songs into dataframe')
        df_songs = bot_data.read_save_df(my_songs)
        print('Reading Followed Artists into dataframe')
        df_artists = bot_data.read_save_df(my_artists)
        print('Reading Playlists into dataframe')
        df_playlists = bot_data.read_save_df(my_playlists)

        # getmostlistenedsongs(sp)
        # gettoplikedsongs(sp)
    elif inp == '2':
        # read from json file
        print('Read Liked Songs from JSON file')
        df_songs = bot_data.read_jsonfile('songs')
        print('Read Followed Artists from JSON file')
        df_artists = bot_data.read_jsonfile('artists')
        print('Read Playlists from JSON file')
        df_playlists = bot_data.read_jsonfile('playlists')
    elif inp == '3':
        if df_songs.size>0:
            print('Loaded Songs')
            bot_data.print_df(df_songs)
            print('Loaded Artists')
            bot_data.print_df(df_artists)
            print('Loaded Playlists')
            bot_data.print_df(df_playlists)
        else:
            print('SPIT InvalidFilesError. JSON not Loaded!')
    elif inp == '4':
        print('Extract relevant tuples from JSON data into clean CSV dataframe')
        if not df_songs.empty and not df_artists.empty and not df_playlists.empty:
            print('Dataframes OK')
            df_songs_c, df_artists_c, df_playlists_c = bot_data.clean_json_df(df_songs, df_artists, df_playlists)
            bot_data.save_cleaned_csv_files(df_songs_c, df_artists_c, df_playlists_c)
        else:
            print('Invalid Dataframes Error')
    elif inp =='5':
        print('Loading CSVs')
        df_songs_c, df_artists_c, df_playlists_c = bot_data.read_clean_csv_files()
        print('Done loading Clean CSVs' if df_songs_c.size>0 else 'Error Loading CSV')
    elif inp == '6':
        print('View Cleaned CSV Dataframes')
        if df_songs_c.size>0:
            print('Cleaned Songs DF')
            bot_data.print_df(df_songs_c)
            print('Cleaned Artists DF')
            bot_data.print_df(df_artists_c)
            print('Cleaned Playlists DF')
            bot_data.print_df(df_playlists_c)
        else:
            print('SPIT InvalidFilesError. CSVs not Found!')
    elif inp == 'q':
        print('Quitting...')
        break
    else:
        print('Invalid option input. Try again!') 

print('Thanks\n_END_')
