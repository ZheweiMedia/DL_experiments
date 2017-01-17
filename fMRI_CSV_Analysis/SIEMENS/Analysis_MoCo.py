"""
1. Analysis how many valid subject of SIEMENS in csv file.
2. The csv file is ida_ADNIGO_ADNI2.csv
3. Find the subject that has MRI and fMRI at the same time.


"""



import csv
import gzip
import pickle


class _EachSubject:
    # each subject is a element of a list
    def __init__(self, SubjectID, DX_Group, MRI_imageID, fMRI_imageID):
        self.DX_Group = DX_Group
        self.SubjectID = SubjectID
        # baseline 
        self.MRI_baseline = MRI_imageID
        self.fMRI_baseline = fMRI_imageID
        # otherdata after baseline 
        self.MRI_other = list()
        self.fMRI_other = list()

def main():
    with open('ida_ADNIGO_ADNI2.csv','r') as csvfile:
        reader = csv.DictReader(csvfile)
        wholeDataOfCSV = list()
        for row in reader:
            wholeDataOfCSV.append(row)

    # analysis wholeDataOfCSV now
    subject_list = list()

    for row in wholeDataOfCSV:
       subject_list.append(row['Subject ID'])

    # print(len(subject_list))
    print('Totally we have',len(set(subject_list)), 'Subjects in ADNI GO and ADNI 2.')


    
    # analysis wholeDataOfCSV now

    # For MoCo series
    MRI_ImageID = None
    fMRI_ImageID = None
    Subject_ID = None
    Baseline_flag = False # False means no baseline exist
    DX_group = None
    iAge = 0
    ValidData = list()
    _Subject = None

    for row in wholeDataOfCSV:
        if Subject_ID != row['Subject ID']:
            # end of a subject
            if MRI_ImageID != None and fMRI_ImageID != None:
                if Baseline_flag == False:
                    # False means no baseline exist
                    _Subject = _EachSubject(Subject_ID, DX_group, MRI_ImageID, fMRI_ImageID)
                    Baseline_flag = True
                else:
                    _Subject.MRI_other.append(MRI_ImageID)
                    _Subject.fMRI_other.append(fMRI_ImageID)

            if _Subject != None:
                ValidData.append(_Subject)
            MRI_ImageID = None
            fMRI_ImageID = None
            if row['Description'] == 'MoCoSeries' :
                fMRI_ImageID = row['Image ID']
            if row['Description'] == 'MPRAGE':
                MRI_ImageID = row['Image ID']
            Subject_ID = row['Subject ID']
            iAge = row['Age']
            DX_group = row['DX Group']
            Baseline_flag = False
            _Subject = None
            

        if Subject_ID == row['Subject ID']:
            # same subject
            if row['Age'] != iAge:
                # end of a scan
                if MRI_ImageID != None and fMRI_ImageID != None:
                    if Baseline_flag == False:
                        # False means no baseline exist
                        _Subject = _EachSubject(Subject_ID, DX_group, MRI_ImageID, fMRI_ImageID)
                        Baseline_flag = True
                    else:
                        _Subject.MRI_other.append(MRI_ImageID)
                        _Subject.fMRI_other.append(fMRI_ImageID)
                MRI_ImageID = None
                fMRI_ImageID = None
                if row['Description'] == 'MoCoSeries' :
                    fMRI_ImageID = row['Image ID']
                if row['Description'] == 'MPRAGE':
                    MRI_ImageID = row['Image ID']
                iAge = row['Age']
            else:
                # during a scan
                if row['Description'] == 'MoCoSeries' :
                    fMRI_ImageID = row['Image ID']
                if row['Description'] == 'MPRAGE':
                    MRI_ImageID = row['Image ID']

    
    print('Totally we have subjects :', len(ValidData), 'for MoCoSeries')

    # save the data structure
    with gzip.open("Original_Moco_imageID.gz", "wb") as output_file:
        pickle.dump(ValidData, output_file)

    MRI_list = list()
    fMRI_list = list()
    Subjects_in_group = 0

    with open('Original_MRI_ImageID','w') as f:
        for subject in ValidData:
            if subject.DX_Group == "AD" or subject.DX_Group == "Normal":
                Subjects_in_group += 1
                if subject.MRI_baseline != None:
                    MRI_list.append(subject.MRI_baseline)
                    f.write(subject.MRI_baseline)
                    f.write(',')
                if subject.MRI_other:
                    for ID in subject.MRI_other:
                        if ID != None:
                            MRI_list.append(ID)
                            f.write(ID)
                            f.write(',')

    print('We have', Subjects_in_group, 'subjects.')
    print('MRI Image:', len(MRI_list))

    Subjects_in_group = 0
    with open('Original_fMRI_ImageID','w') as f:
        for subject in ValidData:
            if subject.DX_Group == "AD" or subject.DX_Group == "Normal":
                Subjects_in_group += 1
                if subject.MRI_baseline != None:
                    fMRI_list.append(subject.fMRI_baseline)
                    f.write(subject.fMRI_baseline)
                    f.write(',')
                if subject.MRI_other:
                    for ID in subject.fMRI_other:
                        if ID != None:
                            fMRI_list.append(ID)
                            f.write(ID)
                            f.write(',')

    print('We have', Subjects_in_group, 'subjects.')
    print('fMRI Image:', len(fMRI_list))





    Moco_list = list()
    for subject in ValidData:
        Moco_list.append(subject.SubjectID)


    # For ASL
    MRI_ImageID = None
    fMRI_ImageID = None
    Subject_ID = None
    Baseline_flag = False # False means no baseline exist
    DX_group = None
    iAge = 0
    ValidData = list()
    _Subject = None

    for row in wholeDataOfCSV:
        if Subject_ID != row['Subject ID']:
            # end of a subject
            if MRI_ImageID != None and fMRI_ImageID != None:
                if Baseline_flag == False:
                    # False means no baseline exist
                    _Subject = _EachSubject(Subject_ID, DX_group, MRI_ImageID, fMRI_ImageID)
                    Baseline_flag = True
                else:
                    _Subject.MRI_other.append(MRI_ImageID)
                    _Subject.fMRI_other.append(fMRI_ImageID)

            if _Subject != None:
                ValidData.append(_Subject)
            MRI_ImageID = None
            fMRI_ImageID = None
            if row['Description'] == 'ASL_PERFUSION' or \
               row['Description'] == 'ASL PERFUSION' or \
               row['Description'] == 'ASL PERFUSION(EYES OPEN)' or \
               row['Description'] == 'ASL PERFUSION____EYES_OPEN' or \
               row['Description'] == 'ASL' or \
               row['Description'] == 'ASL PERFUSION-EYES OPEN' or \
               row['Description'] == 'ASL PERF' :
                fMRI_ImageID = row['Image ID']
            if row['Description'] == 'MPRAGE':
                MRI_ImageID = row['Image ID']
            Subject_ID = row['Subject ID']
            iAge = row['Age']
            DX_group = row['DX Group']
            Baseline_flag = False
            _Subject = None
            

        if Subject_ID == row['Subject ID']:
            # same subject
            if row['Age'] != iAge:
                # end of a scan
                if MRI_ImageID != None and fMRI_ImageID != None:
                    if Baseline_flag == False:
                        # False means no baseline exist
                        _Subject = _EachSubject(Subject_ID, DX_group, MRI_ImageID, fMRI_ImageID)
                        Baseline_flag = True
                    else:
                        _Subject.MRI_other.append(MRI_ImageID)
                        _Subject.fMRI_other.append(fMRI_ImageID)
                MRI_ImageID = None
                fMRI_ImageID = None
                if row['Description'] == 'ASL_PERFUSION'  or \
                   row['Description'] == 'ASL PERFUSION' or \
                   row['Description'] == 'ASL PERFUSION(EYES OPEN)' or \
                   row['Description'] == 'ASL PERFUSION____EYES_OPEN'  or \
                   row['Description'] == 'ASL' or \
                   row['Description'] == 'ASL PERFUSION-EYES OPEN' or \
                   row['Description'] == 'ASL PERF' :
                    fMRI_ImageID = row['Image ID']
                if row['Description'] == 'MPRAGE':
                    MRI_ImageID = row['Image ID']
                iAge = row['Age']
            else:
                # during a scan
                if row['Description'] == 'ASL_PERFUSION'  or \
                   row['Description'] == 'ASL PERFUSION' or \
                   row['Description'] == 'ASL PERFUSION(EYES OPEN)' or \
                   row['Description'] == 'ASL PERFUSION____EYES_OPEN'  or \
                   row['Description'] == 'ASL' or \
                   row['Description'] == 'ASL PERFUSION-EYES OPEN' or \
                   row['Description'] == 'ASL PERF' :
                    fMRI_ImageID = row['Image ID']
                if row['Description'] == 'MPRAGE':
                    MRI_ImageID = row['Image ID']

    
    print('Totally we have subjects :', len(ValidData), 'for ASL.')

    ASL_list = list()
    for subject in ValidData:
        ASL_list.append(subject.SubjectID)

    print('Differences of MoCo and ASL:')
    for subject in Moco_list:
        if subject not in ASL_list:
            print (subject)








if __name__ == '__main__':
    main()
