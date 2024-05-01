"""
init.py

Starting script to run NetPyNE-based A1 model.


Usage:
    python init.py # Run simulation, optionally plot a raster


MPI usage:
    mpiexec -n 4 nrniv -python -mpi init.py


Contributors: ericaygriffith@gmail.com, salvadordura@gmail.com
"""

import matplotlib; matplotlib.use('Agg')  # to avoid graphics error in servers
from datetime import datetime
from netpyne import sim
import random
from simTools import editNet

cfg, netParams = sim.readCmdLineArgs(simConfigDefault='cfg.py', netParamsDefault='netParams.py')

# sim.createSimulateAnalyze(netParams, cfg)

sim.initialize(
    simConfig = cfg,
    netParams = netParams)  				# create network object and set cfg and net params
sim.net.createPops()               			# instantiate network populations
sim.net.createCells()              			# instantiate network cells based on defined populations
sim.net.connectCells()                      # create connections between cells based on params

deepL3_yRangeNorm = [0.3433333333333333, 0.475]
deepL3_yRange     = [i * cfg.sizeY for i in deepL3_yRangeNorm]

for cell in sim.net.cells:
    if cell.tags['pop'] in cfg.CorticalEPops:
        for conn in cell.conns:
            if conn['synMech'] == 'AMPA' or 'NMDA':
                editNet.pruneSynapses(cell, conn, probability= 0.20, pruning_range=deepL3_yRange)



sim.net.addStims() 							# add network stimulation
sim.setupRecording()              			# setup variables to record for each cell (spikes, V traces, etc)
sim.runSim()                      			# run parallel Neuron simulation
sim.gatherData()                  			# gather spiking data and cell info from each node

# distributed saving (to avoid errors with large output data)
sim.saveDataInNodes()
sim.gatherDataFromFiles()

sim.saveData()

sim.analysis.plotData()         			# plot spike raster etc

now = datetime.now()

current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)