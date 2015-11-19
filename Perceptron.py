#!/usr/bin/python

import numpy

class Perceptron:

	def __init__(self,training_data,num_of_labels,test_data):
		self.training_data = training_data
		self.test_data = test_data
		self.num_of_labels = num_of_labels

	w_vector = []
	LABEL_W_VECTORS = []
	ITERATIONS = 100
	BIAS = []
	TARGET_OUTPUT = []
	feature_v_length = 0

	def preprocess(self):
	
		self.feature_v_length = len(self.training_data[0])-2
		for i in range(0,self.feature_v_length):
			self.w_vector.append(0.0)

		for i in range(0,self.num_of_labels):
			self.LABEL_W_VECTORS.append(self.w_vector)
			self.BIAS.append(1.0)
			self.TARGET_OUTPUT.append(i)

		print self.LABEL_W_VECTORS
	
	def train_model(self):
		
		for i in range(0,self.ITERATIONS):
			for j in self.training_data:
				INPUT = []
				for k in range(1,len(j)-1):
					INPUT.append(j[k])

				WEIGHTED_INPUT = []
				OUTPUT = []
				ERROR = []
				for l in range(0,self.num_of_labels):			
					weighted_input = self.BIAS[l]
					for k in range(0,self.feature_v_length):
						weighted_input += self.LABEL_W_VECTORS[l][k]*INPUT[k]
					WEIGHTED_INPUT.append(weighted_input)
					
					output = 1.0/(1.0 + numpy.power(2.7,-(WEIGHTED_INPUT[l])))
					OUTPUT.append(output)
					
					error = OUTPUT[l]*(1.0 - OUTPUT[l])*(self.TARGET_OUTPUT[l] - OUTPUT[l])
					ERROR.append(error)

					LEARNING_RATE = 1.0/(1.0 + i)
					
					for k in range(0,self.feature_v_length):
						self.LABEL_W_VECTORS[l][k] = self.LABEL_W_VECTORS[l][k] + LEARNING_RATE*ERROR[l]*OUTPUT[l]
					self.BIAS[l] = self.BIAS[l] + LEARNING_RATE*ERROR[l]

			print "ITERATION ",i
			print "**********************"
			print self.LABEL_W_VECTORS
			print self.BIAS
					
				
				

					
				
		
			
		
	def test_model(self):
		
		CLASS_VALUE = []
		for l in range(0,self.num_of_labels):
			value = self.BIAS[l]
			for i in range(1,len(self.test_data)):
				value = value + self.LABEL_W_VECTORS[l][i-1]*self.test_data[i]
				CLASS_VALUE.append(value)

		max_value = CLASS_VALUE[0]
		output_class = 0
		for l in range(0,self.num_of_labels):
			if CLASS_VALUE[l] > max_value :
				max_value = CLASS_VALUE[l]
				output_class = l

		return output_class
				
		
		
