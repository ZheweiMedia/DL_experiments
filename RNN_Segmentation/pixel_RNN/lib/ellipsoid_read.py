"""
Read ellipsoid.mat data. Like mnist.py, will return a generator.
ellipsoid is 3D, ellipse is 2D. 
Let's start from 2D.


1. replace the input as our data, then use pixel-RNN to do segmentation.


@Zhewei
7/13/2016
"""

import scipy.io
mat = scipy.io.loadmat('../data/ellipsoid_dataset_boundary_enhanced.mat')
print (len(mat.keys()))
print (len(mat.values()))
keys = list(mat.keys())
print (mat['ellipsoid_dataset'].shape)


mat = scipy.io.loadmat('../data/ellipse_dataset_boundary_enhanced.mat')
print (len(mat.keys()))
print (len(mat.values()))
keys = list(mat.keys())
print (keys)
print (mat['ellipse_dataset'].shape)
