from pyspark.sql import SparkSession
import sys
sys.path.append('src/Consumer/')
from consumer import Consumer

class FeatureSelection:
    def __init__(self):
        self.consumer = Consumer('bus', 'localhost')
        self.stream = self.consumer.get_stream()

    def select_feature(self):
        pass

