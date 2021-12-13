#!/bin/bash 
#SBATCH -e mergeData.err 
#SBATCH -o mergeData.out 
#SBATCH -J mergeData
#SBATCH -N 1
#SBATCH -t 120:00:00
#SBATCH --ntasks-per-node=2
#SBATCH -p compute

conda activate geo_env
landcover_percent.py

