#!/bin/bash
#SBATCH -A dp004
#SBATCH -p cosma6
#SBATCH -t 0-3:00
#SBATCH --ntasks 4
#SBATCH -o std_output.%J
#SBATCH -e std_error.%J


# #SBATCH --cpus-per-task=1
# #SBATCH --ntasks-per-node=16

module load pythonconda3/4.5.4
source activate eagle
python parent.py 

