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

from netpyne import sim
import random

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
def pruneSynapses(cell, conn_index, probability, pruning_range):
    # Get the section
    sec = cell.secs[conn['sec']]

    # Get the 3D points of the section
    points = sec['geom']['pt3d']

    y1 = points[0][1]
    y2 = points[1][1]

    syn_rel = conn['loc'] * (y2-y1)

    # Get the position of the cell within the network
    y_cell = cell.tags['y']

    # Calculate the 3D coordinates relative to the network
    y_net = syn_rel + y_cell

    if pruning_range[1] > y_net > pruning_range[0]:
        if random.random() < probability:
            print(len(cell.conns))
            cell.conns.remove(conn)
            print("Conn Removed")
            print(len(cell.conns))

for cell in sim.net.cells:
    if cell.tags['pop'] in cfg.allCorticalPops:
        for conn in cell.conns:
            if conn['synMech'] == 'AMPA' or 'NMDA':
                pruneSynapses(cell, conn, probability= 0.20, pruning_range=deepL3_yRange)

sim.net.addStims() 							# add network stimulation
sim.setupRecording()              			# setup variables to record for each cell (spikes, V traces, etc)
sim.runSim()                      			# run parallel Neuron simulation
sim.gatherData()                  			# gather spiking data and cell info from each node

# distributed saving (to avoid errors with large output data)
sim.saveDataInNodes()
sim.gatherDataFromFiles()

sim.saveData()

sim.analysis.plotData()         			# plot spike raster etc