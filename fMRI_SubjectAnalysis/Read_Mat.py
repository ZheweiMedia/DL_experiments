"""
Test for reading .mat files.


"""

import os
import subprocess
import scipy.io as sio
import numpy

os.chdir("/home/medialab/Zhewei/data")
f=os.popen("ls *.mat")
Name_List = list()
for i in f.readlines():
    Name_List.append(str(i).rstrip())
    
mat_content = sio.loadmat(Name_List[0])
feature =  mat_content['feature']
print (feature.shape)
print (feature[0,:])
print (Name_List[0][:6])
