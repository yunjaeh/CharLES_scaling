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

nodes=['16','16_low_cfl','16_makefile','16_makefile_inflow','16_compiler','16_compiler_inflow']

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

#%% comparison: dt
fig, axes = plt.subplots(figsize=(10,5),ncols=2)
for node in nodes[0:2]:
    axes[0].plot(cfl[test_case,node], time_sec[test_case,node],'.')
    axes[1].plot(cfl[test_case,node], norm_spd[test_case,node],'.')
    
axes[0].set(ylabel='Time per time step [sec]', ylim=(5,20))
axes[1].set(ylabel='Normalized speed [core-s/Mcv/step]', ylim=(0,600))

for ax in axes:
    ax.legend(['DT=0.02','DT=0.01'])
    ax.set(xlabel='CFL #', xlim=(0.2, 1.4))
    ax.grid()
fig.savefig('results/comparison_dt.png')

#%% comparison: dt
fig, axes = plt.subplots(figsize=(6,4))


for i in [0,2,3,4,5]:
    # axes[0].plot(step, time_sec[test_case,nodes[0]],'.')
    plt_data = np.transpose(time_sec[test_case,nodes[i]])[step_data]
    print(i, np.mean(plt_data))
    axes.plot(i, np.mean(plt_data),'o')
    
axes.set(xlabel='Cases', ylabel='Time per time step',\
         xticklabels=['base','M','M/I', 'M/C', 'M/C/I'], \
         xticks=[0,2,3,4,5], ylim=(14,17))
axes.grid()
fig.savefig('results/comparison_MCI.png')
