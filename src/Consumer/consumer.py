
import pika
import json
import datetime
import time
import numpy as np
import os
import ast
from pymongo import MongoClient

class Consumer:

	def __init__(self, flag, host):
		self.flag = flag
		self.host = host

	def pull_message(self):
		connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
		channel = connection.channel()
		channel.queue_declare(queue=str(self.flag))
		# channel.basic_consume(self.callback, queue=str(self.flag), no_ack=True)
		channel.basic_consume(self.callback, queue=str(self.flag), no_ack=True)
		message = channel.start_consuming()
		return message

	def callback(self, ch, method, properties, body):
		values = ast.literal_eval(body)
		essential_data = list()
		print(type(values))
		read_dictionary = np.load(os.getcwd() + "/model/d1.npy").item()

		for i in values.keys():
			l = values.get(i)
			item = dict()
			item["stopid"] = str(i)
			counter = 0;
			for j in l:
				if j["duetime"]=="due":
					counter = counter+1
			item["due_count"] = str(counter)
			item["longitude"] = read_dictionary[i][0]
			item["lattitude"] = read_dictionary[i][1]
			essential_data.append(item)
		print essential_data
		self.pushToMongo(essential_data[0])
		print essential_data
		#return essential_data
			# pass
			# print(" [x] Received %r" % body)
	def pushToMongo(self, dataToBePushed):
		client = MongoClient()
		client = MongoClient('localhost', 27017)
		db = client['bus-database']
		posts = db.posts
		post = dataToBePushed
		print "----------------"
		print type(post)
		post_id = posts.insert_one(post).inserted_id
		print post_id




	def terminate_connection(self):
		self.connection.close()

