# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 17:03:50 2020

@author: Kiaru
"""

#from more_itertools import unique_everseen

import os 
import csv
import sys
import shutil
import pandas as pd

processingPath = "E:\\Numerical Model v4\\Outputs\\_For Processing"
trainDataPath = "E:\\Neural Network\\Data - Training"
evalDataPath = "E:\\Neural Network\\Data - Evaluation"
fileName = "Strain Summary.csv"
configName = "ModelConfigurations.xls"
inputName = "Config Inputs.csv"
outputName = "Config Output.csv"
modeVal = 0
modeSelected = False

while not modeSelected:
    modeVal = input("Select Mode:\n[1] - Training Data\n[2] - Evaluation Data\nInput Option: ")
    if modeVal == '1':
        outputTypePath = trainDataPath
        modeSelected = True
    elif modeVal == '2':
        outputTypePath = evalDataPath
        modeSelected = True
    else:
        print("\n -- Bad Input --\n\n\n")

for subdirs, dateDirs, files in os.walk(processingPath):
    for dateVal in dateDirs:
        if not(dateVal[0].isnumeric()):
            break
        folderPath = os.path.join(processingPath,dateVal)
        saveDirPath = os.path.join(outputTypePath,dateVal)
        if os.path.isdir(saveDirPath):
            print("Deleting old directory...")
            #shutil.rmtree(savePath)
        os.mkdir(saveDirPath)
        print(folderPath)
        for root,dirs,files in os.walk(folderPath):
            for folderName in dirs:
                if folderName.startswith("D"):
                    break
                dataPath = os.path.join(folderPath,folderName)
                savePath = os.path.join(saveDirPath,folderName)
                os.mkdir(savePath)
                trainingFolderPath = os.path.join(trainDataPath,folderName)
                configID = []
                configVals = []

                if not os.path.exists(trainingFolderPath):
                    os.makedirs(trainingFolderPath)

                # Get Config ID
                for element in folderName:
                    if element.isnumeric():
                        configID.append(int(element))
                print(configID)

                # Identify file paths
                inputPath = os.path.join(savePath,inputName)
                outputPath = os.path.join(savePath,outputName)
                filePath = os.path.join(dataPath,fileName)
                configPath = os.path.join(dataPath,configName)
                configCSVPath = os.path.join(dataPath,"ModelConfigurations.csv")

                # Get configuration data for the input file
                xls_file = pd.read_excel(configPath)
                xls_file.to_csv(configCSVPath,index=False, header=False)

                with open(configCSVPath,'r') as configFile:
                    configReader = csv.reader(configFile)
                    configData = list(configReader)

                for i in range(0,len(configID)):

                    configVals.append(float(configData[configID[i]-1][i]))

                with open(filePath,'r') as summaryFile:
                    summaryReader = csv.reader(summaryFile)
                    summaryData = list(summaryReader)

                inputData = []
                outputData = []
                dataPointIndex = 0
                dataHeader = None

                summaryData.sort(key=lambda x: int(x[0]))
                for dataPoint in summaryData:
                    if dataPointIndex == 0:
                        dataHeader = dataPoint[-1]
                    strainPoint = dataPoint[-1]
                    cyclePoint = dataPoint[0]
                    inputData.append(strainPoint)
                    outputData.append(cyclePoint)
                    dataPointIndex += 1

                inputData = list(inputData)
                outputData = list(outputData)

                inputData = [x for x in inputData if x != '0']
                inputData = [x for x in inputData if x != dataHeader]
                outputData = [x for x in outputData if x != '0']

                #print(len(inputData))
                #print(len(outputData))

                #del inputData[0:1]
                #del outputData[0:1]
                outputData.reverse()

                with open(inputPath,'w',newline='') as inputFile:
                    inputWriter = csv.writer(inputFile)
                    for item in inputData:
                        newRow = (item,configVals[0],configVals[1],configVals[5],configVals[6])
                        inputWriter.writerow(newRow)

                with open(outputPath,'w',newline='') as outputFile:
                    outputWriter = csv.writer(outputFile)
                    for item in outputData:
                        outputWriter.writerow([item])
