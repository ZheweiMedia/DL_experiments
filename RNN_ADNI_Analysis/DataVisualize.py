"""
Data visualize. Now the data should be compressed to 2D or 3D. But I don't think
3D is better than 2D. So let's only handle the 2D data.
Assume the data is output of AutoEncoder.py, then we have labels of each sample.

Label:  0: NC
        1: AD
        2: EMCI
        3: LMCI
        4: SMC
color: each sample has its color but keep the whole group as close color.

@Zhewei
5/24/2016
"""

import sys,os
import gzip
import cPickle as Pickle
import numpy as np
import matplotlib.pyplot as pyplot
from matplotlib.pyplot import figure, show

timesteps = 130


def main(args):
    if len(args) < 2:
        usage( args[0] )
        pass
    else:
        work( args[1] )
        pass
    pass

def usage (programm):
    print ("usage: %s data/CopmressedData.Pickle.gz"%(programm))

def work(fnames):
    f = gzip.open(files,'rb')
    data,label = Pickle.load(f)
    f.close()
    for iLabel in label:
        if iLabel == 0:
            NCNo += 1
        if iLabel == 1:
            ADNo += 1
        if iLabel == 2:
            EMCINo += 1
        if iLabel == 3:
            LMCINo += 1
        if iLabel == 4:
            SMCNo += 1
    print 'We have', NCNo, 'NC samples.'
    print 'We have', ADNo, 'AD samples.'
    print 'We have', EMCINo, 'EMCI samples.'
    print 'We have', LMCINo, 'LMCI samples.'
    print 'We have', SMCNo, 'SMC samples.'

    iNC = 0
    iAD = 0
    iEMCI = 0
    iLMCI = 0
    iSMC = 0
    for iLabel, Lb in enumerate(label):
        if Lb == 0: # NC
            color = ((iNC)/(NCNo),0,0)
            iNC += 1
        if Lb == 1:
            color = (0,(iAD)/(ADNo),0)
            iAD += 1
        if Lb == 2:
            color = (0,0,(iEMCI)/(EMCINo))
            iEMCI += 1
        if Lb == 3:
            color = (0,0.5, (iLMCI)/(LMCINo))
            iLMCI += 1
        if Lb == 4:
            color = (0.5, 0.5, (iSMC)/(SMCNo))
            iSMC += 1

        pyplot.plot(data(iLabel*timesteps:(iLabel+1)*timesteps,0), \
                        data(iLabel*timesteps:(iLabel+1)*timesteps,1), \
                            'o', color = color)
    pyplot.show()
