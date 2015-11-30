from Naive_Bayes import Naive_Bayes
from Perceptron import Perceptron
import operator

DIRECTORY = "facedata"
DIGIT_LENGTH = 70
DIGIT_WIDTH = 60
digitdata = []
digitlabels = []
digittestdata = []
digittestlabels = []
def parse_training_data():
    with open(DIRECTORY + "/facedatatrain", "rb") as f:
	temp = []
	counter = 1
	for line in f:
	    if counter >= DIGIT_LENGTH:
		digitdata.append(temp)
		temp = []
		counter = 1
	    else:
		temp.append(line.replace("\n", "").ljust(DIGIT_WIDTH, " "))
		counter += 1
    with open(DIRECTORY + "/facedatatrainlabels", "rb") as f:
	for line in f:
	    digitlabels.append(int(line))

def parse_testing_data():
    with open(DIRECTORY + "/facedatatest", "rb") as f:
	temp = []
	counter = 1
	for line in f:
	    if counter >= DIGIT_LENGTH:
		digittestdata.append(temp)
		temp = []
		counter = 1
	    else:
		temp.append(line.replace("\n", "").ljust(DIGIT_WIDTH, " "))
		counter += 1
    with open(DIRECTORY + "/facedatatestlabels", "rb") as f:
	for line in f:
	    digittestlabels.append(int(line))


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

def get_loops_horizontal(digit):
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

def get_chunks_string(ROWS, COLS, digit, ):
    chunks = []
    temp_chunks = []
    for i in range(0, COLS):
	temp_chunks.append([])
    for d in digit:
	for i in range(0, COLS):
	    if len(temp_chunks[i]) == ROWS:
		chunks.append(temp_chunks[i])
		temp_chunks[i] = []
	strings = chunkstring(d, 30/COLS)
	#print strings
	for i in range(0, COLS):
	    temp_chunks[i].append(strings[i])
    return chunks


def get_block_density(digit):
    chunks = get_chunks_string(4, 10, digit)    #print chunks
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
class Node:
    x = -1
    y = -1
    color = -1
    visited = False
    def __init__(self, x, y, color):
	self.x = x
	self.y = y
	self.color = color
    def __repr__(self):
	return str(self.color)

def get_edges(v, temp_digit):
    stack = []
    if v.x == 0:
	if v.y == 0:
	    stack.append(temp_digit[v.x][v.y+1])
	    stack.append(temp_digit[v.x+1][v.y])
	elif v.y == len(temp_digit[0])-1:
	    stack.append(temp_digit[v.x][v.y-1])
	    stack.append(temp_digit[v.x+1][v.y])
	else:
	    #print "%s,%s"%(v.x, v.y)
	    stack.append(temp_digit[v.x][v.y-1])
	    stack.append(temp_digit[v.x][v.y+1])
	    stack.append(temp_digit[v.x+1][v.y])
    elif v.x == len(temp_digit)-1:
	if v.y == len(temp_digit[0])-1:
	    stack.append(temp_digit[v.x][v.y-1])
	    stack.append(temp_digit[v.x-1][v.y])
	elif v.y == 0:
	    stack.append(temp_digit[v.x][v.y+1])
	    stack.append(temp_digit[v.x-1][v.y])
	else:
	    stack.append(temp_digit[v.x][v.y-1])
	    stack.append(temp_digit[v.x][v.y+1])
	    stack.append(temp_digit[v.x-1][v.y])
    elif v.y == 0:
	stack.append(temp_digit[v.x+1][v.y])
	stack.append(temp_digit[v.x-1][v.y])
	stack.append(temp_digit[v.x][v.y+1])
    elif v.y == len(temp_digit[0])-1:
	stack.append(temp_digit[v.x+1][v.y])
	stack.append(temp_digit[v.x-1][v.y])
	stack.append(temp_digit[v.x][v.y-1])
    else:
	stack.append(temp_digit[v.x+1][v.y])
	stack.append(temp_digit[v.x-1][v.y])
	stack.append(temp_digit[v.x][v.y+1])
	stack.append(temp_digit[v.x][v.y-1])
    BLACK = 1
    for s in stack:
	if s.color ==  BLACK:
	    stack.remove(s)
    return stack

