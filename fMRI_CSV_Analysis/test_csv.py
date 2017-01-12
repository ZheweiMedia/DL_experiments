"""
1. Analysis how many valid subject in csv file.
2. The csv file is idaSearch_1_11_2017.csv
3. Find the subject that has MRI and fMRI at the same time.


"""



import csv


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
           

    
    print(len(subject_list))
    print(len(set(subject_list)))









if __name__ == '__main__':
    main()
