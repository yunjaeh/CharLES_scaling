#!/bin/bash

#SBATCH -p skx-normal
#SBATCH -J 128	      		# Job name
#SBATCH -o job.%j.out         # Name of stdout output file (%j expands to jobId)
#SBATCH -e job.%j.err	      # Name of error file (%j expands to jobID)
#SBATCH -N 128                  # Total number of nodes requested
#SBATCH -n 6144	              # Total number of mpi tasks requested (1 node : 68 CPU)
#SBATCH -t 6:00:00          # Run time (hh:mm:ss), 12  hours
#SBATCH --mail-type=ALL       # mail alert
#SBATCH --mail-user=yunjaeh@stanford.edu 


echo "Running [your app] with: $cmd on $SLURM_JOB_NODELIST in directory "`pwd`
date

# Working directory
# /scratch/07279/tg865790/CharLES_scaling
cd $SCRATCH
cd ./CharLES_scaling/128/

nNodes=128
nCores=$((48*$nNodes))

fInput='01_charles.in'
fLog='log.charles1'

mpiexec -n $nCores ../charles.exe -i $fInput >  $fLog



