#!/bin/bash
#$ -cwd
#$ -N Scz_cfgTune
#$ -q cpu.q
#$ -pe smp 50
#$ -l h_vmem=512G
#$ -l h_rt=2:00:00
#$ -o /ddn/smcelroy97/SczA1model/data/singleSim.out
#$ -e /ddn/smcelroy97/SczA1model/data/singleSim.err

source ~/.bashrc
mpiexec -n $NSLOTS -hosts $(hostname) nrniv -python -mpi init.py