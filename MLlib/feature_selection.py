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
            .map(lambda message: round(float(message))) \
            .transform(lambda rdd: rdd.sortByKey())
        assembler = VectorAssembler(inputCols = ['stop_id', 'delay', 'route_id', 'temperature'], outputCol = 'features')
        return assembler.transform(rdd)

    def random_forests(self):
        features = self.select_feature()
        rf = RandomForestClassifier(labelCol = 'temperature', featuresCol = 'features')
        final_df = features.select('features', 'temperature')
        rf_model = rf.fit(final_df)
        print(rf_model.featureImportances)
        return rf_model.featureImportances

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False