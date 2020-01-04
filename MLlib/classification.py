from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.feature import VectorAssembler, StringIndexer, VectorIndexer, OneHotEncoder
from pyspark.ml import Pipeline
import sys
sys.path.append('src/Consumer/')
from consumer import Consumer
import pandas as pd

class Classification:
    def __init__(self):
        self.consumer = Consumer('bus', 'localhost')
        self.stream = self.consumer.get_stream()

    def logistic_regression(self):
        # read from the stream
        rdd = self.stream.filter(lambda message: is_number(message)) \
            .map(lambda message: round(float(message))) \
            .transform(lambda rdd: rdd.sortByKey())
        # select the required features
        columns = rdd.select(['stop_id', 'delay', 'route_id', 'temperature'])


