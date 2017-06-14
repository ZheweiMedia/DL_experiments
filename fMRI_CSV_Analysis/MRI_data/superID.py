"""





"""

import csv
import nibabel
import cv2
import numpy


class _EachSubject:
    # each subject is a element of a list
    def __init__(self, SubjectID, MRI_15imgID, MRI_30imgID):
        self.SubjectID = SubjectID
        # baseline 
        self.MRI_15ID = list()
        # otherdata after baseline 
        self.MRI_30ID = list()
        self.MRI_15ID.append(MRI_15imgID)
        self.MRI_30ID.append(MRI_30imgID)

wholeDataofCSV = list()
with open ('superResolution.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        wholeDataofCSV.append(row)




# For MoCo series
MRI_Image15 = None
MRI_Image30 = None
Subject_ID = None
Baseline_flag = False # False means no baseline exist
iAge = 0
ValidData = list()
_Subject = None

for row in wholeDataofCSV:
    if Subject_ID != row['Subject ID']:
        # end of a subject
        if MRI_Image15 != None and MRI_Image30 != None:
            if Baseline_flag == False:
                # False means no baseline exist
                _Subject = _EachSubject(Subject_ID, MRI_Image15, MRI_Image30)
                Baseline_flag = True
            else:
                _Subject.MRI_15ID.append(MRI_Image15)
                _Subject.MRI_30ID.append(MRI_Image30)

        if _Subject != None:
            ValidData.append(_Subject)
        MRI_Image15 = None
        MRI_Image30 = None
        if row['Imaging Protocol'] == 'Field Strength=1.5':
            MRI_Image15 = row['Image ID']
        if row['Imaging Protocol'] == 'Field Strength=3.0':
            MRI_Image30 = row['Image ID']
        Subject_ID = row['Subject ID']
        iAge = row['Age']
        Baseline_flag = False
        _Subject = None

    if Subject_ID == row['Subject ID']:
            # same subject
            if row['Age'] != iAge:
                # end of a scan
                if MRI_Image15 != None and MRI_Image30 != None:
                    if Baseline_flag == False:
                        # False means no baseline exist
                        _Subject = _EachSubject(Subject_ID, MRI_Image15, MRI_Image30)
                        Baseline_flag = True
                    else:
                        _Subject.MRI_15ID.append(MRI_Image15)
                        _Subject.MRI_30ID.append(MRI_Image30)
                MRI_Image15 = None
                MRI_Image30 = None
                if row['Imaging Protocol'] == 'Field Strength=1.5':
                    MRI_Image15 = row['Image ID']
                if row['Imaging Protocol'] == 'Field Strength=3.0':
                    MRI_Image30 = row['Image ID']
                iAge = row['Age']
            else:
                # during a scan
                if row['Imaging Protocol'] == 'Field Strength=1.5':
                    MRI_Image15 = row['Image ID']
                if row['Imaging Protocol'] == 'Field Strength=3.0':
                    MRI_Image30 = row['Image ID']

        
print('Totally we have subjects :', len(ValidData), 'for SuperResolution.')

MRI_15List = list()
MRI_30List = list()

for subject in ValidData:
    MRI_15List += subject.MRI_15ID
    MRI_30List += subject.MRI_30ID

print (len(MRI_15List))
print (len(MRI_30List))

with open('superResolution15ID.txt', 'w') as outputFile:
    for i in MRI_15List:
        outputFile.write(i)
        outputFile.write(' ')

with open('superResolution30ID.txt', 'w') as outputFile:
    for i in MRI_30List:
        outputFile.write(i)
        outputFile.write(' ')

badData = ['41449']
imgID = 0
for ino, i in enumerate(MRI_30List):
    if i not in badData:
    
        niiimage15 = nibabel.load('/home/medialab/data/SuperResolution/Experiment/'+str(i)+'/skullstrip15.nii').get_data().copy()
        niiimage30 = nibabel.load('/home/medialab/data/SuperResolution/Experiment/'+str(i)+'/skullstrip30.nii').get_data().copy()

        if niiimage30.shape == (256, 256, 170):
            for img_index in range(35, niiimage30.shape[2]-35):
                sample = niiimage15[:,:,img_index].copy()
                norm_sample = cv2.normalize(sample.astype('float'), dst=sample,  alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
                norm_sample = numpy.uint8(norm_sample*255)

                label = niiimage30[:,:,img_index].copy()
                norm_label = cv2.normalize(label.astype('float'), dst=label,  alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
                norm_label = numpy.uint8(norm_label*255)

                cv2.imwrite('/home/medialab/Zhewei/fMRI_CSV_Analysis/MRI_data/15and30MRI/'+'sample'+str(imgID)+'.png', norm_sample)
                cv2.imwrite('/home/medialab/Zhewei/fMRI_CSV_Analysis/MRI_data/15and30MRI/'+'label'+str(imgID)+'.png', norm_label)
                imgID += 1
    else:
        print ('BadData', MRI_15List[ino], MRI_30List[ino])


