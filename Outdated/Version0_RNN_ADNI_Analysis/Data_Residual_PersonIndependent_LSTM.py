"""
7/24/2016 start:

This program used to generate general pickle files from the raw data from MatLab.

This time we change the strategy: store the data in a data structure: a dict, and then

save the whole data as a pickle file.

Classes and frames and Label: 

AD     0
NC     1


1. all data read or write in ../data/ADNC_data/ADNC_07_28_16/

2. data structure: the whole data is a dict.

        keys are subjects, values are a dict, keys are classes, each class results are in a array, 120(zones)*timeframes.
3. We'd better use the residual values. 
4. length. What should we do about different length? Now just simply choose the shortest one.

******************************************

******************************************

Usage:  

Output: an array with the 3D shape SampleNo*FrameNo*FeatureNo and label for each sample

@Zhewei


"""

import sys,os
import gzip
import pickle as Pickle
import numpy as np
import random
import math
from collections import defaultdict
import matplotlib.pyplot as pyplot
np.random.seed(123)
random.seed(123)

from random import shuffle, randint
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers.core import Dense, Activation
from keras.layers import LSTM
from keras.optimizers import RMSprop, SGD
from keras.initializations import normal, identity

from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2, f_classif


#******************************
#******************************

WholeData = defaultdict(lambda : defaultdict(dict))
WholeRes = defaultdict(lambda : defaultdict(dict))

postfix = '.pickle.gz'
#******************************

ZoneNo = 120
Length = 130-1
EM_Length = 176
RE_Length = 232
MagicNoClass = 2 # for subject
MagicNoSubjBegin = 7
MagicNoSubjEnd = 17
MagicNoContaintBegin = 18
MagicNoContaintEnd = 22

global_max = 6611
global_min = -1993

select_feature = 120
nb_classes = 2
hd_notes = 60
learning_rate = 1e-6
nb_epoch = 500

#******************************


def main(args):
    if len(args) < 2:
        usage( args[0] )
        pass
    else:
        dataAnalysis( args[1:] )
        pass
    pass
    
def usage (programm):
    print ("usage: %s ../data/ADNC_data/ADNC_07_28_16/*"%(programm))
    
def Renormalize(className, value):
    # className = 'EM', 'GA', 'LA', 'MO', 'RE', 'SO', 'WM'
    if className == 'AD':
        local_max = 4950
        local_min = -1074
    if className == 'NC':
        local_max = 6611
        local_min = -1993
    # go back to the original value
    value = value*(local_max-local_min)+local_min
    # renormalize
    value = (value-global_min)/(global_max-global_min)
    return value

def origin_Or_res(datalist, option=None):
    data = np.array(datalist)
    data = data.reshape(-1, ZoneNo)
    if option == 'res':
        timeStep = 130
        print (data.shape)
        data = data.reshape(-1, timeStep, ZoneNo)
        print (data.shape)
        tmpData = np.zeros((data.shape[0], data.shape[1]-1, data.shape[2]))
        for sampleNo in range(tmpData.shape[0]):
            for time in range(1, timeStep):
                tmpData[sampleNo, time-1, :,] = data[sampleNo, time, :]-data[sampleNo, time-1, :]
        data = tmpData.reshape(-1, ZoneNo)
    return data
            
    
def data_clean(files):
    # can return wholedata or whole residual data
    invalidSubj = list()
    for fNo, fi in enumerate(files):
        tmpFile = os.path.basename(fi)
        Class = str(tmpFile[0:MagicNoClass])
        Subj = str(tmpFile[MagicNoSubjBegin:MagicNoSubjEnd])
        Containt = str(tmpFile[MagicNoContaintBegin:MagicNoContaintEnd])
        with open(fi) as f:
            content = f.readlines()
            
        tmpData = list()

        for line in content:
            try:
                tmp = float(line)
                # renormalize
                tmp = Renormalize(Class, tmp)
                tmpData.append(tmp)
                if math.isnan(tmp):
                    invalidSubj.append(Subj+Class)
            except ValueError:
                pass
        # save the class value in a dict
        WholeData[Class][Subj][Containt] = origin_Or_res(tmpData)
        WholeRes[Class][Subj][Containt] = origin_Or_res(tmpData,option='res')
    
    print ('The subjects that contain NaN valuse are :',set(invalidSubj))
    return WholeRes
    # return WholeData
    

