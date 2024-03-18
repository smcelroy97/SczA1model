from lfpykit.eegmegcalc import NYHeadModel
from scipy import signal
from scipy.signal import butter, filtfilt
from netpyne.support.morlet import MorletSpec, index2ms
import os
import numpy as np
import matplotlib
matplotlib.use("MacOSX")
from    matplotlib  import  pyplot  as plt



class simTools:
    def calculateEEG(sim, stimOn, end):
        # Load 3D head model for EEG
        nyhead = NYHeadModel(nyhead_file=os.getenv('NP_LFPYKIT_HEAD_FILE', None))
        nyhead.set_dipole_pos('parietal_lobe')
        M = nyhead.get_transformation_matrix()

        # Adjsut time for stimulation window
        timeRange = [stimOn, end]
        timeSteps = [int(timeRange[0] / 0.05), int(timeRange[1] / 0.05)]
        t = np.arange(timeRange[0], timeRange[1], 0.05)

        # gather dipole data
        p = sim.allSimData['dipoleSum']
        p = np.array(p).T
        p = p[:, timeSteps[0]: timeSteps[1]]
        p = nyhead.rotate_dipole_to_surface_normal(p)

        # Calculate EEG
        eeg = M @ p * 1e9
        goodchan = eeg[38, :]

        onset = int(stimOn / 0.05)
        offset = int(end / 0.05)
        return goodchan, t

    def filterEEG(EEG, lowcut, highcut, fs, order):
        b, a = butter(order, [lowcut, highcut], btype='band', fs=fs)
        filtered_signal = filtfilt(b, a, EEG)
        return filtered_signal
    def processRaster(spkTimes, spkGids):
        raster_dict = {'tone': {}}
        for event in raster_dict.keys(): raster_dict[event].update({'spkTimes': [], 'spkGids': []})
        for spkt_ind, spkt in enumerate(spkTimes):
            if (1500 <= (spkt) <= 5500):
                event = 'tone'
            raster_dict[event]['spkTimes'].append(spkTimes[spkt_ind])
            raster_dict[event]['spkGids'].append(spkGids[spkt_ind])
        return raster_dict

    def getPopSpks(spkTimes, spkGids, popGids, window):
        spk_gids = []
        spk_times = []
        for spk_gid_ind, spk_gid in enumerate(spkGids):
            if (spk_gid in popGids) and (window[0]<= (spkTimes[spk_gid_ind])<= window[1]):
                print(spk_gid)
                spk_gids.append(spkGids[spk_gid_ind])
                spk_times.append(spkTimes[spk_gid_ind])
        return spk_gids, spk_times
    def plotERP(data, time, fname, batch, figsize = (30,20)):
        plt.figure(figsize=figsize)
        plt.plot(time,data/1000, linewidth = 4)
        plt.tick_params(labelsize=50)
        plt.xlabel('Time (s)', fontsize = 65)
        plt.ylabel('uV', fontsize = 65)
        if not os.path.exists('/Users/scottmcelroy/A1_scz/A1_figs/SIMfigs/' + batch):
            os.mkdir('/Users/scottmcelroy/A1_scz/A1_figs/SIMfigs/' + batch)
        plt.savefig('/Users/scottmcelroy/A1_scz/A1_figs/SIMfigs/' + batch + '/' + fname + 'ERP.png')

    def plot_spectrogram(data, time, fname, batch, figsize = (20,20)):
        # sampling frequency
        fs = int(1000.0 / 0.05)

        # Define freqs you care about
        minFreq = 1
        maxFreq = 60

        # Perform Morlet transform
        freqList = None
        spec = (MorletSpec(data, fs, freqmin=minFreq, freqmax=maxFreq, freqstep=1, lfreq=freqList))

        # Min and mox for the color of normalized power
        vmin = spec.TFR.min()
        vmax = spec.TFR.max()

        T = time  # Time
        F = spec.f  # Define frequencies
        S = spec.TFR  # Spectral data for spectrogram
        signal = 10 * (np.log10(np.mean(S, 1)))  # Use this for PSD plotting

        # Spectrogram plot params
        plt.figure(figsize=figsize)
        plt.xlabel('Time (s)')
        plt.ylabel('Frequency (Hz)')
        plt.imshow(S, extent=(np.amin(T), np.amax(T), np.amin(F), np.amax(F)),
                   origin='lower',
                   interpolation='None',
                   aspect='auto',
                   vmin=vmin,
                   vmax=vmax,
                   cmap=plt.get_cmap('viridis')
                   )
        if not os.path.exists('/Users/scottmcelroy/A1_scz/A1_figs/SIMfigs/' + batch):
            os.mkdir('/Users/scottmcelroy/A1_scz/A1_figs/SIMfigs/' + batch)
        plt.savefig('/Users/scottmcelroy/A1_scz/A1_figs/SIMfigs/' + batch + '/' + fname + 'spect.png')






