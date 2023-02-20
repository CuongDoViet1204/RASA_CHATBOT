from sklearn.ensemble import RandomForestClassifier
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv
import math
from sklearn import metrics

# import trans

class Random_Forest(object):
    def __init__(self, filename):
        self.trainPath          = filename + "\Training.csv"
        self.testPath           = filename + "\Testing.csv"
        self.data               = None
        self.test               = None
        self.dataValue          = None
        self.testValue          = None
        self.dataHeader         = None
        self.numberOfHeader     = None
        self.numberOfLabel      = None
        self.label              = None
        self.labelValue         = None
        self.TlabelValue        = None
        self.predictLabel       = None
        self.predictLabelT      = None
        self.numberOfInstances  = None
        self.numberOfTest       = None
        self.clf                = None
        self.featureVN          = None

    def PreProcessingCSV(self, isTrain = True):
        if isTrain == True:
            self.data = pd.read_csv(self.trainPath, delimiter = None)
            self.dataHeader = self.data.columns.values
            self.numberOfHeader = len(self.dataHeader.tolist()) - 2
            self.dataHeader = [self.dataHeader[idxHeader].strip()
                               for idxHeader in range (self.numberOfHeader + 1)]
            self.label = list(set(self.data[self.dataHeader[self.numberOfHeader]].values.tolist()))
            self.numberOfLabel = len(self.label)
            self.dataValue = self.data[self.dataHeader[:self.numberOfHeader]].values.tolist()
            self.labelValue = self.data[self.dataHeader[self.numberOfHeader]].values.tolist() 
        else:
            self.test = pd.read_csv(self.testPath, delimiter = None)
            self.testValue = self.test[self.dataHeader[:self.numberOfHeader]].values.tolist()
            self.TlabelValue = self.test[self.dataHeader[self.numberOfHeader]].values.tolist()

    def Fit(self):
        self.clf = RandomForestClassifier(criterion = "gini", max_features = 88, n_estimators = 1000)
        self.clf.fit(self.dataValue, self.labelValue)

    def Predict(self, isTest = True, value = None):
        if isTest == True:
            labelPredict = self.clf.predict(self.testValue)
            print("Accuracy", metrics.accuracy_score(self.TlabelValue, labelPredict))
        else:
            result = self.clf.predict(value)
            return result

    # def setFeatureVN(self):
    #     self.featureVN = [trans.TransToVI(self.dataHeader[idx])
    #                       for idx in range (self.numberOfHeader)]


# filename = "DatasetOriginal"
# random_fr = Random_Forest(filename)
# random_fr.PreProcessingCSV()
# # print(random_fr.label)
# # random_fr.setFeatureVN()
# # print(random_fr.featureVN)
# # print(random_fr.dataHeader)
# # random_fr.PreProcessingCSV(isTrain = False)
# random_fr.Fit()

# # random_fr.Predict(isTest = True)
# result = random_fr.Predict(isTest = False, value = [[1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]])
# print(result)