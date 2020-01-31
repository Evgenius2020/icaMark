function labels = label_components(datafname, locsfname, weightsfname)
    data = csvread(datafname, 1, 1).';
    EEG = pop_importdata('data', data, 'nbchan', 32, 'srate', 512);
    EEG.chanlocs = readlocs(locsfname, 'importmode', 'eeglab', 'filetype', 'sfp');
    EEG.nbchan = 32;
    EEG.icachansind = 1:32;
    EEG.icawinv = csvread(weightsfname).';
    
    % needs to be
    EEG.icaweights = eye(32);
    EEG.icasphere = eye(32);
    
    EEG = iclabel(EEG);
    labels = zeros(1,32);
    for i = 1:EEG.nbchan;
        brain_prob = EEG.etc.ic_classification.ICLabel.classifications(i, 1);
        other_prob = EEG.etc.ic_classification.ICLabel.classifications(i, 7);
        if brain_prob + other_prob > 0.8          
          labels(i) = 1;
        end
    end
end