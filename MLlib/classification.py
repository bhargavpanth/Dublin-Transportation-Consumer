from pyspark import SparkContext
from pyspark.streaming import StreamingContext
import sys
sys.path.append('src/Consumer/')
from consumer import Consumer
import pandas as pd

class Classification:
    def __init__(self):
        self.consumer = Consumer('bus', 'localhost')
        self.stream = self.consumer.get_stream()

    def logistic_regression(self):
        rdd = self.stream.filter(lambda message: is_number(message)) \
            .map(lambda message: round(float(message))) \
            .transform(lambda rdd: rdd.sortByKey())
        pass

