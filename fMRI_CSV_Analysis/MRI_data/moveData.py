"""




"""



import os
import glob
from shutil import copyfile

url = '/media/medialab/Seagate Expansion Drive/ADNI/SIEMENS/fMRI/'

folder_list = glob.glob(url+'*/')

url2 = '/home/medialab/data/tmp/'

for i in folder_list:
    print i[-21:-1]
    if not os.path.exists(url2+i[-21:-1]):
        os.makedirs(url2+i[-21:-1])
        os.makedirs(url2+i[-21:-1]+'/niiFolder')
        print (i+'niiFolder/registration_T1.nii')
        print (url2+i[-21:-1]+'/niiFolder/registration_T1.nii')
        copyfile(i+'niiFolder/registration_T1.nii', url2+i[-21:-1]+'/niiFolder/registration_T1.nii')


# check if all folders have registration_T1.nii
folder_list = glob.glob(url2+'*/')

for i in folder_list:
    if not os.path.exists(i+'niiFolder/registration_T1.nii'):
        print (i)
