"""
Input is all Pickle.gz. Now each pickle is a subject.

train:validation:test = 8:1:1

@Zhewei
5/29/2016

"""

import sys,os
import gzip
import pickle as Pickle
import numpy as np
from random import shuffle, randint
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers.core import Dense, Activation
from keras.layers import LSTM
from keras.optimizers import RMSprop
from keras.initializations import normal, identity

iterationNo = 1
totalNo = 86
trainPercent = 70
validationPercent = 8
testpercent = 8
hd_notes = 10
learning_rate = 1e-6
nb_epoch = 500


def main(args):
    if len(args) < 2:
        usage( args[0] )
        pass
    else:
        work( args[1:] )
        pass
    pass

def usage (programm):
    print ("usage: %s data/*Subj*.pickle.gz"%(programm))
    
def work(fnames):
    finalResults = list()
    for iNo in range(iterationNo):
        index = randint(0, totalNo-1)
