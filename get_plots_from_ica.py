import os
import numpy as np
import pandas as pd
import mne
from mne import create_info
from mne.channels import read_montage
from mne.io import RawArray

from PIL import Image

import matplotlib

matplotlib.rcParams.update({'figure.max_open_warning': 0})
matplotlib.use('Agg')


def create_mne_raw_object(filename):
    data = pd.read_csv(filename)
    ch_names = list(data.columns[1:])

    data = 1e-7 * np.array(data[ch_names]).T
    ch_types = ['eeg'] * len(ch_names)
    montage = read_montage('standard_1005', ch_names)

    info = create_info(ch_names, sfreq=512, ch_types=ch_types, montage=montage)
    return RawArray(data, info, verbose=False)


def mkdirp(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def get_plots_from_ica(csv_path="csv/", csv_filename="subj1_series1_data.csv", png_path="plots/",
                       ica_path="icas/"):
    csv_filename_ = csv_path + csv_filename
    raw = create_mne_raw_object(csv_filename_)
    ch_number = len(raw.ch_names)

    mkdirp(png_path)
    mkdirp(ica_path)
    png_str = csv_filename[:-8]

    ica = mne.preprocessing.ICA(n_components=ch_number, random_state=97, max_iter=800)
    ica.fit(raw)

    for i in range(ch_number):
        plot_to_save = ica.plot_components(i, show=False)
        plot_to_save.savefig(png_path + png_str + ("ica_%d.png" % i))

        # cropping images
        plot_to_save = Image.open(png_path + png_str + ("ica_%d.png" % i))
        plot_to_save = plot_to_save.crop((25, 56, 205, 232))
        plot_to_save.save(png_path + png_str + ("ica_%d.png" % i))

    ica.save(ica_path + png_str + "-ica.fif")


get_plots_from_ica()
