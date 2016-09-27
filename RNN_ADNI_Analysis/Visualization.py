"""
1. 


Zhewei @ 9/27/2016

"""

import os, gzip
import pickle as Pickle
import matplotlib.pyplot as pyplot


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

def visualize_two_dimension_postion(validDataList):
    pyplot.figure(1)
    ADNo = 0
    NCNo = 0
    for validData in validDataList:
        tmp_list = list(validData.baseline.keys())
        for key in tmp_list:
            try:
                if validData.baseline[str(key)].any():
                    tmp_data = validData.baseline[str(key)]
                    timeStep = tmp_data.shape[0]
                    if validData.DX_Group == 'AD':
                        color = (0.5+ADNo/180, 0.0, 0.0)
                        ADNo += 1
                        plotAD, = pyplot.plot(tmp_data[:,0], tmp_data[:,1], 'o-', color = color, label = 'AD', alpha = 0.5)
                    else:
                        color = (0,0,0.5+NCNo/180)
                        NCNo += 1
                        plotNC, = pyplot.plot(tmp_data[:,0], tmp_data[:,1], 'o-', color = color, label = 'NC', alpha = 0.5)
            except AttributeError:
                pass
            if validData.other != {}:
                tmp_list = list(validData.other.keys())
                for other_key in tmp_list:
                    try:
                        if validData.other[str(other_key)].any():
                            tmp_data = validData.other[str(other_key)]
                            timeStep = tmp_data.shape[0]
                            if validData.DX_Group == 'AD':
                                color = (0.5+ADNo/180, 0.0, 0.0)
                                ADNo += 1
                                plotAD, = pyplot.plot(tmp_data[:,0], tmp_data[:,1], 'o-', color = color, label = 'AD', alpha = 0.5)
                            else:
                                color = (0,0,0.5+NCNo/180)
                                NCNo += 1
                                plotNC, = pyplot.plot(tmp_data[:,0], tmp_data[:,1], 'o-', color = color, label = 'NC', alpha = 0.5)
                    except AttributeError:
                        pass

    pyplot.legend(handles=[plotAD, plotNC], loc = 4)
    pyplot.show()


def visualize_two_dimension_sequence(validDataList):
    pyplot.figure(1)
    ADNo = 0
    NCNo = 0
    for validData in validDataList:
        tmp_list = list(validData.baseline.keys())
        for key in tmp_list:
            try:
                if validData.baseline[str(key)].any():
                    tmp_data = validData.baseline[str(key)]
                    timeStep = tmp_data.shape[0]
                    if tmp_data[0,0]< 0.06:
                        print(str(key))
                    if validData.DX_Group == 'AD':
                        color = (0.5+ADNo/180, 0.0, 0.0)
                        ADNo += 1
                        plotAD, = pyplot.plot(range(timeStep), tmp_data[:,0], 'o-', color = color, label = 'AD', alpha = 0.5)
                    else:
                        color = (0,0,0.5+NCNo/180)
                        NCNo += 1
                        plotNC, = pyplot.plot(range(timeStep), tmp_data[:,0], 'o-', color = color, label = 'NC', alpha = 0.5)
            except AttributeError:
                pass
            if validData.other != {}:
                tmp_list = list(validData.other.keys())
                for other_key in tmp_list:
                    try:
                        if validData.other[str(other_key)].any():
                            tmp_data = validData.other[str(other_key)]
                            timeStep = tmp_data.shape[0]
                            if tmp_data[0,0]< 0.06:
                                print(str(key))
                            if validData.DX_Group == 'AD':
                                color = (0.5+ADNo/180, 0.0, 0.0)
                                ADNo += 1
                                plotAD, = pyplot.plot(range(timeStep), tmp_data[:,0], 'o-', color = color, label = 'AD', alpha = 0.5)
                            else:
                                color = (0,0,0.5+NCNo/180)
                                NCNo += 1
                                plotNC, = pyplot.plot(range(timeStep), tmp_data[:,0], 'o-', color = color, label = 'NC', alpha = 0.5)
                    except AttributeError:
                        pass

    pyplot.legend(handles=[plotAD, plotNC], loc = 4)
    pyplot.show()


    
os.chdir("/home/medialab/Zhewei/data")
Raw_data = gzip.open('Feature_Selection_Normalize_as_one_forTwo.pickle.gz', 'rb')
Subjects_data = Pickle.load(Raw_data)

visualize_two_dimension_postion(Subjects_data)
visualize_two_dimension_sequence(Subjects_data)
                            
                        
