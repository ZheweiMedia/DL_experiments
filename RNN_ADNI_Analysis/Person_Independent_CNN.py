"""
LSTM for data analysis after feature selection.

1. Read pickle.gz in.
2. Separate as train, validation, test
3. We have 214 persons. We totally processed 180 fMRI images. Separate the persons as train, vali, test, and then collect all images belongs to corresponding group.
4. Change the percentage a little bit. Make sure have enough validation data and test data.

5. Now lets's try CNN. Or CNN-->RNN.


Zhewei @ 9/28/2016

"""

import os, gzip
import pickle as Pickle
from random import shuffle
import math
import numpy
import datetime

from keras.utils import np_utils
from keras.models import Sequential
from keras.layers.core import Dense, Activation
from keras.layers import LSTM, GRU
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D, Convolution1D
from keras.optimizers import RMSprop
from keras.initializations import normal, identity
import matplotlib.pyplot as pyplot


Train_percentage = 0.6
Valid_percentage = 0.2
Groups = 2
hd_notes = 30
learning_rate = 1e-6
nb_epoch = 100

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

def collect_Baseline_And_Other(validDataList):
    Label = list()
    Data = list()
    ID = list()
    for validData in validDataList:
        tmp_list = list(validData.baseline.keys())
        for key in tmp_list:
            try:
                if validData.baseline[str(key)].any():
                    Label.append(validData.DX_Group)
                    Data.append(validData.baseline[str(key)])
                    ID.append(str(key))
                '''if str(key) == '228872':# test at here
                    print (validData.baseline[str(key)])'''
            except AttributeError:
                pass
        if validData.other != {}:
            tmp_list = list(validData.other.keys())
            for other_key in tmp_list:
                try:
                    if validData.other[str(other_key)].any():
                        Label.append(validData.DX_Group)
                        Data.append(validData.other[str(other_key)])
                        ID.append(str(other_key))
                except AttributeError:
                    pass
    return Label, Data, ID

def collect_Baseline_Only(validDataList):
    Label = list()
    Data = list()
    ID = list()
    for validData in validDataList:
        tmp_list = list(validData.baseline.keys())
        for key in tmp_list:
            try:
                if validData.baseline[str(key)].any():
                    Label.append(validData.DX_Group)
                    Data.append(validData.baseline[str(key)])
                    ID.append(str(key))
                '''if str(key) == '228872':# test at here
                    print (validData.baseline[str(key)])'''
            except AttributeError:
                pass
    return Label, Data, ID

def data_to_4D(dataList):
    featureNo = dataList[0].shape[1]
    timeFrame = dataList[0].shape[0]
    print (featureNo, timeFrame)
    # stack data
    Data = numpy.zeros([1,1])
    for dataNo, data in enumerate(dataList):
        if dataNo == 0:
            Data = data
        else:
            Data = numpy.vstack((Data, data))
    return Data.reshape((-1, 1, timeFrame, featureNo))

def label_to_binary(labelList):
    Label = list()
    for label in labelList:
        if label == 'Normal':
            Label.append(0)
        if label == 'AD':
            Label.append(1)
    return Label

    

os.chdir("/home/medialab/Zhewei/data")
Raw_data = gzip.open('Hippo_BandPassFilter_Fifty.pickle.gz', 'rb')
Subjects_data = Pickle.load(Raw_data)

# Now data are in the list Subjects_data.
print ('Totally we have', len(Subjects_data), 'subjects.')
shuffle(Subjects_data)

trainNo = math.floor(len(Subjects_data)*Train_percentage)
validNo = math.floor(len(Subjects_data)*Valid_percentage)

train_Subjects = Subjects_data[0:trainNo]
valid_Subjects = Subjects_data[trainNo:trainNo+validNo]
test_Subjects = Subjects_data[trainNo+validNo:]

print ('We have', len(train_Subjects), 'train subjects.')
print ('We have', len(valid_Subjects), 'valid subjects.')
print ('We have', len(test_Subjects), 'test subjects.')

