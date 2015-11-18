#!/usr/bin/python

import numpy

class Naive_Bayes:
	
	prior_prob = []
	posterior_prob = []
	conditional_prob = []
	label_count = []
	total_count = 0
	mean = []
	sd = []
	
	def __init__(self,training_data,num_of_labels,test_data):
		self.training_data = training_data
		self.test_data = test_data
		self.num_of_labels = number_of_labels

	def preprocess(self, training_data):

		label_count = []
		for i in range(1,number_of_labels):
			label_count.append(0)
		total_count = 0
		feature_count = len(training_data[0])
		features = []
		label = []
		values = []
		for j in range(0,feature_count-1):
			for k in range(0,label_count-1):
				label.append(values)
			features.append(label)
				
				
		
		for i in training_data:
			label_count[i.label] += 1
			total_count += 1
			for j in range(0,feature_count-1):
				for k in range(0,number_of_labels-1):
					features[j].label[k].values.append(i[j+1])
	
		cols_mean = []
		mean = []
		cols_sd = []
		sd = []
		
		for i in features:
			cols_mean = []
			cols_sd = []
			for j in i.labels:
				cols_mean.append(numpy.mean(j.values))
				cols_sd.append(numpy.std(j.values))
			mean.append(cols_mean)
			sd.append(cols_sd)

				
					


	def train_model(self, training_data, number_of_labels):

		preprocess(self,training_data)
		prior_prob = []
		for i in label_count:
			prior_prob.append(label_count[i]/total_count)

	def normal_dist(i,j,data):
		
		return ((1/numpy.sqrt(2*3.14)*sd[j-1][i])*numpy.power(2.7,-((data - mean[j-1][i])*(data - mean[j-1][i])/(2*sd[j-1][i]*sd[j-1][i]))))
	
	def test_model(self,test_data,number_of_labels):
		
		for i in range(0,nember_of_labels-1):
			joint_prob = 1
			for j in range(1,len(test_data)-1):
				joint_prob = joint_prob*normal_dist(i,j,test_data[j])
			posterior_prob.append(prior_prob[i]*joint_prob)

		max_posterior_prob = posterior_prob[0]
 		output_class = 0
		for i in range(0,nember_of_labels-1):
			if posterior_prob[i] > max_posterior_prob :
				max_posterior_prob = posterior_prob[i]
				output_class = i
		return output_class
				
				
		
			
			


