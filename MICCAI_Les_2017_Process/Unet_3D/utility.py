import os
import math
import pickle
from functools import partial
from keras.callbacks import ModelCheckpoint, CSVLogger, Callback, LearningRateScheduler

def pickle_dump(item, out_file):
    with open(out_file, "wb") as opened_file:
        pickle.dump(item, opened_file)

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
