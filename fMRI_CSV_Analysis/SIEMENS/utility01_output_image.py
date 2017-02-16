"""

output registration images


"""


from os import listdir
import nibabel as nib
import math
import scipy.misc
from keras.preprocessing.image import load_img, img_to_array
import numpy as np

import matplotlib.image

from PIL import Image


# step 1: go to the folder

data_list = listdir('/home/medialab/data/ADNI/process_test_SIEMENS/fMRI')

print (data_list)

std_nii = nib.load('/home/medialab/data/template/std_skullstrip.nii.gz')


# choose the middle image

std_image = std_nii.get_data()[:,math.floor(std_nii.shape[1]/2),:]

matplotlib.image.imsave('/home/medialab/data/ADNI/process_test_SIEMENS/std.png', std_image)

img = Image.open('/home/medialab/data/ADNI/process_test_SIEMENS/std.png')
img = img.convert('RGBA')

matplotlib.image.imsave('/home/medialab/data/ADNI/process_test_SIEMENS/new.png', img)
print (img)
print (img[:,:,2][45,:])




