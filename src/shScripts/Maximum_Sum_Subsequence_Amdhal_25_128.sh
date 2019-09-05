#!/bin/sh
#SBATCH --partition=general-compute
#SBATCH --qos=general-compute
#SBATCH --time=00:03:00
#SBATCH --nodes=128
#SBATCH --ntasks-per-node=1
#SBATCH --mem=5000
#SBATCH --job-name="Amdhal_25_128"
#SBATCH --output=Amdhal_25_128-%j.out
#SBATCH --mail-user=srpothir@buffalo.edu
#SBATCH --mail-type=END
#SBATCH --constraint=IB&CPU-E5645
#SBATCH --exclusive


echo "SLURM_JOBID="$SLURM_JOBID
echo "SLURM_JOB_NODELIST="$SLURM_JOB_NODELIST
echo "SLURM_NNODES="$SLURM_NNODES
echo "SLURMTMPDIR="$SLURMTMPDIR

echo "working directory = "$SLURM_SUBMIT_DIR

ulimit -s unlimited

module load mpi4py

export I_MPI_PMI_LIBRARY=/usr/lib64/libpmi.so

module list
which python

echo "Launch job"
srun -n 128 python AmdhalsTest.py 128 25000000


#
echo "All Done!"

