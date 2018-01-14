import os
import numpy as np
import pandas
from PIL import Image
import math


path = './dataset/'
csvPath = "./offlineData/ColorHistogram.csv"
imgCount = 1000



def Color_Histogram_Func(input):
	input = input.convert("RGB")
	width,height = input.size
	pixel = input.load()

	colorHistogram = [[0 for r in xrange(64)]for g in xrange(8)]

	for i in xrange(width):
		for j in xrange(height):
			red, green, blue = pixel[i,j]
			redHistogram = int(red/32)
			greenHistogram = int(green/32)
			blueHistogram = int(blue/32)
			colorHistogram[redHistogram][greenHistogram*8 + blueHistogram] += 1

	return colorHistogram

def colorHistogram_Euclidean(input,comparison):
	inputData = Color_Histogram_Func(input)
	bestImage = ['',float("inf")]
	for row in xrange(0,len(comparison),9):
		distance = 0
		for i in xrange(8):
			temp = 0
			for j in xrange(64):
				# print str(i+row+1) + " " + str(j+1)
				temp += abs(float(inputData[i][j]) - float(comparison[i+row+1][j+1]))
			distance += temp	
		print distance
		if distance < bestImage[1]:
			bestImage = [comparison[row][0], distance]
	print bestImage
	return bestImage

if __name__ == '__main__':

	if os.path.exists("./offlineData/ColorHistogram.csv"):
		os.remove("./offlineData/ColorHistogram.csv")
	for i in xrange(imgCount):
		fileName = 'ukbench' + '0'*(5-len(str(i))) + str(i) + '.jpg'
		imgPath = path + fileName
		image = Image.open(imgPath)
		data = pandas.DataFrame(Color_Histogram_Func(image))
		with open(csvPath,'a') as save:
			data.to_csv(save, header=True, index_label=fileName)
		print fileName + ' have finished recording.'