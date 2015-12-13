import math
import random
import string

ITERATIONS = 1000
random.seed(0)

# calculate a random number where:  a <= rand < b
def rand(a, b):
    return (b-a)*random.random() + a

# Make a matrix (we could use NumPy to speed this up)
def makeMatrix(I, J, fill=0.0):
    m = []
    for i in range(I):
        m.append([fill]*J)
    return m

# our sigmoid function, tanh is a little nicer than the standard 1/(1+e^-x)
def sigmoid(x):
    return math.tanh(x)

# derivative of our sigmoid function, in terms of the output (i.e. y)
def dsigmoid(y):
    return 1.0 - y**2

class NN:
    def __init__(self, ni, nh, no):
        # number of input, hidden, and output nodes
        self.ni = ni + 1 # +1 for bias node
        self.nh = []
	self.nhnodes = int(math.ceil((ni+no)*.75))
	for i in range(nh):
	    self.nh.append(nhnodes)
        self.no = no

        # activations for nodes
        self.ai = [1.0]*self.ni
        self.ah = []
	for i in range(nh):
	    self.ah.append([1.0]*self.nhnodes)
        self.ao = [1.0]*self.no

        self.h_weights = []
	for i in range(nh):
	    self.h_weights.append([1.0]*self.nhnodes)

        self.training_errors = []

        # create weights
        self.wi = makeMatrix(self.ni, self.nh)
        self.wo = makeMatrix(self.nh, self.no)

        # set them to random vaules
        for i in range(self.ni):
            for j in range(self.nh):
                self.wi[i][j] = rand(-0.2, 0.2)
        for j in range(self.nh):
            for k in range(self.no):
                self.wo[j][k] = rand(-2.0, 2.0)

        # last change in weights for momentum
        self.ci = makeMatrix(self.ni, self.nh)
        self.co = makeMatrix(self.nh, self.no)

    def update(self, inputs):
        if len(inputs) != self.ni-1:
            raise ValueError('wrong number of inputs')

        # input activations
        for i in range(self.ni-1):
            #self.ai[i] = sigmoid(inputs[i])
            self.ai[i] = inputs[i]

        # hidden activations
        for j in range(self.nh):
            sum = 0.0
            for i in range(self.ni):
                sum = sum + self.ai[i] * self.wi[i][j]
            self.ah[j] = sigmoid(sum) * self.h_weights[j]

        # output activations
        for k in range(self.no):
            sum = 0.0
            for j in range(self.nh):
                sum = sum + self.ah[j] * self.wo[j][k]
            self.ao[k] = sigmoid(sum)

        return self.ao[:]


    def backPropagate(self, targets, N, M):
        if len(targets) != self.no:
            raise ValueError('wrong number of target values')

        # calculate error terms for output
        output_deltas = [0.0] * self.no
        for k in range(self.no):
            error = targets[k]-self.ao[k]
            output_deltas[k] = dsigmoid(self.ao[k]) * error

        # calculate error terms for hidden
        hidden_deltas = [0.0] * self.nh
        for j in range(self.nh):
            error = 0.0
            for k in range(self.no):
                error = error + output_deltas[k]*self.wo[j][k]
            hidden_deltas[j] = dsigmoid(self.ah[j]) * error

        # update output weights
        for j in range(self.nh):
            for k in range(self.no):
                change = output_deltas[k]*self.ah[j]
                self.wo[j][k] = self.wo[j][k] + N*change + M*self.co[j][k]
                self.co[j][k] = change
                #print N*change, M*self.co[j][k]

        # update input weights
        for i in range(self.ni):
            for j in range(self.nh):
                change = hidden_deltas[j]*self.ai[i]
                self.wi[i][j] = self.wi[i][j] + N*change + M*self.ci[i][j]
                self.ci[i][j] = change

        # calculate error
        error = 0.0
        for k in range(len(targets)):
            error = error + 0.5*(targets[k]-self.ao[k])**2
        return error


    def test(self, patterns):
	output = []
        for p in patterns:
	    output_arr = self.update(p)
            print(p, '->', output_arr)
	    output.append(output_arr.index(max(output_arr)))
	return output

    def weights(self):
        print('Input weights:')
        for i in range(self.ni):
            print(self.wi[i])
        print()
        print('Output weights:')
        for j in range(self.nh):
            print(self.wo[j])

    def train(self, patterns, iterations, N=0.5, M=0.1):
        # N: learning rate
        # M: momentum factor
	counter = 0
	total = len(patterns)*ITERATIONS
        for i in range(iterations):
            error = 0.0
            for f, l in patterns:
		print("iteration:%s, counter:%s, total:%s"%(i, counter, total))
		counter+=1
                inputs = f
                targets = l
		print("features:%s, output:%s"%(inputs, targets))
                self.update(inputs)
                error = error + self.backPropagate(targets, N, M)

            self.training_errors.append(error)

            if i % 100 == 0:
                print('error %-.5f' % error)


class ANN:
	def __init__(self, training_data, training_labels, num_of_labels, test_data):
		self.training_data = training_data
		self.training_labels = training_labels
		self.num_of_labels = num_of_labels
		self.test_data = test_data

	def train(self):
	    pat = [
		[[0,0], [1, 0]],
		[[0,1], [0, 1]],
		[[1,0], [0, 1]],
		[[1,1], [1, 0]]
	    ]

	    self.n = NN(len(self.training_data[0]),int( math.ceil(len(self.training_data[0])*5)), self.num_of_labels)
	    self.n.train(zip(self.training_data, self.training_labels), iterations = ITERATIONS)

	def test(self):
	    # test it
	    print("Testing...")
	    print(self.test_data)
	    return self.n.test(self.test_data)

