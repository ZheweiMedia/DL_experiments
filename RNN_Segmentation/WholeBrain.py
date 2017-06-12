"""




"""


import os
import glob
from nifti import *
#import cv2
import pickle
import gzip





os.chdir('/home/medialab/data/Challenges/MICCAI_2012_MultiAtlas_Challenge/Training')

sample_list = list()
label_list = list()
for files in glob.glob('*.nii'):
    #print (files)
    if (files[-7:-4]) != 'glm':
        sample_ID = files[:6]+'.nii'
        label_ID = files[:6]+'_glm.nii'
        print (sample_ID)
        sample = NiftiImage(sample_ID).data
        label = NiftiImage(label_ID).data
        sample_list.append(sample)
        label_list.append(label)

with gzip.open('/home/medialab/Zhewei/RNN_Segmentation/images.tar.gz', 'w') as outfiles:
    pickle.dump([sample_list, label_list], outfiles)

"""
        for index in range(sample.shape[2]):
            sampleimg = sample[:,:,index]
            labelimg = label[:,:,index]
            norm_sampleimg = cv2.normalize(sampleimg.astype('float'), dst=tmp, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
            norm_sampleimg = np.uint8(norm_sampleimg*255)
            cv2.imwrite('/home/medialab/Zhewei/RNN_Segmentation/data/sample'+str(img_ID)+'.png', norm_sampleimg)
            cv2.imwrite('/home/medialab/Zhewei/RNN_Segmentation/data/label'+str(img_ID)+'.png', labelimg)
        print (ax)
"""
        

