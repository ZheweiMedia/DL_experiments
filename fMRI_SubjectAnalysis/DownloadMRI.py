"""
1. We already downloaded fMRI data.
2. Now we need to download the corresponding MRI data.

Zhewei@ 9/16/2016

"""

import csv

fMRI_ImageID_List = ['238623', '303069', '240811', '371994', '304790', '243902', '322442', '286519', '361612', '287493', '361431', '254581', '273218', '391150', '335999', '290923', '257271', '395105', '340048', '274579', '297353', '259654', '299159', '346113', '397604', '274825', '259806', '260580', '346801', '277135', '301757', '398533', '395980', '265132', '265125', '336212', '389367', '336216', '289854', '289846', '268914', '286464', '286461', '349320', '405706', '311257', '311258', '268917', '349326', '279468', '298515', '279472', '362889', '319632', '319634', '298510', '281881', '303083', '281887', '326301', '326298', '361294', '337404', '363620', '283913', '350450', '319211', '238540', '238542', '253525', '296769', '352724', '375151', '296863', '368950', '369618', '340743', '300088', '314505', '343935', '368923', '308182', '262078', '296612', '320519', '268925', '321439', '297183', '401398', '266634', '296891', '399633', '315798', '272223', '327813', '354839', '403913', '301492', '273503', '296638', '409002', '353130', '316619', '269279', '347150', '401663', '288745', '306127', '315850', '383452', '355339', '338813', '370595', '246871', '300743', '261918', '234917', '305150', '251325', '270397', '371750', '255986', '391167', '337977', '274090', '292605', '280365', '321203', '302555', '282646', '325233', '303248', '414942', '362235', '290815', '337993', '366388', '309727', '289559', '366944', '310188', '289656', '387091', '334140', '350835', '348304', '350735', '353800', '266208', '350046', '398573', '310240', '289588', '267713', '302615', '346744', '285316', '399995', '365086', '264214', '285011', '401073', '330165', '279084', '336199', '308403', '308418']

with open('idaSearch_9_16_2016_ADNI2_fMRI_MRI.csv','r') as csvfile:
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

for row in wholeDataOFcsv:
    if iSubjID == None:
        iSubjID = row['Subject ID']
        iAge = row['Age']
        if row['Description'] == 'MPRAGE':
            MRI_tmp.append(row['Image ID'])
            Flag_MRI = True
        if row['Description'] == 'Resting State fMRI':
            if row['Image ID'] in fMRI_ImageID_List:
                ifMRI_ImageID = row['Image ID']
                Flag_fMRI = True
    elif iSubjID == row['Subject ID'] and iAge == row['Age']:
        # same scan
        if row['Description'] == 'MPRAGE':
            MRI_tmp.append(row['Image ID'])
            Flag_MRI = True
        if row['Description'] == 'Resting State fMRI':
            if Flag_fMRI == True:
                if row['Image ID'] in fMRI_ImageID_List:
                    print (ifMRI_ImageID)
                    print (row['Image ID'])
                    raise ValueError('ALready have A fMRI.')
            else:
                if row['Image ID'] in fMRI_ImageID_List:
                    ifMRI_ImageID = row['Image ID']
                    Flag_fMRI = True
    elif iSubjID != row['Subject ID'] or iAge != row['Age']:
        # different scan
        if Flag_MRI == True and Flag_fMRI == True:
            # both exist
            print (ifMRI_ImageID)
            if len(MRI_tmp)>1:
                raise ValueError('More than one MRI')
            if ifMRI_ImageID in fMRI_ImageID_List:
                MRI_ImageID_List_tmp.append(MRI_tmp[0])
                print (iMRI_ImageID)
                fMRI_ImageID_List_tmp.append(ifMRI_ImageID)
        Flag_MRI = False
        Flag_fMRI = False
        iSubjID = row['Subject ID']
        iAge = row['Age']
        MRI_tmp = list()
        if row['Description'] == 'MPRAGE':
            MRI_tmp.append(row['Image ID'])
            Flag_MRI = True
        if row['Description'] == 'Resting State fMRI':
            if row['Image ID'] in fMRI_ImageID_List:
                ifMRI_ImageID = row['Image ID']
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
        
            
