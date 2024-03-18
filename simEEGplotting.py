from netpyne import sim
from simTools import simTools
import os
import numpy as np
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
        sim.load(os.path.join(base_dir, file), 'rb', instantiateStims=False, instantiateConns=False)
        fname = file[0:18]
        stim_data, stim_window = simTools.calculateEEG(sim, stimOn=4000, end=5000)
        filtered_data = simTools.filterEEG(stim_data, 1, 80, 1000, 4)
        simTools.plotERP(filtered_data, stim_window, fname, batch)
        simTools.plot_spectrogram(data=filtered_data, time=stim_window, fname=fname, batch=batch)


# Line ran for grant fig raster
# sim.analysis.plotRaster(timeRange=(4000,5000), orderInverse=True, markerSize=1000, figSize = (27,23),
# saveFig = '/Users/scottmcelroy/A1_scz/A1_figs/0228_RasterF')