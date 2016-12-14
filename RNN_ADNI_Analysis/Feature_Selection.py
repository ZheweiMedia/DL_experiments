"""
Read the raw data in. Then save the data and corresponding image ID in two lista. Then we can do feature selection and store the selected feature back.

Zhewei @ 9/25/2015

"""

import gzip, os
import pickle as Pickle
import numpy,math
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2, f_classif
from keras.layers import Input, Dense
from keras.models import Model

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
        print (validData.DX_Group)
        for key in tmp_list:
            try:
                if validData.baseline[str(key)].any():
                    Label.append(validData.DX_Group)
                    Data.append(validData.baseline[str(key)])
                    ID.append(str(key))
                    print (str(key))
                '''if str(key) == '228872':# test at here
                    print (validData.baseline[str(key)])'''
            except AttributeError:
                pass
            
        if validData.other != {}:
            tmp_list = list(validData.other.keys())
            print 
            for other_key in tmp_list:
                try:
                    if validData.other[str(other_key)].any():
                        Label.append(validData.DX_Group)
                        Data.append(validData.other[str(other_key)])
                        ID.append(str(other_key))
                        print(str(other_key))
                except AttributeError:
                    pass
    return Label, Data, ID


def ReNewData(validDataList, Data_New, ID, residual):
    no = 0
    if residual == 0:
        timeFrame = 130
    else:
        timeFrame = 129
    for validData in validDataList:
        tmp_list = list(validData.baseline.keys())
        for key in tmp_list:
            try:
                if validData.baseline[str(key)].any():
                    position = ID.index(str(key))
                    dataNew = Data_new[timeFrame*position:timeFrame*(position+1),:]
                    validData.baseline[str(key)] = dataNew
                    no += 1
                if str(key) == '228872':# test at here
                    for i in range(validData.baseline[str(key)].shape[1]):
                        print (validData.baseline[str(key)][:,i])
                    print (validData.baseline[str(key)].shape)
            except AttributeError:
                pass
        if validData.other != {}:
            tmp_list = list(validData.other.keys())
            for other_key in tmp_list:
                try:
                    if validData.other[str(other_key)].any():
                        position = ID.index(str(other_key))
                        dataNew = Data_new[timeFrame*position:timeFrame*(position+1),:]
                        validData.other[str(other_key)] = dataNew
                        no += 1
                except AttributeError:
                    pass
    print (no)
    return validDataList

def stackData(Data_list):
    Data = numpy.zeros([1,1])
    for data_no, data in enumerate(Data_list):
        if data_no == 0:
            # Data = difference_of_data(data)
            Data = data
        else:
            # Data = numpy.hstack((Data, difference_of_data(data)))
            Data = numpy.hstack((Data, data))
    return Data.transpose()

def expandLabel_for_origin(Label_list):
    Label = list()
    for label in Label_list:
        Label += [label]*(TimeFrame)
    return Label

def expandLabel_for_residual(Label_list):
    Label = list()
    for label in Label_list:
        Label += [label]*(TimeFrame-1)
    return Label

def difference_of_data(dataList):
    timeframe = dataList[0].shape[1]
    print (timeframe)
    new_list = list()
    for data in dataList:
        tmp_data = numpy.zeros([1,1])
        for i in range(1, timeframe):
            if i == 1:
                tmp_data = data[:,i]-data[:,i-1]
            else:
                tmp_data = numpy.vstack((tmp_data, data[:,i]-data[:,i-1]))
        new_list.append(tmp_data.transpose())
    return new_list

def Normalize_Each_subject_as_NDB(dataList):
    for data in dataList:
        featureNo = data.shape[0]
        for i in range(featureNo):
            data[i,:] = (data[i,:]-numpy.mean(data[i,:]))/numpy.linalg.norm(data[i,:])
            print (numpy.mean(data[i,:]))

    print(dataList[0][0,:])
    return dataList


def Normlize_Each_subject_as_Zero_One(dataList):
    print (len(dataList))
    for data in dataList:
        featureNo = data.shape[0]
        for i in range(featureNo):
            max_value = numpy.amax(data[i,:])
            min_value = numpy.amin(data[i,:])
            data[i,:] = (data[i,:]-min_value)/(max_value-min_value)
    print(dataList[0][0,:])

    return dataList
def timesData(DataArray):
    for i in range(DataArray.shape[1]):
        DataArray[:,i] = DataArray[:,i]*100000
    return DataArray

