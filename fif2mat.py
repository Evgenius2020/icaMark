import mne
from scipy import io
fif_filepath="rudych_28_05_2018_tomoseg_3raw.fif"
raw = mne.io.Raw(fif_filepath, preload=True, verbose=True)
data, time = raw[:, :]
data = data * 1000000
io.savemat(fif_filepath[:-5], dict(data=data), oned_as='row')

