#!/bin/bash -l
#SBATCH -J FLARES-pysphv #Give it something meaningful.
#SBATCH -o logs/output_flythrough.%J.out
#SBATCH -e logs/error_flythrough.%J.err
#SBATCH -p cosma7 #or some other partition, e.g. cosma, cosma6, etc.
#SBATCH -A dp004
#SBATCH -t 001:00:00
#SBATCH --array=0-35
#SBATCH --ntasks 1 # The number of cores you need...
#SBATCH --cpus-per-task=8

module purge
module load pythonconda3/2020-02
conda activate eagle3p9

python dm_rotate_movie.py $SLURM_ARRAY_TASK_ID 36

echo "Job done, info follows..."
sacct -j $SLURM_JOBID --format=JobID,JobName,Partition,MaxRSS,Elapsed,ExitCode
exit


