import os
import numpy as np
import pandas
from PIL import Image
from scipy import spatial
import colorsys
import math

path = './dataset/'
csvPath = "./offlineData/avg_HSV.csv"
imgCount = 1000

def avg_HSV_Func(input):
	input = input.convert("RGB")
	width,height = input.size
	pixel = input.load()
	avgHSV = [0,0,0]

	for i in xrange(width):
		for j in xrange(height):
			red, green, blue = pixel[i,j]
			red /= 255.0
			green /= 255.0
			blue /= 255.0
			H,S,V = colorsys.rgb_to_hsv(red, green, blue)
			avgHSV[0] += H
			avgHSV[1] += S
			avgHSV[2] += V

	avgHSV[0] /= width * height
	avgHSV[1] /= width * height
	avgHSV[2] /= width * height

	return avgHSV

def avgHSV_Euclidean(input,comparison):
	inputData = avg_HSV_Func(input)
	bestImage = ['',float("inf")]
	for row in xrange(0,len(comparison),4):
		distance = 0
		for i in xrange(3):
			distance += pow(abs(float(inputData[i]) - float(comparison[row+i+1][1])),2)
		distance = math.sqrt(distance)
		if distance < bestImage[1]:
			bestImage = [comparison[row][0], distance]
	return bestImage

def avgHSV_Manhattan(input,comparison):
	inputData = avg_HSV_Func(input)
	bestImage = ['',float("inf")]
	for row in xrange(0,len(comparison),4):
		distance = 0
		for i in xrange(3):
			distance += abs((float(inputData[i])) -(float(comparison[row+i+1][1])))
		if distance < bestImage[1]:
			bestImage = [comparison[row][0], distance]
	return bestImage

def avgHSV_CosSimilarity(input,comparison):
	inputData = avg_HSV_Func(input)
	bestImage = ['',float("inf")]
	for row in xrange (0,len(comparison),4):
		inputArr = []
		compArr = []
		for i in xrange(3):
			inputArr.append(float(inputData[i]))
			compArr.append(float(comparison[row+i+1][1]))
		distance = spatial.distance.cosine(inputArr,compArr)
		if distance < bestImage[1]:
			bestImage = [comparison[row][0], distance]
	return bestImage

if __name__ == '__main__':

	if os.path.exists("./offlineData/avg_HSV.csv"):
		os.remove("./offlineData/avg_HSV.csv")
	for i in xrange(imgCount):
		fileName = 'ukbench' + '0'*(5-len(str(i))) + str(i) + '.jpg'
		imgPath = path + fileName
		image = Image.open(imgPath)
		data = pandas.DataFrame(avg_HSV_Func(image))
		with open(csvPath,'a') as save:
			data.to_csv(save, header=True, index_label=fileName)
		print fileName + ' have finished recording.'