from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import RandomForestClassifier
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import Row, SparkSession
import sys
sys.path.append('src/Consumer/')
from consumer import Consumer, ConsumerKafka

'''
Periodically collect metrics from the stream and throw it in a log file. The 
log file can then be used to perform sampling based experiments.

This method is not used as the stream are structured
'''
def temp_log_accumulation():
    # Spark has inbuilt check-points. If the session was terminated unexpectedly
    # getOrCreate helps resume form where things were left off
    spark = SparkSession.builder.appName('feature_selection_stream').getOrCreate()
    # monitor for new lines being added to the data file
    return spark.readStream.text('data')


class FeatureSelection:
    def __init__(self):
        self.stream = Consumer('bus', 'localhost').get_stream()
        self.kafka_stream = ConsumerKafka('bus', 'localhost')

    # kafka_stream and stream are both interchangable
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

