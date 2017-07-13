import os

config = dict()
config["channels"] = 4 # image itself, and GM, WM, CSF probability
config["batch_size"] = 10
config["GT_class"] = 3 # 0,1,2
config["input_shape"] = [6, 10, 6, 8]
config["input1_shape"] = [6, 10, 6, 4]
config["input2_shape"] = [6, 10, 6, 4]
config["collapse_shape"] = [6, 10, 6, 1]
config["downsize_nb_filters_factor"] = 1
config["pool_size"] = [2,2,2]
config["initial_learning_rate"] = 0.0001
config["model_file"] =  os.path.abspath("./3d_unet_model.h5")
config["learning_rate_drop"] = 0.5
config["decay_learning_rate_every_x_epochs"] = 10
config["n_epochs"] = 50
