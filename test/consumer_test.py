import unittest
import json
import pika

'''
Note - unittest module expects that method names start with test_
ex: test_return_formatted_url
'''

class Consumer_Pipeline(unittest.TestCase):
	""" test suit class """

	def test_rabbitmq_init(self):
		self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
		self.channel = self.connection.channel()
		self.channel.queue_declare(queue= 'test_queue')

	

		
if __name__ == '__main__':
	unittest.main()