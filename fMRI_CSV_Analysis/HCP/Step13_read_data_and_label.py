"""

read all results in an array.



"""


import sys
import os
import numpy
import glob
import pickle
import gzip


def read_1D_files(folder, time_length):
    signals = numpy.empty([2, 2])
    for zone_no in range(1,feature_no+1):
        file_name = glob.glob('/home/medialab/data/HCP-Q1/fMRI/' + folder \
                              + '/'+singal_type + '/' + '_t'+str(zone_no)+'.1D')
        with open(file_name[0], 'rb') as f:
            zone_singal = list()
            if os.stat(file_name[0]).st_size != 0:
                for i in f.readlines():
                    zone_singal.append(str(i)[1:][1:-3])
            else:
                for i in range(time_length):
                    zone_singal.append('0.0') 
        if zone_no == 1:
            signals = zone_singal;
        else:
            signals = numpy.concatenate((signals, zone_singal))
    signals = signals.reshape((120,-1))
    return signals




singal_type = 'Bandpass'
feature_no = 120
time_sequence = 171
folders_name = list()

with open(sys.argv[1], 'r') as f:
    folders_name  = f.read().split()

subjects_no = len(folders_name)

whole_data = numpy.empty([subjects_no,feature_no,time_sequence])
for i in range(subjects_no):
    _signal = read_1D_files(folders_name[i], time_sequence)
    whole_data[i,:,:] = _signal

print (whole_data.shape)

with gzip.open('Data.pickle.gz', 'w') as datafile:
    pickle.dump(whole_data, datafile)

with gzip.open('Label.pickle.gz', 'r') as labelfile:
    whole_label = pickle.load(labelfile)

print (whole_label.shape)
