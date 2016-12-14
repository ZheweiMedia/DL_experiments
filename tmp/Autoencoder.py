



import numpy as np
import math
from keras.layers import Input, Dense
from keras.models import Model







def normalize(X_n):
    X_n = X_n/(np.linalg.norm(X_n, axis=1).reshape((135, 1)))
    return X_n



def extract_examples(file):
    """Extract the images into a 4D uint8 numpy array [index, y, x, depth].
    Args:
     f: A file object that can be passed into a gzip reader.
    Returns:
     data: A 4D unit8 numpy array [index, y, x, depth].
    Raises:
     ValueError: If the bytestream does not start with 2051.
    """
    print('Extracting', file.name)
    X = np.array([]).reshape(0, 120)
    X_n = []
    
    for line in file:
       if line == '\n' and len(X_n) > 0:
           X_n = np.array(X_n).T
           X_n = normalize(X_n)
           assert X_n.shape == (135, 120)
           X = np.vstack((X, X_n))
           #X = np.vstack((X, np.array(X_n).T))
           X_n = []
       elif line != '\n':
           attributes = line.strip().split(",")
           assert len(attributes) == 136
           X_n_row = [np.float64(attribute) for attribute in attributes[0:135]]
           X_n.append(X_n_row)
    
    #examples = np.array(X)
    return X



def Autoencoder(StackedData):
    # stack data together. Daone
    # 
    
    # data = StackedData.transpose()
    input_feature = StackedData.shape[1]
    print (input_feature)

    x_train = StackedData[0:math.floor(StackedData.shape[0]*0.9), :]
    x_test = StackedData[math.floor(StackedData.shape[0]*0.9):, ]
    input_data = Input(shape=(input_feature,))
    encoded = Dense(200, activation='tanh')(input_data)
    encoded = Dense(100, activation='tanh')(encoded)
    encoded = Dense(50, activation='tanh')(encoded)
    encoded = Dense(5, activation='tanh')(encoded)

    decoded = Dense(50, activation='tanh')(encoded)
    decoded = Dense(100, activation='tanh')(decoded)
    decoded = Dense(200, activation='tanh')(decoded)
    decoded = Dense(input_feature, activation='tanh')(decoded)

    autoencoder = Model(input=input_data, output=decoded)
    autoencoder.compile(optimizer='adadelta', loss='mean_squared_error')
    encoder = Model(input=input_data, output=encoded)
    autoencoder.fit(x_train, x_train,
                nb_epoch=500,
                batch_size=1000,
                shuffle=True,
                validation_data=(x_test, x_test))
    
    return encoder.predict(StackedData)




AD_data = extract_examples( open('AD.txt', 'r'))
compressed_AD = Autoencoder(AD_data)

print (compressed_AD[10])
print (compressed_AD[100])
print (compressed_AD[1000])
print (compressed_AD[1600])
print (compressed_AD[1400])