def visualize(wholeData):

    # a lot of dirty code at here.
    # the same size length, all data
    # wht the order is randomly?

    sampNo = len(list(wholeData.keys()))
    No1 = 0
    No2 = 0
    pyplot.figure(1)
    for ikey in list(WholeData.keys()):
        for jkey in list(WholeData[ikey].keys()):
            for kkey in list(WholeData[ikey][jkey].keys()):
                tmpData = WholeData[ikey][jkey][kkey]
                NoOFFeature = tmpData.shape[1]
                ttmpData = tmpData.reshape(-1, Length, NoOFFeature)
                if ikey == 'AD':
                    color = (1,0,0)
                    for sample in range(ttmpData.shape[0]):
                        plot1, = pyplot.plot(ttmpData[sample,:,0], \
                                ttmpData[sample,:,1], 'o-', color = color, label = 'AD', alpha = 0.7)
                                
                if ikey == 'NC':
                    color = (0,1,0)
                    for sample in range(ttmpData.shape[0]):
                        plot2, = pyplot.plot(ttmpData[sample,:,0], \
                                ttmpData[sample,:,1], 'o-', color = color, label = 'NC', alpha = 0.7)

    pyplot.legend(handles=[plot1, plot2], loc = 4)   
    pyplot.show()
    
def stackData(WholeData, Subj):
    # input whole data and subject ID
    # output stacked subject data, and labels. 
    # now we only consider about two classes, and I wrote very dirty code again...
    # and keep the t
    Data = np.array([])
    Label = list()
    orderClass = list() # use for go back the dist
    orderSubj = list()
    orderContaint = list()
    sampleNO = list()
    sampleLabel = list()
    flag = False
    for ikey in list(WholeData.keys()):
        for jkey in list(WholeData[ikey].keys()):
            for kkey in list(WholeData[ikey][jkey].keys()):
                if Data.size == 0:
                    tmpData = WholeData[ikey][jkey][kkey]
                    Data = tmpData
                    orderClass += [ikey]
                    orderSubj += [jkey]
                    orderContaint += [kkey]
                else:
                    tmpData = WholeData[ikey][jkey][kkey]
                    Data = np.vstack((Data, tmpData))
                    orderClass += [ikey]
                    orderSubj += [jkey]
                    orderContaint += [kkey]
                NoOFFeature = tmpData.shape[1]
                print(tmpData.shape)
                ttmpData = tmpData.reshape(-1, Length, NoOFFeature)
                NoOfSample = ttmpData.shape[0]
                if ikey == 'AD':
                    Label += [0 for i in range(NoOfSample)]
                    sampleLabel += [0]
                    sampleNO += [NoOfSample]
                elif ikey == 'NC':
                    Label += [1 for i in range(NoOfSample)]
                    sampleLabel += [0]
                    sampleNO += [NoOfSample]
    
    return Data, Label, orderClass, orderSubj, orderContaint, sampleLabel, sampleNO 


def SeparateData(WholeData, Subj, option):
    # input whole data and subject ID
    # output stacked subject data, and labels. 
    # now we only consider about two classes, and I wrote very dirty code again...
    # and keep the t
    Data = np.array([])
    Label = list()
    orderClass = list() # use for go back the dist
    orderSubj = list()
    orderContaint = list()
    sampleNO = list()
    sampleLabel = list()
    flag = False
    for ikey in list(WholeData.keys()):
        for jkey in list(WholeData[ikey].keys()):
            if jkey in Subj:
                if option == 'train':
                    kkey = 'Base'
                else:
                    kkey = 'Base'
                tmpData = np.array([])
                if Data.size == 0:
                    try:
                        tmpData = WholeData[ikey][jkey][kkey]
                        Data = tmpData
                        orderClass += [ikey]
                        orderSubj += [jkey]
                        orderContaint += [kkey]
                    except KeyError:
                        pass
                else:
                    try:
                        tmpData = WholeData[ikey][jkey][kkey]
                        Data = np.vstack((Data, tmpData))
                        orderClass += [ikey]
                        orderSubj += [jkey]
                        orderContaint += [kkey]
                    except KeyError:
                        pass
                if tmpData.shape != (0,):
                    NoOFFeature = tmpData.shape[1]
                    ttmpData = tmpData.reshape(-1, Length, NoOFFeature)
                    NoOfSample = ttmpData.shape[0]
                    if ikey == 'AD':
                        Label += [0 for i in range(NoOfSample)]
                        sampleLabel += [0]
                        sampleNO += [NoOfSample]
                    elif ikey == 'NC':
                        Label += [1 for i in range(NoOfSample)]
                        sampleLabel += [0]
                        sampleNO += [NoOfSample]
    
    print (Data.shape, len(Label))        
    return Data, Label

