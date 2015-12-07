import numpy
import random
import math

def dsigmoid(y):
    return 1.0 - y**2

def sigmoid(x):
    return math.tanh(x)

class NeuralNetwork:
    DEBUG = False
    LEARNING_RATE = .5


    def __init__(self,NUM_INPUT_NODES, NUM_LABELS):
	self.NUM_OUTPUT_NODES = NUM_LABELS
	self.NUM_INPUT_NODES = NUM_INPUT_NODES + 1
	self.NUM_HIDDEN_NODES = int(math.floor((self.NUM_INPUT_NODES)/float(2)))
	#self.NUM_HIDDEN_NODES = NUM_INPUT_NODES/2.0
	self.INPUT_NODES = []
	self.HIDDEN_NODES = []
	self.OUTPUT_NODES = []
	if self.DEBUG: print "input:%s, hidden:%s, output:%s"%(self.NUM_INPUT_NODES, self.NUM_HIDDEN_NODES, self.NUM_OUTPUT_NODES)

    def preprocess(self):
	#setup input nodes
	if self.DEBUG: print "input weights"
	for i in range(self.NUM_INPUT_NODES):
	    node = Node(self.NUM_HIDDEN_NODES)
	    self.INPUT_NODES.append(node)
	    if self.DEBUG: print node.weights

	#setup hidden nodes
	if self.DEBUG: print "hidden weights"
	for i in range(self.NUM_HIDDEN_NODES):
	    self.HIDDEN_NODES.append(Node(self.NUM_OUTPUT_NODES))
	    if self.DEBUG: print self.HIDDEN_NODES[i].weights

	#setup output nodes
	for i in range(self.NUM_OUTPUT_NODES):
	    self.OUTPUT_NODES.append(Node(0))

    def update(self, features):
	#set data inside input nodes
	for i in range(self.NUM_INPUT_NODES-1):
	    self.INPUT_NODES[i].output = features[i]
	    if self.DEBUG: print "input node: %s, output: %s"%(i, features[i])
	self.INPUT_NODES[-1].output = 1

	#calculate output for all hidden nodes
	for j in range(self.NUM_HIDDEN_NODES):
	    #calculate feature*weight from all input node output(features)
	    net = 0.0
	    for i in range(self.NUM_INPUT_NODES):
		net += self.INPUT_NODES[i].output * self.INPUT_NODES[i].weights[j]
	    #apply activation function
	    if self.DEBUG: print "hidden node: %s, output: %s"%(j, net)
	    self.HIDDEN_NODES[j].output = sigmoid(net)

	output = 0.0
	#calculate output for all output nodes
	for k in range(self.NUM_OUTPUT_NODES):
	    #calculate feature*weight from all hidden node output(features which have activation function applied)
	    net = 0.0
	    for j in range(self.NUM_HIDDEN_NODES):
		net += self.HIDDEN_NODES[j].output * self.HIDDEN_NODES[j].weights[k]
	    #apply activation function
	    if self.DEBUG: print "output node: %s, output: %s"%(k, sigmoid(net))
	    self.OUTPUT_NODES[k].output = sigmoid(net)
	    output = sigmoid(net)
	return output

    def backpropagate(self, target):
        output_deltas = [0.0] * self.NUM_OUTPUT_NODES
        for k in range(self.NUM_OUTPUT_NODES):
            error = target-self.OUTPUT_NODES[k].output
            output_deltas[k] = dsigmoid(self.OUTPUT_NODES[k].output) * error


	# calculate error terms for hidden
        hidden_deltas = [0.0] * self.NUM_HIDDEN_NODES
        for j in range(self.NUM_HIDDEN_NODES):
            error = 0.0
            for k in range(self.NUM_OUTPUT_NODES):
                error = error + output_deltas[k]*self.HIDDEN_NODES[j].weights[k]
            hidden_deltas[j] = dsigmoid(self.HIDDEN_NODES[j].output) * error

	# update output weights
        for j in range(self.NUM_HIDDEN_NODES):
            for k in range(self.NUM_OUTPUT_NODES):
                change = output_deltas[k]*self.HIDDEN_NODES[j].output
		if self.DEBUG: print 'updating hidden weights(%s,%s) by %s'%(j, k, change)
                self.HIDDEN_NODES[j].weights[k] += self.LEARNING_RATE*change

        # update input weights
        for i in range(self.NUM_INPUT_NODES):
            for j in range(self.NUM_HIDDEN_NODES):
                change = hidden_deltas[j]*self.INPUT_NODES[i].output
		if self.DEBUG: print 'updating input weights(%s,%s) by %s'%(i, j, change)
                self.INPUT_NODES[i].weights[j] += self.LEARNING_RATE*change


    def train(self, features, label):
	if self.DEBUG: print "TRAINING Feature: %s with label:%s"%(features, label)
	if self.DEBUG: print "curr_label:%s"%(label)
	targets = []
	self.update(features)
	#for k in range(self.NUM_OUTPUT_NODES):
	    #if k == label:
		#targets.append(1.0)
	    #else:
		#targets.append(0.0)


	self.backpropagate(label)
	#apply backpropogration algorithm

	# calculate error terms for output
        # calculate error

       # #update weights from output to hidden
	    #for j in range(self.NUM_OUTPUT_NODES):
		#target = 0
		#if j == label:
		    #target = 1
		#else:
		    #target = 0
		#actual_output = self.OUTPUT_NODES[j].output
		#actual_hidden = self.HIDDEN_NODES[i].output
		#weight_output_hidden = (target - actual_output) * actual_output * (1.0 - actual_output) * actual_hidden
		#if self.DEBUG: print "deltak:%s"%((target - actual_output) * actual_output * (1 - actual_output))
		#if self.DEBUG: print "update output hidden(%s, %s): %s"%(j, i, weight_output_hidden)
		##update weight of output to hidden
		#self.HIDDEN_NODES[i].weights[j] += self.LEARNING_RATE*weight_output_hidden
		#if self.DEBUG: print "new weight(%s,%s):%s"%(j, i,self.HIDDEN_NODES[i].weights[j] )
	##update weights from hidden to input
	#for i in range(self.NUM_INPUT_NODES):
	    #for j in range(self.NUM_HIDDEN_NODES):
		#sum_output = 0
		#for k in range(self.NUM_OUTPUT_NODES):
		    #target = 0
		    #if k == label:
			#target = 1
		    #else:
			#target = 0
		    #actual_output = self.OUTPUT_NODES[k].output
		    #weight_output_hidden = self.HIDDEN_NODES[j].weights[k]
		    #if self.DEBUG: print "weight_output_hidden:%s"%(weight_output_hidden)
		    #if self.DEBUG: print "deltak:%s"%((target - actual_output) * actual_output * (1 - actual_output))
		    #sum_output += (target - actual_output) * actual_output * (1.0 - actual_output) * weight_output_hidden

		#actual_hidden = self.HIDDEN_NODES[j].output
		#actual_input = self.INPUT_NODES[i].output
		#if self.DEBUG: print "sumoutput:%s"%(sum_output)
		#weight_hidden_input = sum_output * actual_hidden * (1-actual_hidden) * actual_input
		#if self.DEBUG: print "update hidden input(%s, %s): %s"%(j, i, weight_hidden_input)
		#self.INPUT_NODES[i].weights[j] += self.LEARNING_RATE*weight_hidden_input
		#if self.DEBUG: print "new weight(%s,%s):%s"%(j, i,self.INPUT_NODES[i].weights[j] )
	#print "\n\n"




    def printInput(self):
	for i in range(self.NUM_INPUT_NODES):
	    if self.DEBUG: print self.INPUT_NODES[i].weights

    def test(self, features):
	print "TESTING"
	self.printInput()
	output = self.update(features)
	#print "output: %s"%(output)
	return output



