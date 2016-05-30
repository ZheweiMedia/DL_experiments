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

totalNo = 71
trainPercent = 60
validationPercent = 6

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
    timeStep = wholeData.shape[1]
    featureNo = wholeData.shape[2]
    wholeData = wholeData.reshape(-1, featureNo)
    print (wholeData.shape)
    wholeLabel = np.append(trainLabel,validationLabel)
    wholeLabel = np.append(wholeLabel, testLabel)
    print (wholeLabel.shape)
    
    









if __name__ == '__main__':
    main(sys.argv)
    pass
