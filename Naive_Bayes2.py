#!/usr/bin/python

import numpy
import math
import numbers
import json

class Naive_Bayes:

	DEBUG = True
    	PRIOR_PROBABILITY = []
    	#PRIOR_CONDITIONAL_PROBABILITY = []
  	FEATURES = []
	INSTANCES_OF_LABELS = []
	FEATURES_SPLITTED_ON_LABEL = []

	number_of_instances = 0
	number_of_features = 0
	TYPE_OF_FEATURES = []
    	PARSED_JSON = ""
  	MEAN = []
   	SD = []

   	def __init__(self,training_data,num_of_labels,test_data):
		self.training_data = training_data
		self.test_data = test_data
		self.num_of_labels = num_of_labels

   	def isDiscrete(self,f_c):
		u = numpy.unique(f_c)
		for n in range(0,len(u)):
			if isinstance(u[n],int):
				continue
			else:
				return False
		return True

	def make_json(self):
		json_string ='{'
		for i in range(0,self.number_of_features-1):
			json_string +='\"'+str(i)+'\":{},'
		json_string +='\"'+str(i+1)+'\":{}}'
		self.PARSED_JSON = json.loads(json_string)
		#print json.dumps(self.PARSED_JSON, sort_keys = True, indent = 4)

	def for_Discrete(self,feature,feature_splitted,f_no):
		
		u = numpy.unique(feature)
		json_string = '{'
		for i in range(0,len(u)-1):
			json_string +='\"'+str(u[i])+'\":{},'
		json_string +='\"'+str(u[i+1])+'\":{}}'
		self.PARSED_JSON[str(f_no)] = json.loads(json_string)
		for i in range(0,len(u)): 
			json_string2 = '{'
			for l in range(0,self.num_of_labels-1):
				json_string2 += '\"'+str(l)+'\": {"count":0,"cond_prior":0},' 
			json_string2 += '\"'+str(l+1)+'\":{"count":0,"cond_prior":0}}'
			self.PARSED_JSON[str(f_no)][str(u[i])] = json.loads(json_string2)
		
		

		for l in range(0,self.num_of_labels):
			for i in range(0,len(feature_splitted[l])):
				#print feature_splitted[l][i]
				s =int(self.PARSED_JSON[str(f_no)][str(feature_splitted[l][i])][str(l)]["count"])
				s +=1
				self.PARSED_JSON[str(f_no)][str(feature_splitted[l][i])][str(l)]["count"] = s
		
		print json.dumps(self.PARSED_JSON, sort_keys = True, indent = 4)

	def for_Continuous(self,feature,f_no):
		for l in range(0,self.num_of_labels):
			self.MEAN[f_no][l] = numpy.mean(feature[l])
			self.SD[f_no][l] = numpy.std(feature[l])


   	def preprocess(self):
		
		for i in range(0,self.num_of_labels):
		
			self.INSTANCES_OF_LABELS.append(0)
		self.number_of_instances = len(self.training_data)
		self.number_of_features = len(self.training_data[0])-2

		self.make_json()

		for f in range(0,self.number_of_features):
			feature_values = []
			self.FEATURES.append(feature_values)

			label = []
			col_m = []
			col_sd = []
			for l in range(0,self.num_of_labels):
				v = []
				w = []
				label.append(v)
				col_m.append(w)
				col_sd.append(w)
			self.FEATURES_SPLITTED_ON_LABEL.append(label)
			self.MEAN.append(col_m)
			self.SD.append(col_sd)

		print self.MEAN
		print self.SD

		

			
		for t in self.training_data:
			tuples_label = t[len(t)-1]
			self.INSTANCES_OF_LABELS[tuples_label] += 1
			for f in range(0,self.number_of_features):
				self.FEATURES[f].append(t[f+1])
				self.FEATURES_SPLITTED_ON_LABEL[f][tuples_label].append(t[f+1])
				

		print self.FEATURES
		print self.INSTANCES_OF_LABELS
		print self.FEATURES_SPLITTED_ON_LABEL

		for f in range(0,self.number_of_features):
			
			if self.isDiscrete(self.FEATURES[f]):
				self.TYPE_OF_FEATURES.append(1)
				self.for_Discrete(self.FEATURES[f],self.FEATURES_SPLITTED_ON_LABEL[f],f)
			else:
				self.TYPE_OF_FEATURES.append(0)
				self.for_Continuous(self.FEATURES_SPLITTED_ON_LABEL[f],f)	
			
		print self.TYPE_OF_FEATURES
				
		print self.MEAN	
		print self.SD
	
	def train_model(self):
		for l in range(0,self.num_of_labels):
			self.PRIOR_PROBABILITY.append(self.INSTANCES_OF_LABELS[l]/float(self.number_of_instances))
		print "self.PRIOR_PROBABILITY"
		print self.PRIOR_PROBABILITY

		#calculate posterior probability

		for f in range(0,self.number_of_features):
			if self.TYPE_OF_FEATURES[f] == 1:
				for l in range(0,self.num_of_labels):
					temp = self.FEATURES[f]
					f_range = len(temp)
					class_f_length = len(self.FEATURES_SPLITTED_ON_LABEL[f][l])
				#print length
					# Laplace smoothing
					for k in range(0,f_range):
						if int(str(self.PARSED_JSON[str(f)][str(temp[k])][str(l)]["count"])) == 0:
							for j in range(0,f_range):
								self.PARSED_JSON[str(f)][str(temp[j])][str(l)]["count"] = int(str(self.PARSED_JSON[str(f)][str(temp[j])][str(l)]["count"])) + 1
							class_f_length += 1

					for k in range(0,f_range):
						self.PARSED_JSON[str(f)][str(temp[k])][str(l)]["cond_prior"] = int(str(self.PARSED_JSON[str(f)][str(temp[k])][str(l)]["count"]))/float(class_f_length)

		print json.dumps(self.PARSED_JSON, sort_keys = True, indent = 4)
	def normal_dist(self,i,j,data):

		return ((1/numpy.sqrt(2*3.14)*self.SD[j-1][i])*numpy.power(2.7,-((data - self.MEAN[j-1][i])*(data - self.MEAN[j-1][i])/(2*self.SD[j-1][i]*self.SD[j-1][i]))))

	


	def test_model(self):
		OUTPUT = []
		
		for t in self.test_data:
			posterior_prob = []
			for l in range(0,self.num_of_labels):
				joint_prob = 1.0
				for f in range(1,len(t)):
					if self.TYPE_OF_FEATURES[f-1] == 1:
						if t[f] in self.PARSED_JSON[str(f-1)]:
							joint_prob *= float(str(self.PARSED_JSON[str(f-1)][str(t[f])][str(l)]["cond_prior"]))
						else:
							joint_prob = joint_prob * (1.0/self.number_of_instances)
					else:
						if math.isnan(self.normal_dist(l,f,t[f])):
				    			joint_prob = joint_prob*1
						else:
				    			joint_prob = joint_prob*self.normal_dist(l,f,t[f])
				posterior_prob.append(joint_prob)
						
						
			max_posterior_prob = posterior_prob[0]
			output_class = 0
			for i in range(0,self.num_of_labels):
				if posterior_prob[i] > max_posterior_prob :
					max_posterior_prob = posterior_prob[i]
					output_class = i
			OUTPUT.append(output_class)	

		return OUTPUT



