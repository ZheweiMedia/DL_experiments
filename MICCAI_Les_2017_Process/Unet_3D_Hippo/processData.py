import gzip
import pickle
import numpy
import nibabel



def readfile(trainfile, trainannotfile, testfile, testannotfile):
    trainlinks = list()
    trainannotlinks = list()
    testlinks = list()
    testannotlinks = list()
    with open(trainfile, 'r') as f:
        trainlinks = f.read().splitlines()
    with open(trainannotfile, 'r') as f:
        trainannotlinks = f.read().splitlines()
    with open(testfile, 'r') as f:
        testlinks = f.read().splitlines()
    with open(testannotfile, 'r') as f:
        testannotlinks = f.read().splitlines()
    return trainlinks, trainannotlinks,  testlinks, testannotlinks


def data_generator(inputsamplelinks, inputlabellinks, conf, batch_size, rdm=True):
    while True:
        images = inputsamplelinks
        targets = inputlabellinks
        index = [i for i in range(len(images))]

        if rdm:
            rng_state = numpy.random.get_state()
            numpy.random.shuffle(images)
            numpy.random.set_state(rng_state)
            numpy.random.shuffle(targets)

        sample_in_batch = 0
        all_img = numpy.zeros((2,2))
        all_targ = numpy.zeros((2,2))
        for i in range(len(images)):
            img = nibabel.load(images[i]).get_data()
            targ = nibabel.load(targets[i]).get_data()
            targ = targ/255
            img = img.reshape((1, img.shape[0], img.shape[1], img.shape[2], 1))
            targ = targ.reshape((1, targ.shape[0], targ.shape[1], targ.shape[2]))
            targ = multiclass(targ, conf)
            if sample_in_batch == 0:
                all_img = img
                all_targ = targ
                sample_in_batch += 1
            else:
                all_img = numpy.concatenate((all_img, img))
                all_targ = numpy.concatenate((all_targ, targ))
                sample_in_batch += 1
            if sample_in_batch == batch_size:
                sample_in_batch = 0
                yield (numpy.copy(all_img), numpy.copy(all_targ))
                


def multiclass(dataset, conf):
    # CamVid has 12 classes
    new_dataset = numpy.zeros((dataset.shape[0], dataset.shape[1], dataset.shape[2], dataset.shape[3], conf["GT_class"]))
    for data_no in range(dataset.shape[0]):
        data = dataset[data_no,:,:]
        all_pixel = list()
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                for k in range(data.shape[2]):
                    new_dataset[data_no,i,j,k,int(data[i,j,k])] = 1
    return new_dataset
