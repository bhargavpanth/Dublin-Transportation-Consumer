from pyspark.sql import SparkSession
import sys
sys.path.append('src/Consumer/')
from consumer import Consumer

class FeatureSelection:
    def __init__(self):
        self.stream = Consumer('bus', 'localhost')
        self.spark = SparkSession.builder.appName('dublin_transportation').getOrCreate()
        