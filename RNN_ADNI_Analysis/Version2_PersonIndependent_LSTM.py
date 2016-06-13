"""
Input is all Pickle.gz. Now each pickle is a subject.

train:validation:test = 8:1:1

********************************************************
Train use all record, validation and test use baseline.
********************************************************

Now subjects with all records are pickle.gz, and subjects with baseline
are pickle.gz, in different folds. So, what should we do?

randomly choose train, validation, test index. For train, directly read the
pickle.gz, for validation and test, from the index get the subjects name, then 
find out corresponding pickle.gz. 

**********************************************************************
So if we want to expand this code to MCI, then 
EMCI, LMCI and SMC should be named also with 2 prefix charactors.

Remember to add commit for experiment log. Did have the trigger to check it now.
**********************************************************************

Generate experiment log in Experiment+time.txt

@Zhewei
5/31/2016

Add random.seed()
@Zhewei
6/3/2016

"""

import sys,os
import datetime
import gzip
import pickle as Pickle
import numpy as np
np.random.seed(1337)  # for reproducibility
from random import shuffle, randint
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers.core import Dense, Activation
from keras.layers import LSTM
from keras.optimizers import RMSprop
from keras.initializations import normal, identity

iterationNo = 1
Groups = 2

BATCH_SIZE = 30

totalNo = 103#190
trainPercent = 80#152
validationPercent = 13#19
testpercent = 10#19
MagicNumber = 17

hd_notes = 40
learning_rate = 1e-5
nb_epoch = 1000


def main(args):
    if len(args) < 2:
        usage( args[0] )
        pass
    else:
        work( args[1:-1], args[-1])
        pass
    pass

def usage (programm):
    print ("usage: %s ../data/Subjects_Alltime/*.gz ../data/Subjects_Baseline/*.gz"%(programm))
    
