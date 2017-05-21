import time
import tensorflow as tf
import math
import pickle
import numpy as np

from python_speech_features import mfcc
from preprocess import *

SAMPLE_RATE = 44100
POOLED_MFCC_SIZE = 60

class Baseline(object):
  def __init__(self, mode):
    self.mode = mode
 
  # Read train, valid and test data.
  def read_data(self):
    """
    print("[*] Converting wav files to mfcc features")
    trainX = list(map(lambda x: mfcc(x, samplerate= SAMPLE_RATE), train_set[0]))
    testX = list(map(lambda x: mfcc(x, samplerate= SAMPLE_RATE), test_set[0]))

    print("[*] Saving mfcc features to disk for later use")
    print(trainX[0].shape)
    with open("mfcc_train_set.pkl", "wb") as f:
      pickle.dump(trainX, f)
    with open("mfcc_test_set.pkl", "wb") as f:
      pickle.dump(testX, f)
    
    print("[*] Loading mfcc features from disk")
    with open("mfcc_train_set.pkl", "rb") as f:
      trainX = pickle.load(f)
    with open("mfcc_test_set.pkl", "rb") as f:
      testX = pickle.load(f)

    trainX = [trainX, train_set[1]]
    testX = [testX, test_set[1]]
    print("[*] Saving mfcc features to disk for later use")
    with open("mfcc_train_set.pkl", "wb") as f:
      pickle.dump(trainX, f)
    with open("mfcc_test_set.pkl", "wb") as f:
      pickle.dump(testX, f)

    trainX, testX = createMfccDataset()
    
    print("[*] Pooling mfcc features to fixed size")
    trainX[0] = poolMfccs(trainX[0], POOLED_MFCC_SIZE)
    testX[0] = poolMfccs(testX[0], POOLED_MFCC_SIZE)
    
    print("[*] Saving pooled mfcc features for later use")
    with open("pooled_train_set.pkl", "wb") as f:
      pickle.dump(trainX, f)
    with open("pooled_test_set.pkl", "wb") as f:
      pickle.dump(testX, f)    
    
    """
    print("[*] Loading pooled mfcc features from disk")
    with open("pooled_train_set.pkl", "rb") as f:
      trainX = pickle.load(f)
    with open("pooled_test_set.pkl", "rb") as f:
      testX = pickle.load(f)
      
    """
    # Load labels
    trainY = np.asarray(train_set[1])
    testY = np.asarray(test_set[1])
    """
    return trainX[0], trainX[1], testX[0], testX[1]

  # Baseline model.
  def model_1(self, X, hidden_size):
    # ======================================================================
    # One fully connected layer.
    #
    # ----------------- YOUR CODE HERE ----------------------
    #
    
    # flatten all last dimensions
    XFlat = tf.reshape(X, [-1, POOLED_MFCC_SIZE * 13]) 
    w1_init = tf.truncated_normal([POOLED_MFCC_SIZE * 13, hidden_size], stddev=0.1)
    # Why didn't the below work ?? #
    #w1_init = tf.random_uniform([784, hidden_size])
    b1_init = tf.zeros([hidden_size])

    # Declare Variables
    w1 = tf.Variable(w1_init, name= "w1")
    b1 = tf.Variable(b1_init, name= "b1")
    
    fcl = tf.sigmoid(tf.matmul(XFlat, w1) + b1) 
    
    return fcl

  # Entry point for training and evaluation.
  def train_and_evaluate(self, FLAGS):
    class_num     = 2
    num_epochs    = FLAGS.num_epochs
    batch_size    = FLAGS.batch_size
    learning_rate = FLAGS.learning_rate
    hidden_size   = FLAGS.hiddenSize
    decay         = FLAGS.decay

    trainX, trainY, testX, testY = self.read_data()
    print("[*] Preprocessing done")

    
    with tf.Graph().as_default():
      # Input data
      X = tf.placeholder(tf.float32, [None, POOLED_MFCC_SIZE, 13])
      Y = tf.placeholder(tf.int32, [None])
      is_train = tf.placeholder(tf.bool)
    
      # model 1: base line
      if self.mode == 1:
        features = self.model_1(X, hidden_size)

      # ======================================================================
      # Define softmax layer, use the features.
      # ----------------- YOUR CODE HERE ----------------------
      #
      softmax_W1 = tf.Variable(tf.random_uniform([hidden_size, class_num]),
                               name= "softmax-weights")
      softmax_b1 = tf.Variable(tf.zeros([class_num]),
                               name= "softmax-bias")
      # Produce BATCH_SIZE X CLASS_NUM matrix
      logits = tf.matmul(features, softmax_W1) + softmax_b1

      # ======================================================================
      # Define loss function, use the logits.
      # ----------------- YOUR CODE HERE ----------------------
      #
      loss = tf.reduce_mean(tf.nn.sparse_softmax_cross_entropy_with_logits(logits=logits,
                                                                           labels=Y))

      # ============================f==========================================
      # Define training op, use the loss.
      # ----------------- YOUR CODE HERE ----------------------
      #
      optimizer = tf.train.AdamOptimizer()
      train_op = optimizer.minimize(loss)

      # ======================================================================
      # Define accuracy op.
      # ----------------- YOUR CODE HERE ----------------------
      #
      pred = tf.cast(tf.argmax(logits, axis= 1), "int32")
      accuracy = tf.reduce_sum(tf.cast(tf.equal(pred, Y), "float"))
      # ======================================================================
      # Allocate percentage of GPU memory to the session.
      # If you system does not have GPU, set has_GPU = False
      #
      has_GPU = True
      if has_GPU:
        gpu_option = tf.GPUOptions(per_process_gpu_memory_fraction=0.3)
        config = tf.ConfigProto(gpu_options=gpu_option)
      else:
        config = tf.ConfigProto()

      # Create TensorFlow session with GPU setting.
      with tf.Session(config=config).as_default() as sess:
        tf.global_variables_initializer().run()

        for i in range(num_epochs):
          print(20 * '*', 'epoch', i+1, 20 * '*')
          start_time = time.time()
          s = 0
          while s < len(trainX):
            e = min(s + batch_size, len(trainX))
            batch_x = trainX[s : e]
            batch_y = trainY[s : e]
            sess.run(train_op, feed_dict={X: batch_x, Y: batch_y, is_train: True})
            s = e
            
          end_time = time.time()
          print ('the training took: %d(s)' % (end_time - start_time))

          total_correct = sess.run(accuracy, feed_dict={X: testX, Y: testY, is_train: False})
          print ('accuracy of the trained model %f' % (total_correct / testX.shape[0]))
          print ()
          
        return sess.run(accuracy, feed_dict={X: testX, Y: testY, is_train: False}) / len(testX)
