"""
1. Analysis ADNI2 data in .csv file.
2. DCM2NII by run a shell script in this python progamme.



Zhewei@ 9/7/2016
"""
import os
from subprocess import call
from collections import defaultdict
import csv

badDataList = [229146, 249406, 249407, 282008, 297689,
               312870, 313953, 316542, 317121, 322060,
               336708, 341918, 348187, 365243, 373523,
               368889, 377213, 424849, 310441, 348166,
               257275, 322438, 272229, 296788, 303081,
               274420, 314141, 642409, 248516, 375331]

class _EachSubject:
    # each subject is a element of a list
    def __init__(self, SubjectID, Sex, DX_Group, imageID):
        self.Sex = Sex
        self.DX_Group = DX_Group
        self.SubjectID = SubjectID
        # baseline is a dict, imageID:data
        self.baseline = {imageID:list()}
        # otherdata after baseline is also a dict, imageID:data
        self.other = {}

def printAnalysis(ValidData):
    labels = defaultdict(list)
    for idata in ValidData:
        if idata.DX_Group not in labels.keys():
            labels[idata.DX_Group] = [1,0]
            if idata.other != {}:
                labels[idata.DX_Group][1] += 1
        else:
            labels[idata.DX_Group][0] += 1
            if idata.other != {}:
                labels[idata.DX_Group][1] += 1
                # print (idata.SubjectID)
    for ikey in labels.keys():
        print(ikey, 'We have',labels[ikey][0],'subjects,', labels[ikey][1], 'of them have more once scan.')

def outputImageId(ValidData, DX_Group):
    # output the images ID for AD
    print ('Images ID for', DX_Group, 'is:')
    with open(DX_Group,'w') as f:
        for idata in ValidData:
            if idata.DX_Group == DX_Group:
                print (list(idata.baseline.keys()))
                for imageID in list(idata.baseline.keys()):
                    f.write(str(imageID))
                    f.write(',')
                if idata.other != {}:
                    print (list(idata.other.keys()))
                    for imageID in list((idata.other.keys())):
                        f.write(str(imageID))
                        f.write(',')


def ImageIDFilter(ValidData, DX_Group, badDataList):
    #output the valid image ID
    validList = list()
    print ('Valid Images ID for', DX_Group, ':')
    for idata in ValidData:
        if idata.DX_Group == DX_Group:
            ImageIDList_Baseline = list(idata.baseline.keys())
            for imageID in ImageIDList_Baseline:
                if int(imageID) not in badDataList:
                    validList.append(imageID)
            if idata.other != {}:
                ImageIDList_Other = list(idata.other.keys())
                for imageID in ImageIDList_Other:
                    if int(imageID) not in badDataList:
                        validList.append(imageID)
    print (len(validList))
    print (validList)
                        
def main():
    with open('idaSearch_9_07_2016_ADNI2.csv','r') as csvfile:
        reader = csv.DictReader(csvfile)
        wholeDataOFcsv = []
        for row in reader:
            wholeDataOFcsv.append(row)

    #analysis wholeDataOFcsv now
    iSubjectID = None
    jSubjectID = None
    iAge = 0
    ValidData = list()
    _Subject = []
    for row in wholeDataOFcsv:
        if row['Description'] == 'Resting State fMRI':
            if iSubjectID == None:
                iSubjectID = row['Subject ID']
                iAge = row['Age']
                _Subject = _EachSubject(row['Subject ID'], row['Sex'],
                                        row['DX Group'], row['Image ID'])
            else:
                jSubjectID = row['Subject ID']
                if jSubjectID == iSubjectID:
                    if row['Age'] < iAge:
                        raise ValueError('Wring Baseline Age!')
                    _Subject.other[row['Image ID']] = list()
                    iAge = row['Age']
                else:
                    ValidData.append(_Subject)
                    _Subject = _EachSubject(row['Subject ID'], row['Sex'],
                                            row['DX Group'], row['Image ID'])
                    iSubjectID = jSubjectID
                    iAge = row['Age']
                    
                        
    ValidData.append(_Subject)
    print ('\n')
    print ('*'*40)
    print('Totally we have', len(ValidData), 'subjects.')
    # print(ValidData[-2].SubjectID)
    printAnalysis(ValidData)
    print ('*'*40)
    print ('\n')

    # print ImageID and transform DCM to NII
    outputImageId(ValidData, 'AD')
    # os.system("bash Step1_DCM2NII.sh Normal")    

    # print the valid imaeg ID
    ImageIDFilter(ValidData, 'AD', badDataList)











if __name__ == '__main__':
    main()
                    
            
