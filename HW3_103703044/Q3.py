import os
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise
import sift
import csv
import pandas


fileList = os.listdir("./dataset/")
# print fileList
fileCount = len(fileList)
clustersNum = 50
for i in xrange(fileCount):
	fileList[i] = fileList[i][7:-4]
# print fileList

def Q3_offline_run(inputs,fileList):
	rank = []
	with open('./Q3.csv', 'rb') as csvfile:
		reader = csv.reader(csvfile)
		index = int(inputs[7:-4]) * (clustersNum+1)
		data = [row for row in reader]
		base = []

		for row in xrange(0,len(data),clustersNum+1):
			b = [0 for i in xrange(clustersNum)]
			for i in xrange(clustersNum):
				b[i] = int (data[row+i+1][1])
			base.append(b)

		query=[]
		for i in xrange(index+1,index+clustersNum+1):
			query.append(int(data[i][1]))

	scoreList = countDistance(query,base)
	for x in xrange(0, len(scoreList)):
		rank.append([scoreList[x],'ukbench'+data[x*(clustersNum+1)][0][:-4]+'jpg'])
		print rank
	rank = sorted(rank,key = lambda x: x[0],reverse=True)[:10]
	return rank
        # res = []
        # n_clusters = 50
        # with open('./Q3.csv', 'rb') as voc:
        #     vocReader = csv.reader(voc)
        #     qIndex = int(inputs[7:-4]) * (n_clusters+1)
        #     data = [row for row in vocReader]
        #     base = []

        #     for row in xrange(0,len(data),n_clusters+1):
        #         b = [0 for i in xrange(n_clusters)]
        #         for i in xrange(n_clusters):
        #             b[i] = int(data[row+i+1][1])
        #         base.append(b)
            
        #     query = []
        #     for i in xrange(qIndex+1,qIndex+1+n_clusters):
        #         query.append(int(data[i][1]))
    
        # scoreList = countDistance(query, base)
        # for x in xrange(0, len(scoreList)):
        #     res.append([scoreList[x],'ukbench'+data[x*(n_clusters+1)][0][:-4]+'jpg'])
        # res = sorted(res,key = lambda x: x[0],reverse=True)[:10]
        # return res
def countDistance(target, codewords):
    codewords.insert(0, target)
    scoreList = pairwise.cosine_similarity(np.array(codewords))[0][1:]
    return scoreList

if __name__ == '__main__':
	path = './offline/sift/'
	n_clusters = 50
	file_number = 1005
	if os.path.exists("./Q3.csv"):
		os.remove("./Q3.csv")
	# siftGroup = sift.read_features_from_file('./offline/sift/00000.sift')[1]
	# for i in fileList:
	# 	filePath = './offline/sift/'+ i + ".sift"
	# 	if 'siftGroup' in locals():
	# 		siftGroup = np.append(siftGroup,sift.read_features_from_file(filePath)[1],axis=0)
	# 	else :
	# 		siftGroup = sift.read_features_from_file(filePath)[1]

	# visual_vocabulary = KMeans(n_clusters=clustersNum, random_state=0).fit(siftGroup)

	sift_bag  = sift.read_features_from_file('./offline/sift/00000.sift')[1]

	for i in xrange(1, file_number+1):
	    file_name = path + '0'*(5-len(str(i))) + str(i) + '.sift'
	    sift_bag = np.append(sift_bag, sift.read_features_from_file(file_name)[1], axis=0)
	visual_vocabulary = KMeans(n_clusters=n_clusters, random_state=0).fit(sift_bag)

	with open("./Q3.csv",'a') as save:
		for i in fileList:
			count = [0 for j in xrange(clustersNum)]
			filePath = './offline/sift/'+ i + ".sift"
			vocList = visual_vocabulary.predict(sift.read_features_from_file(filePath)[1])
			for j in vocList:
				count[j] += 1
			data = pandas.DataFrame(count)
			data.to_csv(save,header=True,index_label = filePath[-10:])

	# path = './offline/sift/'
	# n_clusters = 50
	# file_number = 1005

	# sift_bag  = sift.read_features_from_file('./offline/sift/00000.sift')[1]
	# for i in xrange(1, file_number+1):
	# 	file_name = path + '0'*(5-len(str(i))) + str(i) + '.sift'
	# 	sift_bag = np.append(sift_bag, sift.read_features_from_file(file_name)[1], axis=0)
	# visual_vocabulary = KMeans(n_clusters=n_clusters, random_state=0).fit(sift_bag)

	# with open("./Q3.csv",'a') as save:
	# 	for i in xrange(0, file_number+1):
	# 		count = [0 for j in xrange(n_clusters)]
	# 		file_name = path + '0'*(5-len(str(i))) + str(i) + '.sift'
	# 		vocList = visual_vocabulary.predict(sift.read_features_from_file(file_name)[1])
 #        #codewords.append(visual_vocabulary.predict(sift.read_features_from_file(file_name)[1]))
 #        for j in vocList:
 #        	count[j] += 1
 #        data = pandas.DataFrame(count)
 #        data.to_csv(save,header=True,index_label = file_name[-10:])