def get_loops(digit):
    WHITE = 0
    BLACK = 1
    colors = 2
    temp_digit = []
    x = 0
    for line in digit:
	y = 0
	temp = []
	for char in line:
	    if char == ' ':
		temp.append(Node(x, y, WHITE))
	    else:
		temp.append(Node(x, y, BLACK))
	    y+= 1
	temp_digit.append(temp)
	x += 1
    stack = []
    v = temp_digit[0][0]
    stack.append(v)
    while True:
	while stack:
	    v = stack.pop()
	    if v.color == WHITE and v.visited == False:
		v.color = colors
		v.visited = True
		stack = stack + get_edges(v, temp_digit)
	colors+=1
	test = False
	for temp in temp_digit:
	    if not test:
		for c in temp:
		    if not test:
			if c.color == WHITE:
			    stack.append(c)
			    test = True
	if test == False:
	    break

    #for temp in temp_digit:
	#print temp
    numColors = []
    temp_digit_max = []
    temp_digit_avg = []
    for temp in temp_digit:
	color_counts = {}
	for i in range(0, colors):
	    color_counts[i] = 0
	for char in temp:
	    color_counts[char.color] +=1
	    if char.color not in numColors:
		numColors.append(char.color)

	color_counts = sorted(color_counts.items(), key=operator.itemgetter(1), reverse=True)
	temp = 0
	for c in color_counts:
	    temp = temp + c[0]*c[1]
	temp_digit_avg.append(temp)
	print color_counts
	temp_digit_max.append(color_counts[0][0])

    #return len(numColors)
    temp_digit_max.append(max(numColors))
    print "Loops: %s"%(temp_digit_max)
    return temp_digit_max

def get_outline_text(digit):
    temp_digit = []
    x = 0
    for line in digit:
	y = 0
	temp = ""
	for char in line:
	    #print "(%s, %s)"%(x,y)
	    if char == ' ':
		temp+=" "
	    else:
		if len(digit) -1 <=x:
		    if digit[x][y] == ' ' or digit[x-1][y] == ' ' or digit[x][y+1] == ' ' or digit[x][y-1] != ' ':
			#print "%s,%s->%s"%(x, y, "BLACK1")
			temp+="*"
		    else:
			temp+=" "

		elif digit[x+1][y] == ' ' or digit[x-1][y] == ' ' or digit[x][y+1] == ' ' or digit[x][y-1] == ' ':
		    #print "%s,%s->%s"%(x, y, "BLACK2")
		    temp+="*"
		else:
		    temp+=" "
	    y+= 1
	temp_digit.append(temp)
	x += 1
    return temp_digit

def get_outline(digit):
    WHITE = 0
    BLACK = 1
    temp_digit = []
    v = None
    x = 0
    for line in digit:
	y = 0
	temp = []
	for char in line:
	    #print "(%s, %s)"%(x,y)
	    if char == ' ':
		temp.append(Node(x, y, WHITE))
	    else:
		if len(digit) -1 <=x:
		    if digit[x][y] == ' ' or digit[x-1][y] == ' ' or digit[x][y+1] == ' ' or digit[x][y-1] != ' ':
			#print "%s,%s->%s"%(x, y, "BLACK1")
			temp.append(Node(x, y, BLACK))
		    else:
			temp.append(Node(x, y, WHITE))

		elif digit[x+1][y] == ' ' or digit[x-1][y] == ' ' or digit[x][y+1] == ' ' or digit[x][y-1] == ' ':
		    #print "%s,%s->%s"%(x, y, "BLACK2")
		    if not v:
			v = Node(x, y, BLACK)
			temp.append(v)
		    else:
			temp.append(Node(x, y, BLACK))
		else:
		    temp.append(Node(x, y, WHITE))
	    y+= 1
	temp_digit.append(temp)
	x += 1
    return (temp_digit, v)

def chunkarray(l, n):
    n = max(1, n)
    return [l[i:i + n] for i in range(0, len(l), n)]

def get_chunks_array(ROWS, COLS, digit, ):
    chunks = []
    temp_chunks = []
    for i in range(0, COLS):
	temp_chunks.append([])
    for d in digit:
	for i in range(0, COLS):
	    if len(temp_chunks[i]) == ROWS:
		chunks.append(temp_chunks[i])
		temp_chunks[i] = []
	strings = chunkarray(d, 30/COLS)
	#print strings
	for i in range(0, COLS):
	    temp_chunks[i].append(strings[i])
    return chunks


