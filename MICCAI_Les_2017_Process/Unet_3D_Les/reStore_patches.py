"""



"""

import nibabel
import cv2
import os
import math
import random
from shutil import copy2
import subprocess
from random import shuffle
from sklearn.preprocessing import scale
import gzip
import pickle
import numpy
import cv2

random.seed(123)
url = '/home/medialab/data/Challenges/MICCAI_Les_2017/GE3T'
urlForTrain = '/home/medialab/Zhewei/MICCAI_Les_2017_Process/data/train'
urlForTest = '/home/medialab/Zhewei/MICCAI_Les_2017_Process/data/test'

Les_list = list()
for dirpath, dirnames, filenames in os.walk(url):
    if filenames:
        if filenames[0] == 'wmh.nii.gz':
            foldername = '/home/medialab/Zhewei/MICCAI_Les_2017_Process/data/'+dirpath[-3:]
            #os.mkdir(foldername)
            #copy2(dirpath+'/wmh.nii.gz', foldername)
            #copy2(dirpath+'/pre/FLAIR.nii.gz', foldername)
            #os.chdir(foldername)
            #bashCommand = '3dSkullStrip -o_ply skullstrip_mask.nii.gz -input FLAIR.nii.gz'
            #subprocess.call(bashCommand, shell=True)
            #bashCommand = '3dcalc -prefix brain_FLAIR.nii.gz -expr \'a*step(b)\' -b skullstrip_mask.nii.gz -a FLAIR.nii.gz'
            #subprocess.call(bashCommand, shell=True)
            #bashCommand = 'fsl5.0-fast -o T1_segm_A -t 1 -n 3 -g -p brain_FLAIR.nii'
            #subprocess.call(bashCommand, shell=True)
            Les_list.append(foldername)


train_percentage = 0.8
totalSample = len(Les_list)
trainNo = math.floor(totalSample*train_percentage)
shuffle(Les_list)
trainSampleList = Les_list[:trainNo]

## IMPORTANT: should be even number
# three types of patches: 5*5*9, 8*8*11, 11*11*15
# shape = (x, y, z), (132, 256, 83)
# the patch is 5*9*5, 8*11*8, 11*15*11
patch_size = [6, 10, 6]
patch_strid = [math.floor(patch_size[0]/2), math.floor(patch_size[1]/2), math.floor(patch_size[2]/2)]

def xyz_range(x, shapes, strids, image, index):
    if x*strids[index]+shapes[index]> image.shape[index]:
        x_start = image.shape[index]-shapes[index]
    else:
        x_start = x*strids[index]

    return x_start

def xyz_size(image):
    def _size(image, index):
        i_min = 0
        i_max = 0
        def _get_frame(image, index, frameNo):
            if index == 0:
                tmp = image[frameNo, :,:]
            elif index == 1:
                tmp = image[:,frameNo,:]
            else:
                tmp = image[:,:,frameNo]
            return tmp
        for i in range(image.shape[index]):
            tmp = _get_frame(image, index, i)
            if numpy.any(tmp != 0):
                i_min = i
                break
        for i in reversed(range(image.shape[index])):
            tmp = _get_frame(image, index, i)
            if numpy.any(tmp != 0):
                i_max = i
                break
        return i_min, i_max
    x_min, x_max = _size(image, 0)
    y_min, y_max = _size(image, 1)
    z_min, z_max = _size(image, 2)

    return x_min, x_max, y_min, y_max, z_min, z_max


imageID = 0
trainLabelList = list()
testLabelList = list()

