"""
1. We already downloaded fMRI data.
2. Now we need to download the corresponding MRI data.
3. Generate a list of MRI ID. If two fMRI vs. one MRI, then repeat MRI ID, if
   one fMRI vs. two MRI, then repeat fMRI ID. So finally we have the same length
   ID list for fMRI and MRI.

Zhewei@ 9/16/2016

"""

import sys
import csv

def main(args):
    if len(args) < 2:
        usage( args[0] )
        pass
    else:
        work( args[1] )
        pass
    pass
    
def usage (programm):
    print ("usage: %s fMRI_AD_Filter"%(programm))
    
def work(fnames):
    with open(fnames,'r') as IDFile:
        fMRI_ImageID_List = IDFile.read()

    with open('idaSearch_9_17_2016.csv','r') as csvfile:
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
                if len(fMRI_tmp)>1 and len(MRI_tmp)>1:
                    raise ValueError('More than one MRI VS. More than one fMRI')
                if len(MRI_tmp)>1 and len(fMRI_tmp) == 1:
                    print ('Two MRI')
                    print (MRI_tmp)
                    id_tmp = fMRI_tmp[0]
                    fMRI_tmp = list()
                    for iMRI in MRI_tmp:
                        fMRI_tmp.append(id_tmp)
                    # raise ValueError('More than one MRI')
                if len(fMRI_tmp)>1 and len(MRI_tmp) == 1:
                    print ('Two fMRI')
                    print (fMRI_tmp)
                    id_tmp = MRI_tmp[0]
                    MRI_tmp = list()
                    for ifMRI in fMRI_tmp:
                        MRI_tmp.append(id_tmp)
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

    with open(fnames[1:],'w') as f:
        for ID in MRI_ImageID_List_tmp:
            f.write(str(ID))
            f.write(',')







        
            
if __name__ == "__main__":
    main( sys.argv )
    pass
