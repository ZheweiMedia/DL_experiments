"""
Read all pickle.gz, and plot train, validation, test. 
Given train, validation, test index.


@Zhewei
5/30/2016


Label of NC:    0
Label of AD:    1
Label of EMCI:  2
Label of LMCI:  3
Label of SMC:   4

@Zhewei
6/14/2016 
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


totalNo = 189

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
    wholeData, wholeLabel = stackData(fnames, DataIndex)
    
    print (len(DataIndex))
    print (wholeData.shape)
    sampleNo = wholeData.shape[0]
    timeStep = wholeData.shape[1]
    featureNo = wholeData.shape[2]
    
    
    
    # find one of AD, NC, EMCI, LMCI
    wholeLabel = wholeLabel.tolist()

    AD_index = wholeLabel.index(1)
    NC_index = wholeLabel.index(0)
    EMCI_index = wholeLabel.index(2)
    LMCI_index = wholeLabel.index(3)
    
    print (AD_index, NC_index, EMCI_index, LMCI_index)
    
    
    


    
    '''
    Draw
    '''
    pyplot.figure(1)
    
    for t in range(timeStep):
        tmp = wholeData[AD_index, :, :]
        tmp = tmp.reshape(timeStep, featureNo)
        color = 'r'
        plotAD, = pyplot.plot(range(featureNo), tmp[t,:], 'o-', color = color, label = 'AD', alpha = 0.7)
    
    for t in range(timeStep):
        tmp = wholeData[EMCI_index, :, :]
        tmp = tmp.reshape(timeStep, featureNo)
        color = 'g'
        plotNC, = pyplot.plot(range(featureNo), tmp[t,:], 'o-', color = color, label = 'EMCI', alpha = 0.7)
    
    pyplot.legend(handles=[plotNC, plotAD], loc = 4)

    pyplot.figure(2)
    
    for t in range(timeStep):
        tmp = wholeData[NC_index, :, :]
        tmp = tmp.reshape(timeStep, featureNo)
        color = 'b'
        plotEM, = pyplot.plot(range(featureNo), tmp[t,:], 'o-', color = color, label = 'NC', alpha = 0.7)
    
    for t in range(timeStep):
        tmp = wholeData[LMCI_index, :, :]
        tmp = tmp.reshape(timeStep, featureNo)
        color = 'm'
        plotLM, = pyplot.plot(range(featureNo), tmp[t,:], 'o-', color = color, label = 'LMCI', alpha = 0.7)
    


    
    pyplot.legend(handles=[plotEM, plotLM], loc = 4)
    pyplot.show()
    
    
    
    









if __name__ == '__main__':
    main(sys.argv)
    pass
