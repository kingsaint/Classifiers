#!/usr/bin/python

#!/usr/bin/python

from ANN import ANN
from array import array
def main():
	r1 = [1,6,180,12,1]
	r2 = [2,5.92,190,11,1]
	r3 = [3,5.58,170,12,1]
	r4 = [4,5.92,165,10,1]
	r5 = [5,5,100,6,0]
	r6 = [6,5.5,150,8,0]
	r7 = [7,5.42,130,7,0]
	r8 = [8,5.75,150,9,0]
	
	data = []
	data.append(r1)
	data.append(r2)
	data.append(r3)
	data.append(r4)
	data.append(r5)
	data.append(r6)
	data.append(r7)
	data.append(r8)

	

	print data

	t1 = [1,5.5,150,9]
	t2 = [2,6,182,11]
	
	test = []
	test.append(t1)
	test.append(t2)
	
	p = ANN(data,2,test)
	p.preprocess()
	p.train_model()
	p.test_model()


main()

