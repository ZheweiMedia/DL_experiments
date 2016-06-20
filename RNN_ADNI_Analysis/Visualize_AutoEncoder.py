"""
Read all pickle.gz, and plot train, validation, test. 
Given train, validation, test index.


@Zhewei
5/30/2016

Randomly select train, validation and test index.
6/9/2016 
"""

import sys,os
import datetime
import gzip
import pickle as Pickle
import numpy as np
from random import shuffle, randint
from PersonIndependent_LSTM import stackData
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
import matplotlib.pyplot as pyplot


totalNo = 84
trainPercent = 60
validationPercent = 14
testPercent = 10
Group1_No = 300
Group2_No = 300



index = [i for i in range(totalNo)]
# shuffle(index)
trainIndex = index[0:trainPercent]
validationIndex = index[trainPercent:trainPercent+validationPercent]
testIndex = index[trainPercent+validationPercent:]

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

    f = gzip.open(fnames[0],'rb')
    wholeData,wholeLabel = Pickle.load(f)
    print (wholeData.shape)
    print (wholeLabel.shape)
    print (wholeData[212,0,:])
    sampleNo = wholeData.shape[0]
    timeStep = wholeData.shape[1]
    featureNo = wholeData.shape[2]
    wholeData = wholeData.reshape(-1, featureNo)
    
    labelFor_eachFrame = list()
    for i in wholeLabel:
        tmp = [i for i in range(timeStep)]
        labelFor_eachFrame += tmp
        pass
    print (len(labelFor_eachFrame))
    
    '''
    Feature selection
    '''
    
    # SelectedData = SelectKBest(chi2, k=2).fit_transform(wholeData, labelFor_eachFrame)
    SelectedData = wholeData
    print(SelectedData.shape)
    
    '''
    Draw
    '''
    iAD = 0
    iNC = 0
    iLM = 0
    print (sampleNo)
    for i in range(sampleNo):
        if i < sampleNo:
            if wholeLabel[i] == 1: #AD
                color = (0, (iAD+(Group1_No))/(Group1_No+(Group1_No)), 0)
                plotNC, = pyplot.plot(SelectedData[i*timeStep:(i+1)*timeStep,0], SelectedData[i*timeStep:(i+1)*timeStep,1], 'o-', color = color, label = 'AD', alpha = 0.7)
                iAD += 1
            if wholeLabel[i] == 0: #NC
                color = ((iNC+Group2_No)/(Group2_No+Group2_No),0,0)
                plotAD, = pyplot.plot(SelectedData[i*timeStep:(i+1)*timeStep,0], SelectedData[i*timeStep:(i+1)*timeStep,1], 'o-', color = color, label = 'NC', alpha = 0.7)
                iNC += 1
    
    print (iNC, iAD)
    pyplot.legend(handles=[plotNC, plotAD], loc = 4)
    pyplot.show()
    
    
    
    









if __name__ == '__main__':
    main(sys.argv)
    pass
