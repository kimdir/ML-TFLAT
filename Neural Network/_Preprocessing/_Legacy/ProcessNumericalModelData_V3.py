
import os
import csv
from natsort import natsorted

rootPath = 'E:\\Numerical Model v4\\Outputs\\_Legacy\\Training Data 4-7-2020'

varPaths = [f.path for f in os.scandir(rootPath) if f.is_dir()] # Variable Folders

# Find all configuration directories for each variable
for varPath in varPaths:
    configPaths = [f.path for f in os.scandir(varPath) if f.is_dir()] # Config Folders
    
    # Find all data type directories for each configuration
    for configPath in configPaths:
        dataTypePaths = [f.path for f in os.scandir(configPath) if f.is_dir()] # Data Type Folders
        
        for dataTypePath in dataTypePaths:
            dataName = os.path.basename(os.path.normpath(dataTypePath))
            summaryOutputPath = os.path.join(configPath,(dataName + " Summary.csv"))
            
            # Write a new summary file, overwriting previous versions if existing.
            print("Creating %s in directory %s..." % 
                  (os.path.basename(summaryOutputPath),
                   os.path.basename(configPath)))
            newSummary = open(summaryOutputPath,'w',newline='')
            newSummary.close()
            
            # Sort the files by Part #
            sourceFiles = natsorted([f.path for f in os.scandir(dataTypePath) 
                                     if f.path.endswith(".csv")])
            
            # Iterate through sorted file list and append to summary file, removing trailing zeros
            for sourceIndex, sourceFile in enumerate(sourceFiles):
                with open(summaryOutputPath,'a',newline='') as sFile, open(sourceFile,'r') as rFile:
                    rReader = csv.reader(rFile)
                    sWriter = csv.writer(sFile)
                    if sourceIndex > 0:
                        next(rReader)
                    uncheckedList = list(rReader)
                    outList = [cycle for cycle in uncheckedList if not all(val == '0' for val in cycle)]
                    sWriter.writerows(outList)
                