def work(fnames, comment):
    finalResults = list()
    logTime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    logName = '../data/Experiments_log '+logTime+comment+'.txt'
    f_txt = open(logName, 'w')
    f_txt.write(str(sys.argv[0]))
    f_txt.write('\n')
    f_txt.write(str(sys.argv[1:]))
    f_txt.write('\n'*3)
    for iNo in range(iterationNo):
        index = [i for i in range(totalNo)]
        shuffle(index)
        AlltimeFile = fnames[0:totalNo]
        BaselineFile = fnames[totalNo:]
        trainIndex = index[0:trainPercent]
        trainData, trainLabel = stackData(AlltimeFile, trainIndex)
        
        # validation
        validationIndex = index[trainPercent:trainPercent+validationPercent]
        validationFile = BaselineFile
        validationBaselineIndex = list()
        for iva in validationIndex:
            tmpFile = os.path.basename(AlltimeFile[iva])
            tmpSubj = tmpFile[0:MagicNumber]#<=========================== magic number, to get subject value, such like 013_S_234
            validationBaseline = [sNo for sNo,s in enumerate(validationFile) if tmpSubj in s]
            if validationBaseline:
                validationBaseline = validationBaseline[0]
                validationBaselineIndex.append(validationBaseline)
                
        validationData, validationLabel = stackData(BaselineFile, validationBaselineIndex)   
        
        # test   
        testIndex = index[trainPercent+validationPercent:]
        testFile = BaselineFile
        testBaselineIndex = list()
        for ite in testIndex:
            tmpFile = os.path.basename(AlltimeFile[ite])
            tmpSubj = tmpFile[0:MagicNumber]#<=========================== magic number
            testBaseline = [sNo for sNo,s in enumerate(testFile) if tmpSubj in s]
            if testBaseline:
                testBaseline = testBaseline[0]
                testBaselineIndex.append(testBaseline)
                
        testData, testLabel = stackData(BaselineFile, testBaselineIndex)
        
        print ('*'*30)
        print ('Iteration:', iNo)
        print ('Training subjects:', trainPercent)
        print ('Training samples:', trainData.shape[0])
        print ('Validation subjects:', validationPercent)
        print ('Validation samples:', validationData.shape[0])
        print ('Test subjects:', testpercent)
        print ('Test samples:', testData.shape[0])
        print ('*'*30)
        
        
        """
        LSTM
        """
        
        nb_classes = Groups
        timesteps = trainData.shape[1]
        featureNo = trainData.shape[2]

        Y_train = np_utils.to_categorical(trainLabel, nb_classes)
        Y_test = np_utils.to_categorical(testLabel, nb_classes)
        Y_valid = np_utils.to_categorical(validationLabel, nb_classes)
        
        print ("Building model...")
        model = Sequential()
        model.add(LSTM(hd_notes, input_shape=(timesteps, featureNo),\
                            init='normal',\
                            inner_init='identity',\
                            activation='tanh', return_sequences=False,\
                            dropout_W=0, dropout_U=0))
        model.add(Dense(nb_classes))
        model.add(Activation('softmax'))
        rmsprop = RMSprop(lr=learning_rate, rho=0.95, epsilon=1e-06)
        model.compile(loss='categorical_crossentropy', optimizer=rmsprop, \
                        metrics=["accuracy"])

        print ("Training model...")

        model.fit(trainData, Y_train, \
                    batch_size = BATCH_SIZE, nb_epoch=nb_epoch, verbose=1, validation_data=(validationData, Y_valid))

        scores = model.evaluate(testData, Y_test, verbose=1)
        print('RNN test score:', scores[0])
        print('RNN test accuracy:', scores[1])
        print (testLabel)
        print (model.predict_classes(testData))
        finalResults.append(scores[1])
        validationScore = model.evaluate(validationData, Y_valid, verbose=0)
        
        # record all the information
        f_txt.write('*'*30)
        f_txt.write('\n')
        f_txt.write('Iteration: ' + str(iNo))
        f_txt.write('\n')
        f_txt.write('Training samples: ' + str(trainData.shape[0]))
        f_txt.write('\n')
        f_txt.write('Training Index: ' + str(trainIndex))
        f_txt.write('\n')
        f_txt.write('Validation samples: ' + str(validationData.shape[0]))
        f_txt.write('\n')
        f_txt.write('Validation Index: ' + str(validationIndex))
        f_txt.write('\n')
        f_txt.write('Test samples: ' + str(testData.shape[0]))
        f_txt.write('\n')
        f_txt.write('Test Index: ' + str(testIndex))
        f_txt.write('\n')
        f_txt.write('Training results: ' + str(model.predict_classes(trainData)))
        f_txt.write('\n')
        f_txt.write('Validation ground truth: ' + str(validationLabel))
        f_txt.write('\n')
        f_txt.write('Validation result: ' + str(model.predict_classes(validationData)))
        f_txt.write('\n')
        f_txt.write('Validation accurate: ' + str(validationScore[1]))
        f_txt.write('\n')
        f_txt.write('Test ground truth: ' + str(testLabel))
        f_txt.write('\n')
        f_txt.write('Test result: ' + str(model.predict_classes(testData)))
        f_txt.write('\n')
        f_txt.write('Test accurate: ' + str(scores[1]))
        f_txt.write('\n')
        pass
    
    print ('Final results is:', finalResults)
    print ('Final accurate results of LSTM is:', sum(finalResults)/iterationNo)
    f_txt.write('\n'*3)
    f_txt.write('Final results are: ' + str(finalResults))
    f_txt.write('\n')
    f_txt.write('Final accurate results of LSTM is: ' + str(sum(finalResults)/iterationNo))
    f_txt.write('\n')
    f_txt.close()



        
def stackData(fnames, index):
    Data = np.zeros([1,1])
    Label = np.zeros([1,1])
    for iNo, i in enumerate(index):
        f = gzip.open(fnames[i],'rb')
        tmpdata,tmplabel = Pickle.load(f)
        if iNo == 0:
            Data = tmpdata
            Label = tmplabel
        else:
            Data = np.vstack((Data, tmpdata))
            Label = np.append(Label, tmplabel)
    return Data, Label
    
if __name__ == "__main__":
    main(sys.argv)
    pass
            
