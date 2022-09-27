# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 23:37:49 2020

@author: Michael Stebbins
"""

import os, csv

rootdir = "D:\\Matlab\\Numerical Model v4\\Outputs\\07-Apr-2020 22-13-40"
dataTypes = ['Damage','Stress','Strain','Temperature']
configsComplete = 0

for subdirs, configs, files in os.walk(rootdir):
    totalConfigs = len(configs)
    for configID in configs:
        configPath = os.path.join(rootdir,configID)
        for subdirs, dataTypes, files in os.walk(configPath):
            for dataType in dataTypes:
                typePath = os.path.join(configPath,dataType)
                for dType in dataTypes:
                    summaryName = dataType + ' Summary.csv'
                    summaryPath = os.path.join(configPath,summaryName)
                    summaryData = None
                    if dataType == dType:
                        for subdirs, dirs4, files in os.walk(typePath):    
                            for file in files:
                                fileCount = 0
                                if file.endswith(".csv"):
                                    filePath = os.path.join(typePath,file)
                                    with open (filePath,'r') as dataFile:
                                        fileCount += 1
                                        dataReader = csv.reader(dataFile)
                                        if fileCount != 1:
                                            next(dataReader)
                                        tempData = list(dataReader)
                                    with open (summaryPath,'a', newline='') as summaryFile:
                                        dataWriter = csv.writer(summaryFile, delimiter=',')
                                        dataWriter.writerows(tempData)
        configsComplete += 1
        pctComplete = configsComplete/totalConfigs * 100
        if configsComplete%5 == 0:
            print("Configs Completed: %d/%d, (%4.2f%%)", (configsComplete,totalConfigs,pctComplete))