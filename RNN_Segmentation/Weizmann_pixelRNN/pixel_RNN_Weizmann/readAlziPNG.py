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
import matplotlib.image as mpimg

dataNo = 100
height = 50
width = 50
channel = 1



# data tag
data = numpy.zeros((dataNo, height*width*channel))
for i in range(dataNo):
    tag_data = "../data/BW/"+str(i)+'.jpg'
    pngfile = Image.open(tag_data)
    pix = pngfile.load()
    pixelValue = numpy.zeros((height, width, channel))
    for h in range(height):
        for w in range(width):
            pixelValue[h,w] = numpy.array(pix[h,w])/256
    pixelValue = pixelValue.reshape(height*width*channel)
    data[i-1,:] = pixelValue
    
target = numpy.zeros((dataNo, height*width))
for i in range(dataNo):
    tag_target = "../data/Label/50_50/"+str(i)+'.png'
    pngfile = Image.open(tag_target)
    pix = pngfile.load()
    pixelValue = numpy.zeros((height, width))
    for h in range(height):
        for w in range(width):
            pixelValue[h,w] = numpy.array(pix[h,w])/256
    pixelValue = pixelValue.reshape(height*width)
    target[i,:] = pixelValue

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

for i in range(validNo):
    tmp = validData[i,:]
    tmp = tmp.reshape((height, width))
    tag = "No{}".format(i)
    mpimg.imsave(tag, tmp, cmap='Greys_r')
    

 
