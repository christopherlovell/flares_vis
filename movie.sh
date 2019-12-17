#!/bin/sh
#SBATCH --job-name=geagle0000_vis   # Job name
#SBATCH -A dp004
#SBATCH -p cosma6
#SBATCH --nodes=1                   # Use one node
#SBATCH --ntasks=1                  # Run a single task
#SBATCH --time=00:25:00             # Time limit hrs:min:sec
#SBATCH --output=logs/array_%A-%a.out    # Standard output and error log
#SBATCH --array=1-14               # Array range


# #SBATCH --mem-per-cpu=1gb           # Memory per processor
 
# This is an example script that combines array tasks with
# bash loops to process many short runs. Array jobs are convenient
# for running lots of tasks, but if each task is short, they
# quickly become inefficient, taking more time to schedule than
# they spend doing any work and bogging down the scheduler for
# all users.
 
pwd; hostname; date

## load conda environment
source activate eagle3
 
#Set the number of runs that each SLURM task should do
PER_TASK=10
 
# Calculate the starting and ending values for this task based
# on the SLURM task and the number of runs per task.
START_NUM=$(( ($SLURM_ARRAY_TASK_ID - 1) * $PER_TASK))
END_NUM=$(( $SLURM_ARRAY_TASK_ID * $PER_TASK ))
 
# Print the task and run range
echo This is task $SLURM_ARRAY_TASK_ID, which will do runs $START_NUM to $END_NUM

python gas_time_movie.py $SLURM_ARRAY_TASK_ID
# python stars_rotate_movie.py $START_NUM $END_NUM 

# # Run the loop of runs for this task.
# for (( run=$START_NUM; run<=END_NUM; run++ )); do
#   echo This is SLURM task $SLURM_ARRAY_TASK_ID, run number $run
#   #Do your stuff here
# 
# done
 
date
