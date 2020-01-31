from pyspark.sql import SparkSession
sys.path.append('src/Consumer/')
from consumer import Consumer

class KMeans:
    def __init__(self):
        self.spark = SparkSession.builder.appName('kmeans').getOrCreate()
        self.consumer = Consumer('bus', 'localhost')
        self.stream = self.consumer.get_stream()
