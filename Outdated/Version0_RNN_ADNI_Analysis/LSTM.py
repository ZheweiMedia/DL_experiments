"""
Input is Pickle.gz of each group, other than the CombineData.
From each group we choose train, test and validation, then np.vstack.

train:validation:test = 8:1:1

@Zhewei
5/21/2016

Add random.seed()
@Zhewei
6/3/2016

"""

# from future import division
import sys,os
import gzip
import pickle as Pickle
import numpy as np
np.random.seed(1337)  # for reproducibility
from random import shuffle
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers.core import Dense, Activation
from keras.layers import LSTM
from keras.optimizers import RMSprop
from keras.initializations import normal, identity

iterationNo = 1

trainPercent = 0.8
validationPercent = 0.1

hd_notes = 10
learning_rate = 1e-9
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
    print ("usage: %s data/AD.Pickle.gz data/NC.Pickle.gz ..."%(programm))

def work(fnames):
    finalResults = list()
    for iNo in range(iterationNo):
        # read data and stack them together
        trainData, trainLabel, validationData, validationLabel,\
            testData, testLabel = dataProcess(fnames)

        '''
        LSTM
        '''
        nb_classes = len(fnames)
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















def printInfo(labelGroup, trainNo, validationNo, testNo):
    if labelGroup == 0:
        print ('Trainning number of NC is:', trainNo)
        print ('Validation number of NC is:', validationNo)
        print ('Test number of NC is:', testNo)
    if labelGroup == 1:
        print ('Trainning number of AD is:', trainNo)
        print ('Validation number of AD is:', validationNo)
        print ('Test number of AD is:', testNo)
    if labelGroup == 2:
        print ('Trainning number of EMCI is:', trainNo)
        print ('Validation number of EMCI is:', validationNo)
        print ('Test number of EMCI is:', testNo)
    if labelGroup == 3:
        print ('Trainning number of LMCI is:', trainNo)
        print ('Validation number of LMCI is:', validationNo)
        print ('Test number of LMCI is:', testNo)
    if labelGroup == 4:
        print ('Trainning number of SMC is:', trainNo)
        print ('Validation number of SMC is:', validationNo)
        print ('Test number of SMC is:', testNo)
    pass



def dataProcess(fnames):
    for fileNo, files in enumerate(fnames):
        f = gzip.open(files,'rb')
        data,label = Pickle.load(f)
        f.close()
        sampleNo = data.shape[0]
        trainNo = int(trainPercent*sampleNo)
        validationNo = int(validationPercent*sampleNo)
        testNo = sampleNo-trainNo-validationNo
        # print some information
        printInfo(label[0],trainNo,validationNo,testNo)
        index = [i for i in range(sampleNo)]
        shuffle(index)
        trainIndex = index[0:trainNo]
        validationIndex = index[trainNo:trainNo+validationNo]
        testIndex = index[trainNo+validationNo:]
        # label is just one dimention, list.append() is better to process
        label = label.tolist()
        if fileNo == 0:
            trainData = data[trainIndex,:,:]
            tmp = [label[i] for i in trainIndex]
            trainLabel = tmp
            validationData = data[validationIndex,:,:]
            tmp = [label[i] for i in validationIndex]
            validationLabel = tmp
            testData = data[testIndex,:,:]
            tmp = [label[i] for i in testIndex]
            testLabel = tmp
        else:
            # np.vstack
            trainData = np.vstack((trainData, data[trainIndex,:,:]))
            tmp = [label[i] for i in trainIndex]
            trainLabel += tmp
            validationData = np.vstack((validationData, \
                                    data[validationIndex,:,:]))
            tmp = [label[i] for i in validationIndex]
            validationLabel += tmp
            testData = np.vstack((testData, data[testIndex,:,:]))
            tmp = [label[i] for i in testIndex]
            testLabel += tmp
        pass

    return trainData, trainLabel, validationData, validationLabel,\
                testData, testLabel










if __name__ == "__main__":
    main( sys.argv )
    pass
