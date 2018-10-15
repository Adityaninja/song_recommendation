class popularity_based():
	def __init__(self):
		self.train_data = None
		self.aggregation_field = None
		self.primary_field = None

		self.popularity_recommendations = None

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

