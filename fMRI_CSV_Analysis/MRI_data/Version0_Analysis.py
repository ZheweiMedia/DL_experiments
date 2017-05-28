"""
If in one scan we have MPRAGE or MP-RAGE, choose one of them (the one show itself later in .csv)

"""


import csv
import numpy
from glob import glob
import os
import pickle
import gzip

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



"""
Subject_ID = None
group_list = list()

for row in wholeDataofCSV:
    if row['Subject ID'] == '027_S_0461':
        print (row['DX Group'])
    if Subject_ID != row['Subject ID']:
        # end of a subject
        Subject_ID = row['Subject ID']
        DX_group = row['DX Group']
        group_list.append(DX_group)
    if Subject_ID == row['Subject ID']:
        
        if row['DX Group'] != DX_group:
            print ('ERROR: The GX group changed.')
        group_list.append(DX_group)

print (list(set(group_list)))
                    

print (a)
"""


# For MoCo series
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

def read_1D_files(fMRI_imageID):
    signals = numpy.empty([2, 2])
    for zone_no in range(1,121):
        file_name = glob('/home/medialab/Zhewei/fMRI_CSV_Analysis/MRI_data/MRI_results/'\
                              +fMRI_imageID+'/' + '_t'+str(zone_no)+'.1D')
        try:
            open(file_name[0], 'rb')
            pass
        except IndexError:
            print (fMRI_imageID)
        with open(file_name[0], 'rb') as f:
            zone_singal = list()
            if os.stat(file_name[0]).st_size != 0:
                for i in f.readlines():
                    zone_singal.append(str(i)[1:][1:-3])
            else:
                for i in range(100):
                    zone_singal.append('0.0') 
        if zone_no == 1:
            signals = zone_singal;
        else:
            signals = numpy.concatenate((signals, zone_singal))
    signals = signals.reshape((120,-1))
    return signals



Subjects_with_data = list()
flag = False
for subject in ValidData:
    if subject.DX_Group == 'AD' or subject.DX_Group =='Normal':
        flag = False
        subject2 = _Subject_with_data(subject.SubjectID, subject.DX_Group)
        # baseline
        if subject.MRI_baseline != None:
            MRI_baseline_ID = list(subject.MRI_baseline.keys())[0]
            signals = read_1D_files(MRI_baseline_ID)
            subject2.MRI_baseline = {MRI_baseline_ID:signals}
            flag = True
        if flag:
            Subjects_with_data.append(subject2)


with gzip.open("MRIDataset_imageID_with_Data.gz", "wb") as output_file:
    pickle.dump(Subjects_with_data, output_file)
