
import pika
import json
import datetime
import time
import numpy as np
import os
import ast
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming import DStream
from mqtt_util import MQTTUtils
from cassandra.cluster import Cluster

class Consumer:

	def __init__(self, flag, host):
		self.flag = flag
		self.host = host
		self.cluster_ip = ''
		self.sc = SparkContext()
		self.ssc = StreamingContext(self.sc, 10)
		self.cassandra = Cluster([self.cluster_ip])
		self.mqtt_stream = MQTTUtils.createStream(self.ssc, 'tcp://{host}:1883', flag)

	# Fetching data from RabbitMQ
	def pull_message(self):
		self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
		channel = self.connection.channel()
		channel.queue_declare(queue=str(self.flag))
		channel.basic_consume(self.callback, queue=str(self.flag), no_ack=True)
		return channel.start_consuming()

	def callback(self, ch, method, properties, body):
		values = ast.literal_eval(body)
		essential_data = list()
		print(type(values))
		read_dictionary = np.load(os.getcwd() + '/model/d1.npy').item()

		for i in values.keys():
			l = values.get(i)
			item = dict()
			item['stopid'] = str(i)
			counter = 0
			for j in l:
				if j['duetime']=='due':
					counter = counter+1
			item['due_count'] = str(counter)
			item['longitude'] = read_dictionary[i][0]
			item['latitude'] = read_dictionary[i][1]
			essential_data.append(item)
		# Deprecate MonogDB and introduce Cassandra
		# self.pushToMongo(essential_data[0])

	def store_in_cassandra(self):
		"""
		docstring
		"""
		pass

	def terminate_connection(self):
		self.connection.close()

