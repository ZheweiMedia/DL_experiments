from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import sys
import time
import gzip
import pickle
import numpy

from train_baseline import Baseline
from train_lstm import LSTMNet

# Set parameters for Sparse Autoencoder
parser = argparse.ArgumentParser('CNN Exercise.')
parser.add_argument('--learning_rate', 
                    type=float, default=0.1,
                    help='Initial learning rate.')
parser.add_argument('--num_epochs',
                    type=int,
                    default=40, 
                    help='Number of epochs to run trainer.')
parser.add_argument('--decay',
                    type=float,
                    default=0.008, 
                    help='Decay rate of l2 regularization.')
parser.add_argument('--batch_size', 
                    type=int,
                    default=32, 
                    help='Batch size. Must divide evenly into the dataset sizes.')
parser.add_argument('--input_data_dir', 
                    type=str, 
                    default='../mnist/data', 
                    help='Directory to put the training data.')
parser.add_argument('--expanded_data', 
                    type=str, 
                    default='../mnist/data/mnist_expanded.pkl.gz', 
                    help='Directory to put the extended mnist data.')
parser.add_argument('--log_dir', 
                    type=str, 
                    default='logs', 
                    help='Directory to put logging.')
parser.add_argument('--visibleSize',
                    type=int,
                    default=str(28 * 28),
                    help='Used for gradient checking.')
parser.add_argument('--hiddenSize', 
                    type=int,
                    default='200',
                    help='.')
parser.add_argument("--sample_rate",
                    type=int,
                    default=str(44100),
                    help="Sample rate of wav data")
 
FLAGS = None
FLAGS, unparsed = parser.parse_known_args()
mode = int(sys.argv[1])

# ======================================================================
#  STEP 1: Train a baseline model.

if mode == 1:
  FLAGS.batch_size = 30
  nn = Baseline(1)
  accuracy = nn.train_and_evaluate(FLAGS)

  # Output accuracy.
  print(20 * '*' + ' model 1 (Baseline)' + 20 * '*')
  print('accuracy is %f' % accuracy)
  print()


# ====================================================================
# STEP 2: Train an LSTM model.

if mode == 2:
  lstm = LSTMNet(1)
  accuracy, precision, recall = lstm.train_and_evaluate(FLAGS)

  # Output accuracy.
  print(20 * '*' + ' model 2 (LSTM 1) ' + 20 * '*')
  print('accuracy is %f' % accuracy)
  print("precision is %f" % precision)
  print("recall is %f" % recall)
  print()

# ====================================================================
# STEP 3: Train a 2-Layer LSTM model.

if mode == 3:
  lstm = LSTMNet(2)
  accuracy, precision, recall = lstm.train_and_evaluate(FLAGS)

  # Output accuracy.
  print(20 * '*' + ' model 3 (LSTM 2) ' + 20 * '*')
  print('accuracy is %f' % accuracy)
  print("precision is %f" % precision)
  print("recall is %f" % recall)
  print()

# ====================================================================
# STEP 4: Train a 1-Layer Bidirectional LSTM model.

if mode == 4:
  lstm = LSTMNet(3)
  accuracy, precision, recall = lstm.train_and_evaluate(FLAGS)

  # Output accuracy.
  print(20 * '*' + ' model 4 (LSTM 3) ' + 20 * '*')
  print('accuracy is %f' % accuracy)
  print("precision is %f" % precision)
  print("recall is %f" % recall)
  print()
  
