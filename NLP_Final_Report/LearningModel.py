#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Read results from DataAnalysis.
Separate as train, validation, and test data as the ratio 8:1:1

@Author: Zhewei

"""

import sys,os
import gzip
import cPickle as Pickle
import math
import numpy
from random import shuffle
from DataAnalysis import _org_of_proj
from DataAnalysis import _project
from sklearn import svm
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers.recurrent import SimpleRNN
from keras.layers.core import Dense, Activation
from keras.layers import LSTM
from keras.optimizers import RMSprop
from keras.initializations import normal, identity

train_ratio = 0.8
validation_ratio = 0.1
iteration = 1 # Monte Carlo cross-validation
totleFeatureLen = 300


def main(args):
    if len(args) < 3:
        usage( args[0] )
        pass
    else:
        work( args[1:3] )
        pass
    pass
    
def usage (programm):
    print ("usage: %s data/valid_projects.pickel.gz data/Allproject.pickel.gz"%(programm))
    
def work(fname):
    if not (os.path.isfile(fname[0]) and os.path.isfile(fname[1])):
        raise IOError, "%s is not exist!"%( fname )
        pass
    print "Prepare data:"
    data = Pickle.load(gzip.open( fname[0], 'rb'))
    print "We have", len(data.keys()), "samples."
    
    # read project to get the papers published on this project
    # should store in the valid_projects file...Forget to do that way.
    
    all_project = Pickle.load(gzip.open( fname[1], 'rb'))
    
    sampleId = list(data.keys())
    
    ppp = []
    for pr in data.keys():
        nnn = 0
        for pp in data[pr]:
            nnn += pp.paper_number
        ppp.append(nnn)
    print ppp
    
    # transform the data shape to array(sampleNo, [features, sampleId])
    # sampleId as the last element just for debug.
    # labels are the paper numbers
    dataForTrain = 0
    labels = list()
    
    flagOf1st = 0
    for keyNo, Id in enumerate(sampleId):
        if len(all_project[Id].papers.keys()) != 0:
            labels += [len(all_project[Id].papers.keys())]
            tmpFeature = list()
            for org in data[Id]:
                # if nan in org list
                # set it as 0.
                for simNo, sim in enumerate(org.similarity):
                    if math.isnan(sim):
                        org.similarity[simNo] = 0
                tmpFeature += org.similarity
                pass
            # set the features as the same length
            papersNo = len(tmpFeature)
            tmpFeature += [0 for i in range(totleFeatureLen-len(tmpFeature))]
            tmpFeature += [papersNo]
            # tmpFeature += [Id]
            # stack the features
        
            tmpFeature = numpy.array(tmpFeature, dtype='float')
            if flagOf1st ==0:
                dataForTrain = tmpFeature
                flagOf1st = 1
            else:
                dataForTrain = numpy.vstack((dataForTrain,tmpFeature))
        
    sampleNo = len(labels)
    trainNo = int(math.floor(sampleNo*train_ratio))
    validNo = int(math.floor(sampleNo*validation_ratio))
    testNo = int(sampleNo-trainNo-validNo)
    labels = numpy.array(labels, dtype='float')        
    order = range(sampleNo)
    
    print sampleNo, trainNo, testNo, dataForTrain.shape  
         
    for ite in range(iteration):
        shuffle(order)
        trainData = dataForTrain[order[0:trainNo],:]
        trainLabel = labels[order[0:trainNo]]
        validData = dataForTrain[order[trainNo:trainNo+validNo],:]
        validLabel = labels[order[trainNo:trainNo+validNo]]
        testData = dataForTrain[order[trainNo+validNo:],:]
        testLabel = labels[order[trainNo+validNo:]]
        
        print trainData[0,:]
        print trainLabel[0]
        clf = svm.SVC(decision_function_shape='ovo')
        print clf.fit(trainData, trainLabel)
        # print len(clf.support_vectors_)
    
        print "Presict results are: \n", clf.predict(testData)
        print "Ground truth: \n", testLabel
        print "Accurate: \n", clf.score(testData, testLabel)
        
        
    '''# try other learning model..
    # Let's try RNN
    
    hd_notes = 1
    learning_rate = 1e-6
    nb_epoch = 500
    timesteps = totleFeatureLen+1
    tmp = dataForTrain.reshape(-1,timesteps,1)
    
    for ite in range(iteration):
        shuffle(order)
        trainData = tmp[order[0:trainNo],:,:]
        trainLabel = labels[order[0:trainNo]]
        validData = tmp[order[trainNo:trainNo+validNo],:,:]
        validLabel = labels[order[trainNo:trainNo+validNo]]
        testData = tmp[order[trainNo+validNo:],:,:]
        testLabel = labels[order[trainNo+validNo:]]
        
        nb_classes = 15
        
        Y_train = np_utils.to_categorical(trainLabel, nb_classes)
        Y_test = np_utils.to_categorical(testLabel, nb_classes)
        Y_valid = np_utils.to_categorical(validLabel, nb_classes)
        
        print "Building model..."
        model = Sequential()
        model.add(SimpleRNN(hd_notes, input_shape=(timesteps, 1),\
                            init='normal',\
                            inner_init='identity',\
                            activation='relu', return_sequences=False,\
                            dropout_W=0.0, dropout_U=0.0))
                            
        model.add(Dense(nb_classes))
        model.add(Activation('softmax'))
        rmsprop = RMSprop(lr=learning_rate, rho=0.9, epsilon=1e-06)
        model.compile(loss='categorical_crossentropy', optimizer=rmsprop, metrics=["accuracy"])
    
        print "Training model..."
    
        model.fit(trainData, Y_train, \
                    nb_epoch=nb_epoch, verbose=1, validation_data=(validData, Y_valid))
                    
        scores = model.evaluate(testData, Y_test, verbose=1)
        print('RNN test score:', scores[0])
        print('RNN test accuracy:', scores[1])
        print model.predict_classes(testData)'''











































if __name__ == "__main__":
    main( sys.argv )
    pass
