# -*- coding: utf-8 -*-
"""
Created on Sun Mar  8 16:21:05 2020

Takes input and output datasets and produces grouped time-series data samples
based on values set by the dataOptions array

Input:  inputData       (2D Float Array, Column 0 is Cycles) 
        outputData      (2D Float Array, Column 0 is Cycles)
        stepCount       (Integer)
        dataOptions     (Integer Array)
        
Output: TimeseriesData  (Sequence)

@author: Michael Stebbins
"""

def PreprocessTimeseries(inputData,outputData,stepCount,dataOptions):
    from keras.preprocessing.sequence import TimeseriesGenerator
    
    # Determine batch size based on     
    setCount = len(input[:,0])-stepCount
    
    # Generate time series sequences based on function inputs
    TimeseriesData = TimeseriesGenerator(inputData,outputData,length=stepCount,
                                         sampling_rate=dataOptions[0], 
                                         stride=dataOptions[0],
                                         batch_size=setCount)
    
    return TimeseriesData
    