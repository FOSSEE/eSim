#The MIT License (MIT)

#PSpice to Oscad Schematic Converter
#This code is written by Suryavamshi Tenneti, FOSSEE, IIT Bombay
#The code is modified by Sumanto Kar and Gloria Nandihal, FOSSEE, IIT Bombay


from header import *

class Wire:
	x1 = 0
	y1 = 0
	x2 = 0
	y2 = 0
	def __init__(self, x1 = 0, y1 = 0, x2 = 0, y2 = 0):
		self.x1 = x1
		self.x2 = x2
		self.y1 = y1
		self.y2 = y2 # print

	def print(self, output_stream):
		output_stream.write('Wire Wire Line\n'+'\t')
		output_stream.write(str(self.x1)+' '+str(self.y1)+' '+str(self.x2)+' ' +str(self.y2)+'\n')

class Connector:
	x = 0
	y = 0

	def __init__(self, x = 0, y = 0):
		self.x = x
		self.y = y # print funciton of Connector class to print connectors format to output schematic file as per KiCad format

	def print(self, output_stream):
		output_stream.write('Connection ~ '+str(self.x)+' '+str(self.y)+'\n')# Function parseWire to get the postion of wires

def parseWire(input_stream, wires):

	line = input_stream.readline().strip()
	while(line[0]!='@'): #print('parsing wire', line)
		#print('parsing wire', line)
		if line[0] == 's':  #reading 's'
			#print('Yes')
			string = line
			t,x1,y1,x2,y2 = string.split()[:-1] # retriving the values from string stream
			x1 = int(x1)
			y1 = int(y1)
			x2 = int(x2)
			y2 = int(y2)

			w = Wire(x1*MULT, y1*MULT, x2*MULT, y2*MULT)
			wires.append(w)
		line = input_stream.readline().strip() # Function parseConn to get the position of junction
	return input_stream

def parseConn(input_stream, conns):
	line = input_stream.readline().strip()
	while(line[0]!= '@'):
		if line[0] == 'j':    #reading 'j'
			string = line
			t,x1,y1 = string.split()
			x1 = int(x1)
			y1 = int(y1)
			c = Connector(x1*MULT, y1*MULT)
			conns.append(c)
		line = input_stream.readline().strip()
	return input_stream