def get_hog(vertex_1,vertex_2 ):
    vertex_1.visited = True
    vertex_2.visited = True
    if vertex_1.color == 1 and vertex_2.color == 1:
	return 1
    return 0

#hog_features = {}
def get_diagonals(digit):
    WHITE = 0
    BLACK = 1
    temp_digit, v = get_outline(digit)
    #chunks = get_chunks_array(4, 10, temp_digit)
    #for chunk in chunks:
	#for arr in chunk:
	    #print arr
	#print "\n"
    hog = {}
    possible_values = ['0', '1', '-1', '2']
    for a in possible_values:
	for b in possible_values:
	    for c in possible_values:
		for d in possible_values:
		    hog[a+b+c+d] = 0
		    #for e in possible_values:
			#for f in possible_values:
			    #for g in possible_values:
				#for h in possible_values:

    #h1 - Top
    #h2 - TopRight
    #h3 - Right
    #h4 - BottomRight
    #h5 - Bottom
    #h6 - BottomLeft
    #h7 - Left
    #h8 - TopLeft
    #for i in range(0, len(temp_digit)-1):
	#for j in range(0, len(temp_digit[0])-1):
	    #if i == 0:
		#if j == 0:
		    #h1 = 0
		    #h2 = 0
		    #h3 = get_hog(temp_digit[i][j], temp_digit[i][j+1])
		    #h4 = get_hog(temp_digit[i][j], temp_digit[i+1][j+1])
		    #h5 = get_hog(temp_digit[i][j], temp_digit[i+1][j])
		    #h6 = 0
		    #h7 = 0
		    #h8 = 0
		#elif j == len(temp_digit[0])-1:
		    #h1 = 0
		    #h2 = 0
		    #h3 = 0
		    #h4 = 0
		    #h5 = get_hog(temp_digit[i][j], temp_digit[i+1][j])
		    #h6 = get_hog(temp_digit[i][j], temp_digit[i+1][j-1])
		    #h7 = get_hog(temp_digit[i][j], temp_digit[i][j-1])
		    #h8 = 0
		#else:
		    #h1 = 0
		    #h2 = 0
		    #h3 = get_hog(temp_digit[i][j], temp_digit[i][j+1])
		    #h4 = get_hog(temp_digit[i][j], temp_digit[i+1][j+1])
		    #h5 = get_hog(temp_digit[i][j], temp_digit[i+1][j])
		    #h6 = get_hog(temp_digit[i][j], temp_digit[i+1][j-1])
		    #h7 = get_hog(temp_digit[i][j], temp_digit[i][j-1])
		    #h8 = 0
	    #elif i == len(temp_digit)-1:
		#if j == len(temp_digit[0])-1:
		    #h1 = get_hog(temp_digit[i][j], temp_digit[i-1][j])
		    #h2 = 0
		    #h3 = 0
		    #h4 = 0
		    #h5 = 0
		    #h6 = 0
		    #h7 = get_hog(temp_digit[i][j], temp_digit[i][j-1])
		    #h8 = get_hog(temp_digit[i][j], temp_digit[i-1][j-1])
		#elif j == 0:
		    #h1 = get_hog(temp_digit[i][j], temp_digit[i-1][j])
		    #h2 = get_hog(temp_digit[i][j], temp_digit[i-1][j+1])
		    #h3 = get_hog(temp_digit[i][j], temp_digit[i][j+1])
		    #h4 = 0
		    #h5 = 0
		    #h6 = 0
		    #h7 = 0
		    #h8 = 0
		#else:
		    #h1 = get_hog(temp_digit[i][j], temp_digit[i-1][j])
		    #h2 = get_hog(temp_digit[i][j], temp_digit[i-1][j+1])
		    #h3 = get_hog(temp_digit[i][j], temp_digit[i][j+1])
		    #h4 = 0
		    #h5 = 0
		    #h6 = 0
		    #h7 = get_hog(temp_digit[i][j], temp_digit[i][j-1])
		    #h8 = get_hog(temp_digit[i][j], temp_digit[i-1][j-1])
	    #elif j == 0:
		#h1 = get_hog(temp_digit[i][j], temp_digit[i-1][j])
		#h2 = get_hog(temp_digit[i][j], temp_digit[i-1][j+1])
		#h3 = get_hog(temp_digit[i][j], temp_digit[i][j+1])
		#h4 = get_hog(temp_digit[i][j], temp_digit[i+1][j+1])
		#h5 = get_hog(temp_digit[i][j], temp_digit[i+1][j])
		#h6 = 0
		#h7 = 0
		#h8 = 0
	    #elif j == len(temp_digit[0])-1:
		#h1 = get_hog(temp_digit[i][j], temp_digit[i-1][j])
		#h2 = 0
		#h3 = 0
		#h4 = 0
		#h5 = get_hog(temp_digit[i][j], temp_digit[i+1][j])
		#h6 = get_hog(temp_digit[i][j], temp_digit[i+1][j-1])
		#h7 = get_hog(temp_digit[i][j], temp_digit[i][j-1])
		#h8 = get_hog(temp_digit[i][j], temp_digit[i-1][j-1])
	    #else:
		#h1 = get_hog(temp_digit[i][j], temp_digit[i-1][j])
		#h2 = get_hog(temp_digit[i][j], temp_digit[i-1][j+1])
		#h3 = get_hog(temp_digit[i][j], temp_digit[i][j+1])
		#h4 = get_hog(temp_digit[i][j], temp_digit[i+1][j+1])
		#h5 = get_hog(temp_digit[i][j], temp_digit[i+1][j])
		#h6 = get_hog(temp_digit[i][j], temp_digit[i+1][j-1])
		#h7 = get_hog(temp_digit[i][j], temp_digit[i][j-1])
		#h8 = get_hog(temp_digit[i][j], temp_digit[i-1][j-1])
	    #key = str(h1) + str(h2) + str(h3) + str(h4) + str(h5) + str(h6) + str(h7) + str(h8)
	    #if key not in hog_features:
		#hog_features[key] = 0
	    #if key not in hog:
		#hog[key] = 1
	    #else:
		#hog[key] += 1

    #h1 - Top - Bottom
    #h2 - Left - Right
    #h3 - TopLeft - BottomLeft
    #h4 - TopRight - BottomLeft
    #for i in range(0, len(temp_digit)):
	#for j in range(0, len(temp_digit[0])):
	    #if i == 0 or i == len(temp_digit)-1:
		#if j == 0 or j == len(temp_digit[0])-1:
		    #h1 = 0
		    #h2 = 0
		    #h3 = 0
		    #h4 = 0
		#else:
		    #h1 = 0
		    #h2 = get_hog(temp_digit[i][j-1], temp_digit[i][j+1])
		    #h3 = 0
		    #h4 = 0
	    #elif j == 0 or j == len(temp_digit[0])-1:
		#h1 = get_hog(temp_digit[i-1][j], temp_digit[i+1][j])
		#h2 = 0
		#h3 = 0
		#h4 = 0
	    #else:
		#h1 = get_hog(temp_digit[i-1][j], temp_digit[i+1][j])
		#h2 = get_hog(temp_digit[i][j-1], temp_digit[i][j+1])
		#h3 = get_hog(temp_digit[i-1][j-1], temp_digit[i+1][j+1])
		#h4 = get_hog(temp_digit[i+1][j+1], temp_digit[i-1][j-1])
	    #key = str(h1) + str(h2) + str(h3) + str(h4)
	    #if key not in hog:
		#hog[key] = 1
	    #else:
		#hog[key] += 1

    for i in range(0, len(temp_digit)):
	for j in range(0, len(temp_digit[0])):
	    temp_digit[i][j].visited = False
    diags = 0
    straigt = 0
    for i in range(0, len(temp_digit)):
	for j in range(0, len(temp_digit[0])):
	    if temp_digit[i][j].visited == False:
		if i == 0 or i == len(temp_digit)-1:
		    if j == 0 or j == len(temp_digit[0])-1:
			pass
		    else:
			pass
		elif j == 0 or j == len(temp_digit[0])-1:
		    pass
		else:
		    diags += get_hog(temp_digit[i][j], temp_digit[i+1][j+1])
		    diags += get_hog(temp_digit[i][j], temp_digit[i+1][j-1])
		    diags += get_hog(temp_digit[i][j], temp_digit[i-1][j+1])
		    diags += get_hog(temp_digit[i][j], temp_digit[i-1][j-1])
		    straigt += get_hog(temp_digit[i][j], temp_digit[i][j+1])
		    straigt += get_hog(temp_digit[i][j], temp_digit[i][j-1])
		    straigt += get_hog(temp_digit[i][j], temp_digit[i+1][j])
		    straigt += get_hog(temp_digit[i][j], temp_digit[i-1][j])



    #for k,v in sorted(hog.items(), key=operator.itemgetter(1), reverse=True):
	#print "%s, %s"%(k, v)
	#print len(hog)
    #for chunk in chunks:
	#hog.append(get_hog(chunk))
    #for chunk in chunks:
	#print chunk

    #print "(%s, %s)"%(v.x, v.y)
    print "diags: %s, straight: %s"%(diags, straigt)
    return [diags, straigt]
    return hog.values()


