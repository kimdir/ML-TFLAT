# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 14:52:39 2020

@author: Michael Stebbins
"""
import os
import csv

class NNOptionsImporter:
    """Handles the import of model architectures and build options"""
    def __init__(self, rootPath):

        self.rootPath = rootPath

        self.architectures = None

        self.buildOptions = None
        self.compileOptions = None
        self.trainOptions = None
        self.evalOptions = None
        self.ingestOptions = None

        self.options = {}
        
        self.GetOptions()

    def GetOptions(self):
        """
        Pulls the configurations that are located in root/Config and assigns
        them to the class variables for external access as well as an options
        dictionary for simplification of inputs

        Returns
        -------
        None.

        """
        optionsPath = os.path.join(self.rootPath, 'Config', 'Options.csv')
        with open(optionsPath, 'r') as oFile:
            oReader = csv.reader(oFile)
            optionsList = list(oReader)

        self.compileOptions = optionsList[0]
        self.trainOptions = optionsList[1]
        self.evalOptions = optionsList[2]
        self.ingestOptions = optionsList[3]

        architecturePath = os.path.join(self.rootPath, 'Config', 'Architectures.csv')
        with open(architecturePath, 'r') as aPath:
            aReader = csv.reader(aPath)
            self.architectures = list(aReader)
        
        buildPath = os.path.join(self.rootPath, 'Config', 'Build Options.csv')
        with open(buildPath, 'r') as bPath:
            bReader = csv.reader(bPath)
            self.buildOptions = list(bReader)        

        indexList = ['compile', 'train', 'evaluate','ingest','build','architecture']
        for index, label in enumerate(indexList):
            if label == 'build':
                self.options[label] = self.buildOptions
            elif label == 'architecture':
                self.options[label] = self.architectures   
            else:
                self.options[label] = optionsList[index]
