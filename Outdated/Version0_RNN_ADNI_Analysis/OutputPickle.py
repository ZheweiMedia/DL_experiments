"""
This program used to generate general pickle files from the raw data from MatLab.

Label of NC:    0
Label of AD:    1
Label of EMCI:  2
Label of LMCI:  3
Label of SMC:   4

all data read or write in ./data

Usage:  python data/AD.txt AD 32
Output: an array with the 3D shape SampleNo*FrameNo*FeatureNo

@Zhewei
5/21/2016

"""

import sys,os
import gzip
import pickle as Pickle
import numpy as np

FrameNo = 130
FeatureNo = 120


def main(args):
    if len(args) < 4:
        usage( args[0] )
        pass
    else:
        work( args[1],args[2],args[3] )
        pass
    pass

def usage (programm):
    print ("usage: %s data/AD or NC.txt groupName SampleNo"%(programm))

def work(fname, group, No):
    if not os.path.isfile(fname):
        raise (IOError, "%s is not exist!"%( fname ))
        pass
    # group
    if group == 'NC':
        label = 0
    if group == 'AD':
        label = 1
    if group == 'EMCI':
        label = 2
    if group == 'LMCI':
        label = 3
    if group == 'SMC':
        label = 4
    # SampleNo
    SampleNo = int(No)

    with open(fname) as f:
        content = f.readlines()

    tmpData = []
    for line in content:
        try:
            tmp = float(line)
            tmpData.append(tmp)
        except ValueError:
            pass

    Data = np.asarray(tmpData)
    Data = Data.reshape(-1,FrameNo,FeatureNo)
    Label = [label for i in range(SampleNo)]
    Label = np.asarray(Label)

    print ('#'*20)
    print ('The group type is:', group)
    print ('Set the group label as:', label)
    print ('Sample number is:', Data.shape[0])
    print ('The length of time frame is:', Data.shape[1])
    print ('Each time frame we have features:', Data.shape[-1])
    print ('#'*20)

    fileName = '../data/'+group+'.pickle.gz'
    with gzip.open(fileName, "wb") as output_file:
        Pickle.dump((Data, Label), output_file)











if __name__ == "__main__":
    main( sys.argv )
    pass
