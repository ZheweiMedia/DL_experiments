"""
AutoEncoder, used for data compression.
Followed the steps of http://blog.keras.io/building-autoencoders-in-keras.html

inputData: same as LSTM, but we don't need to separate them as train, validation,
            and test.

AutoEncoder: 120-200-100-50-2-50-100-200-120

@Zhewei
5/23/2016

Data don't need to be normalized.
@Zhewei
6/18/2016

We need validation data to monitor the system.
@Zhewei
6/21/2016

"""

import sys,os
import gzip
import pickle as Pickle
import numpy as np
from PersonIndependent_LSTM import stackData
from keras.layers import Dense, Input
from keras.models import Model


compressedFeatureNo = 10
AlltimeScanNo = 84
trainNo = 70
validationNo = AlltimeScanNo-trainNo

totalNo = 76+84


TrainIndex = [i for i in range(trainNo)]
validationIndex = [i for i in range(trainNo,AlltimeScanNo)]
DataIndex = [i for i in range(totalNo)]


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
    trainData, trainLabel = stackData(fnames, TrainIndex)
    validationData, validationLabel = stackData(fnames, validationIndex)
    print (trainData.shape)
    print (validationData.shape)
    sampleNo = trainData.shape[0]
    timeStep = trainData.shape[1]
    featureNo = trainData.shape[2]
    
    print (np.amax(trainData))
    print (np.amin(trainData))
    print ('We have', trainData.shape[0], 'training samples.')
    print ('We have', validationData.shape[0], 'validation samples.')
    # just realized the trainData now is SampleNo*timesteps*FeatureNo, need
    # to reshape to (SampleNo*timesteps)*FeatureNo
    trainData = trainData.reshape((trainData.shape[0]*trainData.shape[1],\
                                            trainData.shape[2]))
    validationData = validationData.reshape((-1, validationData.shape[2]))
    print ('Each sample has', trainData.shape[1], 'features.')

    '''
    AutoEncoder
    120-200-100-50-2-50-100-200-120
    '''
    input_data = Input(shape=(120,))
    encode = Dense(200, activation = 'relu')(input_data)
    encode = Dense(100, activation = 'relu')(encode)
    encode = Dense(50, activation = 'relu')(encode)
    encode = Dense(compressedFeatureNo, activation = 'relu')(encode)

    decode = Dense(50, activation = 'relu')(encode)
    decode = Dense(100, activation = 'relu')(decode)
    decode = Dense(200, activation = 'relu')(decode)
    decode = Dense(120, activation = 'relu')(decode)

    AutoEncoder = Model(input = input_data, output = decode)
    encoder = Model(input = input_data, output = encode)
    AutoEncoder.compile(optimizer = 'adadelta', loss = 'mean_squared_error')

    AutoEncoder.fit(trainData, trainData,\
                        nb_epoch = 100, \
                        batch_size = 100, \
                        shuffle = True, \
                        validation_data = (validationData, validationData                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      ))
    
    fnames = list(fnames)
    print (len(fnames))
    for iNo in DataIndex:
        f = gzip.open(fnames[iNo],'rb')
        tmpdata,tmplabel = Pickle.load(f)
        tmpdata = tmpdata.reshape((tmpdata.shape[0]*tmpdata.shape[1],\
                                            tmpdata.shape[2]))
        fName = os.path.basename(fnames[iNo])
        fileName = '../data/'+fName
        print (fileName)
        CompressedResult = encoder.predict(tmpdata)
        print (CompressedResult.shape)
        CompressedResult = CompressedResult.reshape(-1, timeStep, compressedFeatureNo)
        print (CompressedResult.shape)
        print (tmplabel)
    
        with gzip.open(fileName, "wb") as output_file:
                Pickle.dump((CompressedResult, tmplabel), output_file)




















if __name__ == "__main__":
    main( sys.argv )
    pass
