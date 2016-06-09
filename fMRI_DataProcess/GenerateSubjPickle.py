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
2. Set how many sans with noise will generate.
3. Set postfix name for output pickle. '.pickle.gz' for no-noise, 'noise.pickle.gz' for noise data.
4. Make sure input correct .txt files.
******************************************

Usage:  python3.5 data/AD_Results/AD_Subj*.txt

Output: an array with the 3D shape SampleNo*FrameNo*FeatureNo and label for each sample

@Zhewei


"""

import sys,os
import gzip
import pickle as Pickle
import numpy as np
import random

#******************************
label = 3
NoiseScanNo = 0
postfix = '.pickle.gz'
#******************************

FrameNo = 130
FeatureNo = 120


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
        
        tmpData = []
        for line in content:
            try:
                tmp = float(line)
                tmpData.append(tmp)
            except ValueError:
                pass
        
        # now generate (copy) NoiseScanNo scans
        TmpNoiseData = list()
        for noiseNo in range(NoiseScanNo):
            TmpNoiseData += tmpData
        
        # now generate noise (0-1) , add to scans
        TmpNoiseData = [d+random.random() for d in TmpNoiseData]
        
        # print (len(TmpNoiseData))
        # print (NoiseScanNo*len(tmpData))
        
        tmpData = tmpData+TmpNoiseData
        Data = np.asarray(tmpData)
        Data = Data.reshape(-1,FrameNo,FeatureNo)
        Label = [label for i in range(Data.shape[0])]
        Label = np.asarray(Label)
        
        print ('#'*20)
        print ('Sample number is:', Data.shape[0])
        print ('#'*20)
        
        fName = os.path.basename(fi)
        fileName = '../data/'+fName+postfix
        with gzip.open(fileName, "wb") as output_file:
            Pickle.dump((Data, Label), output_file)
        
            



if __name__ == "__main__":
    main( sys.argv )
    pass
