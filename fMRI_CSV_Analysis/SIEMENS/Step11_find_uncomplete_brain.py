"""

find out the uncomplete brain



"""


import os
import numpy
import nibabel as nib

in_complete_brain = list()
in_complete_rate = 0.1

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

folder_names = os.listdir('/home/medialab/data/ADNI/SIEMENS/fMRI/')
base_folder = '/home/medialab/data/ADNI/SIEMENS/fMRI/'

invalid_list = list()

for folder in folder_names:
    image_path = base_folder+folder+'/result_image/fMRI_removenoise.nii'
    img = nib.load(image_path)
    img_data = img.get_data()

    for zone_no, index in enumerate(index_list):
        zone_data = img_data[zone_index_list[zone_no]]
        total_pixel = 1
        for shape in list(zone_data.shape):
            total_pixel = total_pixel*shape

        zero_in_zone = numpy.where(zone_data == 0)
        
        zero_percentage = (len(zero_in_zone[0]))/(total_pixel)
        if zero_percentage > in_complete_rate or zero_percentage == in_complete_rate:
            invalid_list.append(folder)
            




#print (img.shape)
# (91, 109, 91, 100)
