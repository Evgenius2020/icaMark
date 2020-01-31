import numpy as np
import pandas as pd
import mne
from mne import create_info
from mne.channels import read_montage
from mne.io import RawArray
import csv
from PIL import Image

import matplotlib
import matplotlib.pyplot as plt

plt.ioff()
matplotlib.rcParams.update({'figure.max_open_warning': 0})


def load_raw_eeg(filename):
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


def process_eeg(source_dir, out_dir, plots_dir, subj_name):
    data_filename = source_dir + subj_name + "_data.csv"
    locations_filename = out_dir + subj_name + "_locations.csv"
    ica_weights_filename = out_dir + subj_name + "_ica_weights.csv"
    plot_filenames = []

    raw, ch_locations = load_raw_eeg(data_filename)
    writecsv(ch_locations, locations_filename)

    ch_number = len(raw.ch_names)

    ica = mne.preprocessing.ICA(n_components=ch_number)
    ica.fit(raw)

    for i in range(ch_number):
        plot_to_save = ica.plot_components(i, show=False)
        plot_filename = out_dir + plots_dir + subj_name + ("_%d.png" % (i + 1))
        plot_filenames.append(plot_filename)
        plot_to_save.savefig(plot_filename)

        # cropping images
        plot_to_save = Image.open(plot_filename)
        plot_to_save = plot_to_save.crop((25, 56, 205, 232))
        plot_to_save.save(plot_filename)

    weights_map = get_ica_weights_map(ica)
    np.savetxt(ica_weights_filename, weights_map, delimiter=', ')

    plt.close('all')

    return data_filename, locations_filename, ica_weights_filename, plot_filenames
