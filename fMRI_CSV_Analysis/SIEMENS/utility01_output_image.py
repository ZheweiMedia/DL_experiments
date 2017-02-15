"""

output registration images


"""


from os import listdir
import nibabel as nib
import math
import scipy.misc
from keras.preprocessing.image import load_img, img_to_array
import numpy as np

# step 1: go to the folder

data_list = listdir('/home/medialab/data/ADNI/process_test_SIEMENS/fMRI')

print (data_list)

std_nii = nib.load('/home/medialab/data/template/std_skullstrip.nii.gz')

print (std_nii.shape)

# choose the middle image

print (math.floor(std_nii.shape[1]/2))

std_image = std_nii.get_data()[:,math.floor(std_nii.shape[1]/2),:]

print (std_image[45,:])

scipy.misc.imsave('/home/medialab/data/ADNI/process_test_SIEMENS/std.png', std_image)

img = load_img('/home/medialab/data/ADNI/process_test_SIEMENS/std.png')
img = img_to_array(img)
print (img[:,:,0][45,:])