def featureSelection(dataDict):
    # We know we only have two class
    classes = list(dataDict.keys())
    subj = list()
    for cl in classes:
        subj += list(dataDict[cl].keys())
    all_data, all_label, orderClass, orderSubj, orderContaint, sampleLabel, sampleNO = stackData(dataDict, subj)
    all_label = list(all_label)
    tmp_wholeList = list()
    for i in all_label:
        timeLength = Length
        tmpList = [i for j in range(timeLength)]
        tmp_wholeList = tmp_wholeList+tmpList
    
    print(all_data.shape)
    SelectedData = SelectKBest(f_classif, k=select_feature).fit_transform(all_data, tmp_wholeList)
    print(SelectedData.shape)
    stopPoint = 0
    for orderNo in range(len(orderSubj)):
        dataDict[orderClass[orderNo]][orderSubj[orderNo]][orderContaint[orderNo]] = \
                                        SelectedData[stopPoint*Length:(stopPoint+sampleNO[orderNo])*Length,:]
        stopPoint = stopPoint+sampleNO[orderNo]
    
    return dataDict

def Normalize_eachFeature(dataDict):
    all_data, all_label, orderClass, orderSubj, orderContaint, sampleLabel, sampleNO = stackData(dataDict, list(dataDict.keys()))
    print (all_data.shape, len(all_label),len(orderSubj))
    for col in range(all_data.shape[1]):
        local_max = np.amax(all_data[:,col])
        local_min = np.amin(all_data[:,col])
        all_data[:,col] = (all_data[:,col]-local_min)/(local_max-local_min)
    stopPoint = 0
    
    for orderNo in range(len(orderSubj)):
        dataDict[orderClass[orderNo]][orderSubj[orderNo]][orderContaint[orderNo]] = all_data[stopPoint*Length:(stopPoint+sampleNO[orderNo])*Length,:]
        stopPoint = stopPoint+sampleNO[orderNo]
    
    return dataDict

def dataAnalysis(files):
    ALLData = data_clean(files)
    
    
    ALLData = Normalize_eachFeature(ALLData)
    # featureSelection
    ALLData = featureSelection(ALLData)
    # visualize(ALLData)
    
    
    # Now lets's do RNN
    
    classes = list(ALLData.keys())
    subj = list()
    for cl in classes:
        subj += list(ALLData[cl].keys())
    
    # separate as train, test, validation first...
    sampleNo = len(subj)
    
    trainNo = math.floor(0.8*sampleNo)
    validationNo = math.floor(0.1*sampleNo)
    
    trainSubj = subj[0:trainNo]
    validationSubj = subj[trainNo:trainNo+validationNo]
    testSubj = subj[trainNo+validationNo:]
    
    trainData, trainLabel = SeparateData(ALLData, trainSubj, option='train')
    validationData, validationLabel = SeparateData(ALLData, validationSubj, option='validation')
    testData, testLabel = SeparateData(ALLData, testSubj, option='test')
    print (trainData.shape)
    print (len(trainLabel))
    
    trainData = trainData.reshape((-1, Length, select_feature))
    validationData = validationData.reshape((-1, Length, select_feature))
    testData = testData.reshape((-1, Length, select_feature))
    print (sampleNo)    
    print (trainData.shape)
        
    Y_train = np_utils.to_categorical(trainLabel, nb_classes)
    Y_test = np_utils.to_categorical(testLabel, nb_classes)
    Y_valid = np_utils.to_categorical(validationLabel, nb_classes)
        
    print ("Building model...")
    model = Sequential()
    model.add(LSTM(hd_notes, input_shape=(Length, select_feature),\
                        init='glorot_uniform',\
                        inner_init='orthogonal',\
                        forget_bias_init='one',\
                        inner_activation='sigmoid',\
                        activation='tanh', return_sequences=False,\
                        dropout_W=0, dropout_U=0))
    '''model.add(LSTM(hd_notes, input_shape=(Length, select_feature),\
                            init='normal',\
                            inner_init='identity',\
                            activation='sigmoid', return_sequences=False,\
                            dropout_W=0.1, dropout_U=0.1))'''
    model.add(Dense(nb_classes))
    model.add(Activation('softmax'))
    rmsprop = RMSprop(lr=learning_rate, rho=0.9, epsilon=1e-06)
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=["accuracy"])
    # sgd = SGD(lr=learning_rate, momentum=0.0, decay=0.0, nesterov=False)
    # model.compile(loss='binary_crossentropy', optimizer=sgd, metrics=["accuracy"])
        
    print ("Training model...")

    model.fit(trainData, Y_train, \
                nb_epoch=nb_epoch, verbose=1, validation_data=(validationData, Y_valid))

    scores = model.evaluate(testData, Y_test, verbose=1)
    print('RNN test score:', scores[0])
    print('RNN test accuracy:', scores[1])
    print (testLabel)
    print (model.predict_classes(testData))
        
        
    
    
    





















if __name__ == "__main__":
    main( sys.argv )
    pass
