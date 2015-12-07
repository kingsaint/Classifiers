#!/usr/bin/python

from ANN2 import ANN
def main():

	data = [[0,0],
		[0,1],
		[1,0],
		[1,1]]
	data = [[0,1],
		[0,2],
		[0,3],
		[0,4]]

	data_labels = [0,1,1,0]
	data_labels = [0,1,2,3]

	print data
	print data_labels

	p = ANN(data,data_labels,4,data, data_labels)
	p.train()
	p.test()


main()
