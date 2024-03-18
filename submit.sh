#!/bin/bash
#$ -cwd
#$ -N Scz_cfgTune
#$ -q cpu.q
#$ -pe smp 60
#$ -l h_vmem=256G
#$ -l h_rt=1:15:00
#$ -o /ddn/smcelroy97/SczA1model/data/singleSim.out
#$ -e /ddn/smcelroy97/SczA1model/data/singleSim.err

source ~/.bashrc
mpiexec -n $NSLOTS -hosts $(hostname) nrniv -python -mpi init.py