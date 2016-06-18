"""
5/29/2016 start:

This program used to generate general pickle files from the raw data from MatLab.

Each subject as a pickle.

Label of NC:    0
Label of AD:    1
Label of EMCI:  2
Label of LMCI:  3
Label of SMC:   4

all data read or write in ./data

******************************************
1. Set group label.
2. Make sure input correct .txt files.
3. Add some code to check if value is Nan. It happened for a subject of LMCI. Don't know why. 
   So now if the file contains Nan, will print the file name.(maybe we can do better.)
******************************************

Usage:  python3.5 data/AD_Results/AD_Subj*.txt

Output: an array with the 3D shape SampleNo*FrameNo*FeatureNo and label for each sample
            And the feature is next time frame minus last time frame.

@Zhewei
6/16/2016

"""

import sys,os
import gzip
import pickle as Pickle
import numpy as np
import random
import math

#******************************
#******************************
label = 1
NoiseScanNo = 5
postfix = 'Residual.pickle.gz'
#******************************
#******************************

FrameNo = 130
FeatureNo = 120

local_max = 5253
local_min = -1021
global_max = 6611
global_min = -1993


def main(args):
    if len(args) < 2:
        usage( args[0] )
        pass
    else:
        work( args[1:] )
        pass
    pass
    
def usage (programm):
    print ("usage: %s data/AD_Results/AD_Subj*.txt"%(programm))
    
def work(files):
    for fNo, fi in enumerate(files):
        with open(fi) as f:
            content = f.readlines()
        
        tmpData = list()
        for line in content:
            try:
                tmp = float(line)
                tmp = tmp*(local_max-local_min)+local_min
                tmp = (tmp-global_min)/(global_max-global_min)
                tmpData.append(tmp)
                if math.isnan(tmp):
                    print (fi)
            except ValueError:
                pass
        
        # now generate noise data
        TmpNoiseData = list()
        for noiseNo in range(NoiseScanNo):
            TmpNoiseData += tmpData
        
        # now generate noise (0-1) , add to scans
        TmpNoiseData = [d+random.uniform(-0.001,0.001) for d in TmpNoiseData]
        tmpData = tmpData+TmpNoiseData
        # now generate residual data
        
        Data = np.asarray(tmpData)
        Data = Data.reshape(-1,FrameNo,FeatureNo)
        DataResidual = Data
        for iSample in range(Data.shape[0]):
            for iFrame in range(Data.shape[1]-1):
                DataResidual[iSample, iFrame,:] = (Data[iSample, iFrame+1,:]-Data[iSample, iFrame,:])*1000
        
        print (DataResidual.shape)
        print (DataResidual[0,128,:])
        # print (DataResidual[0,129,:])
        
        DataResidual = DataResidual[:,0:-1,:]
        print (DataResidual.shape)
        Label = [label for i in range(DataResidual.shape[0])]
        Label = np.asarray(Label)
        
        print ('#'*20)
        print ('Sample number is:', DataResidual.shape[0])
        print ('#'*20)
        
        fName = os.path.basename(fi)
        fileName = '../data/'+fName+postfix
        with gzip.open(fileName, "wb") as output_file:
            Pickle.dump((DataResidual, Label), output_file)
        
            



if __name__ == "__main__":
    main( sys.argv )
    pass
