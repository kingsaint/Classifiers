from Naive_Bayes import Naive_Bayes
from Perceptron import Perceptron
from MIRA import MIRA
import operator
import argparse
import time

train_data = []
train_data_labels = []
test_data = []
test_data_labels = []

def parse_training_data(train_file, train_label_file, length, width):
    with open(train_file, "rb") as f:
	temp = []
	counter = 1
	for line in f:
	    if counter >= length:
		train_data.append(temp)
		temp = []
		counter = 1
	    else:
		temp.append(line.replace("\n", "").ljust(width, " "))
		counter += 1
    with open(train_label_file, "rb") as f:
	for line in f:
	    train_data_labels.append(int(line))

def parse_testing_data(test_file, test_label_file, length, width):
    with open(test_file, "rb") as f:
	temp = []
	counter = 1
	for line in f:
	    if counter >= length:
		test_data.append(temp)
		temp = []
		counter = 1
	    else:
		temp.append(line.replace("\n", "").ljust(width, " "))
		counter += 1
    with open(test_label_file, "rb") as f:
	for line in f:
	    test_data_labels.append(int(line))

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
	#print color_counts
	temp_digit_max.append(color_counts[0][0])

    #return len(numColors)
    temp_digit_max.append(max(numColors))
    #print "Loops: %s"%(temp_digit_max)
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
#    hog = {}
    #possible_values = ['0', '1', '-1']
    #for a in possible_values:
	#for b in possible_values:
	    #for c in possible_values:
		#for d in possible_values:
		    #hog[a+b+c+d] = 0
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
#    for i in range(0, len(temp_digit)):
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
    #print "diags: %s, straight: %s"%(diags, straigt)
    return [diags, straigt]
    return hog.values()



def get_filled_blocks5(block_density):
    filled = []
    for b in block_density:
	if b > .5:
	    filled.append(1)
	else:
	    filled.append(0)
    return filled

def get_filled_blocks3(block_density):
    filled = []
    for b in block_density:
	if b > .5:
	    filled.append(1)
	else:
	    filled.append(0)
    return filled

def get_filled_blocks7(block_density):
    filled = []
    for b in block_density:
	if b > .7:
	    filled.append(1)
	else:
	    filled.append(0)
    return filled

def get_pixels(digit):
    pixels = []
    for line in digit:
	for d in line:
	    if d == ' ':
		pixels.append(0)
	    else:
		pixels.append(1)
    return pixels

def extract_features(digit):
   feature_1 = get_loops_horizontal(digit)
   feature_2 = get_block_density(digit)
   feature_3_1 = get_filled_blocks3(feature_2)
   feature_3_2 = get_filled_blocks5(feature_2)
   feature_3_3 = get_filled_blocks7(feature_2)
   feature_3 = feature_3_1 + feature_3_2 + feature_3_3
   #feature_3 = []
   feature_4 = get_loops(digit)
   feature_5 = get_diagonals(digit)
   #feature_6 = get_pixels(digit)
   #feature_5 = []
   return feature_1 + feature_2 + feature_3 + feature_4 + feature_5
   #return feature_5

def extract_features_nb_face(digit):
   feature_1 = get_loops_horizontal(digit)
   feature_2 = get_block_density(digit)
   #feature_2 = []
   feature_3_1 = get_filled_blocks3(feature_2)
   feature_3_2 = get_filled_blocks5(feature_2)
   feature_3_3 = get_filled_blocks7(feature_2)
   feature_3 = feature_3_1+ feature_3_2 + feature_3_3
   #feature_3 = []
   feature_4 = get_loops(digit)
   feature_5 = get_diagonals(digit)
   #feature_5 = []
   return feature_1 + feature_2 + feature_3 + feature_4 + feature_5
   #return feature_5


