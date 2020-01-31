function EEG = import_csv(datafname, locsfname, weightsfname)
    data = csvread(datafname, 1, 1).';
    EEG = pop_importdata('data', data, 'nbchan', 32, 'srate', 512);
    EEG.chanlocs = readlocs(locsfname, 'importmode', 'eeglab', 'filetype', 'sfp');
    EEG.icawinv = csvread(weightsfname).';
    pop_selectcomps(EEG, 1:32);
end