from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import RandomForestClassifier
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import Row, SparkSession
import sys
sys.path.append('src/Consumer/')
from consumer import Consumer

'''
Introduce structured streaming

Periodically collect metrics from the stream and throw it in a log file. The 
log file can then be used to perform sampling based experiments
'''

def temp_log_accumulation():
    pass

class FeatureSelection:
    def __init__(self):
        self.stream = Consumer('bus', 'localhost').get_stream()

    def select_feature(self):
        rdd = self.stream.filter(lambda message: float(message)) \
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

# def main():
#     FeatureSelection().random_forests()

# if __name__ == '__main__':
#     main()

