import mne
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import peakutils


class EEG_artefact_proceeding(object):
    def __init__(self,directory,file_name):
        self.directory=directory
        self.file_name=file_name = dira + file_name



    def read_vhdr(self):
        # data = mne.io.read_raw_on(self.file_name, preload=True, montage=None, verbose=False)

        # self.data = data
        pass
    def read_fif(self):
        data = mne.io.read_raw_fif(self.file_name, preload=True, verbose=False)

        self.data = data


    def read_eeglab(self):
        data = mne.io.read_raw_eeglab(self.file_name)

        self.data = data

    def read_edf(self):
        data = mne.io.read_raw_edf(self.file_name)

        self.data = data



sfreq=5000.0 # sampling frequency
time_tomo=100*1e-6 #100 ms time one scan
delta_tomo=150
dira = ""
file_name="rudych_28_05_2018_tomoseg_1raw.fif"
Sp1=EEG_artefact_proceeding(directory=dira,file_name=file_name)
Sp1.read_fif()
data=Sp1.data
# data.filter(1219.99, 1220.01)  # 89
lm= np.sum(data.get_data()[:-3,:],axis=0)#[:20000]

dydx = np.gradient(lm*lm)
ff=dydx*dydx/max(dydx)/max(dydx)

peakind=peakutils.indexes(ff, thres=0.1,min_dist=2)
i=0

evka=[]


listOdd = peakind[1::2] # Elements from list1 starting from 1 iterating by 2
listEven = peakind[::2] # Elements from list1 starting from 0 iterating by 2# print evka*5000
evka=(listEven+listOdd)*0.5


print "scans nums:  ",int(len(evka)/25.0)


delts=[]



ev= np.array(evka)/5000.0
datas={"Latency":ev,"Type":"slice","Position":1}
bd_events=pd.DataFrame(datas)
bd_events=bd_events[["Latency","Type","Position"]]
file_name_tosave=file_name[:-5]+"eve.csv"

bd_events.to_csv(file_name_tosave,sep="\t",index=False)
print file_name_tosave +" is saved"
