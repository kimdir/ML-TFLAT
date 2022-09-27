# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 13:22:18 2020

@author: Michael Stebbins
"""

#import os, csv, math, time, sys, random
#import tensorflow as tf
#from sklearn.preprocessing import MinMaxScaler
#from keras.models import Sequential
#from keras.layers import Dense, LSTM
#from keras.callbacks import EarlyStopping,TensorBoard,ModelCheckpoint,ReduceLROnPlateau
#from keras.initializers import RandomUniform,VarianceScaling
#from keras.preprocessing.sequence import TimeseriesGenerator

from NNOptionsImporter import NNOptionsImporter
from NNDataImporter import NNDataImporter
from NNFileHandler import NNFileHandler
from NeuralNetwork_V3 import NeuralNetwork

debugFlag = False

# Eval Mode Parameters
evalMode = False
loadPaths = ["E:\\Neural Network\Models\\_Valid Models\\Sigmoid Activation\\133 5-7\\Model Weights.hdf5",
             "E:\\Neural Network\Models\\_Valid Models\\Sigmoid Activation\\134 0-6-7\\Model Weights.hdf5"]


# Initialize variables
rootPath = 'E:\\Neural Network'
customNames = False #input('Use custom model names? ')
modelList = []

#Initialize helper classes
nnOptions = NNOptionsImporter(rootPath)
nnData = NNDataImporter(rootPath, nnOptions.options['ingest'])
FileManager = NNFileHandler(rootPath)

print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
print('\nHelpers Initiated!\n')
print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')


# Set up list of models
for architecture in nnOptions.architectures:
    if customNames:
        modelName = input('Enter custom model name: ')
    else:
        modelName = None

    FileManager.BuildDirs(modelName)
    modelList.append(NeuralNetwork(FileManager.modelName,
                                   FileManager.GetPaths(),
                                   architecture,
                                   nnOptions.options,
                                   nnData.units,
                                   nnData.trainGenList,
                                   nnData.evalGenList,
                                   ['mse','accuracy']))
    
for modelIndex,model in enumerate(modelList):    
    if evalMode == True:
        print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
        print('\nEvaluation Only Mode Active\n')
        print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
        
        model.LoadNN(loadPaths[modelIndex])
        model.EvaluateNN()

        print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
        print('\nEvaluation Only Mode Completed!\n')
        print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
        
    else:
        # Build each model
        model.BuildNN()
        
    # Allow User to review models
if not debugFlag:
    reviewFlag = True if input('Review the models? (Y/N) ') == 'Y' else False
    if reviewFlag:
        for index, model in enumerate(modelList):
            model.model.summary()
            print('\n\nModel %0.0f of %0.0f.' %(index+1, len(modelList)))
            input('Press Enter to continue.\n')

# Train the models
for index, model in enumerate(modelList):
    model.TrainNN()
    print('//////////////////////////////////////////////////')
    print('\n Training Models...%0.0f%% Complete' % ((index+1)/len(modelList)*100))
    print('//////////////////////////////////////////////////')
    model.EvaluateNN()
    print('//////////////////////////////////////////////////')
    print('\n Evaluating Models...%0.0f Complete' % ((index+1)/len(modelList)*100))
    print('//////////////////////////////////////////////////')

print('$$$$$$$$$$$&&&&&&&&$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
print('\nEvaluation Complete!\n')
print('$$$$$$$$$$$&&&&&&&&$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
