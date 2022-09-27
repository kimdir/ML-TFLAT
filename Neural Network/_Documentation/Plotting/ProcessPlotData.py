import os
import csv
from more_itertools import unique_everseen

dataPath = "E:\\Numerical Model v4\\Outputs\\_Legacy\\Training Data 4-7-2020"
plotOutputPath = "E:\\Numerical Model v4\\Plots"

variableList = ['Flow Rate Data',
                'In Temp Data',
                'Length Data',
                'Out Diameter Data',
                'Out Temp Data',
                'Pressure Data']
dataTypes = ["Damage",
                "Stress",
                "Strain",
                "Temperature"]
summaryFiles = ["Damage Summary.csv",
                "Stress Summary.csv",
                "Strain Summary.csv",
                "Temperature Summary.csv"]
columnLabels = ['Cycle','Config 1','Config 2','Config 3']

fileIndex = [181,366,183,61]

plotInterval = 1000 # Step between sampled points

pathList = [f.path for f in os.scandir(dataPath) if f.is_dir()]

def SortData(unsortData):
    zerolessData = [int(x) for x in unsortData if x]
    del unsortData
    sortData = sorted(unique_everseen(zerolessData))
    #sortData = sorted(unique_everseen(zerolessData),key=lambda x: int(x[0]))                           
    del zerolessData
    return sortData

for varIndex,dirName in enumerate(variableList):
    print("Loading %s..." % dirName)
    # Initialize output holders
    outputData = [[],[],[],[]]
    dataList = [[[],[],[],[]],
                [[],[],[],[]],
                [[],[],[],[]],
                [[],[],[],[]]]   
    
    # Get date folder
    dirPath = os.path.join(dataPath,dirName) # Date Folder
    # if not os.path.is_dir(os.path.join(dirPath,"Plot Output")):
    #     os.mkdir(os.path.join(dirPath,"Plot Output"))
    
    # Get config folder
    configPaths = [f.path for f in os.scandir(dirPath) if f.is_dir()] # Config Folder
    
 
    
    for configIndex,configPath in enumerate(configPaths):
        print(">> Loading %s..." % configPath)
        # Get data file paths
        filePaths = [os.path.join(configPath,dataType) for dataType in summaryFiles] 
        
        # Append data from the config file to the correct plot output file
        for index,filePath in enumerate(filePaths):
            # sourceFilePath = os.path.join(filePath,summaryFiles[index])
            
            # Set first column to cycles
            with open(filePath,'r') as sFile:
                sReader = csv.reader(sFile)
                sContent = list(sReader)
                cyclesList = SortData([cycle[0] for cycle in sContent if int(cycle[0])%plotInterval == 1])
                if len(cyclesList) > len(dataList[index][0]):
                    dataList[index][0] = cyclesList
                if index == 2:
                    dataList[index][configIndex+1] = [-1*float(sContent[int(rowIndex)][fileIndex[index]]) for rowIndex in cyclesList]
                else:
                    dataList[index][configIndex+1] = [sContent[int(rowIndex)][fileIndex[index]] for rowIndex in cyclesList]
    
    # Resize the data to match largest list length
    for dataClassList in dataList:
        for dataSubList in dataClassList:
            while len(dataSubList) < len(dataClassList[0]):
                dataSubList.append('')

    # Correct Strain Sign
    
    # Transpose the data for output            
    for dataIndex,dataType in enumerate(dataList):
        outputData[dataIndex] = [[dataList[dataIndex][0][x],
                                  dataList[dataIndex][1][x],
                                  dataList[dataIndex][2][x],
                                  dataList[dataIndex][3][x]]
                                 for x in range(len(dataList[dataIndex][1]))                         ]
        # Update column headers
        outputData[dataIndex].insert(0,columnLabels)

        # Set and create plot output file
    for outputIndex,dataSet in enumerate(outputData):
        plotFilePath = os.path.join(plotOutputPath,variableList[varIndex],(dataTypes[outputIndex] + " Plot Output.csv"))
        
        with open(plotFilePath,'w',newline='') as pFile:
            pWriter = csv.writer(pFile)
            pWriter.writerows(dataSet)

