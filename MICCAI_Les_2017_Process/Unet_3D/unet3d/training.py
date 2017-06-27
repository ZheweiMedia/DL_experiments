import os
import math
from functools import partial

from keras import backend as K
from keras.callbacks import ModelCheckpoint, CSVLogger, Callback, LearningRateScheduler
from keras.models import load_model

from .model import dice_coef, dice_coef_loss

K.set_image_dim_ordering('th')


# learning rate schedule
def step_decay(epoch, initial_lrate, drop, epochs_drop):
    return initial_lrate * math.pow(drop, math.floor((1+epoch)/float(epochs_drop)))


class SaveLossHistory(Callback):
    def on_train_begin(self, logs={}):
        self.losses = []

    def on_batch_end(self, batch, logs={}):
        self.losses.append(logs.get('loss'))
        pickle_dump(self.losses, "loss_history.pkl")


def get_callbacks(model_file, initial_learning_rate, learning_rate_drop, learning_rate_epochs, logging_dir="."):
    model_checkpoint = ModelCheckpoint(model_file, save_best_only=True)
    logger = CSVLogger(os.path.join(logging_dir, "training.log"))
    history = SaveLossHistory()
    scheduler = LearningRateScheduler(partial(step_decay,
                                              initial_lrate=initial_learning_rate,
                                              drop=learning_rate_drop,
                                              epochs_drop=learning_rate_epochs))
    return [model_checkpoint, logger, history, scheduler]


def load_old_model(model_file):
    print("Loading pre-trained model")
    custom_objects = {'dice_coef_loss': dice_coef_loss, 'dice_coef': dice_coef}
    try:
        from keras_contrib.layers import Deconvolution3D
        custom_objects["Deconvolution3D"] = Deconvolution3D
    except ImportError:
        print("Could not import Deconvolution3D. To use Deconvolution3D install keras-contrib.")
    return load_model(model_file, custom_objects=custom_objects)


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
