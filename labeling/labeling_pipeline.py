import os
from os import listdir
from os.path import isfile, join
import matlab

from labeling.process_eeg import process_eeg


def mkdirp(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


mkdirp("out")
mkdirp("out/plots")

csv_files = [f for f in listdir("./csv/") if isfile(join("./csv/", f))]
data_filename = csv_files[0].replace("_data.csv", "")
data_filename, locations_filename, ica_weights_filename, plot_filenames = \
    process_eeg("csv/", "out/", "plots/", data_filename)

# eng = matlab.engine.start_matlab()
# run matlab
# append labeling file
