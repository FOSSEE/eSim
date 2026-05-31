#The MIT License (MIT)

#PSpice to Oscad Schematic Converter
#This code is written by Suryavamshi Tenneti, FOSSEE, IIT Bombay
#The code is modified by Sumanto Kar and Gloria Nandihal, FOSSEE, IIT Bombay




from attribute import *
from random import randint
from header import *
import sys
import copy

class ComponentInstance:
	x = 0
	y = 0
	type_ = ''
	orient = ''
	attrs = []

	def __init__(self, input_stream):
		self.attrs = [Attribute() for _ in range(2)]
		tmp = ''
		compnum = 0
		x0 = 0
		y0 = 0
		line = input_stream.readline().strip().split()
		#print(line)
		tmp,compnum,self.type_,x0,y0,self.orient = line
		x0 = int(x0)
		y0 = int(y0)
		self.x = x0 * MULT
		self.y = y0 * MULT
		#input_stream.readline()
		g = input_stream.tell()
		#print('type ->',self.type_)
		line = input_stream.readline().strip()
#if the above cases like VALUE, DC, GAIN doesn 't exist then giving attributes of PKGREF to it#
		#print('component instance',line)
		input_stream.seek(g)
		while(line[0] == 'a'):
			#print('compinst',line)
			attr = Attribute(line)
			#print('compinst->attr.name',attr.name)
			if attr.name == 'PKGREF':
				#print('yes attr[0]')
				self.attrs[0] = attr
			if attr.name == 'VALUE' or attr.name == 'DC' or attr.name == 'GAIN':
				#print('yes attr[1]')
				self.attrs[1] = attr
			g = input_stream.tell()
			line = input_stream.readline().strip()
		input_stream.seek(g)
		#print('attrs[0].value-> '+self.attrs[0].value,'attrs[1].name-> '+self.attrs[1].value)
		if self.attrs[0].name == '':
			#print('null attr[0]')
			self.attrs[0].name = 'PKGREF'
			self.attrs[0].value = self.type_
			self.attrs[0].orient = 'h'
			self.attrs[0].x = self.x
			self.attrs[0].y = self.y
			self.attrs[0].isHidden = True
			self.attrs[0].hjust = 'l'
			self.attrs[0].vjust = 'n'

		if self.attrs[1].name == '':
			#print('null attr[1]')
			self.attrs[1] = copy.copy(self.attrs[0])
			
			self.attrs[1].value = self.type_
			#print(self.attrs[1].value)
			self.attrs[1].y+=80

		self.attrs[0].x+= self.x
		self.attrs[1].x+= self.x
		self.attrs[0].y+= self.y
		self.attrs[1].y+= self.y
		#print('component initiated', self.attrs[0].value)

	#print all the components in output schematic file as per KiCad format
	def print(self, output_stream):
		output_stream.write('$Comp\n'+'L '+self.type_+' '+self.attrs[0].value+'\n')
		output_stream.write('U 1 1 '+str(randint(0, sys.maxsize+1)%90000000+10000000)+'\n')
		output_stream.write('P '+str(self.x)+' '+str(self.y)+'\n') #printing the postion of component
		output_stream.write('F 0')# upto F0 printed
		self.attrs[0].print(output_stream)# print the attributes by calling attributes print
		output_stream.write('F 1')# upto F1 printed
		self.attrs[1].print(output_stream)# print the attributes by calling attributes print
		output_stream.write('\t1    '+str(self.x)+' '+str(self.y)+'\n')# printing the postions of the component again
		if self.orient == 'v':
			output_stream.write('\t0    -1    -1    0\n')# rotation matrix corresponding to KiCad
		if self.orient == 'V':
			output_stream.write('\t0    1    -1    0\n')# rotation matrix corresponding to KiCad
		if self.orient == 'h':
			output_stream.write('\t1    0    0    -1\n')
		if self.orient == 'H':
			output_stream.write('\t-1    0    0    -1\n')
		if self.orient == 'u':
			output_stream.write('\t-1    0    0    1\n')
		if self.orient == 'U':
			output_stream.write('\t1    0    0    1\n')
		if self.orient == 'd':
			output_stream.write('\t0    1    1    0\n')
		if self.orient == 'D':
			output_stream.write('\t0    -1    1    0\n')

		output_stream.write('$EndComp\n')#The MIT License (MIT)

