# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 14:37:56 2020

@author: Kiaru
"""
import csv
import math
import matplotlib.pyplot as plt

phaseDataPath = "E:\\Neural Network\\_Documentation\\Plotting\\Phase Data.csv"
p1Data = []
p2Data = []
p3Data = []

def TransposeList(data):
    out1 = [int(row[0]) for row in data]
    out2 = [float(row[1]) for row in data]
    
    return out1, out2

with open(phaseDataPath,'r') as pFile:
    pReader = csv.reader(pFile)
    headers = next(pReader)
    for row in pReader:
        p1Data.append([row[0],row[1]])
        p2Data.append([row[2],row[3]])
        p3Data.append([row[4],row[5]])

p2Data = [row for row in p2Data if row != ['','']]
p3Data = [row for row in p3Data if row != ['','']]

p1Data = p1Data[1::math.floor(len(p1Data)/100)]
p2Data = p2Data[1::math.floor(len(p2Data)/300)]
p3Data = p3Data[1::math.floor(len(p3Data)/5000)]

p1Cycles,p1Stress = TransposeList(p1Data)
p2Cycles,p2Stress = TransposeList(p2Data)
p3Cycles,p3Stress = TransposeList(p3Data)

# Build Plot
phaseFig = plt.figure(figsize=(10,8))
#plt.title('Fatigue Phases for Aluminum - Stress at Element 61')
plt.xlabel('Cycles')
plt.ylabel('von Mises Stress (Pa)')

lines = plt.plot(p1Cycles,p1Stress,'b',p2Cycles,p2Stress,'--r',p3Cycles,p3Stress,'-.g')



plt.axvline(x=p2Cycles[0])
plt.axvline(x=p3Cycles[0])
ax = plt.axes()
plt.xlim([0,p3Cycles[-1]])

plt.legend(lines,['Phase 1','Phase 2','Phase 3'])

plt.show()