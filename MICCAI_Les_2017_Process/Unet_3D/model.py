import os
import math
import numpy
from utility import *
from keras import backend as K
from keras.engine import Input, Model
from keras.layers import Conv3D, MaxPooling3D, UpSampling3D, Activation
from keras.optimizers import Adam
from keras.models import load_model


try:
    from keras.engine import merge
except ImportError:
    from keras.layers.merge import concatenate




def unet_model_3d(input_shape, downsize_filters_factor=1, pool_size=(2, 2, 2), n_labels=1,
                  initial_learning_rate=0.00001, deconvolution=False):
    """
    Builds the 3D UNet Keras model.
    ## ORIGINAL: :param input_shape: Shape of the input data (n_chanels, x_size, y_size, z_size).
    ## NOW: :param input_shape: Shape of the input data (x_size, y_size, z_size, n_chanels)
    :param downsize_filters_factor: Factor to which to reduce the number of filters. Making this value larger will
    reduce the amount of memory the model will need during training.
    :param pool_size: Pool size for the max pooling operations.
    :param n_labels: Number of binary labels that the model is learning.
    :param initial_learning_rate: Initial learning rate for the model. This will be decayed during training.
    :param deconvolution: If set to True, will use transpose convolution(deconvolution) instead of upsamping. This
    increases the amount memory required during training.
    :return: Untrained 3D UNet Model
    """
    inputs = Input(input_shape)
    conv1 = Conv3D(int(32/downsize_filters_factor), (3, 3, 3), activation='relu',
                   padding='same')(inputs)
    conv1 = Conv3D(int(64/downsize_filters_factor), (3, 3, 3), activation='relu',
                   padding='same')(conv1)
    pool1 = MaxPooling3D(pool_size=pool_size)(conv1)

    conv2 = Conv3D(int(64/downsize_filters_factor), (1, 1, 1), activation='relu',
                   padding='same')(pool1)
    conv2 = Conv3D(int(128/downsize_filters_factor), (1, 1, 1), activation='relu',
                   padding='same')(conv2)

    """
    pool2 = MaxPooling3D(pool_size=pool_size)(conv2)

    conv3 = Conv3D(int(128/downsize_filters_factor), (3, 3, 3), activation='relu',
                   padding='same')(pool2)
    conv3 = Conv3D(int(256/downsize_filters_factor), (3, 3, 3), activation='relu',
                   padding='same')(conv3)
    pool3 = MaxPooling3D(pool_size=pool_size)(conv3)

    conv4 = Conv3D(int(256/downsize_filters_factor), (3, 3, 3), activation='relu',
                   padding='same')(pool3)
    conv4 = Conv3D(int(512/downsize_filters_factor), (3, 3, 3), activation='relu',
                   padding='same')(conv4)
    """
    """
    up5 = get_upconv(pool_size=pool_size, deconvolution=deconvolution, depth=2,
                     nb_filters=int(512/downsize_filters_factor), image_shape=input_shape[1:4])(conv4)
    up5 = concatenate([up5, conv3], axis=-1)
    conv5 = Conv3D(int(256/downsize_filters_factor), (3, 3, 3), activation='relu', padding='same')(up5)
    conv5 = Conv3D(int(256/downsize_filters_factor), (3, 3, 3), activation='relu',
                   padding='same')(conv5)

    up6 = get_upconv(pool_size=pool_size, deconvolution=deconvolution, depth=1,
                     nb_filters=int(256/downsize_filters_factor), image_shape=input_shape[1:4])(conv5)
    up6 = concatenate([up6, conv2], axis=-1)
    conv6 = Conv3D(int(128/downsize_filters_factor), (3, 3, 3), activation='relu', padding='same')(up6)
    conv6 = Conv3D(int(128/downsize_filters_factor), (3, 3, 3), activation='relu',
                   padding='same')(conv6)
    """
    up7 = get_upconv(pool_size=pool_size, deconvolution=deconvolution, depth=0,
                     nb_filters=int(128/downsize_filters_factor), image_shape=input_shape[1:4])(conv2)
    up7 = concatenate([up7, conv1], axis=-1)
    conv7 = Conv3D(int(64/downsize_filters_factor), (3, 3, 3), activation='relu', padding='same')(up7)
    conv7 = Conv3D(int(64/downsize_filters_factor), (3, 3, 3), activation='relu',
                   padding='same')(conv7)

    conv8 = Conv3D(n_labels, (1, 1, 1))(conv7)
    # Shoudl be softmax?
    act = Activation('softmax')(conv8)
    model = Model(inputs=inputs, outputs=act)
    model.compile(optimizer=Adam(lr=initial_learning_rate), loss=dice_coef_loss, metrics=[dice_coef])
    model.summary()
    return model

