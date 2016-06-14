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


totalNo = 86

index = [i for i in range(totalNo)]
shuffle(index)
DataIndex = index


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
    WholeData, WholeLabel = stackData(fnames, DataIndex)

    print (wholeData.shape)
    sampleNo = wholeData.shape[0]
    timeStep = wholeData.shape[1]
    featureNo = wholeData.shape[2]
    
    print (trainLabel.shape)
    print (validationLabel.shape)
    wholeLabel = np.append(trainLabel, validationLabel)
    wholeLabel = np.append(wholeLabel, testLabel)
    print (wholeLabel.shape)
    print (np.amax(wholeData))
    print (np.amin(wholeData))
    
    
    


    
    '''
    Draw
    '''
    iAD = 0
    iNC = 0
    iLM = 0
    print (sampleNo)
    for i in range(sampleNo):
        if i < sampleNo:
            tmp = wholeData[i,:,:]
            tmp.reshape(timeStep,featureNo)
            if wholeLabel[i] == 1: #AD
                for j in range(timeStep):
                    color = (0, (iAD+(Group1_No))/(Group1_No+(Group1_No)), 0)
                    plotNC, = pyplot.plot(range(featureNo), tmp[j,:], 'o-', color = color, label = 'AD', alpha = 0.7)
            iAD += 1
            if wholeLabel[i] == 0: #NC
                for j in range(timeStep):
                    color = ((iNC+Group2_No)/(Group2_No+Group2_No),0,0)
                    plotAD, = pyplot.plot(range(featureNo), tmp[j,:], 'o-', color = color, label = 'NC', alpha = 0.7)
            iNC += 1
    
    print (iNC, iAD)
    pyplot.legend(handles=[plotNC, plotAD], loc = 4)
    pyplot.show()
    
    
    
    









if __name__ == '__main__':
    main(sys.argv)
    pass