trainLabel, trainData, trainID = collect_Baseline_And_Other(train_Subjects)
validLabel, validData, validID = collect_Baseline_And_Other(valid_Subjects)
testLabel, testData, testID = collect_Baseline_And_Other(test_Subjects)

# validLabel, validData, validID = collect_Baseline_Only(valid_Subjects)
# testLabel, testData, testID = collect_Baseline_Only(test_Subjects)

print ('We have', len(trainID), 'train images.')
print ('We have', len(validID), 'valid images.')
print ('We have', len(testID), 'test images.')
# label, data, ID = collect_Baseline_And_Other(Subjects_data)
# print (len(ID))

# visualization:

# transfer data to 3D
# print (trainData[10])
trainData = data_to_4D(trainData)
validData = data_to_4D(validData)
testData = data_to_4D(testData)
# print (testData.shape)
# print (trainData[10,:,:])

# labels to 0 and 1
trainLabel = label_to_binary(trainLabel)
validLabel = label_to_binary(validLabel)
testLabel = label_to_binary(testLabel)
# print (trainLabel)
# print (validLabel)
# print (testLabel)



"""
CNN
CNN
"""
nb_filters = 32
# size of pooling area for max pooling
pool_size = (2, 2)
# convolution kernel size
kernel_size = (1, 1)
batch_size = 10

nb_classes = Groups
#timesteps = trainData.shape[1]
#featureNo = trainData.shape[2]
input_shape = trainData.shape
input_shape = trainData.shape[1:]
print (input_shape)


Y_train = np_utils.to_categorical(trainLabel, nb_classes)
Y_test = np_utils.to_categorical(testLabel, nb_classes)
Y_valid = np_utils.to_categorical(validLabel, nb_classes)

model = Sequential()
model.add(Convolution2D(nb_filters, kernel_size[0], kernel_size[1],
                        border_mode='valid',
                        input_shape=input_shape))
model.add(Activation('relu'))
model.add(Convolution2D(nb_filters, kernel_size[0], kernel_size[1]))
model.add(Activation('relu'))
# model.add(MaxPooling2D(pool_size=pool_size))
"""model.add(Convolution1D(nb_filter=nb_filters,
                        filter_length=kernel_size[0]*2,
                        border_mode='valid',
                        activation='relu',
                        subsample_length=1))
# we use max pooling:
model.add(MaxPooling1D(pool_length=model.output_shape[1]))"""
model.add(Dropout(0.5))

model.add(Flatten())
model.add(Dense(64))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(nb_classes))
model.add(Activation('softmax'))

model.compile(loss='categorical_crossentropy',
              optimizer='adadelta',
              metrics=['accuracy'])

history = model.fit(trainData, Y_train, batch_size=batch_size, nb_epoch=nb_epoch,
          verbose=1, validation_data=(validData, Y_valid))
score = model.evaluate(testData, Y_test, verbose=0)
print('Test score:', score[0])
print('Test accuracy:', score[1])

print (testLabel)
print (model.predict_classes(testData))

logTime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
logName1 = logTime+'_1.png'
logName2 = logTime+'_2.png'

fig1 = pyplot.figure(1)

pyplot.plot(history.history['acc'])
pyplot.plot(history.history['val_acc'])
pyplot.title('model accuracy')
pyplot.ylabel('accuracy')
pyplot.xlabel('epoch')
pyplot.legend(['train', 'valid'], loc='upper left')
pyplot.savefig(logName1)
fig1.show()

fig2 = pyplot.figure(2)
# summarize history for loss
pyplot.plot(history.history['loss'])
pyplot.plot(history.history['val_loss'])
pyplot.title('model loss')
pyplot.ylabel('loss')
pyplot.xlabel('epoch')
pyplot.legend(['train', 'valid'], loc='upper left')
pyplot.savefig(logName2)
fig2.show()

input()
