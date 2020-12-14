# CharLES_scaling
- Parallel scaling study using 
  CharLES Helmholtz solver in Stampede2 cluster
  
- Test case:
  LES simulation for natural ventilation in urban slums of Dhaka, Bangladesh
    # cells: 35M
    Boundary conditions

- Parallel configs.
    - stampede2 cluster
    - KNL computing nodes (68 CPUs / node)
#    - add table 

- Results:

![time each step](results/time_per_step.png)


![mean time](results/mean_time_per_step.png)


![Speedup Curve](results/speedup_curve.png)


