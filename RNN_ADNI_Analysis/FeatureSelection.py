"""
Read all pickle.gz, and plot train, validation, test. 
Given train, validation, test index.


@Zhewei

5/30/2016
"""

import sys,os
import datetime
import gzip
import pickle as Pickle
import numpy as np
from PersonIndependent_LSTM import stackData
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
import matplotlib.pyplot as pyplot


totalNo = 71
trainPercent = 60
validationPercent = 6
AD_No = 118
NC_No = 190

trainIndex = [44, 11, 64, 49, 19, 7, 46, 69, 34, 9, 23, 2, 1, 36, 38, 5, 0, 32, 56, 53, 65, 59, 24, 37, 33, 4, 62, 31, 39, 61, 18, 40, 60, 41, 51, 35, 16, 30, 20, 28, 42, 27, 54, 15, 50, 17, 13, 12, 3, 63, 43, 6, 26, 29, 45, 25, 58, 57, 48, 66]
validationIndex = [55, 22, 67, 68, 8, 52]
testIndex = [47, 21, 10, 14]

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
    trainData, trainLabel = stackData(fnames, trainIndex)
    validationData, validationLabel = stackData(fnames, validationIndex)
    testData, testLabel = stackData(fnames, testIndex)
    wholeData = np.vstack((trainData, validationData,testData))
    print (wholeData.shape)
    sampleNo = wholeData.shape[0]
    timeStep = wholeData.shape[1]
    featureNo = wholeData.shape[2]
    wholeData = wholeData.reshape(-1, featureNo)
    print (wholeData.shape)
    wholeLabel = np.append(trainLabel,validationLabel)
    wholeLabel = np.append(wholeLabel, testLabel)
    print (wholeLabel.shape)
    labelFor_eachFrame = list()
    for i in wholeLabel:
        tmp = [i for i in range(timeStep)]
        labelFor_eachFrame += tmp
        pass
    print (len(labelFor_eachFrame))
    
    '''
    Feature selection
    '''
    
    SelectedData = SelectKBest(chi2, k=2).fit_transform(wholeData, labelFor_eachFrame)
    print(SelectedData.shape)
    
    '''
    Draw
    '''
    iAD = 0
    iNC = 0
    for i in range(sampleNo):
        if i < sampleNo:
            if wholeLabel[i] == 0: #NC
                color = (0, (iAD+100)/(AD_No+100), 0)
                plotNC, = pyplot.plot(SelectedData[i*timeStep:(i+1)*timeStep,0], SelectedData[i*timeStep:(i+1)*timeStep,1], 'o-', color = color, label = 'NC', alpha = 0.7)
                iNC += 1
            if wholeLabel[i] == 1: #AD
                color = ((iNC+200)/(NC_No+200),0,0)
                plotAD, = pyplot.plot(SelectedData[i*timeStep:(i+1)*timeStep,0], SelectedData[i*timeStep:(i+1)*timeStep,1], 'o-', color = color, label = 'AD', alpha = 0.7)
                iAD += 1
    
    print (iNC, iAD)
    pyplot.legend(handles=[plotNC, plotAD],loc = 4)
    pyplot.show()
    
    
    
    









if __name__ == '__main__':
    main(sys.argv)
    pass
