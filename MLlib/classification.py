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
        rdd = self.stream.filter(lambda message: is_number(message.temperature)) \
            .map(lambda message: float(message.delay > 10000)) \
            .map(lambda message: round(float(message))) \
            .transform(lambda rdd: rdd.sortByKey())
        # select the required features
        log_reg = LogisticRegression(featuresCol = 'features', labelCol = 'delay')
        temperature_indexer = StringIndexer(inputCol = 'temperature', outputCol = 'temp_index')
        delay_encoder = OneHotEncoder(inputCol='delay', outputCol = 'delay_vector')
        pipeline = Pipeline(stages = [temperature_indexer, delay_encoder, log_reg])
        columns = rdd.select(['stop_id', 'delay', 'route_id', 'temperature'])
        train, test = columns.randomSplit([0.7, 0.3])
        fit_model = pipeline.fit(train)
        results = fit_model.transform(test)
        print(results)
        return results


