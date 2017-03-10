"""






"""

import pickle
import gzip
import numpy
import math
from random import shuffle
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers.core import Dense, Activation
from keras.layers import LSTM, TimeDistributedDense
from keras.initializations import normal, identity
from keras.optimizers import Adadelta, RMSprop
from keras.regularizers import l1,l2
import matplotlib.pyplot as plt








TRAIN_rate = 0.8
VALID_rate = 0.1
TEST_rate = 0.1
BATCH_SIZE = 20
nb_epoch = 400
hd_notes = 2
Groups = 2


def rescale(_data):
    ## _data shape: subject number, feature number, time length
    ## the output should be (ImageNo, timesteps, featureNo)
    output = numpy.zeros((_data.shape[0], _data.shape[2], _data.shape[1]))
    for iNo in range(_data.shape[0]):
        for fNo in range(_data.shape[1]):
            _tmp = _data[iNo, fNo, :]
            if numpy.any(_tmp):
                _tmp = _tmp/(numpy.linalg.norm(_tmp))
            output[iNo, :, fNo] = _tmp

    return output

def normalize(_data):
    ## _data shape: subject number, feature number, time length
    ## the output should be (ImageNo, timesteps, featureNo)
    output = numpy.zeros((_data.shape[0], _data.shape[2], _data.shape[1]))
    for iNo in range(_data.shape[0]):
        for tNo in range(_data.shape[2]):
            _tmp = _data[iNo, :, tNo]
            if numpy.any(_tmp):
                _tmp_mean = numpy.mean(_tmp)
                _tmp_std = numpy.std(_tmp)
                _tmp = (_tmp - _tmp_mean)/_tmp_std
            output[iNo, tNo, :] = _tmp

    return output




with gzip.open('RELATION_Data.pickle.gz', 'r') as RELATION_datafile:
    RELATION_data = pickle.load(RELATION_datafile)

with gzip.open('EMOTION_Data.pickle.gz', 'r') as EMOTION_datafile:
    EMOTION_data = pickle.load(EMOTION_datafile)

print (RELATION_data.shape)
print (EMOTION_data.shape)

# same size
RELATION_data = RELATION_data[:,:,:EMOTION_data.shape[2]]
print (RELATION_data.shape)

# labels
EMOTION_label = [0 for i in range(EMOTION_data.shape[0])]
RELATION_label = [1 for i in range(RELATION_data.shape[0])]


# concatenate data and labels
original_data = numpy.concatenate((EMOTION_data, RELATION_data))
original_label = EMOTION_label + RELATION_label

# normalize
wholeData = rescale(original_data)
wholeLabel = numpy.array(original_label)

print(wholeData.shape)


whole_index = [i for i in range(wholeData.shape[0])]
shuffle(whole_index)

TRAIN_NO = math.floor(wholeData.shape[0]*TRAIN_rate)
VALID_NO = math.floor(wholeData.shape[0]*VALID_rate)

train_data = wholeData[whole_index[:TRAIN_NO],:,:]
train_label = wholeLabel[whole_index[:TRAIN_NO]]
valid_data = wholeData[whole_index[TRAIN_NO:TRAIN_NO+VALID_NO],:,:]
valid_label = wholeLabel[whole_index[TRAIN_NO:TRAIN_NO+VALID_NO]]
test_data = wholeData[whole_index[TRAIN_NO+VALID_NO:],:,:]
test_label = wholeLabel[whole_index[TRAIN_NO+VALID_NO:]]

print (TRAIN_NO, VALID_NO)
print (train_label)


# data inverse
#train_data_inverse = train_data[:,::-1,:]
#train_label_inverse = train_label




#train_data = numpy.concatenate((train_data, train_data_inverse))
#train_label = numpy.concatenate((train_label, train_label_inverse))

print(train_data.shape)
print(train_label.shape)
print(valid_data.shape)
print(valid_label.shape)
print(test_data.shape)
print(test_label.shape)


Y_train =  np_utils.to_categorical(train_label, Groups)
Y_test = np_utils.to_categorical(test_label, Groups)
Y_valid = np_utils.to_categorical(valid_label, Groups)

print(Y_valid.shape)

timesteps = train_data.shape[1]
featureNo = train_data.shape[2]

print ("Building model...")
model = Sequential()
model.add(LSTM(hd_notes, input_shape=(timesteps, featureNo),\
               init='normal',inner_init='identity',\
               activation='tanh', return_sequences=False,\
               W_regularizer=None, U_regularizer=None, \
               b_regularizer=None,\
               dropout_W=0.8, dropout_U=0.8))

model.add(Dense(Groups))
model.add(Activation('softmax'))

model.compile(loss='categorical_crossentropy', optimizer='RMSprop', \
              metrics=["accuracy"])


print ("Training model...")
history = model.fit(train_data, Y_train, \
                    batch_size = BATCH_SIZE, nb_epoch=nb_epoch, \
                    verbose=1, validation_data=(valid_data, Y_valid))



scores = model.evaluate(test_data, Y_test, verbose=1)
print ('RNN test score:', scores[0])
print ('RNN test accuracy:', scores[1])
print ('True Labels:', test_label)
print (model.predict_classes(test_data))
print ('Baseline of training is:',numpy.mean(train_label))
print ('Baseline of validation is:', numpy.mean(valid_label))
print ('Baseline of validation is:', numpy.mean(test_label))


# summarize history for accuracy
plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'validation'], loc='upper left')
plt.show()
# summarize history for loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'validation'], loc='upper left')
plt.show()
