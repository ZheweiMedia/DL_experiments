


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
from keras.optimizers import Adadelta





# separate as train and test
train_percentage = 0.8
valid_percentage = 0.1
test_percentage = 0.1

Groups = 2
hd_notes = 30
BATCH_SIZE = 30
nb_epoch = 150



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


# read data
with gzip.open('Clean_imageID_with_Data.gz', 'rb') as input_file:
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

print ('*'*40)
print ('We have training subjects:',train_number)
print ('We have validation subjects:',valid_number)
print ('We have test subjects:',test_number)
print ('We have training images:', train_data.shape[0])
print ('We have validation images:', valid_data.shape[0])
print ('We have test images:', test_data.shape[0])
print ('*'*40)

Y_train = np_utils.to_categorical(train_label, Groups)
Y_test = np_utils.to_categorical(test_label, Groups)
Y_valid = np_utils.to_categorical(valid_label, Groups)

timesteps = train_data.shape[1]
featureNo = train_data.shape[2]

print ("Building model...")
model = Sequential()
model.add(LSTM(hd_notes, input_shape=(timesteps, featureNo),\
                            init='normal',\
                            inner_init='identity',\
                            activation='sigmoid', return_sequences=False,\
                            dropout_W=0, dropout_U=0))
model.add(Dense(Groups))
model.add(Activation('softmax'))
adad = Adadelta(lr=1.0, rho=0.95, epsilon=1e-08, decay=0.0)
model.compile(loss='categorical_crossentropy', optimizer=adad, \
                        metrics=["accuracy"])

print ("Training model...")
model.fit(train_data, Y_train, \
          batch_size = BATCH_SIZE, nb_epoch=nb_epoch, verbose=1, validation_data=(valid_data, Y_valid))

scores = model.evaluate(test_data, Y_test, verbose=1)
print ('RNN test score:', scores[0])
print ('RNN test accuracy:', scores[1])
print ('True Labels:', test_label)
print (model.predict_classes(test_data))










