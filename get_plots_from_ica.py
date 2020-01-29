import numpy as np
import pandas as pd
import mne
from mne import create_info
from mne.channels import read_montage
from mne.io import RawArray

import matplotlib
#next line supresses warnings
matplotlib.rcParams.update({'figure.max_open_warning': 0})
#matplotlib.use('Agg') 

def create_mne_raw_object(filename):
    data = pd.read_csv(filename)
    ch_names = list(data.columns[1:])
    montage = read_montage('standard_1005', ch_names)
    
    ev_filename = filename.replace('_data', '_events')
    
    events = pd.read_csv(ev_filename)
    events_names = events.columns[1:]
    events_data = np.array(events[events_names]).T
    
    data = np.concatenate((1e-7 * np.array(data[ch_names]).T, events_data))
    
    ch_type = ['eeg'] * len(ch_names) + ['stim'] * 6
    
    ch_names.extend(events_names)
    info = create_info(ch_names, sfreq=500.0, ch_types=ch_type, montage=montage)
    
    return RawArray(data, info, verbose=False)

def get_plots_from_ica( csv_path="../", csv_filename="subj1_series1_data.csv", png_path="../plots/"):
    csv_filename_ = csv_path+csv_filename
    raw = create_mne_raw_object(csv_filename_)
    data = pd.read_csv(csv_filename_)
    ch_names = list(data.columns[1:])
    my_n = len(ch_names)

    ica = mne.preprocessing.ICA(n_components=my_n, random_state=97, max_iter=800)
    ica.fit(raw)
    
    png_str = csv_filename[:-8]
    
    for i in range(0, my_n):
        plot_to_save = ica.plot_components(i, show=False)
        plot_to_save.savefig(png_path+csv_filename+("ica_%d.png"%i))

    return

get_plots_from_ica()