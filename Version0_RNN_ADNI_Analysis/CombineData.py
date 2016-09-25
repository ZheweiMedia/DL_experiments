'''
Should not do this. Keep each group as a file can make thing easier.

Now the data for each group is a Pickle.gz.
We need to combine them together.
For data, keep the shape as SampleNo*FrameNo*FeatureNo
For label, keep the shape as 1*SampleNo


@Zhewei
5/21/2016
'''

import sys,os
import gzip
import cPickle as Pickle
import numpy as np

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
    for fileNo, files in enumerate(fnames):
        f = gzip.open(files,'rb')
        data,label = Pickle.load(f)
        f.close()
        if label[0] == 0:
            print 'The sample number of NC is:', data.shape[0]
        if label[0] == 1:
            print 'The sample number of AD is:', data.shape[0]
        if label[0] == 2:
            print 'The sample number of EMCI is:', data.shape[0]
        if label[0] == 3:
            print 'The sample number of LMCI is:', data.shape[0]
        if label[0] == 4:
            print 'The sample number of SMC is:', data.shape[0]
        if fileNo == 0:
            WholeData = data
            Label = label
        else:
            WholeData = np.vstack((WholeData,data))
            Label = np.vstack((Label, label))

    Label = Label.reshape(1,-1)
    print 'Totaly we have sample number:', WholeData.shape[0]

    with gzip.open("./data/WholeData.Pickle.gz", "wb") as output_file:
        Pickle.dump((WholeData, Label), output_file)






if __name__ == "__main__":
    main( sys.argv )
    pass
