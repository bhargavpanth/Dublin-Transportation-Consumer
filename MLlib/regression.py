from pyspark import SparkContext
from pyspark.streaming import StreamingContext
import sys
sys.path.append('src/Consumer/')
from consumer import Consumer

class Regression:
    def __init__(self):
        self.consumer = Consumer('bus', 'localhost')
        self.stream = self.consumer.get_stream()

    def clean_up(self):
        pass


