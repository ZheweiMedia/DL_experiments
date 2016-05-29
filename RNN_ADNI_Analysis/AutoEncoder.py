"""
AutoEncoder, used for data compression.
Followed the steps of http://blog.keras.io/building-autoencoders-in-keras.html

inputData: same as LSTM, but we don't need to separate them as train, validation,
            and test.

AutoEncoder: 120-200-100-50-2-50-100-200-120

@Zhewei
5/23/2016

"""

import sys,os
import gzip
import cPickle as Pickle
import numpy as np
from keras.layers import Dense, Input
from keras.models import Model


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
    finalResults = list()
    WholeLabel = list()
    for fileNo, files in enumerate(fnames):
        f = gzip.open(files,'rb')
        data,label = Pickle.load(f)
        f.close()
        sampleNo = data.shape[0]
        WholeLabel.append(label)
        if fileNo == 0:
            WholeData = data
        else:
            WholeData = np.vstack((WholeData, data))

        print 'We have', WholeData.shape[0], 'samples.'
        # just realized the WholeData now is SampleNo*timesteps*FeatureNo, need
        # to reshape to (SampleNo*timesteps)*FeatureNo
        WholeData = WholeData.reshape((WholeData.shape[0]*WholeData[1],\
                                            WholeData.shape[2]))
        print 'Each sample has', WholeData.shape[1], 'features.'

        '''
        AutoEncoder
        120-200-100-50-2-50-100-200-120
        '''
        input_data = Input(shape(120,))
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
        AutoEncoder.compile(optimizer = 'adadelta', loss = 'binary_crossentropy')

        AutoEncoder.fit(WholeData, WholeData,\
                        nb.epoch = 100, \
                        batch_size = 50, \
                        shuffle = True)
        CompressedResult = encoder.predict(WholeData)




















if __name__ == "__main__":
    main( sys.argv )
    pass
