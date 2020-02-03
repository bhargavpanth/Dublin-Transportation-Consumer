import argparse
from MLlib.clustering import K_Means
from MLlib.regression import Regression
from MLlib.classification import Classification
from MLlib.feature_selection import FeatureSelection

def main(flag, host):
	'''
	Run the ensemble of classification and regression methods
	'''
	# Perform feature selection
	feature_importance_matrix = FeatureSelection().random_forests()
	print(feature_importance_matrix)

if __name__ == '__main__':
	
	parser = argparse.ArgumentParser()
	# default='bus'
	parser.add_argument('--flag', type=str, help='Name of the queue (bus | bike | luas)')
	parser.add_argument('--host', type=str, default='localhost', help='Host where RabbitMQ is running')

	args, unparsed = parser.parse_known_args()
	main(args.flag, args.host)