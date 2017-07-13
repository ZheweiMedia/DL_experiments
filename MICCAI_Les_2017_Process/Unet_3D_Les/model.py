import os
import math
import numpy
from utility import *
from keras import backend as K
from keras.engine import Input, Model
from keras.layers import Conv3D, MaxPooling3D, UpSampling3D, Activation
from keras.optimizers import Adam
from keras.models import load_model
from keras.callbacks import ModelCheckpoint, CSVLogger, Callback, LearningRateScheduler
from keras.layers.core import Lambda
import theano


try:
    from keras.engine import merge
except ImportError:
    from keras.layers.merge import concatenate




def unet_model_3d(config, input_shape, downsize_filters_factor=1, pool_size=(2, 2, 2), n_labels=1,
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
    def collapse(features1, features2, Channels, config):
        collapseLayer = Conv3D(1, (1,1,1), activation='relu', padding='same')# same collapseLayer or not....
        AllFeatures = list()
        #for featureIndex in range(Channels):
        #    tmp_input1 = Lambda(lambda x,y:x[:,:,:,:,y:y+1], output_shape=config["collapse_shape"])(features1, featureIndex)
        #    tmp_input2 = Lambda(lambda x,y:x[:,:,:,:,y:y+1], output_shape=config["collapse_shape"])(features2, featureIndex)
        #    tmp_inputs = concatenate([tmp_input1, tmp_input2], axis=-1)
        #    tmp_inputs = Conv3D(1, (1,1,1), activation='relu', padding='same')(tmp_inputs)
        #    AllFeatures.append(tmp_inputs)

        def outfeature1(x):
            return x[:,:,:,:,0:1]
        def outfeature2(x):
            return x[:,:,:,:,1:2]
        def outfeature3(x):
            return x[:,:,:,:,2:3]
        def outfeature4(x):
            return x[:,:,:,:,3:4]
        def outfeature5(x):
            return x[:,:,:,:,4:5]
        def outfeature6(x):
            return x[:,:,:,:,5:6]
        def outfeature7(x):
            return x[:,:,:,:,6:7]
        def outfeature8(x):
            return x[:,:,:,:,7:8]
        def outfeature9(x):
            return x[:,:,:,:,8:9]
        def outfeature10(x):
            return x[:,:,:,:,9:10]
        def outfeature11(x):
            return x[:,:,:,:,10:11]
        def outfeature12(x):
            return x[:,:,:,:,11:12]
        def outfeature13(x):
            return x[:,:,:,:,12:13]
        def outfeature14(x):
            return x[:,:,:,:,13:14]
        def outfeature15(x):
            return x[:,:,:,:,14:15]
        def outfeature16(x):
            return x[:,:,:,:,15:16]
        tmp_input1 = Lambda(outfeature1, output_shape=config["collapse_shape"])(features1)
        tmp_input2 = Lambda(outfeature1, output_shape=config["collapse_shape"])(features2)
        tmp_inputs = concatenate([tmp_input1, tmp_input2], axis=-1)
        tmp_inputs = Conv3D(1, (1,1,1), activation='relu', padding='same')(tmp_inputs)
        AllFeatures.append(tmp_inputs)
        tmp_input1 = Lambda(outfeature2, output_shape=config["collapse_shape"])(features1)
        tmp_input2 = Lambda(outfeature2, output_shape=config["collapse_shape"])(features2)
        tmp_inputs = concatenate([tmp_input1, tmp_input2], axis=-1)
        tmp_inputs = Conv3D(1, (1,1,1), activation='relu', padding='same')(tmp_inputs)
        AllFeatures.append(tmp_inputs)
        tmp_input1 = Lambda(outfeature3, output_shape=config["collapse_shape"])(features1)
        tmp_input2 = Lambda(outfeature3, output_shape=config["collapse_shape"])(features2)
        tmp_inputs = concatenate([tmp_input1, tmp_input2], axis=-1)
        tmp_inputs = Conv3D(1, (1,1,1), activation='relu', padding='same')(tmp_inputs)
        AllFeatures.append(tmp_inputs)
        tmp_input1 = Lambda(outfeature4, output_shape=config["collapse_shape"])(features1)
        tmp_input2 = Lambda(outfeature4, output_shape=config["collapse_shape"])(features2)
        tmp_inputs = concatenate([tmp_input1, tmp_input2], axis=-1)
        tmp_inputs = Conv3D(1, (1,1,1), activation='relu', padding='same')(tmp_inputs)
        AllFeatures.append(tmp_inputs)
        tmp_input1 = Lambda(outfeature5, output_shape=config["collapse_shape"])(features1)
        tmp_input2 = Lambda(outfeature5, output_shape=config["collapse_shape"])(features2)
        tmp_inputs = concatenate([tmp_input1, tmp_input2], axis=-1)
        tmp_inputs = Conv3D(1, (1,1,1), activation='relu', padding='same')(tmp_inputs)
        AllFeatures.append(tmp_inputs)
        tmp_input1 = Lambda(outfeature6, output_shape=config["collapse_shape"])(features1)
        tmp_input2 = Lambda(outfeature6, output_shape=config["collapse_shape"])(features2)
        tmp_inputs = concatenate([tmp_input1, tmp_input2], axis=-1)
        tmp_inputs = Conv3D(1, (1,1,1), activation='relu', padding='same')(tmp_inputs)
        AllFeatures.append(tmp_inputs)
        tmp_input1 = Lambda(outfeature7, output_shape=config["collapse_shape"])(features1)
        tmp_input2 = Lambda(outfeature7, output_shape=config["collapse_shape"])(features2)
        tmp_inputs = concatenate([tmp_input1, tmp_input2], axis=-1)
        tmp_inputs = Conv3D(1, (1,1,1), activation='relu', padding='same')(tmp_inputs)
        AllFeatures.append(tmp_inputs)
        tmp_input1 = Lambda(outfeature8, output_shape=config["collapse_shape"])(features1)
        tmp_input2 = Lambda(outfeature8, output_shape=config["collapse_shape"])(features2)
        tmp_inputs = concatenate([tmp_input1, tmp_input2], axis=-1)
        tmp_inputs = Conv3D(1, (1,1,1), activation='relu', padding='same')(tmp_inputs)
        AllFeatures.append(tmp_inputs)
        tmp_input1 = Lambda(outfeature9, output_shape=config["collapse_shape"])(features1)
        tmp_input2 = Lambda(outfeature9, output_shape=config["collapse_shape"])(features2)
        tmp_inputs = concatenate([tmp_input1, tmp_input2], axis=-1)
        tmp_inputs = Conv3D(1, (1,1,1), activation='relu', padding='same')(tmp_inputs)
        AllFeatures.append(tmp_inputs)
        tmp_input1 = Lambda(outfeature10, output_shape=config["collapse_shape"])(features1)
        tmp_input2 = Lambda(outfeature10, output_shape=config["collapse_shape"])(features2)
        tmp_inputs = concatenate([tmp_input1, tmp_input2], axis=-1)
        tmp_inputs = Conv3D(1, (1,1,1), activation='relu', padding='same')(tmp_inputs)
        AllFeatures.append(tmp_inputs)
        tmp_input1 = Lambda(outfeature11, output_shape=config["collapse_shape"])(features1)
        tmp_input2 = Lambda(outfeature11, output_shape=config["collapse_shape"])(features2)
        tmp_inputs = concatenate([tmp_input1, tmp_input2], axis=-1)
        tmp_inputs = Conv3D(1, (1,1,1), activation='relu', padding='same')(tmp_inputs)
        AllFeatures.append(tmp_inputs)
        tmp_input1 = Lambda(outfeature12, output_shape=config["collapse_shape"])(features1)
        tmp_input2 = Lambda(outfeature12, output_shape=config["collapse_shape"])(features2)
        tmp_inputs = concatenate([tmp_input1, tmp_input2], axis=-1)
        tmp_inputs = Conv3D(1, (1,1,1), activation='relu', padding='same')(tmp_inputs)
        AllFeatures.append(tmp_inputs)
        tmp_input1 = Lambda(outfeature13, output_shape=config["collapse_shape"])(features1)
        tmp_input2 = Lambda(outfeature13, output_shape=config["collapse_shape"])(features2)
        tmp_inputs = concatenate([tmp_input1, tmp_input2], axis=-1)
        tmp_inputs = Conv3D(1, (1,1,1), activation='relu', padding='same')(tmp_inputs)
        AllFeatures.append(tmp_inputs)
        tmp_input1 = Lambda(outfeature14, output_shape=config["collapse_shape"])(features1)
        tmp_input2 = Lambda(outfeature14, output_shape=config["collapse_shape"])(features2)
        tmp_inputs = concatenate([tmp_input1, tmp_input2], axis=-1)
        tmp_inputs = Conv3D(1, (1,1,1), activation='relu', padding='same')(tmp_inputs)
        AllFeatures.append(tmp_inputs)
        tmp_input1 = Lambda(outfeature15, output_shape=config["collapse_shape"])(features1)
        tmp_input2 = Lambda(outfeature15, output_shape=config["collapse_shape"])(features2)
        tmp_inputs = concatenate([tmp_input1, tmp_input2], axis=-1)
        tmp_inputs = Conv3D(1, (1,1,1), activation='relu', padding='same')(tmp_inputs)
        AllFeatures.append(tmp_inputs)
        tmp_input1 = Lambda(outfeature16, output_shape=config["collapse_shape"])(features1)
        tmp_input2 = Lambda(outfeature16, output_shape=config["collapse_shape"])(features2)
        tmp_inputs = concatenate([tmp_input1, tmp_input2], axis=-1)
        tmp_inputs = Conv3D(1, (1,1,1), activation='relu', padding='same')(tmp_inputs)
        AllFeatures.append(tmp_inputs)
        outputs = concatenate(AllFeatures, axis=-1)
        return outputs

    inputs = Input(input_shape)
    # split, encode
    FEATURE_CHANNEL = 16
    def outinput1(x):
        return x[:,:,:,:,:4]
    def outinput2(x):
        return x[:,:,:,:,4:]
    input1 = Lambda(outinput1, output_shape=config["input1_shape"])(inputs)
    input2 = Lambda(outinput2, output_shape=config["input2_shape"])(inputs)
    Encoder = Conv3D(int(FEATURE_CHANNEL/downsize_filters_factor), (3,3,3), activation='relu', padding='same')
    inputs1_feature = Encoder(input1)
    inputs2_feature = Encoder(input2)
    # Cross-Modality CNN
    CM_CNN = collapse(inputs1_feature, inputs2_feature, FEATURE_CHANNEL, config)
    #CM_CNN = concatenate([inputs1_feature, inputs2_feature], axis=-1)
    conv1 = Conv3D(int(32/downsize_filters_factor), (3, 3, 3), activation='relu',
                   padding='same')(CM_CNN)
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
                        callbacks=get_callbacks(model, model_file, initial_learning_rate=initial_learning_rate,
                                                learning_rate_drop=learning_rate_drop,
                                                learning_rate_epochs=learning_rate_epochs))
    #model.save(model_file)



def load_old_model(model_file):
    print("Loading pre-trained model")
    custom_objects = {'dice_coef_loss': dice_coef_loss, 'dice_coef': dice_coef}
    try:
        from keras_contrib.layers import Deconvolution3D
        custom_objects["Deconvolution3D"] = Deconvolution3D
    except ImportError:
        print("Could not import Deconvolution3D. To use Deconvolution3D install keras-contrib.")
    return load_model(model_file, custom_objects=custom_objects)
