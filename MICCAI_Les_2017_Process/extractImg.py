"""




"""

import nibabel
import cv2
import os
import math
from random import shuffle
import numpy
import random


train_percentage = 0.8
test_percentage = 0.2
random.seed(123)

url = '/home/medialab/data/Challenges/MICCAI_Les_2017'
urlForTrain = '/home/medialab/Zhewei/MICCAI_Les_2017_Process/data/train'
urlForTest = '/home/medialab/Zhewei/MICCAI_Les_2017_Process/data/test'

Les_list = list()
for dirpath, dirnames, filenames in os.walk(url):
    if filenames:
        if filenames[0] == 'wmh.nii.gz':
            Les_list.append(dirpath)


totalSample = len(Les_list)
trainNo = math.floor(totalSample*train_percentage)
shuffle(Les_list)
trainSampleList = Les_list[:trainNo]
trainImgPostFix = 0
testImgPostFix = 0
for sampleurl in Les_list:
    if sampleurl in trainSampleList:
        label = nibabel.load(sampleurl+'/wmh.nii.gz').get_data()
        sample = nibabel.load(sampleurl+'/pre/FLAIR.nii.gz').get_data()
        assert label.shape == sample.shape
        # choose the frame with les
        index_list = numpy.where(label == 1)[1]
        index_list = list(set(index_list))
        for index in index_list:
            labelFrame = label[:, index, :]*255
            sampleFrame = sample[:, index, :]
            cv2.imwrite(urlForTrain+'/label'+str(trainImgPostFix)+'.png', labelFrame)
            cv2.imwrite(urlForTrain+'/sample'+str(trainImgPostFix)+'.png', sampleFrame)
            trainImgPostFix += 1

    else:
        # for test
        label = nibabel.load(sampleurl+'/wmh.nii.gz').get_data()
        sample = nibabel.load(sampleurl+'/pre/FLAIR.nii.gz').get_data()
        assert label.shape == sample.shape
        index_list = [i for i in range(label.shape[1])]
        for index in index_list:
            labelFrame = label[:, index, :]*255
            sampleFrame = sample[:, index, :]
            cv2.imwrite(urlForTest+'/label'+str(testImgPostFix)+'.png', labelFrame)
            cv2.imwrite(urlForTest+'/sample'+str(testImgPostFix)+'.png', sampleFrame)
            testImgPostFix += 1

