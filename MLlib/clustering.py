from pyspark.sql import SparkSession

class KMeans:
    def __init__(self):
        self.spark = SparkSession.builder.appName('kmeans').getOrCreate()