def Autoencoder(StackedData):
    # stack data together. Daone
    # 
    
    # data = StackedData.transpose()
    input_feature = StackedData.shape[1]
    print (input_feature)

    x_train = StackedData[0:math.floor(StackedData.shape[1]*0.8), :]
    x_test = StackedData[math.floor(StackedData.shape[1]*0.8):, ]
    input_data = Input(shape=(input_feature,))
    encoded = Dense(200, activation='relu')(input_data)
    encoded = Dense(100, activation='relu')(encoded)
    encoded = Dense(50, activation='relu')(encoded)
    encoded = Dense(20, activation='relu')(encoded)

    decoded = Dense(50, activation='relu')(encoded)
    decoded = Dense(100, activation='relu')(decoded)
    decoded = Dense(200, activation='relu')(decoded)
    decoded = Dense(input_feature, activation='sigmoid')(decoded)

    autoencoder = Model(input=input_data, output=decoded)
    autoencoder.compile(optimizer='adadelta', loss='mean_squared_error')
    encoder = Model(input=input_data, output=encoded)
    autoencoder.fit(x_train, x_train,
                nb_epoch=30,
                batch_size=10,
                shuffle=True,
                validation_data=(x_test, x_test))
    
    return encoder.predict(StackedData)

def print_Each_Subject(validDataList):
    no = 0
    for validData in validDataList:
        tmp_list = list(validData.baseline.keys())
        subject = list()
        for key in tmp_list:
            try:
                if validData.baseline[str(key)].any():
                    subject.append(str(key))
                    no += 1
            except AttributeError:
                pass
        if validData.other != {}:
            tmp_list = list(validData.other.keys())
            for other_key in tmp_list:
                try:
                    if validData.other[str(other_key)].any():
                       subject.append(str(other_key))
                       no += 1
                except AttributeError:
                    pass
        if (subject):
            print (subject, validData.DX_Group)
    



os.chdir("/home/medialab/Zhewei/data")
Raw_data = gzip.open('ADNC_Nitime_Z_Raw.pickle.gz', 'rb')
Subjects_data = Pickle.load(Raw_data)
Label, Data, ID = data_to_list(Subjects_data)

# print_Each_Subject(Subjects_data)

# Now Data is a list of array [featureNo, timestep]. We need to stack the data
# print (len(Label))
# print (len(Data))
print (Data[0].shape)

# If we use residual
# Data = difference_of_data(Data)# Now Data is a list of array [featureNo, timestep-1].
# Now Lable is for each subject. We need to expand to each time frame
Label_New = expandLabel_for_origin(Label)
# Label_New = expandLabel_for_residual(Label)
# print (len(Label))
print (len(Label_New))

# Normalize the data
Data = Normalize_Each_subject_as_NDB(Data)
# Data = Normlize_Each_subject_as_Zero_One(Data)
print('Here:', Data[0].shape)
Data = stackData(Data)
print (Data.shape)
print ((Data[0:130,0]))


Data_new =  Autoencoder(Data)
print (Data_new[10])
# Data_new = SelectKBest(chi2, k=120).fit_transform(Data, Label_New)
'''feature_index = set([57,	55,	100,	53,	62,
	         73,	107,	62,	107,	26,
	         50,	62,	91,	111,	100,
	         62,	107,	107,	62,	40,
	         112,	40,	112,	107,	108,
	         90,	54,	111,	107,	45,
	         107,	74,	50,	91,	26,
	         107,	107,	7,	25,	45,
	         26,	51,	112,	108,	47,
	         56,	2,	113,	53,	49,
                 2,	2,	5,	2,	53,
	         50,	47,	50,	53,	7,
	         2,	55,	53,	51,	90,
	         54,	55,	5,	57,	25,
	         48,	26,	51,	56,	98,
	         74,	2,	7,	48,	25,
	         49,	50,	74,	70,	9,
	         9,	7,	107,	5,	26,
	         5,	2,	5,	5,	2,
	         2,	56,	5,	111,	2,
                 82,	119,	84,	115,	84,
	         118,	9,	118,	117,	84,
	         96,	120,	70,	96,	79,
	         114,	78,	53,	82,	61,
	         118,	66,	117,	84,	96,
	         70,	116,	84,	96,	100,
	         98,	79,	84,	81,	98,
	         53,	119,	114,	64,	10,
	         114,	84,	101,	49,	81,
	         117,	98,	19,	118,	117,
                 1,	51,	9,	84,	82,
	         59,	5,	93,	116,	52,
	         27,	99,	54,	70,	2,
	         84,	14,	5,	61,	82,
	         89,	14,	59,	40,	40,
	         58,	84,	49,	49,	31,
	         49,	34,	48,	67,	53,
	         98,	57,	83,	34,	8,
	         34,	50,	34,	47,	1,
	         84,	55,	3,	83,	39])'''
feature_index = set([57,	55,	100,  	53])
feature_index = numpy.array(list(feature_index))
feature_index = feature_index-1
# Data_new = Data[:, list(feature_index)]
Data_new = timesData(Data)
# print (Data_new[0:130,:])
# print (Data_new.shape)

# Now save it back. Travel the data structure, and feed the data back.
# print (ID)
NewSubjectsData = ReNewData(Subjects_data, Data_new, ID, 0)   


os.chdir("/home/medialab/Zhewei/data/")
with gzip.open('ADNC_BandPass_times100000.pickle.gz', 'wb') as output_file:
    Pickle.dump(NewSubjectsData, output_file)


print('Done!')
    
    



