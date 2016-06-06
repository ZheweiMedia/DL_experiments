"""
This program used to generate general pickle files from the raw data from MatLab.

Each subject as a pickle.

Label of NC:    0
Label of AD:    1
Label of EMCI:  2
Label of LMCI:  3
Label of SMC:   4

all data read or write in ./data

Usage:  python3.5 data/AD_Results/AD_Subj*.txt

Output: an array with the 3D shape SampleNo*FrameNo*FeatureNo and label for each sample

@Zhewei
5/29/2016

"""

import sys,os
import gzip
import pickle as Pickle
import numpy as np

label = 2 #<=========

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
        Data = np.asarray(tmpData)
        Data = Data.reshape(-1,FrameNo,FeatureNo)
        Label = [label for i in range(Data.shape[0])]
        Label = np.asarray(Label)
        
        print ('#'*20)
        print ('Sample number is:', Data.shape[0])
        print ('#'*20)
        
        fName = os.path.basename(fi)
        fileName = '../data/'+fName+'.pickle.gz'
        with gzip.open(fileName, "wb") as output_file:
            Pickle.dump((Data, Label), output_file)
            



if __name__ == "__main__":
    main( sys.argv )
    pass
