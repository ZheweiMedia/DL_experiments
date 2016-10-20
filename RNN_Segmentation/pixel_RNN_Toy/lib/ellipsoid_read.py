"""
Read ellipsoid.mat data. Like mnist.py, will return a generator.
ellipsoid is 3D, ellipse is 2D. 
Let's start from 2D.


1. replace the input as our data, then use pixel-RNN to do segmentation.
        1.1 mnist data is seprate as train, validation, test, and for each part we have data and label.
            data store in a array, size like (50000, 784).
        1.2 need to store our target in a array too. Then save them in a tuple.



@Zhewei
7/13/2016
"""

import scipy.io
import numpy
import math
from random import shuffle
import itertools

def prepareData():

    '''mat = scipy.io.loadmat('../data/ellipsoid_dataset_boundary_enhanced.mat')
    print (len(mat.keys()))
    print (len(mat.values()))
    keys = list(mat.keys())
    print (mat['ellipsoid_dataset'].shape)'''
    
    # data
    mat = scipy.io.loadmat('../data/ellipse_dataset_boundary_enhanced.mat')
    # print (len(mat.keys()))
    # print (len(mat.values()))
    keys = list(mat.keys())
    print (keys)
    print (mat['ellipse_dataset'].shape)

    #target
    target = scipy.io.loadmat('../data/ellipse_labels_boundary_enhanced.mat')
    print (target.keys())

    # data shape now is data_content*data_sample, we need to transfer it to
    # (data_sample, data_content). Here cannot use reshape.

    wholeData = mat['ellipse_dataset'].transpose()
    wholeTarget = target['ellipse_labels'].transpose()
    print (wholeData.shape)

    # test if it's really transfer other than reshape
    '''for i in range(2304):
        if test[10,i] != mat['ellipse_dataset'][i,10]:
            print ('False')'''

    # separate as train, validation, test
    print ('We have', wholeData.shape[0], 'data.')

    dataOrder = [i for i in range(wholeData.shape[0])]
    shuffle(dataOrder)

    # train:validation:test = 8:1:1
    trainNo = math.floor(0.8*wholeData.shape[0])
    validNo = math.floor(0.1*wholeData.shape[0])

    trainData = wholeData[dataOrder[0:trainNo], :]
    validData = wholeData[dataOrder[trainNo:trainNo+validNo], :]
    testData = wholeData[dataOrder[trainNo+validNo:], :]

    trainTarget = wholeTarget[dataOrder[0:trainNo], :]
    validTarget = wholeTarget[dataOrder[trainNo:trainNo+validNo], :]
    testTarget = wholeTarget[dataOrder[trainNo+validNo:], :]

    train = zip(trainData, trainTarget)
    valid = zip(validData, validTarget)
    test = zip(testData, testTarget)
    return trainData, validData, testData, \
                trainTarget, validTarget, testTarget, dataOrder[0:trainNo]





trainData, validData, testData, \
    trainTarget, validTarget, testTarget, trainIndex = prepareData()


print (trainIndex)
shuffle(trainIndex)
print (trainIndex)


