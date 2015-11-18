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

		label_count = []
		for i in range(0,self.num_of_labels):
			label_count.append(0)
		total_count = 0
		feature_count = len(self.training_data[0])-2

		features = []
		label = []
		values = []
	
		print feature_count	
		print label_count

		for j in range(0,feature_count):
			label = []
			for k in range(0,self.num_of_labels):
				label.append(values)
			features.append(label)

		print features
				
		#print feature_count+1	
		
		for i in self.training_data:
			#print len(i)
			label_count[i[len(i)-1]] += 1
			total_count += 1
			for k in range(0,self.num_of_labels):
					if i[len(i)-1] == k:
						for j in range(0,feature_count):
							if not features[j][k]:
								features[j][k] = []
							features[j][k].append(i[j+1])
		

		print label_count
		print "***********************"	
		
		print features
	
		cols_mean = []
		mean = []
		cols_sd = []
		sd = []
		
		for i in features:
			cols_mean = []
			cols_sd = []
			for j in i:
				cols_mean.append(numpy.mean(j))
				cols_sd.append(numpy.std(j))
			mean.append(cols_mean)
			sd.append(cols_sd)

		print mean
		print sd

	def train_model(self):

		preprocess()
		for i in label_count:
			prior_prob.append(label_count[i]/total_count)
		print "****prior probabilities******"

		print prior_prob

				
					


	
				
				
		
			
			


