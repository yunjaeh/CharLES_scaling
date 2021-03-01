#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script for analyzing scaling study result
- Computational resources: Stampede 2 cluster
- Solver: CharLES, Helmholtz solver


Created on Fri Feb 26 18:03:41 2021
@author: yunjaeh
    Last modified Feb. 26, 2020
"""


#%%
import numpy as np
import matplotlib.pyplot as plt

cases = ['knl', 'skx']

## both use base mesh
numCPUs  = {'knl': 68,      'skx':48}
# numCells = {'knl':38475335, 'skx':38475060}
numCells = {'knl':38475335, 'skx':21399033}
numNodes = {'knl':[2, 4, 8, 16, 32, 64], \
            'skx':[2, 4, 8, 16, 32, 64]}

for test_case in cases:
    print('Case:', test_case)
    for node in numNodes[test_case]:
        print('# nodes:', node,
          ', # cores:', (node*numCPUs[test_case]),
          ', # cells/core:', numCells[test_case]/(node*numCPUs[test_case]))

#%% read data from log files

step = np.arange(0,500)
step_save= np.arange(-1,500,50)
step_save[0]+=1
step_data = np.ones(len(step), np.bool)
step_data[step_save] = 0
# print(step,step_save)

time_sec = dict()
norm_spd = dict()

for test_case in cases:
    for node in numNodes[test_case]: 
        time_sec[(test_case,node)]=[]
        norm_spd[(test_case,node)]=[]
        with open('./log_base_'+test_case+'/log.'+str(node),'r') as fp:
            for line in fp:
                line_split=line.split()
                # print(line_split)
                try:
                    if(line_split[1]=='time'):
                        # print(line_split)
                        time_sec[(test_case,node)].append(float(line_split[5]))
                        norm_spd[(test_case,node)].append(float(line_split[9]))
                except:
                    continue

# %% plot

mean_norm_spd = {'knl':[], 'skx':[]}
mean_time_sec = {'knl':[], 'skx':[]}
mean_norm_spd_comp = {'knl':[], 'skx':[]}
mean_time_sec_comp = {'knl':[], 'skx':[]}

fig_num=0
for test_case in cases:
    plt.figure(fig_num,figsize=(10,4))
    fig_num+=1
    for node in numNodes[test_case]:
        time_sec_temp = np.asarray(time_sec[(test_case,node)])
        norm_spd_temp = np.asarray(norm_spd[(test_case,node)])
        
        mean_norm_spd[test_case].append(norm_spd_temp.mean())
        mean_time_sec[test_case].append(time_sec_temp.mean())
        mean_norm_spd_comp[test_case].append(norm_spd_temp[step_data].mean())
        mean_time_sec_comp[test_case].append(time_sec_temp[step_data].mean())
        
        plt.subplot(121)
        plt.plot(step, time_sec_temp)
        
        plt.subplot(122)
        plt.plot(step[step_data], time_sec_temp[step_data])
    
    for i in [121, 122]:
        plt.subplot(i)
        plt.xticks(range(0,501,100))
        plt.xlabel('Time step')
        plt.ylabel('Time [sec]')
        plt.legend(numNodes[test_case],loc='upper right')
        plt.ylim((0,210))
    plt.savefig('results/time_per_step_'+test_case+'.png')
 

#%% mean time taken for time steps

plt.figure(figsize=(6,4))
plt.plot(numNodes['skx'], mean_time_sec['skx'],'b.-')
plt.plot(numNodes['skx'], mean_time_sec_comp['skx'],'b.--')
plt.plot(numNodes['knl'], mean_time_sec['knl'],'r.-')
plt.plot(numNodes['knl'], mean_time_sec_comp['knl'],'r.--')

plt.title('Mean time taken for advanding time steps')
plt.legend(['skx: computation + data IO','skx: computation only',\
            'knl: computation + data IO','knl: computation only'])
plt.xlabel('# nodes')
plt.ylabel('Time [sec]')
plt.xticks(numNodes['knl'])
plt.yticks(range(0,101,20))
plt.ylim(0,100)
plt.grid()
plt.savefig('results/mean_time_per_step_knl_skx.png')

#%% Mean normalized speed

plt.figure(figsize=(6,4))
plt.plot(numNodes['skx'], mean_norm_spd['skx'],'b.-')
plt.plot(numNodes['skx'], mean_norm_spd_comp['skx'],'b.--')
plt.plot(numNodes['knl'], mean_norm_spd['knl'],'r.-')
plt.plot(numNodes['knl'], mean_norm_spd_comp['knl'],'r.--')

plt.title('Mean normalized speed for advanding time steps')
plt.legend(['skx: computation + data IO','skx: computation only',\
            'knl: computation + data IO','knl: computation only'])
plt.xlabel('# nodes')
plt.ylabel('Time [sec]')
plt.xticks(numNodes['knl'])
plt.yticks(range(0,1001,200))
plt.ylim(0,1000)
plt.grid()
plt.savefig('results/mean_norm_spd_knl_skx.png')

    
#%% speed up curve

plt.figure(figsize=(12,4))
su_ideal=dict()
su_IO=dict()
su_comp=dict()

cid='rb'
subplt=121
for key in enumerate(cases):
    plt.subplot(121+key[0])
    test_case=key[1]

    su_ideal[test_case] = np.asarray(numNodes[test_case])/numNodes[test_case][0]
    su_IO[test_case]    = mean_time_sec[test_case][0]/mean_time_sec[test_case]
    su_comp[test_case]  = mean_time_sec_comp[test_case][0]/mean_time_sec_comp[test_case]
    
    plt.plot(numNodes[test_case],su_ideal[test_case],'k.--')
    plt.plot(numNodes[test_case],su_comp[test_case],'.--'+cid[key[0]])
    plt.plot(numNodes[test_case],su_IO[test_case],'.-'+cid[key[0]])
    plt.xticks(numNodes[test_case])
    
    plt.grid()
    plt.xlabel('# nodes')
    plt.ylabel('Speedup')
    plt.title('Speedup curve: '+test_case)
    plt.legend(['Ideal','Computation only','Computation + data IO',])
    
plt.savefig('results/speedup_curve_knl_skx.png')






