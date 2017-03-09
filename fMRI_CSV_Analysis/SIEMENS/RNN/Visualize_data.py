


import gzip
import pickle
import math
from random import shuffle
import numpy
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers.core import Dense, Activation
from keras.layers import LSTM
from keras.initializations import normal, identity
from keras.optimizers import Adadelta, RMSprop
from keras.regularizers import l1,l2
import matplotlib.pyplot as plt

from sklearn.svm import LinearSVC
from sklearn.feature_selection import SelectFromModel






# separate as train and test
train_percentage = 0.8
valid_percentage = 0.1
test_percentage = 0.1

Groups = 2
hd_notes = 20
BATCH_SIZE = 30
nb_epoch = 250



class _Subject_with_data:
    def __init__(self, SubjectID, DX_Group):
        self.DX_Group = DX_Group
        self.SubjectID = SubjectID
        # baseline 
        self.MRI_baseline = dict()
        self.fMRI_baseline = dict()
        # otherdata after baseline 
        self.MRI_other = list()
        self.fMRI_other = list()


def read_data(index_list, total_data):
    _data = list()
    label = list()
    for index in index_list:
        subject = total_data[index]
        if subject.fMRI_baseline:
            imageID = list(subject.fMRI_baseline.keys())[0]
            imageData = subject.fMRI_baseline[imageID]
            _data.append(imageData)
            if subject.DX_Group == 'AD':
                label.append('1')
            else:
                label.append('0')
        if subject.fMRI_other:
            for subj in subject.fMRI_other:
                imageID = list(subj.keys())[0]
                imageData = subj[imageID]
                _data.append(imageData)
                if subject.DX_Group == 'AD':
                    label.append('1')
                else:
                    label.append('0')

    row_of_imageData = _data[0].shape[0]
    col_of_imageData = _data[0].shape[1]

    _array = numpy.empty([2,2])
    for index, content in enumerate(_data):
        if index == 0:
            _array = content;
        else:
            _array = numpy.concatenate((_array, content))

    _array = _array.reshape((len(_data), row_of_imageData, col_of_imageData))
    return _array, label

def normalize(_data):
    ## the shape is (ImageNo, featureNo, timesteps)
    ## the output should be (ImageNo, timesteps, featureNo)
    output = numpy.zeros((_data.shape[0], _data.shape[2], _data.shape[1]))
    for iNo in range(_data.shape[0]):
        for fNo in range(_data.shape[1]):
            _tmp = _data[iNo, fNo, :].astype(numpy.float)
            #_tmp_mean = numpy.mean(_tmp)
            #_tmp_std = numpy.std(_tmp)
            #_tmp = (_tmp - _tmp_mean)/_tmp_std
            if numpy.any(_tmp):
                _tmp = _tmp/(numpy.linalg.norm(_tmp))
            output[iNo, :, fNo] = _tmp

    return output

def balance(_data, _label):
    rate = numpy.mean(_label)
    label_list = list(_label)
    print(_data.shape)
    if rate < 0.5:
        # normal samples more than AD
        augment_rate = math.floor(1/rate)-1
        for label_no, label in enumerate(label_list):
            if label == 1:
                for i in range(augment_rate):
                    # between -0.2 to 0.2
                    _tmp = numpy.random.rand(1, _data.shape[1], _data.shape[2])*0.4-0.2
                    _new_sample = _data[label_no,:,:]+_tmp
                    _data = numpy.concatenate((_data, _new_sample))
                    label_list.append('1')

    else:
        raise ValueError('No implementation for this situation')

    label_list = numpy.asarray(label_list).astype(numpy.float)
    return _data, label_list


def feature_selction(_train_data, _valid_data, _test_data, _train_label, _valid_label, _test_label):
    train_imageNo = _train_data.shape[0]
    valid_imageNo = _valid_data.shape[0]
    whole_data = numpy.concatenate((_train_data, _valid_data, _test_data))
    whole_data = whole_data.reshape((-1, 120))

    whole_label = numpy.concatenate((_train_label, _valid_label, _test_label))
    whole_label = list(whole_label)

    new_label_list = list()
    for i in whole_label:
        for j in range(100):
            new_label_list.append(i)

    assert len(new_label_list) == whole_data.shape[0]

    lsvc = LinearSVC(C=0.1, penalty="l1", dual=False).fit(whole_data, new_label_list)
    model = SelectFromModel(lsvc, prefit=True)
    data_new = model.transform(whole_data)
    print ('After feature selection we have', data_new.shape[1], 'features.')

    data_new = data_new.reshape((-1, 100, data_new.shape[1]))
    _train_data = data_new[:train_imageNo,:,:]
    _valid_data = data_new[train_imageNo:train_imageNo+valid_imageNo,:,:]
    _test_data = data_new[train_imageNo+valid_imageNo:,:,:]

    return _train_data, _valid_data, _test_data

def section_ofData(_data, _data_label):
    _data_label_newList = list()
    _data = _data.reshape((-1, 20, _data.shape[2]))
    for i in _data_label:
        for j in range(5):
            _data_label_newList.append(i)

    _data_label_newList = numpy.asarray(_data_label_newList).astype(numpy.float)

    return _data, _data_label_newList

# read data
with gzip.open('Clean_imageID_with_Data_Bandpass.gz', 'rb') as input_file:
    subjects_list = pickle.load(input_file)




total_number = len(subjects_list)
train_number = math.ceil(total_number*train_percentage)
valid_number = math.ceil(total_number*valid_percentage)
test_number = total_number-train_number-valid_number

index_of_subjects = [i for i in range(total_number)]
shuffle(index_of_subjects)

train_index = index_of_subjects[:train_number]
valid_index = index_of_subjects[train_number:train_number+valid_number]
test_index = index_of_subjects[train_number+valid_number:]

# combine data
train_data, train_label = read_data(train_index, subjects_list)
valid_data, valid_label = read_data(valid_index, subjects_list)
test_data, test_label = read_data(test_index, subjects_list)

train_label = numpy.asarray(train_label).astype(numpy.float)
valid_label = numpy.asarray(valid_label).astype(numpy.float)
test_label = numpy.asarray(test_label).astype(numpy.float)


# normalize data
train_data = normalize(train_data)
valid_data = normalize(valid_data)
test_data = normalize(test_data)


# feature slection

#train_data, valid_data, test_data = feature_selction(train_data, valid_data, test_data, \
#                                                     train_label, valid_label, test_label)


data = numpy.concatenate((train_data, valid_data, test_data))
label = numpy.concatenate((train_label, valid_label, test_label))

data = data[:,:,[53, 54, 55, 56, 57, 58, 71, 72, 39, 40, \
                             1, 2 , 61, 62, 7, 8, 9, 10, 33, 34, 77, \
                             78, 79, 80, 85, 86, 87, 88, 89, 90, 91, \
                             92, 93, 94]]

label =  list(label)

for iNo, i in enumerate(label):
    if i == 0:
        plotNC, = plt.plot(data[iNo,:, 15], 'o-', color = 'g', label = 'Normal', alpha = 0.7)
    else:
        plotAD, = plt.plot(data[iNo,:, 15], 'o-', color = 'r', label = 'AD', alpha = 0.7)

plt.legend(handles=[plotNC, plotAD], loc='upper left')
plt.show()










