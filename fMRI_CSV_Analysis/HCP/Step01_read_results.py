"""







"""
import os
import numpy
import glob
import matplotlib.pyplot as plt


folder_name = 'Bandpass'


def read_1D_files():
    signals = numpy.empty([2, 2])
    for zone_no in range(1,121):
        file_name = glob.glob('/home/medialab/data/HCP-Q1/fMRI/100307'\
                              '/'+folder_name + '/' + '_t'+str(zone_no)+'.1D')
        with open(file_name[0], 'rb') as f:
            zone_singal = list()
            if os.stat(file_name[0]).st_size != 0:
                for i in f.readlines():
                    zone_singal.append(str(i)[1:][1:-3])
            else:
                for i in range(100):
                    zone_singal.append('0.0') 
        if zone_no == 1:
            signals = zone_singal;
        else:
            signals = numpy.concatenate((signals, zone_singal))
    signals = signals.reshape((120,-1))
    return signals



data = read_1D_files()
print (data.shape)

feature_no = data.shape[0]
for f_no in range(2):
    _tmp = data[f_no,:].astype(numpy.float)
    _tmp = _tmp/(numpy.linalg.norm(_tmp))
    plot, = plt.plot(_tmp, 'o-', color = [f_no/feature_no, 0, 0], alpha = 0.7)

plt.show()

