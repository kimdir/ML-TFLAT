# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 11:18:34 2020

@author: Michael Stebbins
"""
import os

class NNFileHandler:
    
    def __init__(self,rootPath):
        
        self.rootPath = rootPath
        self.modelPath = None
        self.trainPath = None
        self.evalPath = None
        
        self.modelName = None
        
    def GetPaths(self):
        pathList = [self.modelPath,self.trainPath,self.evalPath]
        return pathList
    
    def BuildDirs(self,modelName=None):
        
        if modelName:
            self.modelName = modelName
        else:
            self.modelName = self.GetModelSerial(self.rootPath)
        
        isModelDirMade = False
        while not isModelDirMade:
            self.modelPath = os.path.join(self.rootPath,'Models',str(self.modelName))
            if os.path.isdir(self.modelPath):
                print('>>>>> Model Name taken, assigning serial number...')
                self.modelName = self.GetModelSerial(self.rootPath)
            else:
                os.mkdir(self.modelPath)
                isModelDirMade = True
        self.trainPath = os.path.join(self.modelPath,'Training')
        self.evalPath = os.path.join(self.modelPath,'Evaluation')
        os.mkdir(self.trainPath)
        os.mkdir(self.evalPath)
    
    def GetModelSerial(self,rootPath):
        
        import os, csv
        
        serialPath = os.path.join(rootPath,'_Documentation','Serial Numbers.csv')
        with open(serialPath,'r') as sFile:
            sReader = csv.reader(sFile)
            sList = list(sReader)
            
        serial_identified = False
        while serial_identified == False:
            try:
                serialNumber = int(sList[-1][0]) + 1
                serial_identified = True
            except:
                sList.pop()
        
        
        with open(serialPath,'a') as sFile:
            sWriter = csv.writer(sFile)
            sWriter.writerow([serialNumber])
            
        return serialNumber