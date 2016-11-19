"""

Data augament.
6/22/2016

"""

import sys,os
import gzip
import pickle as Pickle
import numpy as np
import random
import math
from PersonIndependent_LSTM import stackData

#******************************
#******************************
label = 0
NoiseScanNo = 5
postfix = '_noise.pickle.gz'
#******************************
#******************************



totalNo = 84+76
index = [i for i in range(totalNo)]


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
    
def work(fnames):
    for iIndex in index:
        tmpdata, tmplabel = stackData(fnames, [iIndex])
        timeStep = tmpdata.shape[1]
        featureNo = tmpdata.shape[2]
        tmpdata = tmpdata.reshape(1, -1)
        
        tmpData = list(tmpdata)
        # now generate noise data
        TmpNoiseData = list()
        for noiseNo in range(NoiseScanNo):
            TmpNoiseData += tmpData
        
        # now generate noise (0-1) , add to scans
        TmpNoiseData = [d+random.uniform(-0.1,0.1) for d in TmpNoiseData]
        tmpData = tmpData+TmpNoiseData
        # now generate residual data
        
        Data = np.asarray(tmpData)
        DataResidual = Data.reshape(-1,timeStep,featureNo)
        print (DataResidual.shape)

        
        
        

        Label = [label for i in range(DataResidual.shape[0])]
        Label = np.asarray(Label)
        print (Label.shape)
        
        fName = os.path.basename(fnames[iIndex])
        fileName = '../data/'+fName
        print (fileName)
        with gzip.open(fileName, "wb") as output_file:
            Pickle.dump((DataResidual, Label), output_file)
        
            



if __name__ == "__main__":
    main( sys.argv )
    pass
