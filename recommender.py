import pandas as pd

triplets_file = 'https://static.turi.com/datasets/millionsong/10000.txt'
songs_metadata_file = 'https://static.turi.com/datasets/millionsong/song_data.csv'

song_df_1 = pd.read_table(triplets_file, header=None)
song_df_1.columns = ['user_id', 'song_id', 'listen_count']

song_df_2 = pd.read_csv(songs_metadata_file)

song_df = pd.merge(song_df_1, song_df_2.drop_duplicates, on='song_id', how='left')
pass

