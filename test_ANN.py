#!/usr/bin/python

#!/usr/bin/python

from ANN import ANN
from array import array
def main():
	r1 = [1,1,2,3,0]
	r2 = [2,4,5,6,1]

	data = []
	data.append(r1)
	data.append(r2)



	print data

	t1 = [1,4,5,6]
	t2 = [1,1,2,3]
	test = []
	test.append(t1)
	test.append(t2)

	p = ANN(data,2,test)
	p.preprocess()
	p.train_model()
	p.test_model()


main()


