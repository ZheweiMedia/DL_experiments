"""



"""

import os
import glob
import nibabel
import cv2
from sklearn.preprocessing import scale
import numpy

os.chdir('/media/medialab/Seagate Expansion Drive/ADNI/SIEMENS/fMRI')
url = '/media/medialab/Seagate Expansion Drive/ADNI/SIEMENS/fMRI/'

for folders in glob.glob('fMRI_*'):
    print (folders)
    try:
        img = nibabel.load(folders+'/niiFolder/registration_fMRI_4d.nii').get_data()
        img2 = img
        img = img.reshape((-1,1))
        img = scale(img, axis=0, with_mean=True, with_std=True, copy=True)
        img = img.reshape(img2.shape)
        img = nibabel.Nifti1Image(img, numpy.eye(4))
        nibabel.save(img, url+folders+'/niiFolder/Normlize_ALL.nii.gz')
        for index in range(img2.shape[-1]):
            tmp = img2[:,:,:,index]
            tmp = tmp.reshape((-1,1))
            tmp = scale(tmp, axis=0, with_mean=True, with_std=True, copy=True)
            tmp = tmp.reshape((img2.shape[0], img2.shape[1], img2.shape[2]))
            img2[:,:,:,index] = tmp
        img2 = nibabel.Nifti1Image(img2, numpy.eye(4))
        nibabel.save(img2, url+folders+'/niiFolder/Normlize_FRAME.nii.gz')
    except FileNotFoundError:
        pass
