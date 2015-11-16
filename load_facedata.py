#!/usr/bin/py

from Class import Facedata

f = open("/home/rajarshi/panda/facedata/facedatatrain","r")

image_obj = []
obj_count = 0
image = []
flag = 1

#print "file name="+f.type
try:
	for line in f:
		if not line.strip():
			if flag == 1 :
				print "Empty line"
				continue
			else:
				obj_count += 1
				image_obj.append(Facedata(obj_count,image,0))
				image = []
				flag = 1
				
				
		
		else:
			flag = 0
			image.append(line[0:60])
finally:
	f.close()

print obj_count

for i in range(0,len(image_obj[0].image)):
	print image_obj[0].image[i]

