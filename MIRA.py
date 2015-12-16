import numpy

class MIRA:

	def __init__(self,training_data,num_of_labels,test_data, iterations):
		self.training_data = training_data
		self.test_data = test_data
		self.num_of_labels = num_of_labels
		self.ITERATIONS = iterations

	DEBUG = False
	LABEL_W_VECTORS = []
	feature_v_length = 0

	def preprocess(self):

		for i in range(0,self.num_of_labels):
		    w_vector = []
		    self.feature_v_length = len(self.training_data[0])-1
		    for i in range(0,self.feature_v_length):
			    w_vector.append(0.0)

		# initialize the weight vectors to 0.0 and the bias to 1.0

		    self.LABEL_W_VECTORS.append(w_vector)


		if self.DEBUG: print self.LABEL_W_VECTORS

	def calculate_mod(self,feature):
		result = 0
		for i in range(len(feature)):
			result += feature[i]*feature[i]

		return numpy.sqrt(result)


	def train_model(self):
	    c = .001
	    for i in range(0,self.ITERATIONS):
		    for j in self.training_data:
			    if self.DEBUG: print "TRAINING TUPLE",j
			    FEATURE = j[0:-1]
			    #for k in range(0,len(j)-1):
				    #FEATURE.append(j[k])

			    target_output = j[-1]

			    f = self.calculate_mod(FEATURE)

			    weighted_inputs = []
			    for l in range(0,self.num_of_labels):
				    weighted_input =0.0
				    for k in range(0,self.feature_v_length):
					    weighted_input += self.LABEL_W_VECTORS[l][k]*FEATURE[k]
				    weighted_inputs.append(weighted_input)

			    max_weight_index = weighted_inputs.index(max(weighted_inputs))
			    #print target_output
			    #print max_weight_index
			    if max_weight_index == target_output:
				continue
			    else:
				    tau = 0

				    diff_sum =	numpy.sum((numpy.array(self.LABEL_W_VECTORS[max_weight_index]) - numpy.array(self.LABEL_W_VECTORS[target_output]))*numpy.array(FEATURE))

				    tau = min(c,(diff_sum + 1)/(2*f*f))

				    for k in range(len(FEATURE)):
					    self.LABEL_W_VECTORS[target_output][k] += tau*FEATURE[k]
					    self.LABEL_W_VECTORS[max_weight_index][k] -= tau*FEATURE[k]

			    if self.DEBUG: print self.LABEL_W_VECTORS


		    if self.DEBUG: print "ITERATION ",i
		    if self.DEBUG: print "**********************"
		    if self.DEBUG: print self.LABEL_W_VECTORS

	  #  c = .001
	    #label = {}
	    #for iteration in range(self.ITERATIONS):
		#for i in range(len(self.training_data)):
		    #features = numpy.array(self.training_data[i][0:-1])
		    #curr_label = self.training_data[i][-1]
		    #for l in range(self.num_of_labels):
			#weights = numpy.array(self.LABEL_W_VECTORS[l])
			##print "faetures:%s"%(features)
			##print "weights:%s"%(weights)
			#label[l] = numpy.dot(features, weights)
		    #all = label.items()
		    #values = [x[1] for x in all]
		    #maxIndex = values.index(max(values))
		    #argmax = all[maxIndex][0]
		    #print "t1:%s"%(label)
		    #print "m1:%s"%(argmax)
		    #f = self.calculate_mod(features)
		    #if curr_label != argmax:
			#weights_max = numpy.array(self.LABEL_W_VECTORS[argmax])
			#weights_label = numpy.array(self.LABEL_W_VECTORS[curr_label])
			#tou = numpy.dot((numpy.subtract(weights_max, weights_label)), features)
			#tou = (tou + 1)/(2.0 * f * f)
			#d = min(c, tou)
			#update_weights = []
			#for j in range(len(self.training_data[i])-1):
			    #update_weights.append(self.training_data[i][j]*d)
			#self.LABEL_W_VECTORS[curr_label] = numpy.add(numpy.array(self.LABEL_W_VECTORS[curr_label]), numpy.array(update_weights))
			#self.LABEL_W_VECTORS[argmax] = numpy.subtract(numpy.array(self.LABEL_W_VECTORS[curr_label]), numpy.array(update_weights))







	def test_model(self):
		#print self.test_data
		output = []
	    	for t in self.test_data:
			CLASS_VALUE = []
			for l in range(0,self.num_of_labels):

				value = 0.0
			   	for i in range(0,len(t)):

					value += self.LABEL_W_VECTORS[l][i]*t[i]
			    	CLASS_VALUE.append(value)

			if self.DEBUG: print CLASS_VALUE
		    	output_class = CLASS_VALUE.index(max(CLASS_VALUE))
		    	output.append(output_class)
	    	return output
