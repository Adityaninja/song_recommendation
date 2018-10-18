import numpy as np
import pandas as pd

class popularity_based():
	def __init__(self):
		self.train_data = None
		self.aggregation_field = None
		self.primary_field = None

		self.popularity_recommendations = 	None

	def train(self, train_data, aggregation_field, primary_field, number_songs):
		"""

		:param train_data: Pandas dataframe
		:param aggregation_field: column name representing the column name to aggregate
		:param primary_field: The column name on which the count is done.
		:return: top 10 recommendations based on popularity
		"""
		train_data_grouped = train_data.groupby([aggregation_field]).agg({primary_field:'count'}).reset_index()

		train_data_grouped.rename(columns={'user_id':'score'}, inplace=True)
		train_data_grouped = train_data_grouped.sort_values(['listen_count'], ascending=False)
		self.popularity_recommendations = train_data_grouped.head(number_songs)

	def recommend(self, user_id):
		user_recommendations = self.popularity_recommendations
		user_recommendations['user_id'] = user_id

		# Bring user_id column to the front
		cols = user_recommendations.columns.tolist()
		cols = cols[-1:] + cols[:-1]
		user_recommendations = user_recommendations[cols]
		user_recommendations = user_recommendations.reset_index(drop=True)

		return user_recommendations

class item_based():
	def __init__(self):
		self.train_data = None
		self.user_id = None

	def create(self, training_data, user_id):
		self.train_data = training_data
		self.user_id = user_id

	def get_user_songs(self):
		return self.train_data[self.train_data['user_id'] == self.user_id]['title']

	def get_all_songs(self):
		return self.train_data['title'].unique()

	def get_item(self, song):
		temp = self.train_data[self.train_data['title'] == song]['user_id'].unique()
		return set(temp)

	def create_cooccurance_matrix(self, user_songs, all_songs):
		"""

		:param user_songs: Pandas dataframe shape (n,)
		:param all_songs: Pandas dataframe shape (n, )

		users_songs_users: List of sets

		:return:
		"""

		#Initializing the coocurence matrix with user songs as rows and all the songs as all songs
		cooccurence_matrix = np.zeros(shape=(len(user_songs), len(all_songs)))
		cooccurence_matrix.dtype = float
		user_songs_users = []
		for i in range(0, len(user_songs)):
			users_i = self.get_item(user_songs.iloc[i])
			user_songs_users.append(users_i)



		user_songs = user_songs.tolist()
		all_songs = all_songs.tolist()

		for i in range(0, len(all_songs)):
			users_i = self.get_item(all_songs[i])
			for j in range(0, len(user_songs)):
				coomon_set = user_songs_users[j].intersection(users_i)



	def recommend(self):
		user_songs = self.get_user_songs()
		all_songs = self.get_all_songs()
		self.create_cooccurance_matrix(user_songs, all_songs)







