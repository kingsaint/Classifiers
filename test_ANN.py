#!/usr/bin/python

#!/usr/bin/python

from ANN import ANN
from array import array
def main():
	r1 = [1,0,0,0]
	r2 = [2,0,1,1]
	r3 = [3,1,0,1]
	r4 = [4,1,1,0]

	data = []
	data.append(r1)
	data.append(r2)
	data.append(r3)
	data.append(r4)



	print data

	t1 = [1,0,0]
	t2 = [2,0,1]
	test = []
	test.append(t1)
	test.append(t2)

	p = ANN(data,2,test)
	p.preprocess()
	p.train_model()
	p.test_model()


main()


