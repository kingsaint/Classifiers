#!/usr/bin/python

from ANN2 import ANN
def main():

	r1 = [0,0]
	r2 = [0,1]
	r3 = [1,0]
	r4 = [1,1]
	data_labels = [0,1,1,0]
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
	#data.append(r9)
	#data.append(r10)

	#print data





	p = ANN(data,data_labels,2,data, data_labels)
	p.train()
	p.test()


main()