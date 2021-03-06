
import pika
import json
import datetime
import time
import numpy as np
import os
import ast
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import SparkSession
from mqtt_util import MQTTUtils
from cassandra.cluster import Cluster
from kafka import KafkaConsumer
from pyspark.streaming.kafka import KafkaUtils

'''
For now, Kafka consumer will subscribe to only one topic
'''
class ConsumerKafka:
	def __init__(self, flag, host):
		self.flag = flag
		self.host = host
		# self.cluster_ip = '' #cluster IP to be set
		self.sc = SparkContext(appName='kafka_consumer')
		self.ssc = StreamingContext(self.sc, 2)
	
	def direct_kafka_stream(self):
		return KafkaUtils.createDirectStream(self.ssc, ['add_db_specs_here'], {'metadata.broker.list':'localhost:9092'})

class Consumer:
	def __init__(self, flag, host):
		self.flag = flag
		self.host = host
		self.cluster_ip = '' #cluster IP to be set
		self.sc = SparkContext(appName='consumer')
		self.ssc = StreamingContext(self.sc, 10)
		self.cassandra = Cluster([self.cluster_ip])
		self.spark = SparkSession.builder.appName('consumer').getOrCreate()
		self.mqtt_stream = MQTTUtils.createStream(self.ssc, 'tcp://{host}:1883', flag)

	# Fetching data from RabbitMQ
	def pull_message(self):
		self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
		channel = self.connection.channel()
		channel.queue_declare(queue=str(self.flag))
		channel.basic_consume(self.stream_data, queue=str(self.flag), no_ack=True)
		return channel.start_consuming()

	def stream_data(self, ch, method, properties, body):
		values = ast.literal_eval(body)
		essential_data = list()
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
		self.store_in_cassandra(essential_data[0])

	def get_stream(self):
		return self.mqtt_stream

	def store_in_cassandra(self, data):
		"""
		figure out the schema
		"""
		pass

	def terminate_connection(self):
		self.connection.close()

