"""




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

with gzip.open('After_Registration_Clean_imageID.gz', 'rb') as input_file:
    subjects_list = pickle.load(input_file)

print (len(subjects_list))
