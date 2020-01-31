function EEG = make_icalabels(EEG, filename)
    EEG = iclabel(EEG)
    my_label = 1:EEG.nbchan
    for i = 1:EEG.nbchan 
      max_value = max(EEG.etc.ic_classification.ICLabel.classifications(i, :))
      for j = 1:7
        if EEG.etc.ic_classification.ICLabel.classifications(i, j) == max_value
          my_label(i) = j
        end
      end
    end
    %file_with_labels = fopen('../subj1_series1_labels.csv','w');
    file_with_labels = fopen(filename,'w');
    fprintf(file_with_labels, "%d \t", my_label);
    fclose(file_with_labels);
end
