"""



"""


import os
import cv2
import glob
import numpy
import nibabel


os.chdir ('/home/medialab/data/Hippo/hippo_data/data2')
dataurl = '/home/medialab/Zhewei/MICCAI_Les_2017_Process/Unet_3D_Hippo/data/'
LAYERS = 56
SUBLAYERS = 48

imgID = 0
for iNo, imgpng in enumerate(glob.glob('hippo*.png')):
    img = cv2.imread(imgpng, 0)
    lab = cv2.imread('label'+str(iNo+1)+'.png', 0)
    img = img.reshape((img.shape[0], img.shape[1], 1))
    lab = lab.reshape((lab.shape[0], lab.shape[1], 1))
    if iNo % LAYERS == 0:
        Whol3D_img = img
        Whol3D_lab = lab
    else:
        Whol3D_img = numpy.concatenate((Whol3D_img, img), axis = 2)
        Whol3D_lab = numpy.concatenate((Whol3D_lab, lab), axis = 2)

    if Whol3D_img.shape[2] == LAYERS:
        # a whole sample
        for i in range(LAYERS-SUBLAYERS):
            tmp_3D_img = Whol3D_img[:,:,i:i+SUBLAYERS]
            tmp_3D_lab = Whol3D_lab[:,:,i:i+SUBLAYERS]
            tmp_3D_img = tmp_3D_img.reshape((tmp_3D_img.shape[0], tmp_3D_img.shape[1], tmp_3D_img.shape[2], 1))
            tmp_3D_lab = tmp_3D_lab.reshape((tmp_3D_lab.shape[0], tmp_3D_lab.shape[1], tmp_3D_lab.shape[2], 1))
            tmp_3D_img = nibabel.Nifti1Image(tmp_3D_img, numpy.eye(4))
            tmp_3D_lab = nibabel.Nifti1Image(tmp_3D_lab, numpy.eye(4))
            nibabel.save(tmp_3D_img, dataurl+'sample'+str(imgID)+'.nii.gz')
            nibabel.save(tmp_3D_lab, dataurl+'label'+str(imgID)+'.nii.gz')
            imgID += 1

os.chdir(dataurl)

trainID = [i for i in range(100)]
testID = [i for i in range(100, 110)]

print (len(trainID))
print (testID)

train_sample_link = list()
train_label_link = list()
test_sample_link = list()
test_label_link = list()

for i in trainID:
    for j in range(i*(LAYERS-SUBLAYERS),(i+1)*(LAYERS-SUBLAYERS)):
        train_sample_link.append(dataurl+'sample'+str(j)+'.nii.gz')
        train_label_link.append(dataurl+'label'+str(j)+'.nii.gz')

for i in testID:
    for j in range(i*(LAYERS-SUBLAYERS),(i+1)*(LAYERS-SUBLAYERS)):
        test_sample_link.append(dataurl+'sample'+str(j)+'.nii.gz')
        test_label_link.append(dataurl+'label'+str(j)+'.nii.gz')


with open('/home/medialab/Zhewei/MICCAI_Les_2017_Process/Unet_3D_Hippo/train_sample.txt', 'w') as f:
    for i in train_sample_link:
        f.write(i)
        f.write('\n')

with open('/home/medialab/Zhewei/MICCAI_Les_2017_Process/Unet_3D_Hippo/train_label.txt', 'w') as f:
    for i in train_label_link:
        f.write(i)
        f.write('\n')
with open('/home/medialab/Zhewei/MICCAI_Les_2017_Process/Unet_3D_Hippo/test_sample.txt', 'w') as f:
    for i in test_sample_link:  
        f.write(i)
        f.write('\n')
with open('/home/medialab/Zhewei/MICCAI_Les_2017_Process/Unet_3D_Hippo/test_label.txt', 'w') as f:
    for i in test_label_link:
        f.write(i)
        f.write('\n')
