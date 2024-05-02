"""
init.py

Starting script to run NetPyNE-based A1 model.


Usage:
    python init.py # Run simulation, optionally plot a raster


MPI usage:
    mpiexec -n 4 nrniv -python -mpi init.py


Contributors: ericaygriffith@gmail.com, salvadordura@gmail.com
"""
from datetime import datetime
import matplotlib; matplotlib.use('Agg')  # to avoid graphics error in servers
from datetime import datetime
from netpyne import sim
import random
from simTools import editNet

cfg, netParams = sim.readCmdLineArgs(simConfigDefault='cfg.py', netParamsDefault='netParams.py')

ThalamicCoreLambda = 5.0

# sim.createSimulateAnalyze(netParams, cfg)

sim.initialize(
    simConfig = cfg,
    netParams = netParams)  				# create network object and set cfg and net params
sim.net.createPops()               			# instantiate network populations
sim.net.createCells()              			# instantiate network cells based on defined populations

def setdminID (sim, lpop):
  # setup min,max ID and dnumc for each population in lpop
  alltags = sim._gatherAllCellTags() #gather cell tags; see https://github.com/Neurosim-lab/netpyne/blob/development/netpyne/sim/gather.py
  dGIDs = {pop:[] for pop in lpop}
  for tinds in range(len(alltags)):
    if alltags[tinds]['pop'] in lpop:
      dGIDs[alltags[tinds]['pop']].append(tinds)
  sim.simData['dminID'] = {pop:np.amin(dGIDs[pop]) for pop in lpop if len(dGIDs[pop])>0}
  sim.simData['dmaxID'] = {pop:np.amax(dGIDs[pop]) for pop in lpop if len(dGIDs[pop])>0}
  sim.simData['dnumc'] = {pop:np.amax(dGIDs[pop])-np.amin(dGIDs[pop]) for pop in lpop if len(dGIDs[pop])>0}

setdminID(sim, cfg.allpops)

def setCellGridLocations (pop, sz, scale, checkcf=True):
  # set the cell positions on a square grid, assumes number of cells fits the square size (sz)
  if pop not in sim.net.pops: return
  offset = sim.simData['dminID'][pop]
  for c in sim.net.cells:
    if c.gid in sim.net.pops[pop].cellGids:
      if checkcf:
        cf = cochlearCenterFreqs[c.gid-offset]
        if cf >= cfg.cochThalFreqRange[0] and cf <= cfg.cochThalFreqRange[1]:
          c.tags['x'] = cellx = ((c.gid-offset)/sz) * scale
          c.tags['xnorm'] = cellx / netParams.sizeX # make sure these values consistent
        else:
          c.tags['x'] = cellx = -100000  # put it outside range for core
          c.tags['xnorm'] = cellx / netParams.sizeX # make sure these values consistent
      else:
        c.tags['x'] = cellx = ((c.gid-offset)/sz) * scale
        c.tags['xnorm'] = cellx / netParams.sizeX # make sure these values consistent
      c.updateShape()

setCellGridLocations('cochlea', netParams.popParams['cochlea']['numCells'],
                     netParams.popParams['cochlea']['sizeX'])

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