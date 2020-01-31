from pyspark import SparkContext
from pyspark.sql import SparkSession, SQLContext
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.clustering import KMeans
sys.path.append('src/Consumer/')
from consumer import Consumer

class K_Means:
    def __init__(self):
        self.spark = SparkSession.builder.appName('kmeans').getOrCreate()
        self.consumer = Consumer('bus', 'localhost')
        self.stream = self.consumer.get_stream()

    def kmeans(self):
        rdd = self.stream.filter(lambda message: float(message.temperature)) \
            .filter(lambda message: float(message.delay > 10000)) \
            .transform(lambda rdd: rdd.sortByKey())
        # dataFrame = create
        # assembler = VectorAssembler(inputCols = rdd, outputCol = 'features')
        # final_df = assembler.transform(df)
