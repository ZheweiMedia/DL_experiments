
"""
1. After we check the fMRI image, we get the bad data ID.
2. Now I plan to ge the clean image IDs, that means remove the bad fMRI image ID
   and corresponding MRI image ID.


"""

import gzip
import pickle


class _EachSubject:
    # each subject is a element of a list
    def __init__(self, SubjectID, DX_Group, MRI_imageID, fMRI_imageID):
        self.DX_Group = DX_Group
        self.SubjectID = SubjectID
        # baseline 
        self.MRI_baseline = MRI_imageID
        self.fMRI_baseline = fMRI_imageID
        # otherdata after baseline 
        self.MRI_other = list()
        self.fMRI_other = list()


with gzip.open("Original_imageID.gz", "rb") as original_file:
    Original_Data = pickle.load(original_file)


print(len(Original_Data))
bad_ImageID_List = ['257275', '272229', '296788', '229146', '248516', '249407',
                    '282008', '297689', '312870', '313953', '316542', '317121',
                    '322060', '336708', '341918', '365243', '368889', '377213',
                    '424849', '348187', '373523',]

# travel all Original_Data
for subject in Original_Data:
    if subject.DX_Group == "AD" or subject.DX_Group == "Normal":
        if subject.fMRI_baseline in bad_ImageID_List:
            subject.fMRI_baseline = None
            subject.MRI_baseline = None
        if subject.fMRI_other:
            for ID in subject.fMRI_other:
                if ID in bad_ImageID_List:
                    index_ID = subject.fMRI_other.index(ID)
                    #del subject.fMRI_other[index_ID]
                    #del subject.MRI_other[index_ID]
                    subject.fMRI_other[index_ID] = None
                    subject.MRI_other[index_ID] = None


fMRI_list = list()
for subject in Original_Data:
    if subject.DX_Group == "AD" or subject.DX_Group == "Normal":
        if subject.fMRI_baseline != None:
            fMRI_list.append(subject.fMRI_baseline)
        if subject.fMRI_other:
            for ID in subject.fMRI_other:
                if ID != None:
                    fMRI_list.append(ID)

print (len(fMRI_list))

MRI_list = list()
fMRI_list = list()
Subjects_in_group = 0

with open('Clean_MRI_ImageID','w') as f:
        for subject in Original_Data:
            if subject.DX_Group == "AD" or subject.DX_Group == "Normal":
                Subjects_in_group += 1
                if subject.MRI_baseline != None:
                    MRI_list.append(subject.MRI_baseline)
                    f.write(subject.MRI_baseline)
                    f.write(' ')
                if subject.MRI_other:
                    for ID in subject.MRI_other:
                        if ID != None:
                            MRI_list.append(ID)
                            f.write(ID)
                            f.write(' ')

print('We have', Subjects_in_group, 'subjects.')
print('MRI Image:', len(MRI_list))

with open('Clean_fMRI_ImageID','w') as f:
    for subject in Original_Data:
        if subject.DX_Group == "AD" or subject.DX_Group == "Normal":
            if subject.fMRI_baseline != None:
                fMRI_list.append(subject.fMRI_baseline)
                f.write(subject.fMRI_baseline)
                f.write(' ')
            if subject.fMRI_other:
                for ID in subject.fMRI_other:
                    if ID != None:
                        fMRI_list.append(ID)
                        f.write(ID)
                        f.write(' ')
print('fMRI Image:', len(fMRI_list))

with gzip.open("Clean_imageID.gz", "wb") as output_file:
    pickle.dump(Original_Data, output_file)
