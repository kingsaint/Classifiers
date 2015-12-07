#!/usr/bin/python

from Naive_Bayes2 import Naive_Bayes
from array import array
def main():

	# training data has the following attributes |ID | feature 1 | feature 2 |...|Class_label|. Where ID is just an index( pseudo column)
	# test data has the following attributes |ID | feature 1 | feature 2 |.... . Where ID is just an index( pseudo column)

	r1 = [1,1,2,3,0]
	r2 = [2,4,5,6,1]
       # r3 = [3,5.58,170,12,1]
	#r4 = [4,5.92,165,10,1]
	#r5 = [5,5,100,6,0]
	#r6 = [6,5.5,150,8,0]
	#r7 = [7,5.42,130,7,0]
	#r8 = [8,5.75,150,9,0]

	data = []
	data.append(r1)
	data.append(r2)
	#data.append(r3)
	#data.append(r4)
	#data.append(r5)
	#data.append(r6)
	#data.append(r7)
	#data.append(r8)

	print data

	t1 = [1,1,2,3]
	t2 = [2,4,5,6]

	test = []
	test.append(t1)
	test.append(t2)
	print test
	nb = Naive_Bayes(data,2,test)
	nb.preprocess()
	nb.train_model()
	predictions = nb.test_model()
	print predictions

main()

