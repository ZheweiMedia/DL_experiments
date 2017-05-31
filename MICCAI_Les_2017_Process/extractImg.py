"""




"""
# from __future import devision
import nibabel
import cv2
import os
import math
from random import shuffle
import numpy
import random
from sklearn.cluster import KMeans


train_percentage = 0.8
test_percentage = 0.2
random.seed(123)
x_size = 24
y_size = 24 # patch size
cluster_parameter = 2 # at lease points/2 cluster
step_size_for_test = 18

url = '/home/medialab/data/Challenges/MICCAI_Les_2017/GE3T'
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
        print (sampleurl)
        label = nibabel.load(sampleurl+'/wmh.nii.gz').get_data()
        sample = nibabel.load(sampleurl+'/pre/FLAIR.nii.gz').get_data()
        assert label.shape == sample.shape
        # choose the frame with les
        index_list = numpy.where(label == 1)[1]

        for index in index_list:
            labelFrame = label[:, index, :]*255
            sampleFrame = sample[:, index, :]
            x_index = numpy.where(labelFrame == 255)[0]
            y_index = numpy.where(labelFrame == 255)[1]
            index_list = list(set(index_list))
            lesPoints = numpy.stack((x_index, y_index), axis=1)
            kmeans = KMeans(n_clusters=math.ceil(lesPoints.shape[0]/cluster_parameter), random_state=0).fit(lesPoints)
            centers = kmeans.cluster_centers_

            for index in range(centers.shape[0]):
                x_position = math.floor(centers[index,0])
                y_position = math.floor(centers[index,1])
                if x_position -(x_size/2) <0:
                    x_position = x_size/2
                elif x_position + (x_size/2) >labelFrame.shape[0]:
                    x_position = labelFrame.shape[0] -(x_size/2)-1
                if y_position- (y_size/2) < 0:
                    y_position = y_size/2
                elif y_position + (y_size/2) > labelFrame.shape[1]:
                    y_position = labelFrame.shape[1] -(y-size/2)-1

                labelPatch = labelFrame[int(x_position-x_size/2):int(x_position+x_size/2), int(y_position-y_size/2):int(y_position+y_size/2)]
                samplePatch = sampleFrame[int(x_position-x_size/2):int(x_position+x_size/2), int(y_position-y_size/2):int(y_position+y_size/2)]

                cv2.imwrite(urlForTrain+'/label'+str(trainImgPostFix)+'.png', labelPatch)
                cv2.imwrite(urlForTrain+'/sample'+str(trainImgPostFix)+'.png', samplePatch)
                trainImgPostFix += 1
        

    else:
        # for test
        label = nibabel.load(sampleurl+'/wmh.nii.gz').get_data()
        sample = nibabel.load(sampleurl+'/pre/FLAIR.nii.gz').get_data()
        assert label.shape == sample.shape
        x_index = numpy.arange(0, label.shape[0], step_size_for_test)
        y_index = numpy.arange(0, label.shape[2], step_size_for_test)
        x_index = x_index.tolist()
        y_index = y_index.tolist()
        index_list = [i for i in range(label.shape[1])]
        for index in index_list:
            labelFrame = label[:, index, :]*255
            sampleFrame = sample[:, index, :]
            for x_position in x_index:
                for y_position in y_index:
                    if x_position + x_size >= labelFrame.shape[0]:
                        x_position = labelFrame.shape[0]-x_size-1
                    if y_position + y_size >= labelFrame.shape[1]:
                        y_position = labelFrame.shape[1]-y_size-1
                    labelPatch = labelFrame[int(x_position):int(x_position+x_size), int(y_position):int(y_position+y_size)]
                    samplePatch = sampleFrame[int(x_position):int(x_position+x_size), int(y_position):int(y_position+y_size)]
                    cv2.imwrite(urlForTest+'/label'+str(testImgPostFix)+'.png', labelPatch)
                    cv2.imwrite(urlForTest+'/sample'+str(testImgPostFix)+'.png', samplePatch)
                    testImgPostFix += 1
