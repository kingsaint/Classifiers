import numpy

class MIRA:

	def __init__(self,training_data,num_of_labels,test_data):
		self.training_data = training_data
		self.test_data = test_data
		self.num_of_labels = num_of_labels

	DEBUG = False
	LABEL_W_VECTORS = []
	ITERATIONS = 1
	feature_v_length = 0

	def preprocess(self):

		for i in range(0,self.num_of_labels):
		    w_vector = []
		    self.feature_v_length = len(self.training_data[0])-2
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
				FEATURE = []
				for k in range(1,len(j)-1):
					FEATURE.append(j[k])
				
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

					tau = max(c,(diff_sum + 1)/(2*f*f))

					for k in range(len(FEATURE)):
						self.LABEL_W_VECTORS[target_output][k] += tau*FEATURE[k]
						self.LABEL_W_VECTORS[max_weight_index][k] -= tau*FEATURE[k]
					
				if self.DEBUG: print self.LABEL_W_VECTORS	

					
			if self.DEBUG: print "ITERATION ",i
			if self.DEBUG: print "**********************"
			if self.DEBUG: print self.LABEL_W_VECTORS
		

	def test_model(self):
		#print self.test_data
		output = []
	    	for t in self.test_data:
			CLASS_VALUE = []
			for l in range(0,self.num_of_labels):
				
				value = 0.0
			   	for i in range(1,len(t)):
					
					value += self.LABEL_W_VECTORS[l][i-1]*t[i]
			    	CLASS_VALUE.append(value)
			
			if self.DEBUG: print CLASS_VALUE
		    	output_class = CLASS_VALUE.index(max(CLASS_VALUE))
		    	output.append(output_class)
	    	return output
