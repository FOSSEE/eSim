#The MIT License (MIT)

#PSpice to Oscad Schematic Converter
#This code is written by Suryavamshi Tenneti, FOSSEE, IIT Bombay
#The code is modified by Sumanto Kar and Gloria Nandihal, FOSSEE, IIT Bombay



from header import *						#Importing header file from PythonLib folder
class Attribute:						#defining class Attribute
	x = 0							#declaring and initialising coordinates
	y = 0
	orient = ''						#declaring and initialising orientation
	hjust = ''						#declaring and initialising hjust
	vjust = ''						#declaring and initialising vjust
	isHidden = False					#declaring and initialising isHidden
	name =''						#declaring and initialising component name
	value = ''						#declaring and initialising value
	'''Sample attribute line in a Pspice library:
   	a 0 s 11 0 10 34 hln 100 PART=EPOLY
	a: implies that this line describes an attribute
	s: something to do with "isHidden"
	10, 34: "x", "y" wrt the origin of the Component of which this is an attribute.
	hln: "orient"(h), "hjust"(l), "vjust"(n)
	100: text size in % in Pspice. Ignore.
	PART: "name" of the attribute.
	EPOLY: "value" of the attribute. '''
	def __init__(self,line = ''):						#defining the _init_ Constructor
		a = ''								#declaring and initialising a
		vis = ''							#declaring and initialising vis
		temp = ''							#declaring and initialising temp
		t = 0								#declaring and initialising t
		x0 = 0								#declaring and initialising x0
		y0 = 0								#declaring and initialising y0
		if len(line) != 0:
			input_line = line.strip().split()			#making a copy of line and spliting it
			#print(input_line)
			a,t,temp,vis,x0,y0,temp = input_line[:7]		#copying input_line
			self.orient,self.hjust,self.vjust = list(input_line[7])
			t= input_line[8]					#setting sizes to 8
			temp = ' '.join(map(str,input_line[9:]))		#mapping and then joining in temp
			temp = temp.split()[0]					#spliting the temp
			x0 = int(x0)						#taking the x coordinate in integer format	
			y0 = int(y0)						#taking the y coordinate in integer format

			self.x = x0 * MULT					#as size of pspice components is small therefore 
										#increasing the size 10 times
			self.y = y0 * MULT					#MULT=10 from header file

			t = temp.find('=')					#everything in temp occuring before the '=' is the "name", 
										#and everything after it is the "value".
			self.name = temp[0:t]					#storing the name
			self.value = temp[t+1:]					#storing the value
			if vis.find('13') == -1:				#if '13' is not found returns -1
				self.isHidden = True				#if yes, storing the isHidden as True

			else:
				self.isHidden  = False				#otherwise storing the isHidden as False

			#print('attribute name->',self.name,'attribute value->', self.value)

	def print(self, output_stream):						#defining the print function
		#print('Type in attr->',self.value)
		output_stream.write(' "'+self.value+'" '+self.orient.upper()+' '+str(self.x)+' ' +str(self.y)+' 30  000'+str(int(self.isHidden))+' '+self.hjust.upper()+' ')			#write the values to the output_stream
		if self.vjust == 'n':						#checking vjust is 'n' (representing hln in pspice schematic)
			output_stream.write('C')				#if yes, writing 'C' to the output_stream(EESchema Schematic)
		else:
			output_stream.write(self.vjust.upper())			#if not, writing vjust.upper to the output_stream
		output_stream.write('NN\n')					#writing 'NN\n' 