def get_upconv(depth, nb_filters, pool_size, image_shape, kernel_size=(2, 2, 2), strides=(2, 2, 2),
               deconvolution=False):
    if deconvolution:
        try:
            from keras_contrib.layers import Deconvolution3D
        except ImportError:
            raise ImportError("Install keras_contrib in order to use deconvolution. Otherwise set deconvolution=False.")

        return Deconvolution3D(filters=nb_filters, kernel_size=kernel_size,
                               output_shape=compute_level_output_shape(filters=nb_filters, depth=depth,
                                                                       pool_size=pool_size, image_shape=image_shape),
                               strides=strides, input_shape=compute_level_output_shape(filters=nb_filters,
                                                                                       depth=depth+1,
                                                                                       pool_size=pool_size,
                                                                                       image_shape=image_shape))
    else:
        return UpSampling3D(size=pool_size)

# TODO: Should I add a weight at here?
def dice_coef(y_true, y_pred, smooth=1.):
    y_true_f = K.flatten(y_true[:,:,:,:,1:])#Don't care about the background
    y_pred_f = K.flatten(y_pred[:,:,:,:,1:])
    intersection = K.sum(y_true_f * y_pred_f)
    return (2. * intersection + smooth) / (K.sum(y_true_f) + K.sum(y_pred_f) + smooth)


def dice_coef_loss(y_true, y_pred):
    return -dice_coef(y_true, y_pred)


def train_model(model, model_file, training_generator, validation_generator, steps_per_epoch, validation_steps,
                initial_learning_rate, learning_rate_drop, learning_rate_epochs, n_epochs):
    """
    Train a Keras model.
    :param model: Keras model that will be trained. 
    :param model_file: Where to save the Keras model.
    :param training_generator: Generator that iterates through the training data.
    :param validation_generator: Generator that iterates through the validation data.
    :param steps_per_epoch: Number of batches that the training generator will provide during a given epoch.
    :param validation_steps: Number of batches that the validation generator will provide during a given epoch.
    :param initial_learning_rate: Learning rate at the beginning of training.
    :param learning_rate_drop: How much at which to the learning rate will decay.
    :param learning_rate_epochs: Number of epochs after which the learning rate will drop.
    :param n_epochs: Total number of epochs to train the model.
    :return: 
    """
    model.fit_generator(generator=training_generator,
                        steps_per_epoch=steps_per_epoch,
                        epochs=n_epochs,
                        validation_data=validation_generator,
                        validation_steps=validation_steps,
                        pickle_safe=True,
                        callbacks=get_callbacks(model_file, initial_learning_rate=initial_learning_rate,
                                                learning_rate_drop=learning_rate_drop,
                                                learning_rate_epochs=learning_rate_epochs))
    model.save(model_file)

    """
    # predict
    predID = 0
    for sample, target in validation_generator:
        predict = model.predict(sample)
        for sampleNo in range(predict.shape[0]):
            tmp_sample = predict[sampleNo]
            result = numpy.zeros((tmp_sample.shape[0], tmp_sample.shape[1], tmp_sample.shape[2]))
            if numpy.any(numpy.argmax(tmp_sample, axis=3) != result):
                #print (numpy.argmax(tmp_sample, axis=3) != result)
                print (predID)
            #with gzip.open('/home/medialab/Zhewei/MICCAI_Les_2017_Process/data/predict/'+str(predID)+'.tar.gz','w') as OutputFile:
            #    pickle.dump(result, OutputFile)
            predID += 1
    """


def load_old_model(model_file):
    print("Loading pre-trained model")
    custom_objects = {'dice_coef_loss': dice_coef_loss, 'dice_coef': dice_coef}
    try:
        from keras_contrib.layers import Deconvolution3D
        custom_objects["Deconvolution3D"] = Deconvolution3D
    except ImportError:
        print("Could not import Deconvolution3D. To use Deconvolution3D install keras-contrib.")
    return load_model(model_file, custom_objects=custom_objects)
