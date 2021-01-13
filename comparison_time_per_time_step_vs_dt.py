#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 11:23:52 2021

    Python code to check the relation 
    between CFL number and time taken at each step

@author: yunjaeh

"""


#%%
import numpy as np
import matplotlib.pyplot as plt

## base mesh
test_case = 'base'
num_node=16
num_cells=38475335

print('Case:', test_case)
print('# nodes:', num_node,
      ', # cores:', 68*num_node,
      ', # cells/core:', num_cells/(68*num_node))

nodes=['16','16_low_cfl']

#%% read data from log files

step = np.arange(0,500)
step_save= np.arange(-1,500,50)
step_save[0]+=1
step_data = np.ones(len(step), np.bool)
step_data[step_save] = 0
# print(step,step_save)

time_sec = dict()
norm_spd = dict()
cfl=dict()

for node in nodes:
    time_sec[(test_case,node)]=[]
    norm_spd[(test_case,node)]=[]
    cfl[(test_case,node)]=[]
    with open('./log_'+test_case+'/log.'+node,'r') as fp:
        for line in fp:
            line_split=line.split()
            # print(line_split)
            try:
                if(line_split[1]=='time'):
                    time_sec[(test_case,node)].append(float(line_split[5]))
                    norm_spd[(test_case,node)].append(float(line_split[9]))
                elif(line_split[2]=='CFL,'):
                    # print(line_split[3].split(':')[1])
                    cfl[(test_case,node)].\
                        append(float(line_split[3].split(':')[1]))
                    
            except:
                continue
min_len = len(time_sec['base','16_low_cfl'])

#%%
fig, ax = plt.subplots(figsize=(5,5))
for node in nodes:
    ax.plot(cfl[test_case,node], time_sec[test_case,node],'o')
ax.legend(['DT=0.02','DT=0.01'])
ax.set(title='Base case, #Nodes=16', \
       xlabel='# CFL', ylabel='Time per time step [sec]', \
       xlim=(0.2, 1.4), ylim=(6,20))
ax.grid()
fig.savefig('results/comparison_dt.png')

