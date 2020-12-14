# -*- coding: utf-8 -*-
"""
Script for analyzing scaling study result
- Computational resources: Stampede 2 cluster
- Solver: CharLES, Helmholtz solver

    Written by Yunjae Hwang
    Last modified Dec. 14, 2020
"""

#%%
import numpy as np
import matplotlib.pyplot as plt

# %% read data from log files

step = np.arange(0,500)
step_save= np.arange(-1,500,50)
step_save[0]+=1
step_data = np.ones(len(step), np.bool)
step_data[step_save] = 0
# print(step,step_save)

num_cells = 38475335
num_nodes = [2, 4, 8, 16, 32, 64]

for node in num_nodes:
    print('# nodes:', node,
          ', # cores:', 68*node,
          ', # cells/core:', num_cells/(68*node))
time_sec_dict = dict()
norm_spd_dict = dict()

for node in num_nodes:
    # print(node)
    time_sec_dict[node]=[]
    norm_spd_dict[node]=[]
    with open('./log/log.'+str(node),'r') as fp:
        for line in fp:
            line_split=line.split()
            try:
                if(line_split[1]=='time'):
#                    print(line_split)
                    time_sec_dict[node].append(float(line_split[5]))
                    norm_spd_dict[node].append(float(line_split[9]))
            except:
                continue


# %% plot

mean_norm_spd = []
mean_time_sec = []
mean_norm_spd_comp = []
mean_time_sec_comp = []

for node in num_nodes:
    time_sec = np.asarray(time_sec_dict[node])
    norm_spd = np.asarray(norm_spd_dict[node])

    mean_norm_spd.append(norm_spd.mean())
    mean_time_sec.append(time_sec.mean())
    mean_norm_spd_comp.append(norm_spd[step_data].mean())
    mean_time_sec_comp.append(time_sec[step_data].mean())

    plt.figure(1)
    plt.plot(step, time_sec)

    plt.figure(2)
    plt.plot(step[step_data], time_sec[step_data])
    
    plt.figure(3)
    plt.plot(step[step_save], time_sec[step_save]-time_sec[step_data].mean())


for i in range(1,4):
    plt.figure(i)
    plt.ylim(0,200)
    plt.legend(num_nodes,loc='upper right')
    plt.xlabel('Time step')
    plt.ylabel('Time [sec]')
#print(mean_norm_spd)

#%%
ideal_speedup = np.asarray(num_nodes)/2
print(ideal_speedup)
print(time_sec.mean)
# plt.subplot(131)
# plt.plot(num_nodes,mean_norm_spd,'o-')
# plt.title('Mean normalized spd')
# plt.subplot(132)
plt.plot(num_nodes,mean_time_sec,'bo-')
# plt.plot(num_nodes,mean_time_sec_comp,'ro-')
plt.xticks(num_nodes)
plt.yticks(range(0,120,20))
plt.ylim(0,100)
plt.title('Mean time taken for advanding time steps')
plt.xlabel('# nodes')
plt.ylabel('Time [sec]')
plt.grid()
plt.show()


plt.plot(num_nodes,ideal_speedup,'k--')
plt.plot(num_nodes,mean_time_sec_comp[0]/mean_time_sec_comp,'ro-')
plt.plot(num_nodes,mean_time_sec[0]/mean_time_sec,'bo-')
plt.xticks(num_nodes)
plt.xlabel('# nodes')
plt.ylabel('Speedup')
plt.legend(['Ideal','Computation only','Computation+save'])
plt.title('Speedup curve')
plt.grid()

plt.show()




