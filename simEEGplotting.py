from netpyne import sim
from simTools import simTools
import os
import numpy as np
from scipy import signal
# snippet of code to import matplotlib and dynamically switch backend to "MacOSX" for plotting
from pydoc import source_synopsis
import sys
from netpyne.support.morlet import MorletSpec, index2ms
import matplotlib
matplotlib.use("MacOSX")
from matplotlib import pyplot as plt
from lfpykit.eegmegcalc import NYHeadModel


batch = 'ASSR_grid_0310' #Name of batch for fig saving

# Load sim EEG data
base_dir = '/Users/scottmcelroy/A1_scz/A1_sim_data/'+ batch +'/'
for file in os.listdir(base_dir):
    if file.endswith('.pkl'):
        sim.initialize()
        all = sim.loadAll(os.path.join(base_dir, file))
        fname = file[0:18]+'TEST' # Create filename (can change to whatever)
        # stim_data, stim_window = simTools.calculateEEG(sim, stimOn=2800, end=4000) # Generate EEG data from dipole sums
        # filtered_data = simTools.filterEEG(stim_data, 3, 80, 20000, 2) # Filter (if needed)
        # simTools.plotERP(filtered_data, stim_window, fname, batch) # Create ERP plot of time window specified
        # simTools.plot_spectrogram(data=filtered_data, time=stim_window, fname=fname, batch=batch) # Use filter only if low frq power skews image
        # simTools.plot_PSD(data=stim_data, time=stim_window, fname=fname, batch=batch) #PSD should stay unfiltered ideally
        # # Raster code used for the grant (looks better than base plot raster)
        # sim.analysis.plotRaster(timeRange=(4000,5000), orderInverse=True, markerSize=1000, figSize = (27,23),
        # saveFig = '/Users/scottmcelroy/A1_scz/A1_figs/SIMfigs/'+batch+ '/'+fname+ 'Raster.png')


        ################## Scrap for resampling if needed later ##################################################
        # num_samples = len(stim_data)
        # new_num_samples = int(num_samples * 1000/ 20000)
        # resampled_data = signal.resample(stim_data, new_num_samples)