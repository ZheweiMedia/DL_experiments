"""
1. Analysis how many valid subject in csv file.
2. The csv file is idaSearch_1_11_2017.csv
3. Find the subject that has MRI and fMRI at the same time.
4. Generate image ID.
5. usage: python3.5 csv_Subject.py AD


"""



import csv
import sys
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
    with open('idaSearch_1_11_2017.csv','r') as csvfile:
        reader = csv.DictReader(csvfile)
        wholeDataOfCSV = list()
        for row in reader:
            wholeDataOfCSV.append(row)

    # analysis wholeDataOfCSV now
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
            if row['Description'] == 'Resting State fMRI' :
                # \or row['Description'] == 'Extended Resting State fMRI':
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
                if row['Description'] == 'Resting State fMRI' :
                   # \or row['Description'] == 'Extended Resting State fMRI':
                    fMRI_ImageID = row['Image ID']
                if row['Description'] == 'MPRAGE':
                    MRI_ImageID = row['Image ID']
                iAge = row['Age']
            else:
                # during a scan
                if row['Description'] == 'Resting State fMRI' :
                   # \or row['Description'] == 'Extended Resting State fMRI':
                    fMRI_ImageID = row['Image ID']
                if row['Description'] == 'MPRAGE':
                    MRI_ImageID = row['Image ID']

    
    print('Totally we have subjects :', len(ValidData))

    """
    # print all the image IDs of a group

    MRI_list = list()
    fMRI_list = list()
    Subjects_in_group = 0

    with open(str(sys.argv[1])+'_MRI_ImageID','w') as f:
        for subject in ValidData:
            if subject.DX_Group == str(sys.argv[1]):
                Subjects_in_group += 1
                MRI_list.append(subject.MRI_baseline)
                f.write(subject.MRI_baseline)
                f.write(',')
                if subject.MRI_other:
                    for ID in subject.MRI_other:
                        MRI_list.append(ID)
                        f.write(ID)
                        f.write(',')

    print('We have', Subjects_in_group, 'subjects in', str(sys.argv[1]))
    print('MRI Image of', str(sys.argv[1]), ':', len(MRI_list))

    with open(str(sys.argv[1])+'_fMRI_ImageID','w') as f:
        for subject in ValidData:
            if subject.DX_Group == str(sys.argv[1]):
                fMRI_list.append(subject.fMRI_baseline)
                f.write(subject.fMRI_baseline)
                f.write(',')
                if subject.fMRI_other:
                    for ID in subject.fMRI_other:
                        fMRI_list.append(ID)
                        f.write(ID)
                        f.write(',')
    print('fMRI Image of', str(sys.argv[1]), ':', len(fMRI_list))

    """

    # save the data structure
    with gzip.open("Original_imageID.gz", "wb") as output_file:
        pickle.dump(ValidData, output_file)










if __name__ == '__main__':
    main()
