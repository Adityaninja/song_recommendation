import pandas as pd
from recommendation_systems import popularity_based, item_based
from sklearn.model_selection import train_test_split

triplets_file = 'user_playlist.txt'
songs_metadata_file = 'song_data.csv'

song_df_1 = pd.read_table(triplets_file, header=None)
song_df_1.columns = ['user_id', 'song_id', 'listen_count']

song_df_2 = pd.read_csv('songdata.csv')
song_df = pd.merge(song_df_1, song_df_2.drop_duplicates(['song_id']), on='song_id', how='left')

song_grouped = song_df.groupby(['title']).agg({'listen_count': 'count'}).reset_index()
grouped_sum = song_grouped['listen_count'].sum()
song_grouped['percentage'] = song_grouped['listen_count'].div(grouped_sum)*100
song_grouped = song_grouped.sort_values(['listen_count', 'title'], ascending=False)

train_data, test_data = train_test_split(song_df, test_size=0.2, random_state=0)

# Popularity based recommendation system
# popularity_based_recommender = popularity_based()
# popularity_based_recommender.train(train_data, 'title', 'listen_count', 10)
# song_list = popularity_based_recommender.recommend(32)
# print(song_list)

#Item based recommendation system

item_based_obj = item_based()
item_based_obj.create(train_data, 'a62ea261b06fc91fe52ead186cc5f5602a37abaf')
item_based_obj.recommend()




pass




