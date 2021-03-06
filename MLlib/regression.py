from pyspark import SparkContext, SparkConf, SparkSession
from pyspark.streaming import StreamingContext
from pyspark.sql import Row
from pyspark.ml.regression import LinearRegression
import sys
import json
import ast
import numpy as np
import os
sys.path.append('src/Consumer/')
from consumer import Consumer, ConsumerKafka

# introduce structured streaming
class Regression:
    def __init__(self):
        self.consumer = Consumer('bus', 'localhost')
        self.stream = self.consumer.get_stream()
        self.kafka_stream = ConsumerKafka('bus', 'localhost')
        self.cleaned_stream = self.stream.map(self.clean_up)
        self.conf = SparkConf().setMaster('local').setAppName('linear_regression')
        self.sc = SparkContext(conf = self.conf)
        self.spark = SparkSession(self.sc)

    # kafka_stream and stream are both interchangable
    def clean_up(self, data):
        essential_data = list()
        read_dictionary = np.load(os.getcwd() + '/model/d1.npy').item()
        record = json.dumps(data, separators=(',', ':'))
        values = ast.literal_eval(record)
        for i in values.get():
            rec = values.get(i)
            item = dict()
            item['stopid'] = str(i)
            counter = 0
            for j in rec:
                if j['duetime']=='due':
                    counter = counter+1
            item['due_count'] = str(counter)
            item['longitude'] = read_dictionary[i][0]
            item['latitude'] = read_dictionary[i][1]
            essential_data.append(item)

    def create_data_frame(self):
        return self.spark.createDateFrame(self.cleaned_stream)

    def train_test_split(self, data):
        (train, test) = data.randomSplit([0.3, 0.7])
        return (train, test)

    def linear_regression(self, training_data):
        linear_regression = LinearRegression(maxIter=10)
        return linear_regression.fit(training_data)
        
    def predict(self, model, test_data):
        print('Coefficients: ' + str(model.coefficients))
        print('Intercept: ' + str(model.intercept))
        predictions = model.transform(test_data)
        return predictions.select('delay').show()

def main():
    model = Regression()
    frame = model.create_data_frame()
    train, test = model.train_test_split(frame)
    fit = model.linear_regression(train)
    print(fit.predict(test))

if __name__ == '__main__':
    main()