class Node:

    def __init__(self, num_weights):
	self.output = -1
	self.weights = []
	for i in range(num_weights):
	    #weight = .5
	    weight = random.random()
	    self.weights.append(weight)


class ANN:
    ITERATIONS = 5
    DEBUG = False


    def __init__(self,training_data,training_data_labels, num_of_labels,test_data, test_data_labels):
	self.training_data = training_data
	self.training_data_labels = training_data_labels
	self.test_data = test_data
	self.test_data_labels = test_data_labels
	self.num_of_labels = num_of_labels
	self.ANN = []
	for i in range(num_of_labels):
	    self.ANN.append(NeuralNetwork(len(training_data[0]), 1))
	for i in range(num_of_labels):
	    self.ANN[i].preprocess()
	#self.ANN1 = NeuralNetwork(len(training_data[0]), 1)
	#self.ANN1.preprocess()

    def train(self):
	for i in range(self.ITERATIONS):
	    for features,label in zip(self.training_data, self.training_data_labels):
		for i in range(self.num_of_labels):
		    if i == label:
			if self.DEBUG: print "training ann:%s with %s"%(i, 1)
			self.ANN[i].train(features, 1)
		    else:
			if self.DEBUG: print "training ann:%s with %s"%(i, 0)
			self.ANN[i].train(features, 0)
	#for i in range(self.ITERATIONS):
	    #for features,label in zip(self.training_data, self.training_data_labels):
		#self.ANN1.train(features, label)

    def test(self):
	output_class = []
	for features, label in zip(self.test_data, self.test_data_labels):
	    print "label: %s"%(label)
	    test_arr = []
	    for i in range(self.num_of_labels):
		#print "ann:%s"%(i)
		output = self.ANN[i].test(features)
		test_arr.append(output)
	    print "output:%s"%(test_arr)
	    output_class.append(test_arr.index(max(test_arr)))
	print output_class
	return output_class


	#total_output = []
	#for features, label in zip(self.test_data, self.test_data_labels):
	    #print "label:%s"%(label)
	    #output = self.ANN1.test(features)
	    #print "output:%s"%(output)
	    #total_output.append(output)
	#return total_output
