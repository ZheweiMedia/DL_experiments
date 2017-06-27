"""



"""
from config import config
from processData import readfile, data_generator
from model import unet_model_3d
#from unet3d.training import load_old_model, train_model

url = '/home/medialab/Zhewei/MICCAI_Les_2017_Process/Unet_3D/'

trainlinks, trainannotlinks, testlinks, testannotlinks = readfile(url+'link/UnetSample_train.txt',\
                                                                url+'link/UnetLabel_train.txt', \
                                                                url+'link/UnetSample_test.txt', \
                                                                url+'link/UnetLabel_test.txt')
conf = config
trainPair = data_generator(trainlinks, trainannotlinks, conf, conf["batch_size"])

train = trainPair()
#for i, j in train:
    #print (i.shape)
#    pass


model = unet_model_3d(input_shape=config["input_shape"],
                              downsize_filters_factor=config["downsize_nb_filters_factor"],
                              pool_size=config["pool_size"], n_labels=config["GT_class"],
                              initial_learning_rate=config["initial_learning_rate"])
