#!/usr/bin/python

from ANN2 import ANN
def main():

	r1 = [1,1,1]
	r2 = [2,2,2]
	r3 = [3,3,3]
	r4 = [4,4,4]
	r5 = [1,1,1]
	r6 = [2,2,2]
	r7 = [3,3,3]
	r8 = [4,4,4]
	data_labels = [0,1,0,1,0,1,0,1]
	#r3 = [3,5.58,170,10,1]
	#r4 = [4,5.92,165,10,1]
	#r5 = [5,5,100,6,0]
	#r6 = [6,5.5,127,8,0]
	#r7 = [7,5.42,152,7,2]
	#r8 = [8,5.75,150.2,7,2]
	#r9 = [9,5.3,135,8,0]
	#r10 = [10,5.4,153,7,2]

	data = []
	data.append(r1)
	data.append(r2)
	data.append(r3)
	data.append(r4)
	data.append(r5)
	data.append(r6)
	data.append(r7)
	data.append(r8)
	#data.append(r9)
	#data.append(r10)

	#print data

	t1 = [1,1,1]
	t2 = [2,2,2]
	t3 = [3,3,3]
	t4 = [4,4,4]
	#t3 = [3,5.5,151,7]
	test_data_labels = [0, 1, 0, 1]

	test = []
	test.append(t1)
	test.append(t2)
	test.append(t3)
	test.append(t4)



	p = ANN(data,data_labels,4,test, test_data_labels)
	p.train()
	p.test()


main()
