from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import RandomForestClassifier
import sys
sys.path.append('src/Consumer/')
from consumer import Consumer

class FeatureSelection:
    def __init__(self):
        self.consumer = Consumer('bus', 'localhost')
        self.stream = self.consumer.get_stream()

    def select_feature(self):
        rdd = self.stream.filter(lambda message: is_number(message)) \
            .map(lambda message: ( round(float(message) * 2, 0) / 2, 1 )) \
            .transform(lambda rdd: rdd.sortByKey())
        assembler = VectorAssembler(inputCols = ['stop_id', 'delay', 'route_id', 'departure'], outputCol = 'features')
        assembler.transform(rdd)

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False