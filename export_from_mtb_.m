%PTH = strcat('D:\_004_ica_matrix\',strsplit(ALLEEG(1).filename,'.'))
%mkdir(PTH{1})

%csvwrite(strcat(PTH{1},'/icawinw.csv'), ALLEEG(1).icawinv)
%csvwrite(strcat(PTH{1},'/icasphere.csv'), ALLEEG(1).icasphere)
%csvwrite(strcat(PTH{1},'/icaweights.csv'), ALLEEG(1).icaweights)
%csvwrite(strcat(PTH{1},'/data.csv'), ALLEEG(1).data)


%list = dir('D:\samenko\diplom\EEG data\004')

%files = dir(fullfile('D:\samenko\diplom\EEG data\004', '*.set'));
% Display the names
%files(1).name

% eeg_file = pop_loadset('0040573_1_AOB_before_ICA.set','D:\samenko\diplom\EEG data\004\')

%f_name = '0060037_1_OBP_ICA.set';
%fold = strcat ('D:\eeg_D\006\', f_name);    %folder to look for EEG data
%load(fold)
%pop_loadset(fold)

clear all;

pair_names = [
 "0070371_1_OBP_ICA.set", "0070371_1_OBP_ICA_all.set";
 "0070371_2_OBP_ICA.set", "0070371_2_OBP_ICA_all.set";
 "0070372_1_OBF_ICA.set", "0070372_1_OBF_ICA_all.set";
 "0070372_1_OBP_ICA.set", "0070372_1_OBP_ICA_all.set";
 "0070381_1_OBF_ICA.set", "0070381_1_OBF_ICA_all.set";
 "0070381_1_OBP_ICA.set", "0070381_1_OBP_ICA_all.set";
 "0070381_2_OBP_ICA.set", "0070381_2_OBP_ICA_all.set";
 "0070397_1_OBF_ICA.set", "0070397_1_OBF_ICA_all.set";
 "0070397_1_OBP_ICA.set", "0070397_1_OBP_ICA_all.set";
 "0070397_2_OBP_ICA.set", "0070397_2_OBP_ICArej.set"];

output_pth = 'D:\\output_ica_007\';

%size(EEG_after.icawinv)
%size(EEG_before.icawinv)

%figure;                  
%topoplot( EEG_before.icawinv(:,1), EEG_before.chanlocs, 'verbose', 'off', 'style' , 'fill','electrodes','off', 'numcontour', 0);
%print('BarPlot','-dpng')                  

s = size(pair_names);
for i=1:s(1)
    filename = char(pair_names(i,1));
    disp(filename)
    EEG_before = pop_loadset( 'filename', char(pair_names(i,1)), 'filepath', 'D:\eeg_D\007' );
    EEG_after = pop_loadset( 'filename', char(pair_names(i,2)), 'filepath', 'D:\eeg_D\007' );
    s0 = size(EEG_before.icawinv);
    for col=1:s0(2)
        isIN = ismember(roundn(EEG_before.icawinv(:,col),-5), roundn(EEG_after.icawinv, -5));
        [m,n] = size(isIN);
        ansv = sum(isIN);
        s_fname =size(filename);
        if ansv == m
            out_name = strcat(output_pth, filename(1:s_fname(2)-4), '_comp_',int2str(col),'_',int2str(1));
            disp(out_name)
            figure('visible','off');
            topoplot( EEG_before.icawinv(:,col), EEG_before.chanlocs, 'verbose', 'off', 'style' , 'fill','electrodes','off');
            print(out_name,'-dpng');
        else
            out_name = strcat(output_pth, filename(1:s_fname(2)-4), '_comp_',int2str(col),'_',int2str(0));
            disp(out_name)
            figure('visible','off');
            topoplot( EEG_before.icawinv(:,col), EEG_before.chanlocs, 'verbose', 'off', 'style' , 'fill','electrodes','off');
            print(out_name,'-dpng');
        end
    end
end



%for i=1:s0(2)
%    isIN = ismember(roundn(EEG_before.icawinv(:,i),-5), roundn(EEG_after.icawinv, -5));
%    [m,n] = size(isIN);
%    ansv = sum(isIN);
    %out_name = strcat(output_pth, filename, '_comp_',int2str(i),'_',int2str(0),'.csv');
    
    %comp_name = strcat(output_pth,'icawinw.csv');
%    if ansv == m
%        disp('good')
%        disp(i)
%        out_name = strcat(output_pth, filename, '_comp_',int2str(i),'_',int2str(1));
%        %fig = figure;
%        figure('visible','off');
%        topoplot( EEG_before.icawinv(:,i), EEG_before.chanlocs, 'verbose', 'off', 'style' , 'fill','electrodes','off');
%        print(out_name,'-dpng');
%      
%    else
%        disp('bed')
%        disp(i)
%        out_name = strcat(output_pth, filename, '_comp_',int2str(i),'_',int2str(0));
%        %fig = figure;
%        figure('visible','off');
%        topoplot( EEG_before.icawinv(:,i), EEG_before.chanlocs, 'verbose', 'off', 'style' , 'fill','electrodes','off');
%        print(out_name,'-dpng');
%    end   
%end