def get_filled_blocks(block_density):
    filled = []
    for b in block_density:
	if b > .5:
	    filled.append(1)
	else:
	    filled.append(0)
    return filled

def extract_features(digit):
   feature_1 = get_loops_horizontal(digit)
   feature_2 = get_block_density(digit)
   feature_3 = get_filled_blocks(feature_2)
   #feature_3 = []
   feature_4 = get_loops(digit)
   feature_5 = get_diagonals(digit)
   #feature_5 = []
   return feature_1 + feature_2 + feature_3 + feature_4 + feature_5
   #return feature_5

reduce_features = []
def reduce_matrix_train(matrix):
    print "Number of features before reduce: %s"%(len(matrix[0]))
    for k in range(0, len(matrix[0])):
	for j in range(0, len(matrix[0])):
	    temp = -1
	    test = True
	    for i in range(0, len(matrix)):
		#print "%s, %s"%(i, j)
		if temp == -1:
		    temp = matrix[i][j]
		else:
		    if matrix[i][j] != temp:
			test = False
			break
	    if test == True:
		for i in range(0, len(matrix)):
		    matrix[i].pop(j)
		reduce_features.append(j)
		break

    print "Number of features: %s"%(len(matrix[0]))
    return matrix

def reduce_matrix_test(matrix):
    print "Number of features before reduce: %s"%(len(matrix[0]))
    #print len(reduce_features)
    for i in range(0, len(matrix)):
	for j in reduce_features:
	    matrix[i].pop(j)

    print "Number of features: %s"%(len(matrix[0]))
    return matrix


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
    train_matrix = reduce_matrix_train(train_matrix)
    #print "train_matrix"
    #for train in train_matrix:
	#print len(train)
    #print train_matrix
    parse_testing_data()

    test_matrix = []
    i = 0
    #print '\n'.join(digittestdata[0])
    for d in digittestdata:
	#print "^"*50
	#print "\n".join(d)
	#print l
	#print "$"*50
	features = extract_features(d)
	test_matrix.append([i] + features)
	i+= 1

    test_matrix = reduce_matrix_test(test_matrix)

    #print "test_matrix"
    #print test_matrix
    #for test in test_matrix:
	#print len(test)

    nb = Naive_Bayes(train_matrix, 10,test_matrix )
    nb.preprocess()
    nb.train_model()
    testpredictions = nb.test_model()
    correct = 0
    incorrect = 0
    for prediction, label in zip(testpredictions, digittestlabels):
	if prediction == label:
	    correct += 1
	else:
	    incorrect +=1
	print "%s\t%s"%(prediction, label)
    print "Final: %s"%(float(correct)/(correct + incorrect))

    p = Perceptron(train_matrix, 10,test_matrix )
    p.preprocess()
    p.train_model()
    testpredictions = p.test_model()
    correct = 0
    incorrect = 0
    for prediction, label in zip(testpredictions, digittestlabels):
	if prediction == label:
	    correct += 1
	else:
	    incorrect +=1
	print "%s\t%s"%(prediction, label)
    print "Final: %s"%(float(correct)/(correct + incorrect))


main()
