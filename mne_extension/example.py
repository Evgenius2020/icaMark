import mne

from IC_auto_exclude import ic_auto_exclude

ica = mne.preprocessing.read_ica('example_ica.fif')
ica.exclude = ic_auto_exclude(ica, verbose=True)
print(ica.exclude)
# ica.plot_components(range(0, 32))
