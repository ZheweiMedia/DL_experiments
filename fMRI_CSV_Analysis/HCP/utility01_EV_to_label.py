"""

Transfer EVs/*.txt to 0,1 labels.

Because we removed the first 5 volume, so need '+5' in line 32.


"""

import sys
import os
import numpy
import glob
import math
import pickle
import gzip


time_sequence = 171

with open(sys.argv[1], 'r') as f:
    folders_name  = f.read().split()

subjects_no = len(folders_name)

whole_label = numpy.zeros([subjects_no,time_sequence])
for i in range(subjects_no):
    file_name = glob.glob('/media/medialab/Backup_Data/EMOTION_LR/fMRI/' + folders_name[i] + '/EVs/fear.txt')
    with open(file_name[0], 'rb') as f:
        for line in (raw.strip().split() for raw in f):
            print (line)
            start = math.floor((float(line[0]))/0.72)+5
            duration = math.floor(float(line[1])/0.72)
            if (start+duration < time_sequence):
                whole_label[i,start:start+duration] = 1
            else:
                whole_label[i,start:] = 1

print(whole_label.shape)
with gzip.open("EMOTION_Label.pickle.gz", "wb") as output_file:
    pickle.dump(whole_label, output_file)

