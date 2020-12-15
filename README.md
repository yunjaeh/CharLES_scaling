# CharLES scaling study
### Introduction
- Parallel scaling study using 
- CharLES Helmholtz solver in Stampede2 cluster
- Test with 2 meshes in different resolution (base & fine) 
- 6 different number of nodes (2, 4, 8, 16, 32, 64)
  
### Test case
LES simulation for natural ventilation in urban slums of Dhaka, Bangladesh

- Computational grid 
|    | # cells | Background cell size (m)| Smallest cell size (m)|
|----|-------- |-------------------------|-----------------------| 
|Base| 35M     | 8                       |                       |
|Fine| 85M     | 8                       |                       |

- Inflow condition
    - Turbulent ABL with optimization
    - U_{ref} = 1.67 m/s @ 25 m 
- Boundary conditions
    - Top: slip
    - Ground: rough wall, z0 = 0.3 m
    - Two sides: periodic
    - Outlet

### Parallel configuration
 - stampede2 cluster
 - KNL computing nodes (68 CPUs / node)
 - \# nodes & CPUs
 
| \# nodes     |  2 |  4 |  8 | 16 | 32 | 64 | 
|----------    |----|----|----|----|----|----|
| \# CPUs      | 136| 272| 544|1088|2196|4352|
|#Cells / #CPUs (base mesh)|282k|141k|70.7k|35.3k|17.7k|8.84k|
|#Cells / #CPUs (fine mesh)| | | | | | |


# Results:

![time each step](results/time_per_step.png)


![mean time](results/mean_time_per_step.png)


![Speedup Curve](results/speedup_curve.png)


