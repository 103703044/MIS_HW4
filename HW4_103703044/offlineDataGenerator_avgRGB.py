import os
import numpy as np
import pandas
from PIL import Image
from library import *
import math
path = './dataset/'
csvPath = "./offlineData/avg_RGB.csv"
imgCount = 1000


def avg_RGB_Func(input):
	input = input.convert("RGB")
	width,height = input.size
	pixel = input.load()
	avgRGB = [0,0,0]

	for i in xrange(width):
		for j in xrange(height):
			avgRGB[0] += pixel[i,j][0]
			avgRGB[1] += pixel[i,j][1]
			avgRGB[2] += pixel[i,j][2]

	avgRGB[0] /= width * height
	avgRGB[1] /= width * height
	avgRGB[2] /= width * height

	return avgRGB

def avgRGB_Euclidean(input,comparison):
	inputData = avg_RGB_Func(input)
	bestImage = ['',float("inf")]
	for row in xrange(0,len(comparison),4):
		distance = 0
		for i in xrange(3):
			distance += pow(abs(float(inputData[i]) - float(comparison[row+i+1][1])),2)
		distance = math.sqrt(distance)
		if distance < bestImage[1]:
			bestImage = [comparison[row][0], distance]
	return bestImage

def avgRGB_Manhattan(input,comparison):
	inputData = avg_RGB_Func(input)
	bestImage = ['',float("inf")]
	for row in xrange(0,len(comparison),4):
		distance = 0
		for i in xrange(3):
			distance += abs((float(inputData[i])) -(float(comparison[row+i+1][1])))
		if distance < bestImage[1]:
			bestImage = [comparison[row][0], distance]
	return bestImage

if __name__ == '__main__':

	if os.path.exists("./offlineData/avg_RGB.csv"):
		os.remove("./offlineData/avg_RGB.csv")
	for i in xrange(imgCount):
		fileName = 'ukbench' + '0'*(5-len(str(i))) + str(i) + '.jpg'
		imgPath = path + fileName
		image = Image.open(imgPath)
		data = pandas.DataFrame(avg_RGB_Func(image))
		with open(csvPath,'a') as save:
			data.to_csv(save, header=True, index_label=fileName)
		print fileName + ' have finished recording.'