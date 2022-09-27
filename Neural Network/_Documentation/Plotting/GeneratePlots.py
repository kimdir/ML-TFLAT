# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 16:11:25 2020

@author: Kiaru
"""
import os
import csv
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter

dataPath = "E:\\Numerical Model v4\\Plots"
groupOutPath = "E:\\Numerical Model v4\\Plots\\_Model Validation"
convergencePath = "E:\\Numerical Model v4\\Plots\\Convergence"
legendLabelsPath = "E:\\Numerical Model v4\\Plots\\Plot Legend Labels.csv"
variableList = ['Flow Rate',
                'In Temp',
                'Length',
                'Out Diameter',
                'Out Temp',
                'Pressure']
dataTypes = ['Damage','Strain','Stress','Temperature']
plotFormat = ['b','r--','g-.']
yAxisLabels = ['% Damage','Strain (m/m)','Stress (Pa)','Temperature (°C)']

with open (legendLabelsPath,'r') as lFile:
    lReader = csv.reader(lFile)
    legendLabels = list(lReader)

# Set paths for all variables
variablePaths = [os.path.join(dataPath,variableName + " Data") 
                 for variableName in variableList]

for variableIndex, variablePath in enumerate(variablePaths):
    # Set poths for all data types
    sourcePaths = [f.path for f in os.scandir(variablePath) if f.path.endswith('.csv')]
    
    # Initialize new plot
    fig = plt.figure(figsize=(20,15))
    plt.subplots_adjust(hspace=0.3)

    plt.suptitle(('Effect of Varying ' + variableList[variableIndex]), fontsize=50)
    
    # Loop for plotting each data set
    for sourceIndex, sourcePath in enumerate(sourcePaths):
        with open(sourcePath) as sFile:
            sReader = csv.reader(sFile)
            sourceData = list(sReader) # sourceData[cycle][value]
            sourceData.pop(0)
        
        cycles = [int(item[0]) for item in sourceData if item[0]]
        
        config1 = [float(item[1]) for item in sourceData if item[1]]
        config2 = [float(item[2]) for item in sourceData if item[2]]
        config3 = [float(item[3]) for item in sourceData if item[3]]
        
        cycles1 = cycles[:len(config1)]
        cycles2 = cycles[:len(config2)]
        cycles3 = cycles[:len(config3)]
        
        ax = plt.subplot(2,2,sourceIndex+1)
        lines = plt.plot(cycles1,config1,plotFormat[0],
                 cycles2,config2,plotFormat[1],
                 cycles3,config3,plotFormat[2])
        plt.title(dataTypes[sourceIndex],fontsize='xx-large')
        
        max_yticks = 5
        max_xticks = 25
        yloc = plt.MaxNLocator(max_yticks)
        xloc = plt.MaxNLocator(max_xticks)
        ax.yaxis.set_major_locator(yloc)
        ax.xaxis.set_major_locator(xloc)
        
        plt.xticks(rotation=45)
        plt.xlim(left=0)
        
        plt.xlabel("Cycles",fontsize='x-large')
        plt.ylabel(yAxisLabels[sourceIndex],fontsize='x-large')
    
    fig.legend(lines,legendLabels[variableIndex],'center left',fontsize=18,labelspacing=1,borderaxespad = -.1)
        
    plt.savefig(os.path.join(variablePath,(variableList[variableIndex] + ' Plot.png')))
    plt.savefig(os.path.join(groupOutPath,(variableList[variableIndex] + ' Plot.png')))
    
# Plot Convergence Data
plt.figure(figsize=(10,8))
with open(os.path.join(convergencePath,"ConvergeData.csv")) as sFile:
    sReader = csv.reader(sFile)
    sourceData = list(sReader) # sourceData[cycle][value]
    sourceData.pop(0)

nodes = [int(item[0]) for item in sourceData if item[0]]
cycles = [int(item[1]) for item in sourceData if item[1]]

ax = plt.plot(nodes,cycles,'-o')
plt.title("Numerical Model Convergence",fontsize='xx-large')

# max_yticks = 5
# max_xticks = 25
# yloc = plt.MaxNLocator(max_yticks)
# xloc = plt.MaxNLocator(max_xticks)
# ax.yaxis.set_major_locator(yloc)
# ax.xaxis.set_major_locator(xloc)

# plt.xticks(rotation=45)
plt.xlim(left=0)

plt.xlabel("Number of Nodes",fontsize='x-large')
plt.ylabel("Cycles to Failure",fontsize='x-large')

plt.savefig(os.path.join(convergencePath,('Convergence Plot.png')))
plt.savefig(os.path.join(groupOutPath,('Convergence Plot.png')))
