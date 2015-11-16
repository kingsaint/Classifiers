DIRECTORY = "digitdata"
DIGIT_LENGTH = 20
digitdata = []
digitlabels = []
def parse_training_data():
    BEGIN = 0
    MIDDLE = 1
    END = 2
    with open(DIRECTORY + "/trainingimages", "rb") as f:
	prev = BEGIN
	temp = []
	counter = 0
	for line in f:
	    if line.isspace():
		if prev == MIDDLE:
		    if len(temp) >= DIGIT_LENGTH:
			digitdata.append(temp)
			temp = []
			prev = END
			counter = 0
		    else:
			counter += 1
			temp.append(line)
			continue
		continue
	    else:
		counter += 1
		prev = MIDDLE
		temp.append(line.replace("\n", "").ljust(30, " "))
		print len(line.replace("\n", "").ljust(30, " "))
    #for digit in digitdata:
	#for d in digit:
    with open(DIRECTORY + "/traininglabels", "rb") as f:
	for line in f:
	    digitlabels.append(int(line))

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

    print "\n".join(str(x) for x in looparray)
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
	print strings
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

def extract_features(digit, label):
   feature_1 = get_multi_zone(digit)
   feature_2 = get_loops_h(digit)
   #feature_3 = get_loops(digit, 1)
   feature_4 = get_block_density(digit)

def main():
    parse_training_data()
    maxl = 0
    maxd = []
    for d,l in zip(digitdata, digitlabels):
	print "^"*50
	print "\n".join(d)
	print l
	if len(d) == 25:
	   maxd.append(d)
	maxl = max(len(d), maxl)
	print "$"*50
	extract_features(d, l)
    print maxl
    for d in maxd:
	print "&"*50
	print "".join(d)

main()
