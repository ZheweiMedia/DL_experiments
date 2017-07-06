import os

config = dict()
config["channels"] = 1
config["batch_size"] = 2
config["GT_class"] = 2 # 0,1
config["input_shape"] = [24, 48, 48, 1]
config["downsize_nb_filters_factor"] = 1
config["pool_size"] = [2,2,2]
config["initial_learning_rate"] = 0.00001
config["model_file"] =  os.path.abspath("./3d_unet_model.h5")
config["learning_rate_drop"] = 0.5
config["decay_learning_rate_every_x_epochs"] = 10
config["n_epochs"] = 50
