# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 13:00:30 2020

@author: Michael Stebbins
"""

import os, csv, math
from sklearn.preprocessing import MinMaxScaler
from keras.preprocessing.sequence import TimeseriesGenerator

class NNDataImporter:

    def __init__(self, rootPath, importOptions):

        self.trainDataPath = os.path.join(rootPath, 'Data - Training')
        self.evalDataPath = os.path.join(rootPath, 'Data - Evaluation')

        self.units = 0
        self.batchCount = int(importOptions[0])
        self.sampleRate = int(importOptions[1])
        self.strideLen = int(importOptions[2])

        self.trainGenList = self.LoadData(self.trainDataPath, 'Training')
        self.evalGenList = self.LoadData(self.evalDataPath, 'Evaluation')
    
    def LoadData(self, dataPath, dataType):

        dateList = [f.path for f in os.scandir(dataPath) if f.is_dir()]
        genList = []
        scaler = MinMaxScaler()

        for datePath in dateList:
            pathList = [f.path for f in os.scandir(datePath) if f.is_dir()]
            for path in pathList:

                inputPath = os.path.join(path, "Config Inputs.csv")
                outputPath = os.path.join(path, "Config Output.csv")

                with open(inputPath, 'r') as inputFile, open(outputPath, 'r') as outputFile:
                    inputReader = csv.reader(inputFile)
                    outputReader = csv.reader(outputFile)
                    inputData = list(inputReader)
                    targetData = list(outputReader)

                self.units = len(inputData[0])
                normTargetData = scaler.fit_transform(targetData)
                batchSize = math.floor(len(targetData)/self.batchCount)
                pathTimeseries = TimeseriesGenerator(inputData, normTargetData,
                                                     len(targetData)-1,
                                                     sampling_rate=self.sampleRate,
                                                     stride=self.strideLen,
                                                     start_index=0,
                                                     batch_size=batchSize)
                genList.append(pathTimeseries)
                print("Creating %s TimeseriesGenerators... %0.0f%%"
                      % (dataType, 100*len(genList)/len(pathList)))

        print("%s Data Loaded!" % (dataType))
        print("-----------------------------------------------------------------")
        return genList
