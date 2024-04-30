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


batch = 'ASSR_tune_0228' #Name of batch for fig saving

# Load sim EEG data
base_dir = '/Users/scottmcelroy/A1_scz/A1_sim_data/'+ batch +'/'
for file in os.listdir(base_dir):
    if file.endswith('.pkl'):
        sim.initialize()
        all = sim.loadAll(os.path.join(base_dir, file))
        fname = file[0:12] # Create filename (can change to whatever)
        if not os.path.exists('/Users/scottmcelroy/A1_scz/A1_figs/SIMfigs/' + batch):
            os.mkdir('/Users/scottmcelroy/A1_scz/A1_figs/SIMfigs/' + batch)  # Create Figure directory if one doesn't already exist
        stim_data, stim_window = simTools.calculateEEG(sim, stimOn=4000, end=5000) # Generate EEG data from dipole sums
        filtered_data = simTools.filterEEG(stim_data, 2, 80, 20000, 2) # Filter (if needed)
        # t = np.arange(-200, 1000, 0.05)
        # simTools.plotERP(filtered_data, t, fname, batch) # Create ERP plot of time window specified
        simTools.plot_spectrogram(data=filtered_data, time=stim_window, fname=fname, batch=batch) # Use filter only if low frq power skews image
        # simTools.plot_PSD(data=filtered_data, time=stim_window, fname=fname, batch=batch) #PSD should stay unfiltered ideally
        # # Raster code used for the grant (looks better than base plot raster)
        # sim.analysis.plotRaster(timeRange=(4000,5000), orderInverse=True, markerSize=1000, figSize = (27,23),
        # saveFig = '/Users/scottmcelroy/A1_scz/A1_figs/SIMfigs/'+batch+ '/'+fname+ 'Raster.png')


        ################## Scrap for resampling if needed later ##################################################
        # num_samples = len(stim_data)
        # new_num_samples = int(num_samples * 1000/ 20000)
        # resampled_data = signal.resample(stim_data, new_num_samples)