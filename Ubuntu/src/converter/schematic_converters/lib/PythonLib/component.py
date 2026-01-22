#The MIT License (MIT)

#PSpice to Oscad Schematic Converter
#This code is written by Suryavamshi Tenneti, FOSSEE, IIT Bombay
#The code is modified by Sumanto Kar and Gloria Nandihal, FOSSEE, IIT Bombay


from header import *
from attribute import *
from design import *
from misc import *

class Pin:
	#position of pin and length of the pin.Pin constructor reading  values from corresponding component's pspice library  
	x = 0
	y = 0
	length = 0
	#pin_number is the pin number and elec_type is the electrical type
	n = ''
	elec_type = ''
	#to store the orientation of pin
	orientation = ''
	found = 0
	tmp = 0
	x1 = 0
	x2 = 0
	y1 = 0
	y2 = 0

	def __init__(self, input_stream = None):
		line = ''
		temp =''
		inline = input_stream.readline().split()
		#print(inline)
		t,self.tmp,self.x1,self.y1,temp,temp,self.n,temp,self.x2,self.y2,self.orientation = inline
		self.x = int(self.x2)*MULT			#x co-ordinate of the pin
		self.y = int(self.y2)*(-1)*MULT			#y co-ordinate of the pin
		self.length = 10*MULT				#calculating pin length from points of pins 
		#line = input_stream.readline()
		g = input_stream.tell()
		line = input_stream.readline()
		while(line[0] == 'a'):				#Read the attributes of the pins. lines starting from 'a' stores the attributes 
			attr = Attribute(line)			#called the attribute constructor to store the attributes
			if attr.name == 'ERC' or attr.name == 'erc':	#if the attribute name is 'ERC' or 'erc' its value is the electrical type of the pin
				self.elec_type = attr.value
			g = input_stream.tell()
			line = input_stream.readline()
		input_stream.seek(g)

	def print(self, output_stream, shiftx, shifty):	#converting the annotation to KiCad format as different letters are use in PSpice and KiCad libraries
		output_stream.write("X"+" "+"~ "+str(self.n)+" "+str(self.x-shiftx)+" "+str(self.y-((-1)*shifty))+" "+str(self.length)+" ")
		if self.orientation == 'h':
			output_stream.write('R')	# If Pspice orientation is h, then map it to Right direction
		elif self.orientation == 'u':
			output_stream.write('L')        #If Pspice orientation is u, then map it to Left direction
		elif self.orientation == 'v':
			output_stream.write('U')        #If Pspice orientation is v, then map it to Up direction
		elif self.orientation == 'd':
			output_stream.write('D')	#If Pspice orientation is d, then map it to Down direction

		output_stream.write(' 30 30 0 1 ')      # Mapping electrical tupe of PSpice component to KiCad component

		if self.elec_type == 'i':
			output_stream.write('I\n')	#If Pspice electrical type is i, then map it to Input
		elif self.elec_type == 'o':
			output_stream.write('O\n')	#If Pspice electrical type is o, then map it to Output
		elif self.elec_type == 'p':
			output_stream.write('W\n')      #If Pspice electrical type is p, then map it to Tristate
		elif self.elec_type == 'x':
			output_stream.write('P\n')	#If Pspice electrical type is x, then map it to Passive
		elif self.elec_type == 'b':
			output_stream.write('B\n')	#If Pspice electrical type is b, then map it to Bidirectional
		else:
			output_stream.write('P\n')	#else map it to Passive



class Component:					#Component class method makePins to design pins
							#default Component  class constructor
	type_ = ''
	ref = ''
	value = ''
	pins = []
	des = None
	def __init__(self, input_stream = None, t = ''):
		self.pins = []
		self.type_ = t
		if(input_stream != None):
			g = input_stream.tell()		#To get to the starting point of the component's type in pspice library file
			line = ''
			'''while(('*symbol '+t) not in line):
				input_stream.seek(g)
				line = input_stream.readline().strip()
				g = input_stream.tell()
			'''
			line = skipTo(input_stream, ('*symbol '+t))
			#print('Component Line->', line)
			'''	input_stream.seek(g)
			g = input_stream.tell()
			print('Search t',line[line.rfind(' ')+1:])
			'''
			while(line != '' and line.find('ako')!= -1):
				#print('in finding ako')
				a = line.rfind(' ')+1
				t = line[a:]
				input_stream.seek(g)				
				'''while(('*symbol '+t) not in line):			
					line = input_stream.readline().strip()
					print('Searching ako ref',line)'''
				line = skipTo(input_stream, ('*symbol '+t)) #To get the pspice library of the components having its description written elsewhere
			#print('In component constructor')
			line = input_stream.readline().strip()
			'''while('@attributes' not in line):			
				line = input_stream.readline().strip()'''
			skipTo(input_stream, '@attributes')			#creating attributes by calling its constructor 
			g  = input_stream.tell()
			line = input_stream.readline().strip()			#assigning attributes of PKGREF to the component
			while(line[0] == 'a'):
				attr = Attribute(line)
				if attr.name == 'REFDES' or attr.name == 'refdes':
					self.ref = attr.value[:-1]
				if attr.name == 'VALUE' or attr.name == 'DC' or attr.name == 'GAIN' or attr.name == 'COEFF' or attr.name == 'VPOS' or attr.name == 'VNEG':
					self.value = attr.value			#assigning attributes of above cases to the component
				g  = input_stream.tell()
				line = input_stream.readline().strip()
			input_stream.seek(g)
			'''
			line = input_stream.readline().strip()
			
			while('@pins' not in line):
				line = input_stream.readline().strip()
			'''
			skipTo(input_stream, '@pins')				#to get to the starting point of the pins of the type required 
			self.makePins(input_stream)				#calling makepins function to create pins

			g = input_stream.tell()
			line = input_stream.readline().strip()
			while('@graphics' not in line):
				input_stream.seek(g)
				#print('***',line)
				g = input_stream.tell()
				line = input_stream.readline().strip()
			input_stream.seek(g)
			d = Design(input_stream)				#calling Design constructor to create design
			self.des = d
			#print('Before fixComp',self.type_, 'ref=', self.ref)

	def makePins(self,input_stream):
		#print('making pins')
		line = ''
		g = input_stream.tell()
		line = input_stream.readline().strip()
		while(line[0] == 'p'): 				#Read the pins line from pspice library
			input_stream.seek(g)
			p = Pin(input_stream)			#call the Pin constructor to get the values and pass the library as the parameter
			self.pins.append(p)
			g = input_stream.tell()			#move to the next line to get next 'p' line
			line = input_stream.readline().strip()
		input_stream.seek(g)

	def print(self, output_stream):				#print function of class Pin to print the pins in output's cache lib file 
		output_stream.write('#\n# '+self.type_+'\n#\nDEF '+self.type_+' '+self.ref+' 0 30 Y Y 1 F N'+'\n')#upto DEF line printed
		output_stream.write('F0 \"'+self.ref+"\" 0 0 30 H V L CNN"+'\n')	#F0 line
		output_stream.write('F1 \"'+self.type_+'\" 0 60 30 H V L CNN'+'\n')	#F1 line
		output_stream.write('DRAW\n')						#calling print funcition of design to print design of components
		self.des.print(output_stream)
		for i in range(len(self.pins)):
			self.pins[i].print(output_stream, self.des.shiftx, self.des.shifty)	#calling print function of pins class to print pins
		output_stream.write('ENDDRAW\n'+'ENDDEF\n')
