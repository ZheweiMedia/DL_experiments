"""
Read the raw data in. Then save the data and corresponding image ID in two lista. Then we can do feature selection and store the selected feature back.

Zhewei @ 9/25/2015

"""

import gzip, os
import pickle as Pickle
import numpy
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2

TimeFrame = 130

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

class _VTK_Subject:
    # for VTK class HM01
    def __init__(self, imageID, data, DX_Group):
        self.DX_Group = DX_Group;
        self.Data = {imageID:data}

def data_to_list(validDataList):
    Label = list()
    Data = list()
    ID = list()
    for validData in validDataList:
        tmp_list = list(validData.baseline.keys())
        for key in tmp_list:
            try:
                if validData.baseline[str(key)].any():
                    Label.append(validData.DX_Group)
                    Data.append(validData.baseline[str(key)])
                    ID.append(str(key))
            except AttributeError:
                pass
        if validData.other != {}:
            tmp_list = list(validData.other.keys())
            for other_key in tmp_list:
                try:
                    if validData.other[str(other_key)].any():
                        Label.append(validData.DX_Group)
                        Data.append(validData.other[str(other_key)])
                        ID.append(str(key))
                except AttributeError:
                    pass
    return Label, Data, ID

def stackData(Data_list):
    Data = numpy.zeros([1,1])
    for data_no, data in enumerate(Data_list):
        if data_no == 0:
            Data = data;
        else:
            Data = numpy.hstack((Data, data))
    return Data.transpose()

def expandLabel(Label_list):
    Label = list()
    for label in Label_list:
        Label += [label]*TimeFrame
    return Label

os.chdir("/home/medialab/Zhewei/data")
Raw_data = gzip.open('Subjects_180_ADNC.pickle.gz', 'rb')
Subjects_data = Pickle.load(Raw_data)
Label, Data, ID = data_to_list(Subjects_data)

# Now Data is a list of array. We need to stack the data
# print (len(Label))
# print (len(Data))
# print (Data[0].shape)

Data = stackData(Data)
# print (Data.shape)

# Now Lable is for each subject. We need to expand to each time frame
Label_New = expandLabel(Label)
# print (len(Label))
# print (Label[0])

Data_new = SelectKBest(chi2, k=20).fit_transform(Data, Label_New)

# print (Data_new.shape)

# Now save it to a new data structure
VTK_DataList = list()
for label_no, label in enumerate(Label):
    data = Data_new[TimeFrame*label_no:TimeFrame*(label_no+1),:]
    # print (data.shape)
    subject = _VTK_Subject(ID[label_no], data, label)
    VTK_DataList.append(subject)

print (len(VTK_DataList))

with gzip.open('VTK_Subjects_180.pickle.gz', 'wb') as output_file:
        Pickle.dump(VTK_DataList, output_file)
print('Done!')
    
    



