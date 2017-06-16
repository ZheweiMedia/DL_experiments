"""




"""
import random
import os
import math
from random import shuffle
import nibabel
import numpy
import cv2
from keras.models import Sequential
from keras.layers.convolutional import Convolution3D
from keras.layers.core import Activation
from keras.utils import np_utils
from sklearn.preprocessing import scale


url = '/home/medialab/data/Challenges/MICCAI_Les_2017/GE3T'

train_percentage = 0.8
test_percentage = 0.2
random.seed(123)


Les_list = list()
for dirpath, dirnames, filenames in os.walk(url):
    if filenames:
        if filenames[0] == 'wmh.nii.gz':
            Les_list.append(dirpath)


totalSample = len(Les_list)
trainNo = math.floor(totalSample*train_percentage)

trainSample = list()
trainLabel = list()
validSample = list()
validLabel = list()
shuffle(Les_list)
trainSampleList = Les_list[:trainNo]
imgID_train = 0
imgID_test = 0
for sampleurl in Les_list:
    
    label = nibabel.load(sampleurl+'/wmh.nii.gz').get_data()
    sample = nibabel.load(sampleurl+'/pre/FLAIR.nii.gz').get_data().astype(float)
    if sampleurl in trainSampleList:
        index_list1 = list(set(numpy.where(label==1)[2]))
        index_list2 = list(set(numpy.where(label==2)[2]))
        index_list = list(set(index_list1+index_list2))
        for img_index in index_list:
            tmpsample = sample[:,:,img_index].copy()
            tmplabel = label[:,:,img_index].copy()*255/2
            norm_tmpsample = cv2.normalize(tmpsample.astype('float'), dst=tmpsample,  alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
            norm_tmpsample = numpy.uint8(norm_tmpsample*255)
            cv2.imwrite('/home/medialab/Zhewei/MICCAI_Les_2017_Process/data/train/'+'sample'+str(imgID_train)+'.png', norm_tmpsample)
            cv2.imwrite('/home/medialab/Zhewei/MICCAI_Les_2017_Process/data/train/'+'label'+str(imgID_train)+'.png', tmplabel)
            imgID_train += 1
            pass
    else:
        for img_index in range(label.shape[2]):
            tmpsample = sample[:,:,img_index].copy()
            tmplabel = label[:,:,img_index].copy()*255/2
            norm_tmpsample = cv2.normalize(tmpsample.astype('float'), dst=tmpsample,  alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
            norm_tmpsample = numpy.uint8(norm_tmpsample*255)
            cv2.imwrite('/home/medialab/Zhewei/MICCAI_Les_2017_Process/data/test/'+'sample'+str(imgID_test)+'.png', norm_tmpsample)
            cv2.imwrite('/home/medialab/Zhewei/MICCAI_Les_2017_Process/data/test/'+'label'+str(imgID_test)+'.png', tmplabel)
            imgID_test += 1
            pass

print (a)
trainSample = numpy.stack(trainSample)
trainLabel = numpy.stack(trainLabel)
validSample = numpy.stack(validSample)
validLabel = numpy.stack(validLabel)
tmptrainLabel = np_utils.to_categorical(trainLabel)
trainLabel = tmptrainLabel.reshape(trainLabel.shape[0], trainLabel.shape[1], trainLabel.shape[2], trainLabel.shape[3], -1)
tmpvalidLabel = np_utils.to_categorical(validLabel)
validLabel = tmpvalidLabel.reshape(validLabel.shape[0], validLabel.shape[1], validLabel.shape[2], validLabel.shape[3], -1)

filtersNo = 32
kernel_size = (5,5,5)
imgShape = (132, 256, 83,1)
model = Sequential()
model.add(Convolution3D(filtersNo, kernel_size, activation='relu', padding='same', input_shape=imgShape))
model.add(Convolution3D(3, (3,3,3), activation='relu', padding='same'))
model.compile(loss='categorical_crossentropy', optimizer='adadelta')
model.fit(trainSample, trainLabel, batch_size = 1, epochs=10, validation_data=(validSample, validLabel))
