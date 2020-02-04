import argparse
from MLlib.clustering import K_Means
from MLlib.regression import Regression
from MLlib.classification import Classification
from MLlib.feature_selection import FeatureSelection

def main(flag, host):
	# Perform feature selection
	feature_importance_matrix = FeatureSelection().random_forests()
	print(feature_importance_matrix)

	# classification and clustering
	log_reg = Classification().logistic_regression()
	print(log_reg)

	kmeans = K_Means().kmeans()
	print(kmeans)

	# regression
	model = Regression()
	frame = model.create_data_frame()
	train, test = model.train_test_split(frame)
	fit = model.linear_regression(train)
	print(fit.predict(test))


if __name__ == '__main__':
	
	parser = argparse.ArgumentParser()
	# default='bus'
	parser.add_argument('--flag', type=str, help='Name of the queue (bus | bike | luas)')
	parser.add_argument('--host', type=str, default='localhost', help='Host where RabbitMQ is running')

	args, unparsed = parser.parse_known_args()
	flag = 'bus'
	host = 'localhost'
	# main(args.flag, args.host)
	main(flag, host)