"""

find out the uncomplete brain



"""


import os
import numpy
import nibabel as nib

template = nib.load('/home/medialab/data/template/AAL2.nii')
template_data = template.get_data()
#print (template.shape)
# (91, 109, 91)
with open('/home/medialab/data/template/ROI_index.txt') as index_file:
    whole_index = index_file.read()

index_list = list()
index_list = (whole_index.split())

# print(index_list)
# find the index of each zone
zone_index_list = list()
for zone_no, index in enumerate(index_list):
    tmp = numpy.asarray(template_data,dtype=float)
    tmp = tmp-float(index)
    zero_index = numpy.where(tmp == 0)
    zone_index_list.append(zero_index)

#print(len(zone_index_list))
#print(template_data[zone_index_list[1]])





img = nib.load('/home/medialab/data/ADNI/SIEMENS/fMRI/fMRI_196079_20101008/result_image/fMRI_removenoise.nii')

#print (img.shape)
# (91, 109, 91, 100)
