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

cases = ['base', 'fine']

## base mesh
num_cells={'base':38475335, 'fine':85041048}
num_nodes={'base':[2, 4, 8, 16, 32, 64], 'fine':[4, 8, 16, 32, 64]}

for test_case in cases:
    print('Case:', test_case)
    for node in num_nodes[test_case]:
        print('# nodes:', node,
          ', # cores:', 68*node,
          ', # cells/core:', num_cells[test_case]/(68*node))

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
    for node in num_nodes[test_case]: 
        time_sec[(test_case,node)]=[]
        norm_spd[(test_case,node)]=[]
        with open('./log_'+test_case+'/log.'+str(node),'r') as fp:
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

mean_norm_spd = {'base':[], 'fine':[]}
mean_time_sec = {'base':[], 'fine':[]}
mean_norm_spd_comp = {'base':[], 'fine':[]}
mean_time_sec_comp = {'base':[], 'fine':[]}

fig_num=0
for test_case in cases:
    plt.figure(fig_num,figsize=(10,4))
    fig_num+=1
    for node in num_nodes[test_case]:
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
        plt.legend(num_nodes[test_case],loc='upper right')
        plt.ylim((0,350))
    plt.savefig('results/time_per_step_'+test_case+'.png')
 

#%% mean time taken for time steps

plt.figure(figsize=(6,4))
plt.plot(num_nodes['fine'], mean_time_sec['fine'],'b.-')
plt.plot(num_nodes['fine'], mean_time_sec_comp['fine'],'b.--')
plt.plot(num_nodes['base'], mean_time_sec['base'],'r.-')
plt.plot(num_nodes['base'], mean_time_sec_comp['base'],'r.--')

plt.title('Mean time taken for advanding time steps')
plt.legend(['Fine: computation + data IO','Fine: computation only',\
            'Base: computation + data IO','Base: computation only'])
plt.xlabel('# nodes')
plt.ylabel('Time [sec]')
plt.xticks(num_nodes['base'])
plt.yticks(range(0,121,20))
plt.ylim(0,120)
plt.grid()
plt.savefig('results/mean_time_per_step.png')

    
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

    su_ideal[test_case] = np.asarray(num_nodes[test_case])/num_nodes[test_case][0]
    su_IO[test_case]    = mean_time_sec[test_case][0]/mean_time_sec[test_case]
    su_comp[test_case]  = mean_time_sec_comp[test_case][0]/mean_time_sec_comp[test_case]
    
    plt.plot(num_nodes[test_case],su_ideal[test_case],'k.--')
    plt.plot(num_nodes[test_case],su_comp[test_case],'.--'+cid[key[0]])
    plt.plot(num_nodes[test_case],su_IO[test_case],'.-'+cid[key[0]])
    plt.xticks(num_nodes[test_case])
    
    plt.grid()
    plt.xlabel('# nodes')
    plt.ylabel('Speedup')
    plt.title('Speedup curve: '+test_case)
    plt.legend(['Ideal','Computation only','Computation + data IO',])
    
plt.savefig('results/speedup_curve.png')



#%% speedup curve comparison: base & fine

plt.figure(figsize=(8,6))
su_ideal['base'] = np.asarray(num_nodes['base'])/num_nodes['base'][0]
su_comp['base']  = mean_time_sec_comp['base'][0]/mean_time_sec_comp['base']
su_comp['fine']  = mean_time_sec_comp['fine'][0]/mean_time_sec_comp['fine']
    
plt.plot(num_nodes['base'],su_ideal['base'],'k.--')
plt.plot(num_nodes['fine'],su_comp['fine']*2,'b.-')
plt.plot(num_nodes['base'],su_comp['base'],'r.-')
    
plt.xticks(num_nodes['base'])
plt.yticks(range(0,33,4))

plt.grid()
plt.xlabel('# nodes')
plt.ylabel('Speedup')
plt.title('Speedup curve')
plt.legend(['Ideal','Fine','Base'])

plt.savefig('results/speedup_curve2.png')

#%% percentage

plt.figure(figsize=(8,5))
plt.plot(num_nodes['base'],su_ideal['base']/su_ideal['base'],'k.--')
plt.plot(num_nodes['fine'],su_comp['fine']/su_ideal['fine'],'b.--')
plt.plot(num_nodes['fine'],su_IO['fine']/su_ideal['fine'],'b.-')

plt.plot(num_nodes['base'],su_comp['base']/su_ideal['base'],'r.--')
plt.plot(num_nodes['base'],su_IO['base']/su_ideal['base'],'r.-')
   

plt.xticks(num_nodes['base'])
plt.grid()
plt.xlabel('# nodes')
plt.ylabel('Ratio')
plt.title('Ratio to ideal speedup')
plt.legend(['Ideal',\
            'Fine: computation only','Fine: computation + data IO',\
            'Base: computation only','Base: computation + data IO'])
plt.savefig('results/ratio_to_ideal.png')





