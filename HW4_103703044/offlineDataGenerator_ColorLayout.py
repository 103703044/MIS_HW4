import os
import numpy as np
import pandas
from PIL import Image
from scipy.fftpack import dct
import math

partitionSize = 8

path = './dataset/'
csvPath = "./offlineData/ColorLayout.csv"
imgCount = 1000


def Color_Layout_Func(input):
	partition = partitionFunc(input)
	imageYcbCr = YCbCrConverter(partition)
	imageDCT = DCTConverter(imageYcbCr)
	colorLayout = zigZagConverter(imageDCT)
	return colorLayout

def partitionFunc(inputs):
		width,height = inputs.size
		partitionW = width / partitionSize
		partitionH = height / partitionSize
		pixel = inputs.load()
		partitionRGB = [[[0 for _ in xrange(partitionSize)] for _ in xrange(partitionSize)]for _ in xrange(3)]
		for xIndex in xrange(partitionSize):
			for yIndex in xrange(partitionSize):
				count = 0
				for i in xrange(partitionW):
					for j in xrange(partitionH):
						if (xIndex*partitionW + i < width) and (yIndex*partitionH + j < height):
							partitionRGB[0][xIndex][yIndex] += pixel[xIndex*partitionW + i , yIndex*partitionH + j][0]
							partitionRGB[1][xIndex][yIndex] += pixel[xIndex*partitionW + i , yIndex*partitionH + j][1]
							partitionRGB[2][xIndex][yIndex] += pixel[xIndex*partitionW + i , yIndex*partitionH + j][2]
							count += 1
				partitionRGB[0][xIndex][yIndex] /= count
				partitionRGB[1][xIndex][yIndex] /= count
				partitionRGB[2][xIndex][yIndex] /= count
		return partitionRGB

def YCbCrConverter(inputs):
	partitionYCbCr = [[[0 for _ in xrange(partitionSize)] for _ in xrange(partitionSize)]for _ in xrange(3)]
	for i in xrange(partitionSize):
		for j in xrange(partitionSize):
			R = inputs[0][i][j]
			G = inputs[1][i][j]
			B = inputs[2][i][j]
			Y = 0.299*R + 0.587*G + 0.114*B
			Cb = 0.564*(B - Y)
			Cr = 0.713*(R - Y)
			partitionYCbCr[0][i][j] = Y
			partitionYCbCr[1][i][j] = Cb
			partitionYCbCr[2][i][j] = Cr
	return partitionYCbCr

def DCTConverter(inputs):
	DCT = [0 for _ in xrange(3)]
	for i in xrange(3):
		DCT[i] = dct(inputs[i])
	return DCT

def zigZagConverter(inputs):
	length = partitionSize
	zigZag = [[0 for _ in xrange(int(math.pow(length,2)))]for _ in xrange(3)]
	for i in xrange(3):
		count = 0
		x = 0
		y = 0
		direction = "UP"
		while x + y != (length-1)*2:
			zigZag[i][count] = inputs[i][x][y]
			count += 1
			if x == 0:
				if y == length - 1:
					if direction == "UP":
						direction = "DOWN"
						x += 1
					elif direction == "DOWN":
						x += 1
						y -= 1
				elif direction == "UP":
					direction = "DOWN"
					y += 1
				elif direction == "DOWN":
					y -= 1
					x += 1 
			elif x == length - 1:
				if direction == "UP":
					y += 1
					x -= 1
				elif direction == "DOWN":
					direction = "UP"
					y += 1

			elif y == 0:
				if direction == "UP":
					y += 1
					x -= 1
				elif direction == "DOWN":
					direction = "UP"
					x += 1
			elif y == length - 1:
				if direction == "DOWN":
					y -= 1
					x += 1
				elif direction == "UP":
					direction = "DOWN"
					x += 1

			elif direction == "DOWN":
				x += 1
				y -= 1
			elif direction == "UP":
				x -= 1
				y += 1
		zigZag[i][count] = inputs[i][x][y]
	return zigZag

def colorLayout_Euclidean(input,comparison):
	inputData = Color_Layout_Func(input)
	bestImage = ['',float("inf")]
	for row in xrange(0,len(comparison),4):
		distance = 0
		for i in xrange(3):
			temp = 0
			for j in xrange(64):
				temp += pow(abs(float(inputData[i][j]) - float(comparison[row+i+1][j+1])),2)
			distance += math.sqrt(temp)
		if distance < bestImage[1]:
			bestImage = [comparison[row][0], distance]
	return bestImage


if __name__ == '__main__':

	if os.path.exists("./offlineData/ColorLayout.csv"):
		os.remove("./offlineData/ColorLayout.csv")
	for i in xrange(imgCount):
		fileName = 'ukbench' + '0'*(5-len(str(i))) + str(i) + '.jpg'
		imgPath = path + fileName
		image = Image.open(imgPath)
		data = pandas.DataFrame(Color_Layout_Func(image))
		with open(csvPath,'a') as save:
			data.to_csv(save, header=True, index_label=fileName)
		print fileName + ' have finished recording.'