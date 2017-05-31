"""



"""
import csv
import numpy
from glob import glob
import os
import pickle
import gzip
import cv2
import nibabel

class _EachSubject:
    # each subject is a element of a list
    def __init__(self, SubjectID, DX_Group, MRI_imageID):
        self.DX_Group = DX_Group
        self.SubjectID = SubjectID
        # baseline 
        self.MRI_baseline = {MRI_imageID: list()}
        # otherdata after baseline 
        self.MRI_other = list()


class _Subject_with_data:
    def __init__(self, SubjectID, DX_Group):
        self.DX_Group = DX_Group
        self.SubjectID = SubjectID
        # baseline 
        self.MRI_baseline = dict()
        self.fMRI_baseline = dict()
        # otherdata after baseline 
        self.MRI_other = list()
        self.fMRI_other = list()

wholeDataofCSV = list()
with open ('idaSearch_5_24_2017.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        wholeDataofCSV.append(row)

print (wholeDataofCSV[0])
print (wholeDataofCSV[2])

subject_list = list()
description_list = list()

for i in wholeDataofCSV:
    if i['DX Group'] == 'AD' or i['DX Group'] == 'Normal':
        if i['Description'] == 'MPRAGE':
            subject_list.append(i['Subject ID'])
            description_list.append(i['Description'])

print (list(set(description_list)))
print (len(list(set(subject_list))))



MRI_ImageID = None
Subject_ID = None
Baseline_flag = False # False means no baseline exist
DX_group = None
iAge = 0
ValidData = list()
_Subject = None

for row in wholeDataofCSV:
    if Subject_ID != row['Subject ID']:
        # end of a subject
        if MRI_ImageID != None:
            if Baseline_flag == False:
                # False means no baseline exist
                _Subject = _EachSubject(Subject_ID, DX_group, MRI_ImageID)
                Baseline_flag = True
            else:
                _Subject.MRI_other.append(MRI_ImageID)
        if _Subject != None:
            ValidData.append(_Subject)
        MRI_ImageID = None
        fMRI_ImageID = None
        if row['Description'] == 'MPRAGE':
            MRI_ImageID = row['Image ID']
        Subject_ID = row['Subject ID']
        iAge = row['Age']
        DX_group = row['DX Group']
        Baseline_flag = False
        _Subject = None

    if Subject_ID == row['Subject ID']:
        # same subject
        if row['Age'] != iAge:
            # end of a scan
            if MRI_ImageID != None:
                if Baseline_flag == False:
                    # False means no baseline exist
                    _Subject = _EachSubject(Subject_ID, DX_group, MRI_ImageID)
                    Baseline_flag = True
                else:
                    if row['DX Group'] != DX_group:
                        print ('ERROR: The GX group changed.')
                    _Subject.MRI_other.append(MRI_ImageID)
            MRI_ImageID = None
            if row['Description'] == 'MPRAGE':
                MRI_ImageID = row['Image ID']
                if row['DX Group'] != DX_group:
                    print ('ERROR: The GX group changed.')
            iAge = row['Age']
        else:
            # during a scan
            if row['Description'] == 'MPRAGE':
                MRI_ImageID = row['Image ID']
                if row['DX Group'] != DX_group:
                    print ('ERROR: The GX group changed.')

print ('ValidData:', len(ValidData))
# print the MRI IDs
MRI_list = list()
MRI_baselineList = list()
Subjects_in_group = list()

with open('Original_MRI_ImageID_3','w') as f:
    for subject in ValidData:
        if subject.DX_Group == "AD" or subject.DX_Group == "Normal":
            Subjects_in_group.append(subject.SubjectID)
            if subject.MRI_baseline != None:
                #print (subject.MRI_baseline.keys())
                #print (list(subject.MRI_baseline.keys()))
                MRI_list.append(str(list(subject.MRI_baseline.keys())[0]))
                MRI_baselineList.append(str(list(subject.MRI_baseline.keys())[0]))
                f.write(str(list(subject.MRI_baseline.keys())[0]))
                f.write(',')
            if subject.MRI_other:
                for ID in subject.MRI_other:
                    if ID != None:
                        MRI_list.append(ID)
                        f.write(ID)
                        f.write(',')

print('We have', len(Subjects_in_group), 'subjects.')
print('MRI Image:', len(MRI_list))
print('MRI Baseline:', len(MRI_baselineList))


imgID = 0
sampleWeNeed = 100
for subject in ValidData:
    if subject.DX_Group == 'AD' or subject.DX_Group =='Normal':
        flag = False
        subject2 = _Subject_with_data(subject.SubjectID, subject.DX_Group)
        # baseline
        if subject.MRI_baseline != None:
            if sampleWeNeed > 0:
                MRI_baseline_ID = list(subject.MRI_baseline.keys())[0]
                niiimage = nibabel.load('/home/medialab/data/ALL_MRI_Data/'+str(MRI_baseline_ID)+'/T1.nii').get_data().copy()
                #niiimage = cv2.normalize(niiimage, niiimage,  alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
                #niiimage = numpy.uint8(niiimage*255)
                #print (niiimage.shape)
                if niiimage.shape == (256, 256, 170):
                    try:
                        os.makedirs('/home/medialab/Zhewei/fMRI_CSV_Analysis/MRI_data/MRI_imgs/'+str(MRI_baseline_ID))
                    except FileExistsError:
                        pass
                    for img_index in range(35, niiimage.shape[2]-35):
                        img = niiimage[:,:,img_index].copy()
                        norm_img = cv2.normalize(img.astype('float'), dst=img,  alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
                        norm_img = numpy.uint8(norm_img*255)
                        cv2.imwrite('/home/medialab/Zhewei/fMRI_CSV_Analysis/MRI_data/MRI_imgs/'+str(MRI_baseline_ID)+'/'+str(imgID)+'.png', norm_img)
                        imgID += 1
                    sampleWeNeed -= 1
        
