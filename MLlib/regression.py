from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
from pyspark.sql import Row
import sys
import json
import ast
import numpy as np
import os
sys.path.append('src/Consumer/')
from consumer import Consumer

class Regression:
    conf = SparkConf().setMaster('local').setAppName('linear_regression')
    sc = SparkContext(conf = conf)
    def __init__(self):
        self.consumer = Consumer('bus', 'localhost')
        self.stream = self.consumer.get_stream()
        self.cleaned_stream = self.stream.map(self.clean_up)

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
        spark.createDateFrame(self.cleaned_stream)

