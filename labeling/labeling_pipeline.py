import csv
import os
from os import listdir
from os.path import isfile, join
from time import sleep
import numpy as np
import warnings

from labeling.process_eeg import process_eeg

warnings.filterwarnings("ignore", category=DeprecationWarning)


def mkdirp(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


source_dir = "csv/"
out_dir = "out/"
temp_dir = out_dir + "temp/"
plots_dir = out_dir + "plots/"
all_labels_filename = out_dir + "all_labels.csv"

mkdirp(out_dir)
mkdirp(plots_dir)
mkdirp(temp_dir)

subj_files = []
csv_files = [f for f in listdir("./csv/") if isfile(join("./csv/", f))]
for csv_file in csv_files:
    subj_name = csv_file.replace("_data.csv", "")
    data_filename = source_dir + subj_name + "_data.csv"
    locations_filename = temp_dir + subj_name + "_locations.csv"
    ica_weights_filename = temp_dir + subj_name + "_ica_weights.csv"
    plot_filenames = [plots_dir + subj_name + ("_%d.png" % (i + 1)) for i in range(32)]
    labels_filename = temp_dir + subj_name + "_labels.csv"

    # create channels locations, get ica weights and scalp plots
    process_eeg(data_filename, locations_filename, ica_weights_filename, plot_filenames)

    # run matlab labeling script, async
    os.system(
        "matlab /minimize /nosplash /nodesktop /r \"addpath('%EEGLAB_DIR%');eeglab;"
        "label_components('{0}','{1}','{2}','{3}');exit;\"".format(
            data_filename, locations_filename, ica_weights_filename, labels_filename))

    subj_files.append([labels_filename] + plot_filenames)

# wait all matlab labeling executions
sleep(60 * 2)

# create labeling file
with open(all_labels_filename, 'w', newline='') as all_labels_file:
    csv_writer = csv.writer(all_labels_file, delimiter=',')
    for subj_files_entry in subj_files:
        labels_filename = subj_files_entry[0]
        labels = np.genfromtxt(labels_filename, delimiter=',')
        for i in range(len(labels)):
            csv_writer.writerow([subj_files_entry[i + 1], labels[i]])
