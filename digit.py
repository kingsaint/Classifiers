from Naive_Bayes import Naive_Bayes

DIRECTORY = "digitdata"
DIGIT_LENGTH = 28
digitdata = []
digitlabels = []
digittestdata = []
def parse_training_data():
    with open(DIRECTORY + "/trainingimages", "rb") as f:
	temp = []
	counter = 1
	for line in f:
	    if counter >= DIGIT_LENGTH:
		digitdata.append(temp)
		temp = []
		counter = 1
	    else:
		temp.append(line.replace("\n", "").ljust(30, " "))
		counter += 1
    with open(DIRECTORY + "/traininglabels", "rb") as f:
	for line in f:
	    digitlabels.append(int(line))

def parse_testing_data():
    with open(DIRECTORY + "/testimages", "rb") as f:
	temp = []
	counter = 1
	for line in f:
	    if counter >= DIGIT_LENGTH:
		digittestdata.append(temp)
		temp = []
		counter = 1
	    else:
		temp.append(line.replace("\n", "").ljust(30, " "))
		counter += 1


def get_multi_zone(digit):
    white = 0
    black = 0
    for line in digit:
	for char in line:
	    #print char
	    if char == ' ' or char == '\n':
		white+=1
	    else:
		#print char
		black+=1
    #print white
    #print black
    return float(black)/(black+white)

def get_loops_h(digit):
    EMPTY = 0
    FILLED = 1
    LOOP = 2
    looparray = [-1]*len(digit)
    whitespace = [' ', '\n', '\t']
    BLACK = False
    WHITE = False
    for index,line in enumerate(digit):
	BLACK = False
	WHITE = False
	for char in line:
	    if char in whitespace and BLACK:
		WHITE = True
		BLACK = False
	    elif char in whitespace and WHITE:
		continue
	    elif char in whitespace:
		continue
	    elif char not in whitespace and WHITE:
		looparray[index] = LOOP
		WHITE = False
		BLACK = False
	    elif char not in whitespace:
		BLACK = True
	    else:
		continue
	#print line
    for index,curr in enumerate(looparray):
	if curr == -1:
	    if digit[index].isspace():
		looparray[index] = EMPTY
	    else:
		looparray[index] = FILLED

    return looparray
    #print "\n".join(str(x) for x in looparray)
def chunkstring(string, length):
    return list(string[0+i:length+i] for i in range(0, len(string), length))

def get_block_density(digit):
    chunks = []
    temp_chunks = []
    for i in range(0, 6):
	temp_chunks.append([])
    for d in digit:
	for i in range(0, 6):
	    if len(temp_chunks[i]) == 4:
		chunks.append(temp_chunks[i])
		temp_chunks[i] = []
	strings = chunkstring(d, 5)
	#print strings
	for i in range(0, 6):
	    temp_chunks[i].append(strings[i])
    #print chunks
    white = 0
    black = 0
    percentage = []
    for chunk in chunks:
	white = 0
	black = 0
	for c in chunk:
	    for d in c:
		if d == ' ':
		    white+= 1
		else:
		    black+=1
	percentage.append(float(black)/(black + white))
    return percentage

def extract_features(digit):
   feature_1 = get_multi_zone(digit)
   feature_2 = get_loops_h(digit)
   #feature_3 = get_loops(digit, 1)
   feature_4 = get_block_density(digit)
   return [feature_1] + feature_2 + feature_4

def main():
    parse_training_data()
    train_matrix = []
    i = 0
    for d,l in zip(digitdata, digitlabels):
	print "^"*50
	print "\n".join(d)
	print l
	print "$"*50
	features = extract_features(d)
	train_matrix.append([i] + features + [l])
	i+=1
    print "train_matrix"
    for train in train_matrix:
	print len(train)
    #print train_matrix
    parse_testing_data()

    test_matrix = []
    i = 0
    for d in digittestdata:
	print "^"*50
	print "\n".join(d)
	print l
	print "$"*50
	features = extract_features(d)
	test_matrix.append([i] + features)
	i+= 1

    print "test_matrix"
    #print test_matrix
    for test in test_matrix:
	print len(test)

    nb = Naive_Bayes(train_matrix, 10,test_matrix )
    nb.preprocess()
    nb.train_model()
    c = nb.test_model()
    print c

main()
