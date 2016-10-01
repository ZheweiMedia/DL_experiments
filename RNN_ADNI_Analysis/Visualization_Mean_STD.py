import os, gzip
import pickle as Pickle
import matplotlib.pyplot as pyplot
import numpy


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

def Mean_STD(validDataList):
    pyplot.figure(1)
    ADNo = 0
    NCNo = 0
    AD_Mean = list()
    AD_STD = list()
    NC_Mean = list()
    NC_STD = list()
    AD_IDlist = list()
    NC_IDlist = list()
    AD_dataList = list()
    NC_dataList = list()
    for validData in validDataList:
        tmp_list = list(validData.baseline.keys())
        for key in tmp_list:
            try:
                if validData.baseline[str(key)].any():
                    tmp_data = validData.baseline[str(key)]
                    timeStep = tmp_data.shape[0]
                    if validData.DX_Group == 'AD':
                        AD_Mean.append(numpy.mean(tmp_data[:,0]))
                        AD_STD.append(numpy.std(tmp_data[:,0]))
                        AD_IDlist.append(str(key))
                        AD_dataList.append(tmp_data)
                    else:
                        NC_Mean.append(numpy.mean(tmp_data[:,0]))
                        NC_STD.append(numpy.std(tmp_data[:,0]))
                        NC_IDlist.append(str(key))
                        NC_dataList.append(tmp_data)
            except AttributeError:
                pass
            if validData.other != {}:
                tmp_list = list(validData.other.keys())
                for other_key in tmp_list:
                    try:
                        if validData.other[str(other_key)].any():
                            tmp_data = validData.other[str(other_key)]
                            timeStep = tmp_data.shape[0]
                            if validData.DX_Group == 'AD':
                                AD_Mean.append(numpy.mean(tmp_data[:,0]))
                                AD_STD.append(numpy.std(tmp_data[:,0]))
                                AD_IDlist.append(str(key))
                                AD_dataList.append(tmp_data)
                            else:
                                NC_Mean.append(numpy.mean(tmp_data[:,0]))
                                NC_STD.append(numpy.std(tmp_data[:,0]))
                                NC_IDlist.append(str(key))
                                NC_dataList.append(tmp_data)
                    except AttributeError:
                        pass

    return AD_Mean, AD_STD, NC_Mean, NC_STD, AD_IDlist, NC_IDlist, AD_dataList, NC_dataList

def data_to_1D(dataList):
    featureNo = dataList[0].shape[1]
    timeFrame = dataList[0].shape[0]
    print (timeFrame, featureNo)
    # stack data
    Data = numpy.zeros([1,1])
    for dataNo, data in enumerate(dataList):
        if dataNo == 0:
            Data = data
        else:
            Data = numpy.vstack((Data, data))
    return Data.reshape((-1,1))

os.chdir("/home/medialab/Zhewei/data")
Raw_data = gzip.open('Hippo.pickle.gz', 'rb')
Subjects_data = Pickle.load(Raw_data)

AD_Mean, AD_STD, NC_Mean, NC_STD, AD_IDlist, NC_IDlist, AD_dataList, NC_dataList = Mean_STD(Subjects_data)
print (len(AD_Mean))
# print(NC_Mean)

AD_data = data_to_1D(AD_dataList)
NC_data = data_to_1D(NC_dataList)
print (AD_data.shape)

n, ADbins, patches = pyplot.hist(AD_data, 70, normed=False, facecolor='red', alpha=0.5)
n, NCbins, patches = pyplot.hist(NC_data, 70, normed=False, facecolor='green', alpha=0.5)
# add a 'best fit' line
# y = mlab.normpdf(bins, mu, sigma)
# pyplot.plot(bins)
pyplot.title(r'Histogram of All AD NC data')
pyplot.show()

AD_mean = [y for (y,x) in sorted(zip(AD_Mean, AD_STD))]
print(AD_mean.index(AD_Mean[0]))
AD_std = [x for (y,x) in sorted(zip(AD_Mean, AD_STD))]
print (AD_std[15])
print (AD_STD[0])

NC_mean = [y for (y,x) in sorted(zip(NC_Mean,NC_STD))]
print(AD_mean.index(AD_Mean[0]))
NC_std = [x for (y,x) in sorted(zip(NC_Mean, NC_STD))]
error_config = {'ecolor': '0.3'}
index = numpy.arange(90)
rects1 = pyplot.bar(index, AD_mean, 0.35,
                 alpha=0.4,
                 color='r',
                 yerr=AD_std,
                 error_kw=error_config,
                 label='AD')

rects2 = pyplot.bar(index+0.35, NC_mean, 0.35,
                 alpha=0.4,
                 color='g',
                 yerr=NC_std,
                 error_kw=error_config,
                 label='NC')
pyplot.show()

plotAD, = pyplot.plot(range(90), AD_std, 'o-', color = 'r', label = 'AD', alpha = 1)
plotNC, = pyplot.plot(range(90), NC_std, 'o-', color = 'g', label = 'NC', alpha = 1)
pyplot.legend(handles=[plotAD, plotNC], loc = 4)
pyplot.show()
