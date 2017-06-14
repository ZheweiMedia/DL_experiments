"""





"""


import os
import glob
from distutils.dir_util import copy_tree


os.chdir('/home/medialab/data/SuperResolution/')
for root, dirnames, filenames in os.walk('/home/medialab/data/SuperResolution/'):
    if filenames:
        if filenames[0][-3:] == 'dcm':
            tmp_name = filenames[0][-10:-4]
            if tmp_name.isdigit():
                copy_tree(root, '/home/medialab/data/SuperResolution/Experiment/'+str(tmp_name))
            else:
                tmp_name = tmp_name[1:]
                if tmp_name.isdigit():
                    copy_tree(root, '/home/medialab/data/SuperResolution/Experiment/'+str(tmp_name))
                else:
                    tmp_name = tmp_name[1:]
                    copy_tree(root, '/home/medialab/data/SuperResolution/Experiment/'+str(tmp_name))