def extract_features_nb_digit(digit):
   feature_1 = get_loops_horizontal(digit)
   feature_2 = get_block_density(digit)
   feature_2 = []
   feature_3_1 = get_filled_blocks3(feature_2)
   feature_3_2 = get_filled_blocks5(feature_2)
   feature_3_3 = get_filled_blocks7(feature_2)
   feature_3 =  feature_3_2 + feature_3_3
   #feature_3 = []
   feature_4 = get_loops(digit)
   feature_5 = get_diagonals(digit)
   feature_6 = get_pixels(digit)
   #feature_5 = []
   return feature_1 + feature_2 + feature_3 + feature_4 + feature_5 + feature_6
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

def loadData(percent, algorithm, dataset):
    total = len(train_data)
    count = 0.0
    train_matrix = []
    for d,l in zip(train_data, train_data_labels):
	count+=1
	if algorithm == "naivebayes":
	    if dataset == "face":
		features = extract_features_nb_face(d)
	    else:
		features = extract_features_nb_digit(d)
	else:
	    features = extract_features(d)
	train_matrix.append(features + [l])
	if count/total*100 >= percent:
	    break
    train_matrix = reduce_matrix_train(train_matrix)

    test_matrix = []
    for d in test_data:
	if algorithm == "naivebayes":
	    if dataset == "face":
		features = extract_features_nb_face(d)
	    else:
		features = extract_features_nb_digit(d)
	else:
	    features = extract_features(d)
	test_matrix.append(features)

    test_matrix = reduce_matrix_test(test_matrix)
    return (train_matrix, test_matrix)

def runAlgo(algo, num_of_labels, iterations, train_matrix, test_matrix):
    start = time.time()
    if algo == "perceptron":
	if iterations is None:
	    print "iterations required for perceptron"
	    return
	else:
	    if iterations < 1:
		print "more than 1 iteration required"
		return
	p = Perceptron(train_matrix, num_of_labels,test_matrix, iterations )
    elif algo == "naivebayes":
	p = Naive_Bayes(train_matrix, num_of_labels,test_matrix )
    elif algo == "mira":
	if iterations is None:
	    print "iterations required for mira"
	    return
	else:
	    if iterations < 1:
		print "more than 1 iteration required"
		return
	p = MIRA(train_matrix, num_of_labels,test_matrix, iterations )
    else:
	print "algo not found"
	return

    p.preprocess()
    p.train_model()
    testpredictions = p.test_model()
    correct = 0
    incorrect = 0
    for prediction, label in zip(testpredictions, test_data_labels):
	if prediction == label:
	    correct += 1
	else:
	    incorrect +=1
	print "%s\t%s"%(prediction, label)
    print "Final: %s"%(float(correct)/(correct + incorrect))
    print "Total Time:%s sec"%((time.time() - start))



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", help="choose dataset: face or digit", required=True)
    parser.add_argument("--algorithm", help="choose perceptron, naivebayes, mira", required=True)
    parser.add_argument("--iterations", help="choose iterations for perceptron, and mira", type=int)
    parser.add_argument("--percent", help="choose percentage of training data 0 - 100", type=int, required=True)
    args = parser.parse_args()

    if args.percent < 1 or args.percent > 100:
	print "error with percentage, must be from 1-100"
	return

    if args.dataset == "face":
	parse_training_data("facedata/facedatatrain", "facedata/facedatatrainlabels", 70, 60)
	parse_testing_data("facedata/facedatatest", "facedata/facedatatestlabels", 70, 60)
	train_matrix, test_matrix = loadData(args.percent, args.algorithm, args.dataset)
	runAlgo(args.algorithm, 2, args.iterations, train_matrix, test_matrix)
    elif args.dataset == "digit":
	parse_training_data("digitdata/trainingimages", "digitdata/traininglabels", 28, 30)
	parse_testing_data("digitdata/testimages", "digitdata/testlabels", 28, 30)
	train_matrix, test_matrix = loadData(args.percent, args.algorithm, args.dataset)
	runAlgo(args.algorithm, 10, args.iterations, train_matrix, test_matrix)
    else:
	print "error with dataset, must be digit or face"
	return


main()
