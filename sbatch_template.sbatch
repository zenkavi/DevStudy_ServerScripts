#!/bin/bash

#SBATCH -p normal         # Queue name
#SBATCH -N 1              # Total number of nodes requested
#SBATCH -n 24             # Required, but not sure it has an effect
#SBATCH -t 10:00:00       # Run time (hh:mm:ss) - 1.5 hours
#SBATCH -J myjob          # name of the job (appears in queue under NAME)
#SBATCH --mail-user=zenkavi@stanford.edu
#SBATCH --mail-type=all

# Command or script to execute
python /corral-repl/utexas/poldracklab/users/zenkavi/dev_study/scripts/convert_dicoms_to_niftis.py
