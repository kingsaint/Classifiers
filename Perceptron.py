#!/usr/bin/python

import numpy

class Perceptron:

	def __init__(self,training_data,num_of_labels,test_data):
		self.training_data = training_data
		self.test_data = test_data
		self.num_of_labels = num_of_labels

	LABEL_W_VECTORS = []
	ITERATIONS = 1
	BIAS = []
	TARGET_OUTPUT = []
	feature_v_length = 0

	def preprocess(self):

		for i in range(0,self.num_of_labels):
		    w_vector = []
		    self.feature_v_length = len(self.training_data[0])-2
		    for i in range(0,self.feature_v_length):
			    w_vector.append(0.0)

		# initialize the weight vectors to 0.0 and the bias to 1.0

		    self.LABEL_W_VECTORS.append(w_vector)
		    self.BIAS.append(1.0)
		    self.TARGET_OUTPUT.append(0)

		print self.LABEL_W_VECTORS

	def train_model(self):

		for i in range(0,self.ITERATIONS):
			for j in self.training_data:
				print "TRAINING TUPLE",j
				INPUT = []
				for k in range(1,len(j)-1):
					INPUT.append(j[k])
				#print "Input vector"
				#print INPUT
				#WEIGHTED_INPUT = []
				#OUTPUT = []
				#ERROR = []
				self.TARGET_OUTPUT[j[len(j)-1]] = 1
				for l in range(0,self.num_of_labels):
					weighted_input = self.BIAS[l]
					for k in range(0,self.feature_v_length):
						weighted_input += self.LABEL_W_VECTORS[l][k]*INPUT[k]
					#WEIGHTED_INPUT.append(weighted_input)

					#using Sigmoid function as activation function
					with numpy.errstate(over = 'ignore'):
						output = 1.0/(1.0 + numpy.power(2.7,-(weighted_input)))


					#output = weighted_input

					#print "Sigmoid output"
					#print output

					error =(self.TARGET_OUTPUT[l] - output)
					#ERROR.append(error)

					LEARNING_RATE = 1.0/(1.0 + i)

					print "FOR",l
					print "Before Update"
					print self.LABEL_W_VECTORS
					for k in range(0,self.feature_v_length):
					    print "l=",l,"k=",k
					    #print LEARNING_RATE*error*INPUT[k]
					    print "%s,%s"%(k, self.LABEL_W_VECTORS)
					    self.LABEL_W_VECTORS[l][k] += LEARNING_RATE*error*INPUT[k] #problem here
					    print "%s,%s"%(k, self.LABEL_W_VECTORS)

					print "After Update"
					print self.LABEL_W_VECTORS

					self.BIAS[l] = self.BIAS[l] + LEARNING_RATE*error
				self.TARGET_OUTPUT[j[len(j)-1]] = 0
			print "ITERATION ",i
			print "**********************"
			print self.LABEL_W_VECTORS
			print self.BIAS







	def test_model(self):
		for t in self.test_data:
			CLASS_VALUE = []
			for l in range(0,self.num_of_labels):
				value = self.BIAS[l]
				for i in range(1,len(t)):
					value = value + self.LABEL_W_VECTORS[l][i-1]*t[i]
				CLASS_VALUE.append(value)

			print CLASS_VALUE
			max_value = CLASS_VALUE[0]
			output_class = 0
			for l in range(0,self.num_of_labels):
				if CLASS_VALUE[l] > max_value :
					max_value = CLASS_VALUE[l]
					output_class = l

			print output_class
