#!/bin/bash -l
#SBATCH -J FLARES-pysphv #Give it something meaningful.
#SBATCH -o logs/output_flythrough.%J.out
#SBATCH -e logs/error_flythrough.%J.err
#SBATCH -p cosma6 #or some other partition, e.g. cosma, cosma6, etc.
#SBATCH -A dp004
# #SBATCH --exclusive
#SBATCH -t 00:30:00
# #SBATCH --mail-type=END
# #SBATCH --mail-user=wjr21@sussex.ac.uk #PLEASE PUT YOUR EMAIL ADDRESS HERE (without the <>)
#SBATCH --array=0-36
#SBATCH --ntasks 1 # The number of cores you need...
#SBATCH --cpus-per-task=8

# Run the job from the following directory - change this to point to your own personal space on /lustre
# cd /cosma7/data/dp004/dc-rope1/FLARES/flares

module purge
module load pythonconda3/4.5.4

source activate eagle

# dark matter
# python rotating_sphere.py $SLURM_ARRAY_TASK_ID 1 

# gas
# python rotating_sphere.py $SLURM_ARRAY_TASK_ID 0

# stars
python rotating_sphere.py $SLURM_ARRAY_TASK_ID 4


echo "Job done, info follows..."
sacct -j $SLURM_JOBID --format=JobID,JobName,Partition,MaxRSS,Elapsed,ExitCode
exit


