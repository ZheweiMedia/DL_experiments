"""




"""


import scipy
from scipy.io import loadmat
import pickle
import gzip


data = loadmat('AD_AparcAseg_feature.mat')

AD_data = data['AD_table']

data = loadmat('NC_AparcAseg_feature.mat')

NC_data = data['NC_table']

data = loadmat('pMCI_AparcAseg_feature.mat')

pMCI_data = data['pMCI_table']

data = loadmat('sMCI_AparcAseg_feature.mat')

sMCI_data = data['sMCI_table']

data = loadmat('uMCI_AparcAseg_feature.mat')

uMCI_data = data['uMCI_table']


print (AD_data.shape)
print (NC_data.shape)
print (pMCI_data.shape)
print (sMCI_data.shape)
print (uMCI_data.shape)

with gzip.open("ANpsu.gz", "wb") as output_file:
    pickle.dump([AD_data, NC_data, pMCI_data, sMCI_data, uMCI_data], output_file)
