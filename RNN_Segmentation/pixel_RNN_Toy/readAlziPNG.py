"""
1. Read PNG. Data: hippo+{No}.png, label+{No}.png.
2. Need to store data in [1, height, width, 1].
3. And set the value from 0 to 1.
 


"""

import os, sys
from PIL import Image
import numpy
from random import shuffle
import math

dataNo = 112
height = 48
width = 48


# data tag
data = numpy.zeros((dataNo, height*width))
for i in range(1, dataNo+1):
    tag_data = "data/hippo_center_patches/hippo"+str(i)+'.png'
    pngfile = Image.open(tag_data)
    pix = pngfile.load()
    pixelValue = numpy.zeros((height, width))
    for h in range(height):
        for w in range(width):
            pixelValue[h,w] = pix[h,w]/256
    pixelValue = pixelValue.reshape(height*width)
    data[i-1,:] = pixelValue
    
target = numpy.zeros((dataNo, height*width))
for i in range(1, dataNo+1):
    tag_target = "data/hippo_center_patches/label"+str(i)+'.png'
    pngfile = Image.open(tag_target)
    pix = pngfile.load()
    pixelValue = numpy.zeros((height, width))
    for h in range(height):
        for w in range(width):
            pixelValue[h,w] = pix[h,w]/256
    pixelValue = pixelValue.reshape(height*width)
    target[i-1,:] = pixelValue

print (data.shape,target.shape)


dataOrder = [i for i in range(data.shape[0])]
shuffle(dataOrder)

# train:validation:test = 8:1:1
trainNo = math.floor(0.8*data.shape[0])
validNo = math.floor(0.1*data.shape[0])

trainData = data[dataOrder[0:trainNo], :]
validData = data[dataOrder[trainNo:trainNo+validNo], :]
testData = data[dataOrder[trainNo+validNo:], :]

trainTarget = target[dataOrder[0:trainNo], :]
validTarget = target[dataOrder[trainNo:trainNo+validNo], :]
testTarget = target[dataOrder[trainNo+validNo:], :]


 