#PSpice to Oscad Schematic Converter
#Copyright (c) 2014, Siddhant Ranade,Ashlesha Atrey and Suryavamshi Tenneti, FOSSEE, IIT Bombay
#The code is modified by Sumanto Kar and Gloria Nandihal



from attribute import *
from random import randint
from header import *
import sys
import copy

class ComponentInstance:
	x = 0
	y = 0
	type_ = ''
	orient = ''
	attrs = []

	def __init__(self, input_stream):
		self.attrs = [Attribute() for _ in range(2)]
		tmp = ''
		compnum = 0
		x0 = 0
		y0 = 0
		line = input_stream.readline().strip().split()
		#print(line)
		tmp,compnum,self.type_,x0,y0,self.orient = line
		x0 = int(x0)
		y0 = int(y0)
		self.x = x0 * MULT
		self.y = y0 * MULT
		#input_stream.readline()
		g = input_stream.tell()
		#print('type ->',self.type_)
		line = input_stream.readline().strip()
#if the above cases like VALUE, DC, GAIN doesn 't exist then giving attributes of PKGREF to it#
		#print('component instance',line)
		input_stream.seek(g)
		while(line[0] == 'a'):
			#print('compinst',line)
			attr = Attribute(line)
			#print('compinst->attr.name',attr.name)
			if attr.name == 'PKGREF':
				#print('yes attr[0]')
				self.attrs[0] = attr
			if attr.name == 'VALUE' or attr.name == 'DC' or attr.name == 'GAIN':
				#print('yes attr[1]')
				self.attrs[1] = attr
			g = input_stream.tell()
			line = input_stream.readline().strip()
		input_stream.seek(g)
		#print('attrs[0].value-> '+self.attrs[0].value,'attrs[1].name-> '+self.attrs[1].value)
		if self.attrs[0].name == '':
			#print('null attr[0]')
			self.attrs[0].name = 'PKGREF'
			self.attrs[0].value = self.type_
			self.attrs[0].orient = 'h'
			self.attrs[0].x = self.x
			self.attrs[0].y = self.y
			self.attrs[0].isHidden = True
			self.attrs[0].hjust = 'l'
			self.attrs[0].vjust = 'n'

		if self.attrs[1].name == '':
			#print('null attr[1]')
			self.attrs[1] = copy.copy(self.attrs[0])
			
			self.attrs[1].value = self.type_
			#print(self.attrs[1].value)
			self.attrs[1].y+=80

		self.attrs[0].x+= self.x
		self.attrs[1].x+= self.x
		self.attrs[0].y+= self.y
		self.attrs[1].y+= self.y
		#print('component initiated', self.attrs[0].value)

	#print all the components in output schematic file as per KiCad format
	def print(self, output_stream):
		output_stream.write('$Comp\n'+'L '+self.type_+' '+self.attrs[0].value+'\n')
		output_stream.write('U 1 1 '+str(randint(0, sys.maxsize+1)%90000000+10000000)+'\n')
		output_stream.write('P '+str(self.x)+' '+str(self.y)+'\n') #printing the postion of component
		output_stream.write('F 0')# upto F0 printed
		self.attrs[0].print(output_stream)# print the attributes by calling attributes print
		output_stream.write('F 1')# upto F1 printed
		self.attrs[1].print(output_stream)# print the attributes by calling attributes print
		output_stream.write('\t1    '+str(self.x)+' '+str(self.y)+'\n')# printing the postions of the component again
		if self.orient == 'v':
			output_stream.write('\t0    -1    -1    0\n')# rotation matrix corresponding to KiCad
		if self.orient == 'V':
			output_stream.write('\t0    1    -1    0\n')# rotation matrix corresponding to KiCad
		if self.orient == 'h':
			output_stream.write('\t1    0    0    -1\n')
		if self.orient == 'H':
			output_stream.write('\t-1    0    0    -1\n')
		if self.orient == 'u':
			output_stream.write('\t-1    0    0    1\n')
		if self.orient == 'U':
			output_stream.write('\t1    0    0    1\n')
		if self.orient == 'd':
			output_stream.write('\t0    1    1    0\n')
		if self.orient == 'D':
			output_stream.write('\t0    -1    1    0\n')

		output_stream.write('$EndComp\n')
