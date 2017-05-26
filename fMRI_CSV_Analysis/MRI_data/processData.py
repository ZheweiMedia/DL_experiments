"""





"""

import os
import glob
from shutil import copyfile
from distutils.dir_util import copy_tree




os.chdir('/home/medialab/data/ALL_MRI_Data/ADNI')

url = '/home/medialab/data/ALL_MRI_Data/ADNI'

with open('/home/medialab/Zhewei/fMRI_CSV_Analysis/MRI_data/Old_MRI_baseline') as f:
    MRI_baseline = f.read().split(',')

print (len(MRI_baseline[:-1]))


MRI_baseline = MRI_baseline[:-1]

for dirpath, dirnames, filenames in os.walk(url):
    if  filenames:
        #print (dirpath)
        #print (dirnames)
        #print (filenames[0])
        #print (filenames[0][-10:-4])
        tmp_name = filenames[0][-10:-4]
        if tmp_name.isdigit():
            if str(tmp_name) in MRI_baseline:
                copy_tree(dirpath, '/home/medialab/data/ALL_MRI_Data/'+str(tmp_name))
        else:
            tmp_name = tmp_name[1:]
            if tmp_name.isdigit():
                if str(tmp_name) in MRI_baseline:
                    copy_tree(dirpath, '/home/medialab/data/ALL_MRI_Data/'+str(tmp_name))
            else:
                tmp_name = tmp_name[1:]
                if str(tmp_name) in MRI_baseline:
                    copy_tree(dirpath, '/home/medialab/data/ALL_MRI_Data/'+str(tmp_name))
