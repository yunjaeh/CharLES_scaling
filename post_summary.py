#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 11:33:17 2021

@author: yunjaeh
"""

import numpy as np
import matplotlib.pyplot as plt

cases = [('coarse','knl'),('base','knl'), ('fine','knl'), ('base','skx')]

# {'base':38475335, 'fine':85041048}
numCPUs ={'knl':68, 'skx':48}
numCells={('coarse','knl'):21.4e6, ('base','knl'):38.5e6, ('fine','knl'):85.0e6, \
           ('base','skx'):38.5e6}

numNodes={('coarse','knl'):[2, 4, 8, 16, 32, 64], \
          ('base','knl'): [2, 4, 8, 16, 32, 64],  \
          ('fine','knl'): [4, 8, 16, 32, 64],     \
          ('base','skx'): [2, 4, 8, 16, 32, 64, 128]}
numProcs=dict()

for test_case in cases:
    print('Case:', test_case)
    numProcs[test_case]=[]
    for node in numNodes[test_case]:
        numProcs[test_case].append(node*numCPUs[test_case[1]])
        print('# nodes:', node, ', # CPUs:', node*numCPUs[test_case[1]],
        ', # cells/core:', int(numCells[test_case]/(node*numCPUs[test_case[1]])))

#%% read data from log files

step = np.arange(0,500)
step_IO= np.arange(-1,500,50)
step_IO[0]+=1
step_comp = np.ones(len(step), np.bool)
step_comp[step_IO] = 0
# print(step,step_save)


timeSec = dict()
normSpd = dict()
meanTimeSec = dict()
meanNormSpd = dict()

for case in cases:
    print(case)
    meanTimeSec[case], meanNormSpd[case]=[],[]
    for node in numNodes[case]: 
        timeSecTemp, normSpdTemp = [], []
        with open('./log_'+case[0]+'_'+case[1]+'/log.'+str(node),'r') as fp:
            for line in fp:
                line_split=line.split()
                try:
                    if(line_split[1]=='time'):
                        # print(line_split)
                        timeSecTemp.append(float(line_split[5]))
                        normSpdTemp.append(float(line_split[9]))
                except:
                    continue
        timeSec[(case[0], case[1], node)]=timeSecTemp
        normSpd[(case[0], case[1], node)]=normSpdTemp
        
        # include data IO
        # meanTimeSec[case].append(np.asarray(timeSecTemp).mean())        
        # meanNormSpd[case].append(np.asarray(normSpdTemp).mean())
        
        # computation only
        meanTimeSec[case].append(np.asarray(timeSecTemp)[step_comp].mean())        
        meanNormSpd[case].append(np.asarray(normSpdTemp)[step_comp].mean())
        

#%% log-log time plot

idCode = {'coarse':'o', 'base':'d', 'fine':'s'}
cCode  = {'knl':'r', 'skx':'b'}

# log - log plot
plt.figure(figsize=(8,4))
# plt.loglog(numNodes['skx'], log,'k--')
for i, case in enumerate(cases):
    plt.loglog(numProcs[case], meanTimeSec[case][0]/numProcs[case]*numProcs[case][0],'k--')
    plt.loglog(numProcs[case], meanTimeSec[case], \
               idCode[case[0]]+cCode[case[1]]+'-', label=case[1]+', '+case[0])
    
plt.legend()
plt.xlabel('# Processors')
plt.ylabel('Elapsed time [sec]')
plt.xticks([10**2, 10**3, 10**4])
plt.yticks([10**0, 10**1, 10**2])

plt.grid(True, which="both", ls="-")
plt.savefig('results/summary_time.png')


#%%

plt.figure(figsize=(8,4))
# plt.loglog(numNodes['skx'], log,'k--')
for i, case in enumerate(cases):
    plt.semilogx(numProcs[case], [meanNormSpd[case][0]]*len(numProcs[case]),'k--')
    plt.semilogx(numProcs[case], meanNormSpd[case], \
               idCode[case[0]]+cCode[case[1]]+'-', label=case[1]+', '+case[0])

plt.legend()
plt.title('Norm Spd [core-s/Mcv/step]')
plt.xlabel('# Processors')
plt.ylabel('Normalized speed [sec]')
plt.xticks([10**2, 10**3, 10**4])
plt.ylim(0, 1001)
plt.grid(True, which="both", ls="-")
plt.savefig('results/summary_normalized_speed.png')








