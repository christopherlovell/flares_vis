#!/bin/bash
#SBATCH -A dp004
#SBATCH -p cosma6
#SBATCH -t 0-3:00
#SBATCH --ntasks 1
#SBATCH -o std_output.%J
#SBATCH -e std_error.%J

module load pythonconda3/4.5.4
source activate eagle
python parent.py >> parent_out.txt 

echo "Job done, info follows..."
sacct -j $SLURM_JOBID --format=JobID,JobName,Partition,MaxRSS,Elapsed,ExitCode
exit
