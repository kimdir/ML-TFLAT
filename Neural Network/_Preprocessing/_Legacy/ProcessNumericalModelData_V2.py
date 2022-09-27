# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 23:37:49 2020

@author: Michael Stebbins
"""

import os, csv
from more_itertools import unique_everseen

rootdir = "E:\\Numerical Model v4\\Outputs\\_Legacy\\Training Data 4-7-2020"
dataTypes = ['Damage','Stress','Strain','Temperature']
configsComplete = 0

#Find Date Dir
for subdirs, dateDirs, files in os.walk(rootdir):
    for dateVal in dateDirs:
        datePath = os.path.join(rootdir,dateVal)
        # Find Serial Number Dir
        for subdirs, configs, files in os.walk(datePath):
            totalConfigs = len(configs)
            for configID in configs:
                configPath = os.path.join(datePath,configID)
                
                #Find Data Type Dir
                print("check1")
                for subdirs, dataTypes, files in os.walk(configPath):
                    for dataType in dataTypes:
                        typePath = os.path.join(configPath,dataType)
                        for dType in dataTypes:
                            summaryName = dataType + ' Summary.csv'
                            summaryPath = os.path.join(configPath,summaryName)
                            summaryData = None
                            
                            newSummary = open (summaryPath,'a', newline='')
                            newSummary.close()
                            if dataType == dType:
                                
                                # Find Data Type Files
                                for subdirs, dirs4, files in os.walk(typePath):    
                                    print("check2")
                                    for file in files:
                                        fileCount = 0
                                        if file.endswith(".csv"):
                                            filePath = os.path.join(typePath,file)
                                            
                                            # Append data file to summary file
                                            with open (filePath,'r') as dataFile:
                                                fileCount += 1
                                                dataReader = csv.reader(dataFile)
                                                if fileCount != 1:
                                                    next(dataReader)
                                                tempData = list(dataReader)
                                            with open (summaryPath,'a', newline='') as summaryFile:
                                                dataWriter = csv.writer(summaryFile, delimiter=',')
                                                dataWriter.writerows(tempData)
                                    
                                    # Sort summary file
                                    with open (summaryPath,'r') as unsortFile:
                                        dataReader = csv.reader(unsortFile)
                                        unsortData = list(dataReader)
                                        
                                    zerolessData = [x for x in unsortData if x]
                                    del unsortData
                                    sortData = sorted(unique_everseen(zerolessData),key=lambda x: int(x[0]))                           
                                    del zerolessData

                                    with open (summaryPath,'w', newline='') as sortFile:
                                        sortWriter = csv.writer(sortFile, delimiter=',')
                                        sortWriter.writerows(sortData)
                configsComplete += 1
                pctComplete = configsComplete/totalConfigs * 100
                if configsComplete%5 == 0:
                    print("Configs Completed: %d/%d, (%4.2f%%)", (configsComplete,totalConfigs,pctComplete))