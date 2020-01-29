function eeg = import_csv(filename)
    data = csvread(filename, 1, 1).';
    eeg = pop_importdata('data', data, 'nbchan', 32, 'srate', 512);
end

%eegplot(eeg.data)