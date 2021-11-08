#!/bin/bash 
#SBATCH -e stats.err 
#SBATCH -o stats.out 
#SBATCH -J stats
#SBATCH -N 1
#SBATCH -t 120:00:00
#SBATCH --ntasks-per-node=2
#SBATCH -p compute

python main.py
