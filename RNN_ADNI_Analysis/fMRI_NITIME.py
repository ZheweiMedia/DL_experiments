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
Raw_data = gzip.open('Subjects_From_SPM.pickle.gz', 'rb')
Subjects_data = Pickle.load(Raw_data)

"""
TR = 3
lb = 0.02
ub = 0.08

for validData in Subjects_data:
        tmp_list = list(validData.baseline.keys())
        for key in tmp_list:
            try:
                if validData.baseline[str(key)].any():
                    tmp_data = validData.baseline[str(key)]
                    print (tmp_data.shape)
                    T = TimeSeries(tmp_data, sampling_interval=TR)
                    F = FilterAnalyzer(T, ub=ub, lb=lb, filt_order=40)
                    p_data = NormalizationAnalyzer(F.fir).z_score.data
                    print (numpy.amax(p_data))
                    #print(numpy.argmax(p_data))
                    index = numpy.unravel_index(numpy.argmax(p_data), (120,130))
                    plt.plot(NormalizationAnalyzer(F.fir).percent_change.data[index[0]])
                    plt.plot(NormalizationAnalyzer(F.fir).z_score.data[index[0]])
                    plt.show()
                    validData.baseline[str(key)] = p_data
                    if str(key) == '228872':# test at here
                        print (validData.baseline[str(key)])
                        print('original:', tmp_data)
            except AttributeError:
                pass
        if validData.other != {}:
            tmp_list = list(validData.other.keys())
            for other_key in tmp_list:
                try:
                    if validData.other[str(other_key)].any():
                        tmp_data = validData.other[str(other_key)]
                        T = TimeSeries(tmp_data, sampling_interval=TR)
                        F = FilterAnalyzer(T, ub=ub, lb=lb, filt_order=40)
                        p_data = NormalizationAnalyzer(F.fir).z_score.data
                        validData.other[str(other_key)] = p_data
                except AttributeError:
                    pass



os.chdir("/home/medialab/Zhewei/data/")
with gzip.open('ADNC_Nitime_Z_Raw.pickle.gz', 'wb') as output_file:
    Pickle.dump(Subjects_data, output_file)"""




No = 19             
data = Subjects_data[No].baseline[list(Subjects_data[No].baseline.keys())[0]]
print ( data)
# data = numpy.array(data)
# print (data.shape)
dataList = list()
for i in range(120):
    tmp_data = data[i,:]
    dataList.append(tmp_data)

print(len(dataList))
print(dataList[0].shape)
# data =  data.transpose()
TR = 3
T = TimeSeries(data, sampling_interval=TR)

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




F = FilterAnalyzer(T, ub=0.08, lb=0.02, filt_order=40)

# Initialize a figure to display the results:
fig02 = plt.figure()
ax02 = fig02.add_subplot(1, 1, 1)

# print (F.fir.data[0].shape)
# Plot the original, unfiltered data:
ax02.plot(F.data[0], label='unfiltered')

ax02.plot(F.filtered_boxcar.data[0], label='Boxcar filter')

ax02.plot(F.fir.data[0], label='FIR')
ax02.plot(F.iir.data[0], label='IIR')

ax02.plot(F.filtered_fourier.data[0], label='Fourier')
ax02.legend()
ax02.set_xlabel('Time (TR)')
ax02.set_ylabel('Signal amplitude (a.u.)')


fig04 = plt.figure()
ax04 = fig04.add_subplot(1, 1, 1)

ax04.plot(NormalizationAnalyzer(F.iir).percent_change.data[0], label='% change')
ax04.plot(NormalizationAnalyzer(F.iir).z_score.data[0], label='Z score')
ax04.legend()
ax04.set_xlabel('Time (TR)')
ax04.set_ylabel('Amplitude (% change or Z-score)')

fig05 = plt.figure()
ax05 = fig05.add_subplot(1, 1, 1)
ax05.plot(NormalizationAnalyzer(F.fir).percent_change.data[0], label='% change')
ax05.plot(NormalizationAnalyzer(F.fir).z_score.data[0], label='Z score')
ax05.legend()
ax05.set_xlabel('Time (TR)')
ax05.set_ylabel('Amplitude (% change or Z-score)')
plt.show()
