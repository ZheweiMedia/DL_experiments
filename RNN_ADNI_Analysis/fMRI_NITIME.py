"""
use Nitime to analysis fMRI data from SPM.

Zhewei @ 10/3/2016

"""



import gzip, os
import pickle as Pickle
import numpy,math
import matplotlib.pyplot as plt
from matplotlib.mlab import csv2rec
import nitime

# Import the time-series objects:
from nitime.timeseries import TimeSeries

# Import the analysis objects:
from nitime.analysis import SpectralAnalyzer, FilterAnalyzer, NormalizationAnalyzer
"""
TR = 1.89

data_path = os.path.join(nitime.__path__[0], 'data')

data_rec = csv2rec(os.path.join(data_path, 'fmri_timeseries.csv'))

# Extract ROI information from the csv file headers:
roi_names = numpy.array(data_rec.dtype.names)

# This is the number of samples in each ROI:
n_samples = data_rec.shape[0]

# Make an empty container for the data
data = numpy.zeros((len(roi_names), n_samples))

# Insert the data from each ROI into a row in the data:
for n_idx, roi in enumerate(roi_names):
    data[n_idx] = data_rec[roi]

# Initialize TimeSeries object:
T = TimeSeries(data, sampling_interval=TR)
T.metadata['roi'] = roi_names

S_original = SpectralAnalyzer(T)

# Initialize a figure to put the results into:
fig01 = plt.figure()
ax01 = fig01.add_subplot(1, 1, 1)

ax01.plot(S_original.psd[0],
          S_original.psd[1][9],
          label='Welch PSD')

ax01.plot(S_original.spectrum_fourier[0],
          numpy.abs(S_original.spectrum_fourier[1][9]),
          label='FFT')

ax01.plot(S_original.periodogram[0],
          S_original.periodogram[1][9],
          label='Periodogram')

ax01.plot(S_original.spectrum_multi_taper[0],
          S_original.spectrum_multi_taper[1][9],
          label='Multi-taper')

ax01.set_xlabel('Frequency (Hz)')
ax01.set_ylabel('Power')

ax01.legend()
plt.show()
"""


class _EachSubject:
    # each subject is a element of a list
    def __init__(self, SubjectID, Sex, DX_Group, imageID):
        self.Sex = Sex
        self.DX_Group = DX_Group
        self.SubjectID = SubjectID
        # baseline is a dict, imageID:data
        self.baseline = {imageID:list()}
        # otherdata after baseline is also a dict, imageID:data
        self.other = {}












os.chdir("/home/medialab/Zhewei/data/data_from_SPM/")
Raw_data = gzip.open('Subjects_180_ADNC.pickle.gz', 'rb')
Subjects_data = Pickle.load(Raw_data)

#data = Subjects_data[25].baseline['306889']
print ( Subjects_data[35].baseline.keys())
print (data)
dataList = list()
for i in range(120):
    tmp_data = data[i,:]
    dataList.append(tmp_data)

print(len(dataList))
print(dataList[0].shape)

TR = 1.89
T = TimeSeries(dataList, sampling_interval=TR)

S_original = SpectralAnalyzer(T)

# Initialize a figure to put the results into:
fig01 = plt.figure()
ax01 = fig01.add_subplot(1, 1, 1)

ax01.plot(S_original.psd[0],
          S_original.psd[1][9],
          label='Welch PSD')

ax01.plot(S_original.spectrum_fourier[0],
          numpy.abs(S_original.spectrum_fourier[1][9]),
          label='FFT')

ax01.plot(S_original.periodogram[0],
          S_original.periodogram[1][9],
          label='Periodogram')

ax01.plot(S_original.spectrum_multi_taper[0],
          S_original.spectrum_multi_taper[1][9],
          label='Multi-taper')

ax01.set_xlabel('Frequency (Hz)')
ax01.set_ylabel('Power')

ax01.legend()

plt.show()
