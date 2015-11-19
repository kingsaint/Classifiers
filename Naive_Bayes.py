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
		self.num_of_labels = num_of_labels

	def preprocess(self):

		self.label_count = []
		for i in range(0,self.num_of_labels):
			self.label_count.append(0)
		self.total_count = 0
		feature_count = len(self.training_data[0])-2

		features = []
		label = []
		values = []
	
		print feature_count	
		print self.label_count

		for j in range(0,feature_count):
			label = []
			for k in range(0,self.num_of_labels):
				label.append(values)
			features.append(label)

		print features
				
		#print feature_count+1	
		
		for i in self.training_data:
			#print len(i)
			self.label_count[i[len(i)-1]] += 1
			self.total_count += 1
			for k in range(0,self.num_of_labels):
					if i[len(i)-1] == k:
						for j in range(0,feature_count):
							if not features[j][k]:
								features[j][k] = []
							features[j][k].append(i[j+1])
		

		print self.label_count
		print "***********************"
		print features
	
		cols_mean = []
		#mean = []
		cols_sd = []
		#sd = []
		
		for i in features:
			cols_mean = []
			cols_sd = []
			for j in i:
				cols_mean.append(numpy.mean(j))
				cols_sd.append(numpy.std(j))
			self.mean.append(cols_mean)
			self.sd.append(cols_sd)

		print self.mean
		print self.sd

	def train_model(self):

		self.preprocess()

		for i in range(0,len(self.label_count)):
			self.prior_prob.append(self.label_count[i]/float(self.total_count))
		print "****prior probabilities******"

		print self.prior_prob

	def normal_dist(self,i,j,data):
		
		return ((1/numpy.sqrt(2*3.14)*self.sd[j-1][i])*numpy.power(2.7,-((data - self.mean[j-1][i])*(data - self.mean[j-1][i])/(2*self.sd[j-1][i]*self.sd[j-1][i]))))

	def test_model(self):
		for i in range(0,self.num_of_labels):
			joint_prob = 1
			for j in range(1,len(self.test_data)):
				joint_prob = joint_prob*self.normal_dist(i,j,self.test_data[j])
			self.posterior_prob.append(self.prior_prob[i]*joint_prob)

		max_posterior_prob = self.posterior_prob[0]
 		output_class = 0
		for i in range(0,self.num_of_labels):
			if self.posterior_prob[i] > max_posterior_prob :
				max_posterior_prob = self.posterior_prob[i]
				output_class = i
		return output_class

		


	
				
				
		
			
			


