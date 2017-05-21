"""




"""


import os
from glob import glob
import gzip
import pickle
import numpy


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


with gzip.open("smallDataset_imageID_with_Data.gz", "rb") as output_file:
    subjects = pickle.load(output_file)

print (len(subjects))

subjects_index = 
