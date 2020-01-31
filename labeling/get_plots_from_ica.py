import os
import numpy as np
import pandas as pd
import mne
from mne import create_info
from mne.channels import read_montage
from mne.io import RawArray
import csv

from PIL import Image

import matplotlib

matplotlib.rcParams.update({'figure.max_open_warning': 0})
matplotlib.use('Agg')


def load_csv(filename):
    data = pd.read_csv(filename)
    ch_names = list(data.columns[1:])

    data = 1e-7 * np.array(data[ch_names]).T
    ch_types = ['eeg'] * len(ch_names)
    montage = read_montage('standard_1020', ch_names)

    ch_locations = []
    for i in range(len(ch_names)):
        ch_name = ch_names[i]
        ch_location = montage.pos[i]
        ch_locations.append([ch_name, ch_location[0], ch_location[1], ch_location[2]])

    info = create_info(ch_names, sfreq=512, ch_types=ch_types, montage=montage)

    return RawArray(data, info, verbose=False), ch_locations


def mkdirp(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def get_ica_weights_map(ica):
    components = list(range(ica.n_components_))
    maps = np.dot(ica.mixing_matrix_[:, components].T,
                  ica.pca_components_[:ica.n_components_])
    return maps


def writecsv(data, filename):
    with open(filename, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter='\t')
        for data_row in data:
            writer.writerow(data_row)


def get_plots_from_ica(csv_path="csv/", filename="subj1_series1", png_path="plots/",
                       ica_path="icas/"):
    raw, ch_locations = load_csv(csv_path + filename + "_data.csv")
    writecsv(ch_locations, csv_path + filename + "_locations.csv")

    ch_number = len(raw.ch_names)

    mkdirp(png_path)
    mkdirp(ica_path)

    ica = mne.preprocessing.ICA(n_components=ch_number, random_state=97, max_iter=800)
    ica.fit(raw)

    for i in range(ch_number):
        plot_to_save = ica.plot_components(i, show=False)
        png_filename = png_path + filename + ("_ica_%d.png" % (i + 1))
        plot_to_save.savefig(png_filename)

        # cropping images
        plot_to_save = Image.open(png_filename)
        plot_to_save = plot_to_save.crop((25, 56, 205, 232))
        plot_to_save.save(png_filename)

    weights_map = get_ica_weights_map(ica)
    np.savetxt(ica_path + filename + "_weights.csv", weights_map, delimiter=', ')
    ica.save(ica_path + filename + "_ica.fif")


get_plots_from_ica()
