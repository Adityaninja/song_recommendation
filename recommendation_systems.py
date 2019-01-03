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


def all_songs(args):
	pass


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

		:return:cooccurence matrix
		"""

		#Initializing the coocurence matrix with user songs as rows and all the songs as all songs
		cooccurence_matrix = np.zeros(shape=(len(user_songs), len(all_songs)))
		cooccurence_matrix.dtype = float


		#Getting the users of songs which were listened to by the user under consideration.
		user_songs_users = []
		for i in range(0, len(user_songs)):
			users_i = self.get_item(user_songs.iloc[i])
			user_songs_users.append(users_i)



		for i in range(0, len(all_songs)):

			songs_i_data = self.train_data[self.train_data['title'] == all_songs[i]]

			#Converting to a set to avail the union functionality
			users_i = set(songs_i_data['user_id'].unique())

			for j in range(0, len(user_songs)):
				songs_j_data = self.train_data[self.train_data['title'] == user_songs.iloc[j]]
				users_j = set(songs_j_data['user_id'].unique())

				users_union = users_i.union(users_j)
				users_intersection = users_i.intersection(users_j)

				if len(users_intersection) != 0:
					cooccurence_matrix[j][i] = float(len(users_intersection)) / len(users_union)

				else:
					cooccurence_matrix[j][i] = 0

		return cooccurence_matrix

	def get_top_recommendations(self, coocurrance_matrix, all_songs):
		user_sim_scores = coocurrance_matrix.sum(axis=0)/float(coocurrance_matrix.shape[0])
		user_sim_scores = user_sim_scores.tolist()
		# user_sim_scores = np.array(user_sim_scores)[0].tolist()

		sort_index = sorted(((e, i) for i, e in enumerate(list(user_sim_scores))), reverse=True)
		song_list = []
		for i in range(0, len(sort_index)):
			if i > 10:
				break
			song_list.append(all_songs[sort_index[i][1]])

		return song_list

	def recommend(self):
		user_songs = self.get_user_songs()
		all_songs = self.get_all_songs()
		coocurrance_matrix = self.create_cooccurance_matrix(user_songs, all_songs)
		user_recommendations = self.get_top_recommendations(coocurrance_matrix, all_songs)







