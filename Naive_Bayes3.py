import numpy
import math
import numbers
import json
class Naive_Bayes:

	COND_PROB = {}
	FEATURES = {}
	FEATURES_SPLITTED_ON_LABEL = {}
	FEATURES_COUNT = {}
   	def __init__(self,training_data,num_of_labels,test_data):
		self.training_data = training_data
		self.test_data = test_data
		self.num_of_labels = num_of_labels
		self.INSTANCES_OF_LABELS = {}

	def train_model(self):
	    for f in self.FEATURES.keys():
		self.FEATURES[f] = numpy.unique(self.FEATURES[f])
	    #print self.FEATURES
	    for f in self.FEATURES_SPLITTED_ON_LABEL.keys():
		if f not in self.FEATURES_COUNT.keys():
		    self.FEATURES_COUNT[f] = {}
		for c in self.FEATURES_SPLITTED_ON_LABEL[f].keys():
		    if c not in self.FEATURES_COUNT[f].keys():
			self.FEATURES_COUNT[f][c] = {}
		    #print self.FEATURES_SPLITTED_ON_LABEL[f][c]
		    for unique in self.FEATURES[f]:
			if unique not in self.FEATURES_COUNT[f][c].keys():
			    self.FEATURES_COUNT[f][c][unique] = 0
			if unique in self.FEATURES_SPLITTED_ON_LABEL[f][c]:
			    counter = 0
			    for i in self.FEATURES_SPLITTED_ON_LABEL[f][c]:
				if i == unique:
				    counter +=1
			    self.FEATURES_COUNT[f][c][unique] = counter
		    #print self.FEATURES_COUNT[f][c]
		    counter = 0
		    for v in self.FEATURES_COUNT[f][c].values():
			if v == 0:
			    counter += 1
		    for k in self.FEATURES_COUNT[f][c]:
			self.FEATURES_COUNT[f][c][k]+=float(counter)
			self.FEATURES_COUNT[f][c][k] /= (len(self.FEATURES_SPLITTED_ON_LABEL[f][c])+len(self.FEATURES[f]))
	    #print self.FEATURES_COUNT



   	def preprocess(self):
	    for t in self.training_data:
		class_label = t[-1]
		if class_label not in self.INSTANCES_OF_LABELS.keys():
		    self.INSTANCES_OF_LABELS[t[-1]] = 0
		self.INSTANCES_OF_LABELS[t[-1]] +=1
		for i in range(len(t[0:-1])):
		    if i not in self.FEATURES.keys():
			self.FEATURES[i] = []
		    self.FEATURES[i].append(t[i+1])
		    if i not in self.FEATURES_SPLITTED_ON_LABEL.keys():
			label = {}
			for l in range(self.num_of_labels):
			    label[l] = []
			self.FEATURES_SPLITTED_ON_LABEL[i] = label
		    self.FEATURES_SPLITTED_ON_LABEL[i][class_label].append(t[i+1])

	    for label in self.INSTANCES_OF_LABELS:
		self.INSTANCES_OF_LABELS[label] /= float(len(self.training_data))

	    #print self.FEATURES
	    #print self.FEATURES_SPLITTED_ON_LABEL
	    #print self.INSTANCES_OF_LABELS

	def test_model(self):
	    output = []
	    for t in self.test_data:
		posterior_prob = []
		for l in range(self.num_of_labels):
		    joint_prob = 1.0
		    for f in range(0, len(t)):
			if t[f] in self.FEATURES_COUNT[f][l]:
			    joint_prob *= self.FEATURES_COUNT[f][l][t[f]]
			else:
			    joint_prob *= 1.0 / len(self.training_data)
		    joint_prob*= self.INSTANCES_OF_LABELS[l]
		    posterior_prob.append(joint_prob)

		output.append(posterior_prob.index(max(posterior_prob)))
	    #print output
	    return output




