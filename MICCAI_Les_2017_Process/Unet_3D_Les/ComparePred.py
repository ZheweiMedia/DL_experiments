"""




"""


from processData import readfile
import gzip, pickle, numpy
import nibabel as nib
from shutil import copyfile
import glob
import os
import shutil


url = '/home/medialab/Zhewei/MICCAI_Les_2017_Process/Unet_3D_Les/'

trainlinks, trainannotlinks, testlinks, testannotlinks = readfile(url+'link/UnetSample_train.txt',\
                                                                url+'link/UnetLabel_train.txt', \
                                                                url+'link/UnetSample_test.txt', \
                                                                url+'link/UnetLabel_test.txt')

print (len(testannotlinks))

for iNo, i in enumerate(testannotlinks):
    #gt = nib.load(i).get_data()
    #pred = nib.load('/home/medialab/Zhewei/MICCAI_Les_2017_Process/data/compare/'+str(iNo)+'.nii.gz').get_data()
    #print (iNo, numpy.sum(gt), numpy.sum(pred))
    basename = os.path.basename(i)
    basename = os.path.splitext(os.path.splitext(basename)[0])[0]
    basename = basename[5:]
    shutil.copy('/home/medialab/Zhewei/MICCAI_Les_2017_Process/data/predict_les/'+str(iNo)+'.nii.gz', \
                '/home/medialab/Zhewei/MICCAI_Les_2017_Process/data/compare/'+str(basename)+'.nii.gz')
    shutil.copy(i, '/home/medialab/Zhewei/MICCAI_Les_2017_Process/data/compare/gt'+str(basename)+'.nii.gz')



