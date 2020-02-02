from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession, SQLContext
from pyspark.ml.feature import VectorAssembler, StandardScaler
from pyspark.ml.clustering import KMeans
import sys
sys.path.append('src/Consumer/')
from consumer import Consumer

class K_Means:
    def __init__(self):
        self.spark = SparkSession.builder.appName('kmeans').getOrCreate()
        self.conf = SparkConf().setMaster('local').setAppName('kmeans')
        self.sc = SparkContext(conf = self.conf)
        self.consumer = Consumer('bus', 'localhost')
        self.stream = self.consumer.get_stream()

    def kmeans(self):
        rdd = self.stream.filter(lambda message: float(message.temperature)) \
            .filter(lambda message: float(message.delay > 10000)) \
            .transform(lambda rdd: rdd.sortByKey())
        sqlContext = SQLContext(self.sc)
        schema = sqlContext.createDataFrame(rdd)
        df = schema.createOrReplaceTempView('kmeans')
        assembler = VectorAssembler(inputCols = df.columns, outputCol = 'features')
        final_df = assembler.transform(df)
        scaler = StandardScaler(inputCol = 'features', outputCol = 'scaled_features')
        scaler_model = scaler.fit(final_df)
        return scaler_model.transform(final_df)

def main():
    kmeans = K_Means().kmeans()
    print(kmeans)

if __name__ == '__main__':
    main()

