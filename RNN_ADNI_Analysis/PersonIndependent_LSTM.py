"""
Input is all Pickle.gz. Now each pickle is a subject.

train:validation:test = 8:1:1

@Zhewei
5/29/2016

"""

import sys,os
import gzip
import pickle as Pickle
import numpy as np
from random import shuffle, randint
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers.core import Dense, Activation
from keras.layers import LSTM
from keras.optimizers import RMSprop
from keras.initializations import normal, identity

iterationNo = 20
Groups = 2
totalNo = 71
trainPercent = 60
validationPercent = 6


testpercent = 5
hd_notes = 10
learning_rate = 1e-4
nb_epoch = 500


def main(args):
    if len(args) < 2:
        usage( args[0] )
        pass
    else:
        work( args[1:] )
        pass
    pass

def usage (programm):
    print ("usage: %s ..data/*Subj*.pickle.gz"%(programm))
    
def work(fnames):
    finalResults = list()
    for iNo in range(iterationNo):
        index = [i for i in range(totalNo-1)]
        shuffle(index)
        trainIndex = index[0:trainPercent]
        validationIndex = index[trainPercent:trainPercent+validationPercent]
        testIndex = index[trainPercent+validationPercent:]
        trainData, trainLabel = stackData(fnames, trainIndex)
        validationData, validationLabel = stackData(fnames, validationIndex)
        testData, testLabel = stackData(fnames, testIndex)
        print ('*'*30)
        print ('Training subjects:', trainPercent)
        print ('Training samples:', trainData.shape[0])
        print ('Validation subjects:', validationPercent)
        print ('Validation samples:', validationData.shape[0])
        print ('Test subjects:', testpercent)
        print ('Test samples:', testData.shape[0])
        print ('*'*30)
        
        
        """
        LSTM
        """
        
        nb_classes = Groups
        timesteps = trainData.shape[1]
        featureNo = trainData.shape[2]

        Y_train = np_utils.to_categorical(trainLabel, nb_classes)
        Y_test = np_utils.to_categorical(testLabel, nb_classes)
        Y_valid = np_utils.to_categorical(validationLabel, nb_classes)
        
        print ("Building model...")
        model = Sequential()
        model.add(LSTM(hd_notes, input_shape=(timesteps, featureNo),\
                            init='normal',\
                            inner_init='identity',\
                            activation='sigmoid', return_sequences=False,\
                            dropout_W=0, dropout_U=0))
        model.add(Dense(nb_classes))
        model.add(Activation('softmax'))
        rmsprop = RMSprop(lr=learning_rate, rho=0.9, epsilon=1e-06)
        model.compile(loss='categorical_crossentropy', optimizer=rmsprop, \
                        metrics=["accuracy"])

        print ("Training model...")

        model.fit(trainData, Y_train, \
                    nb_epoch=nb_epoch, verbose=1, validation_data=(validationData, Y_valid))

        scores = model.evaluate(testData, Y_test, verbose=1)
        print('RNN test score:', scores[0])
        print('RNN test accuracy:', scores[1])
        print (model.predict_classes(testData))
        finalResults.append(scores[1])
        pass
    print ('Final results of LSTM is:', sum(finalResults)/iterationNo)
        
def stackData(fnames, index):
    Data = np.empty([1,1])
    Label = np.empty([1,1])
    for iNo, i in enumerate(index):
        f = gzip.open(fnames[i],'rb')
        tmpdata,tmplabel = Pickle.load(f)
        if iNo == 0:
            Data = tmpdata
            Label = tmplabel
        else:
            Data = np.vstack((Data, tmpdata))
            Label = np.append(Label, tmplabel)
    return Data, Label
    
if __name__ == "__main__":
    main(sys.argv)
    pass
            
