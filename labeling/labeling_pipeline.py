import os
from os import listdir
from os.path import isfile, join

from labeling.process_eeg import process_eeg


def mkdirp(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


mkdirp("out")
mkdirp("out/plots")

# create channels locations, get ica weights and scalp plots
csv_files = [f for f in listdir("./csv/") if isfile(join("./csv/", f))]
subj_name = csv_files[0].replace("_data.csv", "")
subj_name = "subj1_series1"
data_filename, locations_filename, ica_weights_filename, plot_filenames = \
    process_eeg("csv/", "out/", "plots/", subj_name)

# run matlab labeling script
os.system(
    "matlab /minimize /nosplash /nodesktop /r \"addpath('%EEGLAB_DIR%');eeglab;label_components('csv/{0}_data.csv', "
    "'out/{0}_locations.csv', 'out/{0}_ica_weights.csv', 'out/{0}_labels.csv');exit;\"".format(
        subj_name))

# append labeling file
