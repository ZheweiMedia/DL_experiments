"""






"""

import pickle
import gzip
import numpy
from random import shuffle
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers.core import Dense, Activation
from keras.layers import LSTM, TimeDistributedDense
from keras.initializations import normal, identity
from keras.optimizers import Adadelta, RMSprop
from keras.regularizers import l1,l2
import matplotlib.pyplot as plt








TRAIN_NO = 56
VALID_NO = 6
TEST_NO = 5
BATCH_SIZE = 30
nb_epoch = 750
hd_notes = 10
Groups = 2


def normalize(_data):
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

def featureSelection(_data, _label):
    ## _data shape: (ImageNo, timesteps, featureNo)
    selected_feature_index = list()
    for iNo in range(_data.shape[0]):
        for fNo in range(_data.shape[2]):
            _tmp = _data[iNo, :, fNo]
            #print (numpy.corrcoef(_tmp, _label[iNo,:])[0,1])
            #print (fNo)
            if (numpy.corrcoef(_tmp, _label[iNo,:])[0,1] > 0.3):
                selected_feature_index.append(fNo)
    print(set(selected_feature_index))
    print (len(set(selected_feature_index)))


def label_for_keras(_label):
    output = numpy.empty((_label.shape[0], _label.shape[1],2))
    for iNo in range(_label.shape[0]):
        for fNo in range(_label.shape[1]):
            if _label[iNo, fNo] == 0:
                output[iNo, fNo,:] = [1,0]
            if _label[iNo, fNo] == 1:
                output[iNo, fNo, :] = [0,1]
    return output




with gzip.open('Data.pickle.gz', 'r') as datafile:
    original_data = pickle.load(datafile)

with gzip.open('Label.pickle.gz', 'r') as labelfile:
    wholeLabel = pickle.load(labelfile)

# normalize
wholeData = normalize(original_data)


print(wholeData.shape)


whole_index = [i for i in range(wholeData.shape[0])]
shuffle(whole_index)

train_data = wholeData[whole_index[:TRAIN_NO],:,:]
train_label = wholeLabel[whole_index[:TRAIN_NO],:]
valid_data = wholeData[whole_index[TRAIN_NO:TRAIN_NO+VALID_NO],:,:]
valid_label = wholeLabel[whole_index[TRAIN_NO:TRAIN_NO+VALID_NO],:]
test_data = wholeData[whole_index[TRAIN_NO+VALID_NO:],:,:]
test_label = wholeLabel[whole_index[TRAIN_NO+VALID_NO:],:]

# data inverse
train_data_inverse = train_data[:,::-1,:]
train_label_inverse = train_label[:,::-1]

print (train_label[0,:])
print (train_label_inverse[0,:])

train_data = numpy.concatenate((train_data, train_data_inverse))
train_label = numpy.concatenate((train_label, train_label_inverse))

print(train_data.shape)
print(train_label.shape)
print(valid_data.shape)
print(valid_label.shape)
print(test_data.shape)
print(test_label.shape)

Y_train = label_for_keras(train_label)
Y_test = label_for_keras(test_label)
Y_valid = label_for_keras(valid_label)

#print(Y_valid.shape)

timesteps = train_data.shape[1]
featureNo = train_data.shape[2]

print ("Building model...")
model = Sequential()
model.add(LSTM(hd_notes, input_shape=(timesteps, featureNo),\
               init='normal',inner_init='identity',\
               activation='sigmoid', return_sequences=True,\
               W_regularizer=None, U_regularizer=None, \
               b_regularizer=None,\
               dropout_W=0.0, dropout_U=0.0))

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
