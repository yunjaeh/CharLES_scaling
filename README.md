# CharLES_scaling
- Parallel scaling study using 
- CharLES Helmholtz solver in Stampede2 cluster
  
# Test case:
LES simulation for natural ventilation in urban slums of Dhaka, Bangladesh
- \# cells: 35M
- Boundary conditions
    - Top: slip
    - Ground: rough wall, z0 = 0.3 m
    - Two sides: periodic

# Parallel configs.
 - stampede2 cluster
 - KNL computing nodes (68 CPUs / node)
 - \# nodes & CPUs
 
| \# nodes |  2 |  4 |  8 | 16 | 32 | 64 | 
|----------|----|----|----|----|----|----|
| \# CPUs  | 136| 272| 544|1088|2196|4352|

# Results:

![time each step](results/time_per_step.png)


![mean time](results/mean_time_per_step.png)


![Speedup Curve](results/speedup_curve.png)


