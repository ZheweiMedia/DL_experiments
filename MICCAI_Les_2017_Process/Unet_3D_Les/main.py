"""



"""
from config import config
from processData import readfile, data_generator
from model import unet_model_3d, train_model, load_old_model
import numpy, gzip, pickle
import nibabel

url = '/home/medialab/Zhewei/MICCAI_Les_2017_Process/Unet_3D_Les/'

trainlinks, trainannotlinks, testlinks, testannotlinks = readfile(url+'link/UnetSample_train.txt',\
                                                                url+'link/UnetLabel_train.txt', \
                                                                url+'link/UnetSample_test.txt', \
                                                                url+'link/UnetLabel_test.txt')
conf = config
trainPair = data_generator(trainlinks, trainannotlinks, conf, conf["batch_size"])
validPair = data_generator(testlinks, testannotlinks, conf, conf["batch_size"], rdm=False)

train_generator = trainPair
validation_generator = validPair
nb_train_samples = 640
nb_test_samples = 260

"""
model = unet_model_3d(input_shape=config["input_shape"],
                              downsize_filters_factor=config["downsize_nb_filters_factor"],
                              pool_size=config["pool_size"], n_labels=config["GT_class"],
                              initial_learning_rate=config["initial_learning_rate"])

# run training
# model = load_old_model(config["model_file"])
train_model(model=model, model_file=config["model_file"], training_generator=train_generator,
            validation_generator=validation_generator, steps_per_epoch=nb_train_samples,
            validation_steps=nb_test_samples, initial_learning_rate=config["initial_learning_rate"],
            learning_rate_drop=config["learning_rate_drop"],
            learning_rate_epochs=config["decay_learning_rate_every_x_epochs"], n_epochs=config["n_epochs"])

"""

model = load_old_model(config["model_file"])
evaluate_list = list()
total_eval = 0
total_No = 0
for sample, target in validation_generator:
    if total_No < 2600:
        each_loss = model.evaluate(sample, target)[1]
        evaluate_list.append(each_loss)
        total_eval += each_loss
        total_No += 10
        print (total_No)
    else:
        print (len(evaluate_list))
        print (total_No)
        print (total_eval/total_No*10)
        break



"""
predID = 0
results_analysis = list()
for sample, target in validation_generator:   
    for sampleNo in range(sample.shape[0]):
        if (predID < 7528):
            each_sample = sample[sampleNo].reshape((1,)+sample[sampleNo].shape)
            each_target = target[sampleNo].reshape((1,)+target[sampleNo].shape)
            tmp_sample = model.predict(each_sample, verbose = 0)
            each_loss = model.evaluate(each_sample, each_target)[1]
            result = numpy.argmax(tmp_sample, axis=-1).astype(numpy.int16)
            result = result.reshape((result.shape[1:]+ (1,)))
            compare_result = ('loss', each_loss, 'GT', numpy.sum(each_target[:,:,:,:,1]), 'PRED', numpy.sum(result))
            results_analysis.append(compare_result)
            result = nibabel.Nifti1Image(result, numpy.eye(4))
            nibabel.save(result, '/home/medialab/Zhewei/MICCAI_Les_2017_Process/data/predict_les/'+str(predID)+'.nii.gz')
            predID += 1

            with open('results_analysis.txt', 'w') as outFile:
                for i in results_analysis:
                    outFile.write(' '.join(str(s) for s in i) +'\n')


"""
