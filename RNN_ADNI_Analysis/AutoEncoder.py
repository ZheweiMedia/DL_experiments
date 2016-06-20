"""
AutoEncoder, used for data compression.
Followed the steps of http://blog.keras.io/building-autoencoders-in-keras.html

inputData: same as LSTM, but we don't need to separate them as train, validation,
            and test.

AutoEncoder: 120-200-100-50-2-50-100-200-120

@Zhewei
5/23/2016

Data need to be normalized.
@Zhewei
6/18/2016

"""

import sys,os
import gzip
import pickle as Pickle
import numpy as np
from PersonIndependent_LSTM import stackData
from keras.layers import Dense, Input
from keras.models import Model


totalNo = 76+84

index = [i for i in range(totalNo)]

DataIndex = index


def main(args):
    if len(args) < 2:
        usage( args[0] )
        pass
    else:
        work( args[1:] )
        pass
    pass

def usage (programm):
    print ("usage: %s data/AD.Pickle.gz data/NC.Pickle.gz ..."%(programm))

def work(fnames):
    wholeData, wholeLabel = stackData(fnames, DataIndex)
    print (wholeData.shape)
    sampleNo = wholeData.shape[0]
    timeStep = wholeData.shape[1]
    featureNo = wholeData.shape[2]

    print ('We have', wholeData.shape[0], 'samples.')
    # just realized the wholeData now is SampleNo*timesteps*FeatureNo, need
    # to reshape to (SampleNo*timesteps)*FeatureNo
    wholeData = wholeData.reshape((wholeData.shape[0]*wholeData.shape[1],\
                                            wholeData.shape[2]))
    print ('Each sample has', wholeData.shape[1], 'features.')

    '''
    AutoEncoder
    120-200-100-50-2-50-100-200-120
    '''
    input_data = Input(shape=(120,))
    encode = Dense(200, activation = 'relu')(input_data)
    encode = Dense(100, activation = 'relu')(encode)
    encode = Dense(50, activation = 'relu')(encode)
    encode = Dense(2, activation = 'relu')(encode)

    decode = Dense(50, activation = 'relu')(encode)
    decode = Dense(100, activation = 'relu')(decode)
    decode = Dense(200, activation = 'relu')(decode)
    decode = Dense(120, activation = 'relu')(decode)

    AutoEncoder = Model(input = input_data, output = decode)
    encoder = Model(input = input_data, output = encode)
    AutoEncoder.compile(optimizer = 'adadelta', loss = 'mean_squared_error')

    AutoEncoder.fit(wholeData, wholeData,\
                        nb_epoch = 100, \
                        batch_size = 100, \
                        shuffle = True)
    CompressedResult = encoder.predict(wholeData)
    print (CompressedResult.shape)
    CompressedResult = CompressedResult.reshape(sampleNo, timeStep, -1)
    print (CompressedResult.shape)
    
    with gzip.open('../data/AutoEncoder_Result.pickle.gz', "wb") as output_file:
            Pickle.dump((CompressedResult, wholeLabel), output_file)




















if __name__ == "__main__":
    main( sys.argv )
    pass
