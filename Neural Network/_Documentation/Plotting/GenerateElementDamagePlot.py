# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 15:30:03 2020

@author: Kiaru
"""


# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 14:37:56 2020

@author: Kiaru
"""
import csv
import math
import matplotlib.pyplot as plt

damageDataPath = "E:\\Numerical Model v4\\Outputs\\_Legacy\\Training Data 4-7-2020\\Flow Rate Data\\[1 1 1 1 1 1 1]\\Damage Summary.csv"
selectData = []

def TransposeList(data):
    out1 = [int(row[0]) for row in data]
    out2 = [float(row[1]) for row in data]
    out3 = [float(row[2]) for row in data]
    out4 = [float(row[3]) for row in data]
    out5 = [float(row[4]) for row in data]
    out6 = [float(row[5]) for row in data]
    out7 = [float(row[6]) for row in data]
    out8 = [float(row[7]) for row in data]
    
    return out1, out2, out3, out4, out5, out6, out7, out8

def TrimList(cycles,data):
    data = [val*100 for val in data if val<1.0]
    cycles = cycles[0:len(data)]
    
    data = data[0::math.floor(len(data)/300)]
    cycles = cycles[0::math.floor(len(cycles)/300)]
    
    return cycles,data

with open(damageDataPath,'r') as pFile:
    pReader = csv.reader(pFile)
    headers = next(pReader)
    for row in pReader:
        selectRow = [val for index,val in enumerate(row) if (index-1)%3==0]
        selectRow = selectRow[0::10]
        selectRow.insert(0,row[0])
        selectData.append(selectRow)

cycles, e1, e11, e21, e31, e41, e51, e61 = TransposeList(selectData)

cE1, e1 = TrimList(cycles,e1)
cE11, e11 = TrimList(cycles,e11)
cE21, e21 = TrimList(cycles,e21)
cE31, e31 = TrimList(cycles,e31)
cE41, e41 = TrimList(cycles,e41)
cE51, e51 = TrimList(cycles,e51)
cE61, e61 = TrimList(cycles,e61)

# Build Plot
phaseFig = plt.figure(figsize=(10,8))
#plt.title('Fatigue Damage for Selected Elements')
plt.xlabel('Cycles')
plt.ylabel('Damage (%)')

lines = plt.plot(cE1, e1, '-b',
                 cE11, e11, '--r',
                 cE21, e21, '-.g',
                 cE31, e31, ':m',
                 cE41, e41, '-c',
                 cE51, e51, '--y',
                 cE61, e61, '-.k')

ax = plt.axes()
ax.xaxis.grid(True)
plt.xlim([0,cE61[-1]])
plt.ylim([0,100])

plt.legend(lines,['Element 1','Element 11','Element 21','Element 31','Element 41','Element 51','Element 61'])

plt.show()