import argparse
import sys
sys.path.append('src/Consumer/')
from consumer import Consumer
import logstash
import logging
# import pymongo
# from pymongo import MongoClient
# from elasticsearch import Elasticsearch
# es = Elasticsearch()

def main(flag, host):
	message = Consumer(flag, host)
	message = message.pull_message()
	print message.callback();
	res = es.index(index="bus", doc_type='json', body=message)
	# filter(res)
	# print res

	
	'''
	Transfer this stub to test
	print len(model_obj)
	print type(model_obj)
	'''

	# MongoDB - Pipline Direct 
	# client = MongoClient(host)
	# db = client['dublinbus']
	# for each_trans in db.bus.find({}):
	# 	filter(each_trans)

	# message = Consumer(flag, host)
	# message = message.pull_message()
	# res = es.index(index="bus", doc_type='json', body=message)
	# print res

def filter(values):
	essential_data = list()
	print(type(values))
	# read_dictionary = np.load(os.getcwd() + "/model/d1.npy").item()

	for i in values.keys():
		l = values.get(i)
		# item = dict()
		# item["stopid"] = str(i)
		counter = 0;
		for j in l:
			if j["duetime"]=="due":
				counter = counter+1
		item["due_count"] = str(counter)
		item["longitude"] = read_dictionary[i][0]
		item["lattitude"] = read_dictionary[i][1]
		essential_data.append(item)
	print essential_data


if __name__ == '__main__':
	
	parser = argparse.ArgumentParser()
	# default='bus'
	parser.add_argument('--flag', type=str, help='Name of the queue (bus | bike | luas)')
	parser.add_argument('--host', type=str, default='localhost', help='Host where RabbitMQ is running')

	args, unparsed = parser.parse_known_args()
	main(args.flag, args.host)