tmp_url_for_uNet_trainSample = list()
tmp_url_for_uNet_trainLabel = list()
tmp_url_for_uNet_testSample = list()
tmp_url_for_uNet_testLabel = list()
print (trainSampleList)
for sampleurl in Les_list:
    print (sampleurl)
    label = nibabel.load(sampleurl+'/T1/wmh.nii.gz').get_data()
    sample = nibabel.load(sampleurl+'/T1/brain_T1.nii.gz').get_data().astype(float)# T1
    pred = numpy.zeros(label.shape)
    
    x_min, x_max, y_min, y_max, z_min, z_max = xyz_size(sample)
    label = label[x_min:x_max, y_min:y_max, z_min:z_max]
    pred = pred[x_min:x_max, y_min:y_max, z_min:z_max]
    times = numpy.zeros(pred.shape)
    for x in range(math.ceil((pred.shape[0]-patch_size[0])/patch_strid[0])+1):
        for y in range(math.ceil((pred.shape[1]-patch_size[1])/patch_strid[1])+1):
            for z in range(math.ceil((pred.shape[2]-patch_size[2])/patch_strid[2])+1):
                x_start = xyz_range(x, patch_size, patch_strid, pred, 0)
                y_start = xyz_range(y, patch_size, patch_strid, pred, 1)
                z_start = xyz_range(z, patch_size, patch_strid, pred, 2)

                patch_label = label[x_start:x_start+patch_size[0], y_start:y_start+patch_size[1], z_start:z_start+patch_size[2]]
                if numpy.any(patch_label == 1.0) or numpy.any(patch_label == 2.0):
                    labelOfPatch = 1
                else:
                    labelOfPatch = 0
                if sampleurl in trainSampleList:
                    urlsave = urlForTrain
                    trainLabelList.append(labelOfPatch)
                else:
                    urlsave = urlForTest
                    testLabelList.append(labelOfPatch)
                if labelOfPatch == 1 :
                    tmp_urlsample = urlsave+'/sample'+str(imageID)+'.nii.gz'
                    tmp_urllabel = urlsave+'/label'+str(imageID)+'.nii.gz'
                    if sampleurl in trainSampleList:
                        tmp_url_for_uNet_trainSample.append(tmp_urlsample)
                        tmp_url_for_uNet_trainLabel.append(tmp_urllabel)
                    else:
                        pred_patch = nibabel.load('/home/medialab/Zhewei/MICCAI_Les_2017_Process/data/compare/'+str(imageID)+'.nii.gz').get_data()
                        pred_patch = pred_patch.reshape(pred_patch.shape[:-1])
                        pred[x_start:x_start+patch_size[0], y_start:y_start+patch_size[1], z_start:z_start+patch_size[2]] =\
                            pred[x_start:x_start+patch_size[0], y_start:y_start+patch_size[1], z_start:z_start+patch_size[2]]+ pred_patch
                        times[x_start:x_start+patch_size[0], y_start:y_start+patch_size[1], z_start:z_start+patch_size[2]] =\
                            times[x_start:x_start+patch_size[0], y_start:y_start+patch_size[1], z_start:z_start+patch_size[2]]+1
                        tmp_url_for_uNet_testSample.append(tmp_urlsample)
                        tmp_url_for_uNet_testLabel.append(tmp_urllabel)

                imageID += 1
    if sampleurl not in trainSampleList:
        print (os.path.basename(sampleurl))
        tmp_pred = numpy.zeros(pred.shape)
        for x in range(pred.shape[0]):
            for y in range(pred.shape[1]):
                for z in range(pred.shape[2]):
                    if pred[x,y,z]*2 > times[x,y,z]:
                        
                        tmp_pred[x,y,z] = 1
                    else:
                        tmp_pred[x,y,z] = 0
        final_pred = numpy.zeros(sample.shape)
        final_pred[x_min:x_max, y_min:y_max, z_min:z_max] = tmp_pred
        final_pred = final_pred.reshape(final_pred.shape+(1,))
        final_pred = nibabel.Nifti1Image(final_pred, numpy.eye(4))
        nibabel.save(final_pred, str(os.path.basename(sampleurl))+'.nii.gz')
    print (len(trainLabelList))
    print (len(testLabelList))
    print (sum(trainLabelList))
    print (sum(testLabelList))
    print ("train", len(tmp_url_for_uNet_trainSample))
    print ("test", len(tmp_url_for_uNet_testSample))

    """
    with open('/home/medialab/Zhewei/MICCAI_Les_2017_Process/trainLabel.txt', 'w') as outputFile:
        for i in trainLabelList:
            outputFile.write(str(i))
            outputFile.write(' ')

    with open('/home/medialab/Zhewei/MICCAI_Les_2017_Process/testLabel.txt', 'w') as outputFile:
        for i in testLabelList:
            outputFile.write(str(i))
            outputFile.write(' ')

    with open('/home/medialab/Zhewei/MICCAI_Les_2017_Process/UnetSample_train.txt', 'w') as outputFile:
        for i in tmp_url_for_uNet_trainSample:
            outputFile.write(str(i))
            outputFile.write('\n')

    with open('/home/medialab/Zhewei/MICCAI_Les_2017_Process/UnetSample_test.txt', 'w') as outputFile:
        for i in tmp_url_for_uNet_testSample:
            outputFile.write(str(i))
            outputFile.write('\n')

    with open('/home/medialab/Zhewei/MICCAI_Les_2017_Process/UnetLabel_train.txt', 'w') as outputFile:
        for i in tmp_url_for_uNet_trainLabel:
            outputFile.write(str(i))
            outputFile.write('\n')

    with open('/home/medialab/Zhewei/MICCAI_Les_2017_Process/UnetLabel_test.txt', 'w') as outputFile:
        for i in tmp_url_for_uNet_testLabel:
            outputFile.write(str(i))
            outputFile.write('\n')

    """

