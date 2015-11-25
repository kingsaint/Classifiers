#!/usr/bin/python

import numpy

class ANN:

	def __init__(self,training_data,num_of_labels,test_data):
		self.training_data = training_data
		self.test_data = test_data
		self.num_of_labels = num_of_labels

	w_vector = []
	OUTPUT_LAYER_W_VECTORS = []
	HIDDEN_LAYER_W_VECTORS = []
	ITERATIONS = 1
	HIDDEN_NODES = 2
	OUTPUT_LAYER_BIAS = []
	HIDDEN_LAYER_BIAS = []
	TARGET_OUTPUT = []
	HIDDEN_LAYER_OUTPUT = []
	feature_v_length = 0

	def preprocess(self):

		# initialize the weight vectors and bias for hidden layer nodes
	
		self.feature_v_length = len(self.training_data[0])-2
		for i in range(0,self.feature_v_length):
			self.w_vector.append(0.0)

		for i in range(0,self.HIDDEN_NODES):
			self.HIDDEN_LAYER_W_VECTORS.append(self.w_vector)
			self.HIDDEN_LAYER_BIAS.append(1.0)
			self.HIDDEN_LAYER_OUTPUT.append(0.0)
		
		#initialize the wight vectors and bias for output layer nodes
		
		for i in range(0,self.HIDDEN_NODES):
			self.w_vector.append(0.0)

		for i in range(0,self.num_of_labels):
			self.OUTPUT_LAYER_W_VECTORS.append(self.w_vector)
			self.OUTPUT_LAYER_BIAS.append(1.0)
			self.TARGET_OUTPUT.append(0.0)

		
	
	def train_model(self):
		
		for i in range(0,self.ITERATIONS):
			for j in self.training_data:
		
				# **********  Propagate the inputs forward forward ************ #				

				HIDDEN_LAYER_INPUT = []
				for k in range(1,len(j)-1):
					HIDDEN_LAYER_INPUT.append(j[k])

				# Hidden layer					
				

				OUTPUT_LAYER_INPUT = [] # this is the output of the hidden layter and input of the output layer
				for h in range(0,self.HIDDEN_NODES):
			
					weighted_input = self.HIDDEN_LAYER_BIAS[h]
					for k in range(0,self.feature_v_length):
						weighted_input += self.HIDDEN_LAYER_W_VECTORS[h][k]*HIDDEN_LAYER_INPUT[k]
					
					#using Sigmoid function as activation function for hidden layer nodes
					with numpy.errstate(over = 'ignore'):
						output = 1.0/(1.0 + numpy.power(2.7,-(weighted_input)))

					OUTPUT_LAYER_INPUT.append(output)

				# Output layer				

				OUTPUT = []
				for l in range(0,self.num_of_labels):
					
					weighted_input = self.OUTPUT_LAYER_BIAS[l]
					for k in range(0,self.HIDDEN_NODES):
						weighted_input += self.OUTPUT_LAYER_W_VECTORS[l][k]*OUTPUT_LAYER_INPUT[k]					

					#using Sigmoid function as activation function for output layer nodes
					with numpy.errstate(over = 'ignore'):
						output = 1.0/(1.0 + numpy.power(2.7,-(weighted_input)))

					OUTPUT.append(output)

				# ***********  Backpropagate the errors ***********#

				LEARNING_RATE = 1.0/(1.0 + i)

				# Calculate the error of each of the output layer nodes				

				OUTPUT_LAYER_ERROR = []
				self.TARGET_OUTPUT[j[len(j)-1]] = 1
				for l in range(0,self.num_of_labels):
					error = OUTPUT[l]*(1-OUTPUT[l])*(self.TARGET_OUTPUT[l] - OUTPUT[l])
					OUTPUT_LAYER_ERROR.append(error)
				self.TARGET_OUTPUT[j[len(j)-1]] = 0

				# Calculate the error of each of the hidden layer nodes

				HIDDEN_LAYER_ERROR = []
				for h in range(0,self.HIDDEN_NODES):
					backpropagated_err = 0
					for l in range(0,self.num_of_labels):
						backpropagated_err += OUTPUT_LAYER_ERROR[l]*self.OUTPUT_LAYER_W_VECTORS[l][h]
					error = OUTPUT_LAYER_INPUT[h]*(1-OUTPUT_LAYER_INPUT[h])*backpropagated_err
					HIDDEN_LAYER_ERROR.append(error)			

				# Update the weights  and bias of the output layer
				
				for l in range(0,self.num_of_labels):	
					for h in range(0,self.HIDDEN_NODES):
						self.OUTPUT_LAYER_W_VECTORS[l][h] += LEARNING_RATE*OUTPUT_LAYER_ERROR[l]*OUTPUT_LAYER_INPUT[h] #problem here
					self.OUTPUT_LAYER_BIAS[l] += LEARNING_RATE*OUTPUT_LAYER_ERROR[l]	
						


				# Update the weights and bias of the hidden layer

				for h in range(0,self.HIDDEN_NODES):
					for k in range(0,self.feature_v_length):
						self.HIDDEN_LAYER_W_VECTORS[h][k] += LEARNING_RATE*HIDDEN_LAYER_ERROR[h]*HIDDEN_LAYER_INPUT[k]
					self.HIDDEN_LAYER_BIAS[h] += LEARNING_RATE*HIDDEN_LAYER_ERROR[h]

					
				self.TARGET_OUTPUT[j[len(j)-1]] = 0
			print "ITERATION ",i
			print "**************"
			print "Hidden Layer weights and bias"
			print "*****************************"
			print self.HIDDEN_LAYER_W_VECTORS
			print self.HIDDEN_LAYER_BIAS
			print "Output Layer weights and bias"
			print "***************************"
			print self.OUTPUT_LAYER_W_VECTORS
			print self.OUTPUT_LAYER_BIAS	
			
					
				
					
				
			
		
	def test_model(self):
		for t in self.test_data:

			HIDDEN_LAYER_INPUT = []
			for k in range(1,len(t)):
				HIDDEN_LAYER_INPUT.append(t[k])

				# Hidden layer					
				

			OUTPUT_LAYER_INPUT = [] # this is the output of the hidden layter and input of the output layer
			for h in range(0,self.HIDDEN_NODES):
			
				weighted_input = self.HIDDEN_LAYER_BIAS[h]
				for k in range(1,len(t)):
					weighted_input += self.HIDDEN_LAYER_W_VECTORS[h][k-1]*HIDDEN_LAYER_INPUT[k-1]
					
					#using Sigmoid function as activation function for hidden layer nodes
				with numpy.errstate(over = 'ignore'):
					output = 1.0/(1.0 + numpy.power(2.7,-(weighted_input)))

				OUTPUT_LAYER_INPUT.append(output)

				# Output layer				

			OUTPUT = []
			for l in range(0,self.num_of_labels):
					
				weighted_input = self.OUTPUT_LAYER_BIAS[l]
				for k in range(0,self.HIDDEN_NODES):
					weighted_input += self.OUTPUT_LAYER_W_VECTORS[l][k]*OUTPUT_LAYER_INPUT[k]					

					#using Sigmoid function as activation function for output layer nodes
				with numpy.errstate(over = 'ignore'):
					output = 1.0/(1.0 + numpy.power(2.7,-(weighted_input)))

				OUTPUT.append(output)

			print OUTPUT
			max_value = OUTPUT[0]
			output_class = 0
			for l in range(0,self.num_of_labels):
				if OUTPUT[l] > max_value :
					max_value = OUTPUT[l]
					output_class = l

			print output_class
				
		
		
