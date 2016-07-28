"""
7/24/2016 start:

This program used to generate general pickle files from the raw data from MatLab.

This time we change the strategy: store the data in a data structure: a dict, and then

save the whole data as a pickle file.

Classes and frames and Label: 

'EMOTION'       176         0
'GAMBLING'      253
'LANGUAGE'      316
'MOTOR'         284
'RELATIONAL'    232         1
'SOCIAL'        274
'WM'            405


1. all data read or write in ./data/HCP_data/

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
IID_List = (100307,103515,103818,111312,114924, \
117122, 118932, 119833, 120212, 125525, 128632, 130013, \
131621, 137128, 138231, 142828, 143325, 144226, 149337, \
150423, 153429, 156637, 159239, 161731, 162329, 167743, \
172332, 182739, 191437, 192439, 192540, 194140, 197550, \
199150, 199251, 200614, 201111, 210617, 217429, 249947, \
250427, 255639, 304020, 307127, 329440, 355542, 499566, \
530635, 559053, 585862, 611231, 638049, 665254, 672756, \
685058, 729557, 732243, 792564, 826353, 856766, 859671, \
861456, 865363, 877168, 889579, 894673, 896778, 896879, \
901139, 917255, 937160 )


WholeData = defaultdict(dict)
WholeRes = defaultdict(dict)

postfix = '.pickle.gz'
#******************************

ZoneNo = 120
Length = 175
EM_Length = 176
RE_Length = 232
MagicNoSub = 6 # for subject
MagicNoClassBegin = 7
MagicNoClassEnd = 9
global_max = 48728
global_min = -6619

select_feature = 60
nb_classes = 2
hd_notes = 50
learning_rate = 1e-5
nb_epoch = 1000

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
    print ("usage: %s ../data/HCP_data/*.txt"%(programm))
    
def Renormalize(className, value):
    # className = 'EM', 'GA', 'LA', 'MO', 'RE', 'SO', 'WM'
    if className == 'EM':
        local_max = 47784
        local_min = -5402
    if className == 'RE':
        local_max = 48728
        local_min = -6619
    # go back to the original value
    value = value*(local_max-local_min)+local_min
    # renormalize
    value = (value-global_min)/(global_max-global_min)
    return value

def origin_Or_res(datalist, option=None):
    data = np.array(datalist)
    data = data.reshape(-1, ZoneNo)
    if option == 'res':
        timeStep = np.shape(data)[0]
        tmpData = np.zeros(( timeStep-1, ZoneNo))
        for time in range(1, timeStep):
            tmpData[time-1, :,] = data[time, :]-data[time-1, :]
        data = tmpData
    return data
            
    
def data_clean(files):
    # can return wholedata or whole residual data
    invalidSubj = list()
    for fNo, fi in enumerate(files):
        tmpFile = os.path.basename(fi)
        Subj = str(tmpFile[0:MagicNoSub])
        Class = str(tmpFile[MagicNoClassBegin:MagicNoClassEnd])
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
        WholeData[Subj][Class] = origin_Or_res(tmpData)
        WholeRes[Subj][Class] = origin_Or_res(tmpData,option='res')
        
    print ('The subjects that contain NaN valuse are :',set(invalidSubj))
    # return WholeRes
    return WholeData
    

def visualize(wholeData, orderList):

    # a lot of dirty code at here.
    # the same size length, all data
    # wht the order is randomly?

    sampNo = len(list(wholeData.keys()))
    No1 = 0
    No2 = 0
    pyplot.figure(1)
    VisuIID = orderList[0:]
    print (wholeData[str(156637)]['EM'])
    for IID in VisuIID:
        print (IID)
        if 'EM' in list(wholeData[str(IID)].keys()):
            color = (No1/(2*sampNo)+0.5,0,0)
            plot1, = pyplot.plot(wholeData[str(IID)]['EM'][:,0], \
                                wholeData[str(IID)]['EM'][:,1], 'o-', color = color, label = 'EM', alpha = 0.7)
            No1 += 1
        if 'RE' in list(wholeData[str(IID)].keys()):
            color = (0,No2/(2*sampNo)+0.5,0)
            plot2, = pyplot.plot(wholeData[str(IID)]['RE'][:,0], \
                                wholeData[str(IID)]['RE'][:,1], 'o-', color = color, label = 'RE', alpha = 0.7)
            No2 += 1
    pyplot.legend(handles=[plot1, plot2], loc = 4)   
    pyplot.show()
    
def stackData(WholeData, Subj):
    # input whole data and subject ID
    # output stacked subject data, and labels. 
    # now we only consider about two classes, and I wrote very dirty code again...
    # and keep the t
    Data = np.zeros([1,1])
    Label = np.zeros([1,1])
    orderSubj = list() # use for go back the dist
    orderClass = list()
    flag = False
    for iNo, i in enumerate(Subj):
        if 'EM' in list(WholeData[i].keys()) and flag == False:
            Data = WholeData[i]['EM'][0:Length,:]
            Label = 0
            orderSubj += [i]
            orderClass += ['EM']
            flag = True
        if 'RE' in list(WholeData[i].keys()) and flag == False:
            Data = WholeData[i]['RE'][0:Length,:]
            Label = 1
            orderSubj += [i]
            orderClass += ['RE']
            flag = True
        if 'EM' in list(WholeData[i].keys()) and flag == True:
            Data = np.vstack((Data, WholeData[i]['EM'][0:Length,:]))
            Label = np.append(Label, 0)
            orderSubj += [i]
            orderClass += ['EM']
        if 'RE' in list(WholeData[i].keys()) and flag == True:
            Data = np.vstack((Data, WholeData[i]['RE'][0:Length,:]))
            Label = np.append(Label, 1)
            orderSubj += [i]
            orderClass += ['RE']
            
    return Data, Label, orderSubj, orderClass


def featureSelection(dataDict):
    all_data, all_label, orderSubj, orderClass = stackData(dataDict, list(dataDict.keys()))
    all_label = list(all_label)
    tmp_wholeList = list()
    for i in all_label:
        timeLength = Length
        tmpList = [i for j in range(timeLength)]
        tmp_wholeList = tmp_wholeList+tmpList
    
    SelectedData = SelectKBest(f_classif, k=select_feature).fit_transform(all_data, tmp_wholeList)
    for orderNo in range(len(orderSubj)):
        dataDict[orderSubj[orderNo]][orderClass[orderNo]] = SelectedData[orderNo*Length:(orderNo+1)*Length,:]
    
    return dataDict

def Normalize_eachFeature(dataDict):
    all_data, all_label, orderSubj, orderClass = stackData(dataDict, list(dataDict.keys()))
    print (all_data.shape)
    for col in range(all_data.shape[1]):
        local_max = np.amax(all_data[:,col])
        local_min = np.amin(all_data[:,col])
        all_data[:,col] = (all_data[:,col]-local_min)/(local_max-local_min)
    for orderNo in range(len(orderSubj)):
        dataDict[orderSubj[orderNo]][orderClass[orderNo]] = all_data[orderNo*Length:(orderNo+1)*Length,:]
    
    return dataDict

def dataAnalysis(files):
    ALLData = data_clean(files)
    
    ALLData = Normalize_eachFeature(ALLData)
    # featureSelection
    ALLData = featureSelection(ALLData)
    # visualize(ALLData, list(IID_List))
    
    
    
    # Now lets's do RNN
    print (ALLData['100307']['EM'].shape)
    print (ALLData['100307']['RE'].shape)
    # separate as train, test, validation first...
    sampleNo = len(list(ALLData.keys()))
    trainNo = math.floor(0.8*sampleNo)
    validationNo = math.floor(0.1*sampleNo)
    
    trainSubj = list(ALLData.keys())[0:trainNo]
    validationSubj = list(ALLData.keys())[trainNo:trainNo+validationNo]
    testSubj = list(ALLData.keys())[trainNo+validationNo:]
    
    trainData, trainLabel, order1, order2 = stackData(ALLData, trainSubj)
    validationData, validationLabel, order1, order2 = stackData(ALLData, validationSubj)
    testData, testLabel, order1, order2 = stackData(ALLData, testSubj)
    
    
    trainData = trainData.reshape((-1, Length, select_feature))
    validationData = validationData.reshape((-1, Length, select_feature))
    testData = testData.reshape((-1, Length, select_feature))
        
    print (trainData.shape)
    print (trainLabel.shape)
        
    Y_train = np_utils.to_categorical(trainLabel, nb_classes)
    Y_test = np_utils.to_categorical(testLabel, nb_classes)
    Y_valid = np_utils.to_categorical(validationLabel, nb_classes)
        
    print ("Building model...")
    model = Sequential()
    '''model.add(LSTM(hd_notes, input_shape=(Length, select_feature),\
                        init='glorot_uniform',\
                        inner_init='orthogonal',\
                        forget_bias_init='one',\
                        inner_activation='sigmoid',\
                        activation='tanh', return_sequences=False,\
                        dropout_W=0, dropout_U=0))'''
    model.add(LSTM(hd_notes, input_shape=(Length, select_feature),\
                            init='normal',\
                            inner_init='identity',\
                            activation='tanh', return_sequences=False,\
                            dropout_W=0, dropout_U=0))
    model.add(Dense(nb_classes))
    model.add(Activation('softmax'))
    rmsprop = RMSprop(lr=learning_rate, rho=0.9, epsilon=1e-06)
    model.compile(loss='binary_crossentropy', optimizer=rmsprop, metrics=["accuracy"])
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
