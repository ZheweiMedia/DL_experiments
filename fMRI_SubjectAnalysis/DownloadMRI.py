"""
1. We already downloaded fMRI data.
2. Now we need to download the corresponding MRI data.

Zhewei@ 9/16/2016

"""

import csv

fMRI_ImageID_List = ['346237', '372812', '398684', '358614', '293808', '335306', '293809', '264987', '390346', '264986', '335307', '258600', '272411', '340024', '272407', '302042', '258605', '302039', '393209', '340021', '287992', '310925', '310931', '336551', '287986', '336552', '322000', '362021', '346367', '346359', '394330', '322009', '360323', '373417', '390453', '301395', '343571', '321520', '306073', '327941', '348646', '360317', '382187', '258955', '300352', '396527', '396530', '272535', '341972', '280778', '359770', '412884', '297106', '322347', '300334', '317435', '343285', '363190', '343912', '400431', '372599', '358050', '345555', '372471', '358811', '415205', '228872', '248870', '297847', '263860', '357475', '415178', '372254', '389296', '376933', '368413', '291229', '347092', '323796', '295969', '367094', '342048', '316009', '300043', '369943', '322371', '342223', '306375', '352396', '335235', '376259', '342326', '370085', '358899', '341793', '369299', '395989', '358857', '342278', '353265', '392395', '364935', '342915', '369264', '347402', '348491', '398911', '360702', '373027', '358777', '371972', '385034', '381307', '367567', '379705', '342514']

with open('idaSearch_9_16_2016.csv','r') as csvfile:
    reader = csv.DictReader(csvfile)
    wholeDataOFcsv = []
    for row in reader:
        wholeDataOFcsv.append(row)


iSubjID = None
iAge = None
iMRI_ImageID = None
ifMRI_ImageID = None
Flag_MRI = False
Flag_fMRI = False
MRI_ImageID_List_tmp = list()
fMRI_ImageID_List_tmp = list()

MRI_tmp = list()
fMRI_tmp = list()

for row in wholeDataOFcsv:
    if iSubjID == None:
        iSubjID = row['Subject ID']
        iAge = row['Age']
        if row['Description'] == 'MPRAGE':
            MRI_tmp.append(row['Image ID'])
            Flag_MRI = True
        if row['Description'] == 'Resting State fMRI':
            if row['Image ID'] in fMRI_ImageID_List:
                fMRI_tmp.append(row['Image ID'])
                Flag_fMRI = True
    elif iSubjID == row['Subject ID'] and iAge == row['Age']:
        # same scan
        if row['Description'] == 'MPRAGE':
            MRI_tmp.append(row['Image ID'])
            Flag_MRI = True
        if row['Description'] == 'Resting State fMRI':
            if row['Image ID'] in fMRI_ImageID_List:
                fMRI_tmp.append(row['Image ID'])
                Flag_fMRI = True
    elif iSubjID != row['Subject ID'] or iAge != row['Age']:
        # different scan
        if Flag_MRI == True and Flag_fMRI == True:
            # both exist
            if len(MRI_tmp)>1:
                print ('Two MRI')
                print (MRI_tmp)
                # raise ValueError('More than one MRI')
            if len(fMRI_tmp)>1:
                print ('Two fMRI')
                print (fMRI_tmp)
                # raise ValueError('More than one fMRI')
            MRI_ImageID_List_tmp += MRI_tmp
            fMRI_ImageID_List_tmp += fMRI_tmp
        Flag_MRI = False
        Flag_fMRI = False
        iSubjID = row['Subject ID']
        iAge = row['Age']
        MRI_tmp = list()
        fMRI_tmp = list()
        if row['Description'] == 'MPRAGE':
            MRI_tmp.append(row['Image ID'])
            Flag_MRI = True
        if row['Description'] == 'Resting State fMRI':
            if row['Image ID'] in fMRI_ImageID_List:
                fMRI_tmp.append(row['Image ID'])
                Flag_fMRI = True

print ('MRI Image IDs:')
print (MRI_ImageID_List_tmp)
print ('fMRI Image IDs:')
print (fMRI_ImageID_List_tmp)
print ('We have valid MRI Images:',len(MRI_ImageID_List_tmp))
print ('We have valid fMRI Images:',len(fMRI_ImageID_List_tmp))

print ('fMRI don\'t have corresponding MRI:')
for ID in fMRI_ImageID_List:
    if ID not in fMRI_ImageID_List_tmp:
        print(ID)
        
            
