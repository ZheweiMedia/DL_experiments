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
from sklearn.feature_selection import chi2, f_classif
import matplotlib.pyplot as pyplot


totalNo = 84+76

Group1_No = 167
Group2_No = 219

'''
trainIndex = [47, 28, 38, 54, 6, 9, 36, 17, 58, 65, 22, 11, 59, 16, 50, 76, 55, 63, 46, 10, 4, 2, 70, 12, 27, 14, 49, 78, 52, 53, 45, 81, 56, 69, 79, 73, 72, 33, 18, 34, 20, 7, 71, 80, 8, 39, 77, 44, 83, 74, 61, 13, 51, 19, 67, 21, 35, 82, 75, 1, 68, 26, 31, 37, 84, 48, 30, 57, 29, 41]
validationIndex = [25, 60, 24, 62, 42, 40, 23, 5]
testIndex = [0, 32, 43, 3, 64, 15, 66]
'''

index = [i for i in range(totalNo)]
# shuffle(index)


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
    wholeData, wholeLabel = stackData(fnames, index)
    print (wholeData.shape)
    sampleNo = wholeData.shape[0]
    timeStep = wholeData.shape[1]
    featureNo = wholeData.shape[2]
    wholeData = wholeData.reshape(-1, featureNo)
    print (wholeData.shape)
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
    
    SelectedData = SelectKBest(f_classif, k=10).fit_transform(wholeData, labelFor_eachFrame)
    print(SelectedData.shape)
    
    point = 0
    for iIndex in index:
        tmpdata, tmplabel = stackData(fnames, [iIndex])
        compressed_data = SelectedData[point:point+tmpdata.shape[0]*tmpdata.shape[1],:]
        point += tmpdata.shape[0]*tmpdata.shape[1]
        print (tmpdata.shape)
        print (compressed_data.shape)
        tmpdata = compressed_data.reshape(tmpdata.shape[0],tmpdata.shape[1], -1)
        print (tmpdata.shape)
        print (fnames[iIndex])
        fName = os.path.basename(fnames[iIndex])
        fileName = '../data/'+fName
        with gzip.open(fileName, "wb") as output_file:
            Pickle.dump((tmpdata, tmplabel), output_file)
    '''
    Draw
    '''
    
    '''
    iAD = 0
    iNC = 0
    iLM = 0
    print (sampleNo)
    for i in range(sampleNo):
        if i < sampleNo:
            if wholeLabel[i] == 1: #AD
                color = (0, (iAD+(Group1_No))/(Group1_No+(Group1_No)), 0)
                plotNC, = pyplot.plot(SelectedData[i*timeStep:(i+1)*timeStep,0], SelectedData[i*timeStep:(i+1)*timeStep,1], 'o-', color = color, label = 'LMCI', alpha = 0.7)
                iAD += 1
            if wholeLabel[i] == 0: #NC
                color = ((iNC+Group2_No)/(Group2_No+Group2_No),0,0)
                plotAD, = pyplot.plot(SelectedData[i*timeStep:(i+1)*timeStep,0], SelectedData[i*timeStep:(i+1)*timeStep,1], 'o-', color = color, label = 'EMCI', alpha = 0.7)
                iNC += 1
    
    print (iNC, iAD)
    pyplot.legend(handles=[plotNC, plotAD], loc = 4)
    pyplot.show()'''
    
    
    
    









if __name__ == '__main__':
    main(sys.argv)
    pass
