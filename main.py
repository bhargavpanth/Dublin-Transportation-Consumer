import argparse
import os
import sys
sys.path.append('src/Consumer/')
from consumer import Consumer
import logstash
import logging
import numpy as np

# def filter(values):
# 	essential_data = []
# 	item = []
# 	read_dictionary = np.load(os.getcwd() + "/model/d1.npy").item()
# 	for i in values.keys():
# 		l = values.get(i)
# 		counter = 0
# 		for j in l:
# 			if j["duetime"]=="due":
# 				counter = counter+1
# 		item["due_count"] = str(counter)
# 		item["longitude"] = read_dictionary[i][0]
# 		item["lattitude"] = read_dictionary[i][1]
# 		essential_data.append(item)

def main(flag, host):
	message = Consumer(flag, host)
	message = message.pull_message()

if __name__ == '__main__':
	
	parser = argparse.ArgumentParser()
	# default='bus'
	parser.add_argument('--flag', type=str, help='Name of the queue (bus | bike | luas)')
	parser.add_argument('--host', type=str, default='localhost', help='Host where RabbitMQ is running')

	args, unparsed = parser.parse_known_args()
	main(args.flag, args.host)