"""



"""
from config import config
from processData import readfile, data_generator
from model import unet_model_3d, train_model, load_old_model
import numpy, gzip, pickle
import nibabel

url = '/home/medialab/Zhewei/MICCAI_Les_2017_Process/Unet_3D_Hippo/'

trainlinks, trainannotlinks, testlinks, testannotlinks = readfile(url+'link/train_sample.txt',\
                                                                url+'link/train_label.txt', \
                                                                url+'link/test_sample.txt', \
                                                                url+'link/test_label.txt')
conf = config
trainPair = data_generator(trainlinks, trainannotlinks, conf, conf["batch_size"])
validPair = data_generator(testlinks, testannotlinks, conf, conf["batch_size"], rdm=False)

train_generator = trainPair
validation_generator = validPair
nb_train_samples = 400
nb_test_samples = 40



model = unet_model_3d(input_shape=config["input_shape"],
                              downsize_filters_factor=config["downsize_nb_filters_factor"],
                              pool_size=config["pool_size"], n_labels=config["GT_class"],
                              initial_learning_rate=config["initial_learning_rate"])

# run training
train_model(model=model, model_file=config["model_file"], training_generator=train_generator,
            validation_generator=validation_generator, steps_per_epoch=nb_train_samples,
            validation_steps=nb_test_samples, initial_learning_rate=config["initial_learning_rate"],
            learning_rate_drop=config["learning_rate_drop"],
            learning_rate_epochs=config["decay_learning_rate_every_x_epochs"], n_epochs=config["n_epochs"])


"""
model = load_old_model(config["model_file"])


predID = 0
for sample, target in validation_generator:
    if (predID < 80):
        predict = model.predict(sample)
        print (model.evaluate(sample, target)[1])
        for sampleNo in range(predict.shape[0]):
            tmp_sample = predict[sampleNo]
            result = numpy.zeros((tmp_sample.shape[0], tmp_sample.shape[1], tmp_sample.shape[2]))
            result = numpy.argmax(tmp_sample, axis=3).astype(numpy.int16)
            result = result.reshape((tmp_sample.shape[0], tmp_sample.shape[1], tmp_sample.shape[2], 1))
            result = nibabel.Nifti1Image(result, numpy.eye(4))
            nibabel.save(result, '/home/medialab/Zhewei/MICCAI_Les_2017_Process/data/predict/'+str(predID)+'.nii.gz')
            predID += 1

"""
