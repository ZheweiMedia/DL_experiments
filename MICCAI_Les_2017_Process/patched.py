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


print (a)
train_percentage = 0.8
totalSample = len(Les_list)
trainNo = math.floor(totalSample*train_percentage)
shuffle(Les_list)
trainSampleList = Les_list[:trainNo]

# three types of patches: 5*5*9, 8*8*11, 11*11*15
# shape = (x, y, z), (132, 256, 83)
# the patch is 5*9*5, 8*11*8, 11*15*11
patch_size = [5, 9, 5]
patch_strid = [math.floor(patch_size[0]/2), math.floor(patch_size[1]/2), math.floor(patch_size[2]/2)]

def xyz_range(x,y,z, shapes, strids, image):
    if x*strids[0]+shapes[0]> image.shape[0]:
        x_start = image.shape[0]-shapes[0]
    else:
        x_start = x*strids[0]

    if y*strids[1]+shapes[1] > image.shape[1]:
        y_start = image.shape[1]-shapes[1]
    else:
        y_start = y*strids[1]

    if z*strids[2]+shapes[2] > image.shape[2]:
        z_start = image.shape[2]-shapes[2]
    else:
        z_start = z*strids[2]

    return x_start, y_start, z_start

imageID = 0
trainLabelList = list()
testLabelList = list()
print (trainSampleList)
for sampleurl in Les_list:
    print (sampleurl)
    label = nibabel.load(sampleurl+'/wmh.nii.gz').get_data()
    sample = nibabel.load(sampleurl+'/brain_FLAIR.nii.gz').get_data().astype(float)
    tmp_sample = sample.reshape((-1, 1))
    tmp_sample = scale(tmp_sample, axis=0, with_mean=True, with_std=True, copy=True)
    sample = tmp_sample.reshape((sample.shape[0], sample.shape[1], sample.shape[2]))

    for x in range(math.ceil((sample.shape[0]-patch_size[0])/patch_strid[0])+1):
        for y in range(math.ceil((sample.shape[1]-patch_size[1])/patch_strid[1])+1):
            for z in range(math.ceil((sample.shape[2]-patch_size[2])/patch_strid[2])+1):
                x_start, y_start, z_start = xyz_range(x, y, z, patch_size, patch_strid,  sample)
                print (x_start, y_start, z_start)
                print (x, y,z)
    print (sample.shape)
    print (a)
    """
                patch_sample = sample[x_start:x_start+patch_size[0], y_start:y_start+patch_size[0], z_start:z_start+patch_size[0]]
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
                with gzip.open(urlsave+'/sample'+str(imageID)+'.tar.gz', 'w') as outputFile:
                   pickle.dump(patch_sample, outputFile)

                with gzip.open(urlsave+'/label'+str(imageID)+'.tar.gz', 'w') as outputFile:
                    pickle.dump(patch_label, outputFile)

                imageID += 1

    print (len(trainLabelList))
    print (len(testLabelList))
    print (sum(trainLabelList))
    print (sum(testLabelList))

    with open('/home/medialab/Zhewei/MICCAI_Les_2017_Process/trainLabel.txt', 'w') as outputFile:
        for i in trainLabelList:
            outputFile.write(str(i))
            outputFile.write(' ')

    with open('/home/medialab/Zhewei/MICCAI_Les_2017_Process/testLabel.txt', 'w') as outputFile:
        for i in testLabelList:
            outputFile.write(str(i))
            outputFile.write(' ')"""

