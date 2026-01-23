#The MIT License (MIT)

#PSpice to Oscad Schematic Converter
#This code is written by Suryavamshi Tenneti, FOSSEE, IIT Bombay
#The code is modified by Sumanto Kar and Gloria Nandihal, FOSSEE, IIT Bombay


from header import *
import math


# In the constructors of Line, Arc, Circle and Rectangle, the input parameters shiftx and shifty have already been scaled.
class Line: #Constructor of Line.
	npoints = 0
	x = []
	y = []
	def __init__(self, input_stream, shiftx, shifty): #This gets called when the first character of a line is "v".This function assumes "v" and the next character(usually 0) have already been read and are NOT in the stream.
		t = 0
		temp = input_stream.readline().strip()
		self.npoints = 0
		self.x = []
		self.y = []
		while(temp!=';'):
			#t = temp
			#print('Line->',temp)
			t = temp.split()
			self.x.append(int(t[0]))
			#t = input_stream.read(1)
			self.y.append(int(t[1]))
			#tmp = input_stream.readline().strip() .The first line, i.e.the one that contains the 'v'
			temp = input_stream.readline().strip()

			self.x[self.npoints]*= MULT
			self.y[self.npoints]*= -1*MULT

			self.x[self.npoints]-=shiftx
			self.y[self.npoints]-= -1*shifty

			self.npoints+=1

		if temp != ';':
			print('Error! \";\" not found\n')# The last character in the description of a line is ";"


	def print(self, output_stream):
		output_stream.write('P '+str(self.npoints)+' 0 1 0  ')
		for i in range(self.npoints):
			output_stream.write(str(self.x[i])+' '+str(self.y[i])+' ')
		output_stream.write('N\n')

class Rectangle:  ## Constructor of Rectangle.
	x1 = 0
	y1 = 0
	x2 = 0
	y2 = 0
	def __init__(self, input_stream, shiftx, shifty):
		input_line = input_stream.readline().strip()
		#print('Rect->',input_line)
		self.x1, self.y1,self.x2,self.y2 = input_line.split()[:4]  # The line that contains the 'r'

		self.x1 = (int(self.x1) * MULT) - shiftx
		self.x2 = (int(self.x2) * MULT) - shiftx
		self.y1 = (int(self.y1) * -1 * MULT) - (-1*shifty)
		self.y2 = (int(self.y2) * -1 * MULT) - (-1*shifty)

	def print(self, output_stream):
		output_stream.write('S '+str(self.x1)+' '+str(self.y1)+' '+str(self.x2)+' '+str(self.y2)+' 0 1 0 N\n')


class Circle:  # Constructor of Circle.
	x = 0
	y = 0
	r = 0
	def __init__(self, input_stream, shiftx, shifty):
		self.x, self.y, self.r = map(int,input_stream.readline().strip().split())
		#tmp = input_stream.readline().strip()
		#print('Circle->','x=',self.x,'y=',self.y,'r=',self.r)
		self.x*= MULT
		self.x-= shiftx
		self.y*=-1*MULT
		self.y-=-1*shifty
		self.r*= MULT

	def print(self, output_stream):
		output_stream.write('C '+str(self.x)+' '+str(self.y)+' '+str(self.r)+' 0 1 0 N\n')

  
class Arc:   # Constructor of Arc.
	x = 0
	y = 0
	r = 0
	sa = 0
	ea = 0
	x1 = 0
	y1 = 0
	x2 = 0
	y2 = 0   ## See Line::Line(istream & in , int shiftx, int shifty) above.#From pspice library, get the 3 points that describe the arc.

	def __init__(self, input_stream, shiftx, shifty):  # Midpoints of the arcs:
		xA = 0.0
		yA = 0.0
		xB = 0.0
		yB = 0.0
		xC = 0.0
		yC = 0.0
		xmAB = 0
		xmBC = 0
		ymAB = 0
		ymBC = 0
		input_line = input_stream.readline().strip()
		#print('Arc->',input_line)
		xA,yA,xB,yB,xC,yC = map(float, input_line.split())
		#tmp = input_stream.readline().strip()
		yA*= -1
		yB*= -1
		yC*= -1

		xmAB = (xA+xB)/2   # The perpendicular bisectors of any two chords of a circle meet at the centre
		ymAB = (yA+yB)/2
		xmBC = (xC+xB)/2
		ymBC = (yC+yB)/2

		mperpAB = -(xB - xA)/(yB - yA)# Get x and y by solving the two lines(perpendicular bisectors)
		mperpBC = -(xB - xC)/(yB - yC)
		
		try:
			self.x = math.trunc((ymBC - ymAB - mperpBC * xmBC + mperpAB * xmAB)/(-mperpBC + mperpAB))  
		except ZeroDivisionError:
			self.x = float('inf')
		try:	
			self.y = math.trunc((xmBC - xmAB + (ymAB/mperpAB) - (ymBC/mperpBC))/((1.0/mperpAB)-(1.0/mperpBC)))
		except ZeroDivisionError:
			if mperpBC == 0.0:
				self.y = -float('inf')
			else:
				self.y = float('inf')
		

		if not math.isinf(self.y) and not math.isinf(self.x) and not math.isnan(self.x) and not math.isnan(self.y):  # Get the radius:
			self.r = math.trunc(((self.x-xA) * (self.x-xA) + (self.y-yA) * (self.y-yA))**0.5)
		else:
			self.r = 0

		a = math.atan2(yA-self.y, xA-self.x)/math.pi*10.0*180.0 # Following code is used to decide which among A and C is the starting point(and thus determines "sa")
		b = math.atan2(yB-self.y, xB-self.x)/math.pi*10.0*180.0
		c = math.atan2(yC-self.y, xC-self.x)/math.pi*10.0*180.0
		
		if b < max(a,c) and b > min(a,c):  #b is between a and c# print('*1')
			#print('*1')
			self.sa = math.trunc(min(a,c))
			self.ea = math.trunc(max(a,c))

		if b > max(a,c):   #b is largest# print('*2')
			#print('*2')
			self.sa = math.trunc(max(a,c))
			self.ea = math.trunc(min(a,c) + 3600.0)

		if b < min(a,c):    #b is smallest# print('*3')
			#print('*3')
			self.sa = math.trunc(max(a,c) - 3600.0)
			self.ea = math.trunc(min(a,c))

		flag_x_inf = False
		flag_y_inf = False

		if math.isinf(self.x) or math.isnan(self.x):
			#self.x = shiftx
			flag_x_inf = True

		if math.isinf(self.y) or math.isnan(self.y):
			#self.y = shifty
			flag_y_inf = True

		
		xA = self.x + self.r*math.cos(self.sa*math.pi/1800.0)
		yA = self.y + self.r*math.sin(self.sa*math.pi/1800.0)
		xC = self.x + self.r*math.cos(self.ea*math.pi/1800.0)
		yC = self.y + self.r*math.sin(self.ea*math.pi/1800.0)
		
		self.sa+=1
		self.ea-=1

		self.r*=MULT

		self.x1 = (xA*MULT)-shiftx
		self.y1 = ((yA*MULT)-(-1)*shifty)
		self.x2 = ((xC*MULT)-shiftx)
		self.y2 = ((yC*MULT)-(-1)*shifty)

		if not flag_x_inf:
			self.x*=MULT
			self.x-=shiftx
		
		else:
			self.x = shiftx

		if not flag_y_inf: 
			self.y*=MULT
			self.y-=(-1)*shifty
		
		else:
			self.y = shifty
		 # scale and shift: #startx, starty, endx, endy are redundant.May not even be in use.Haven 't been fixed.
		
		if math.isinf(self.x1) or math.isnan(self.x1) or math.isinf(self.y1) or math.isnan(self.y1) or math.isinf(self.x2) or math.isnan(self.x2) or math.isinf(self.y2) or math.isnan(self.y2):
			self.x1 = -(2**31)
			self.x2 = -(2**31)
			self.y1 = -(2**31)
			self.y2 = -(2**31)
		
		else:
			self.x1 = math.trunc(self.x1)
			self.y1 = math.trunc(self.y1)
			self.x2 = math.trunc(self.x2)
			self.y2 = math.trunc(self.y2)

		'''
		if mperpAB == 0 or mperpBC == 0:
			print('mperpAB=',mperpAB, 'mperpBC=', mperpBC)
			print('X=',self.x,'Y=',self.y)
			print('Radius=',self.r)
			print('a=',a,'b=',b,'c=',c)
			print('xA=',xA,'yA=',yA,'xC=',xC,'yC=',yC)
			print('x=',self.x,'y=',self.y)
			print('x1=',self.x1,'x2=',self.x2,'y1=',self.y1,'y2=',self.y2)
			print('sa=',self.sa,'ea=',self.ea)
		'''	
	def print(self,output_stream):
		output_stream.write('A '+str(math.trunc(self.x))+' '+str(math.trunc(self.y))+' '+str(int(self.r))+' '+str(int(self.sa))+' '+str(int(self.ea))+' '+' 0 1 0 N '+str(int(self.x1))+' '+str(int(self.y1))+' '+str(int(self.x2))+' '+str(int(self.y2))+' '+'\n')


class Text:  #Constructor of Circle.
	x = 0
	y = 0
	text = ''
	orient = ''

	def __init__(self,input_stream, shiftx, shifty):
		input_line = input_stream.readline().strip().split()
		self.x,self.y,self.orient = input_line[:3]
		self.x = int(self.x)
		self.y = int(self.y)
		#tmp = input_stream.readline().strip()

		self.text = input_stream.readline().strip() 
		self.x*=MULT
		self.y*=-1*MULT
		self.x-=shiftx
		self.y-=-1*shifty

	def print(self,output_stream):
		output_stream.write('T ') # The line that contains the 't'
		if self.orient[0] == 'h':
			output_stream.write('0 ')
		elif self.orient[0] == 'v':
			output_stream.write('900 ')
		output_stream.write(str(self.x)+' '+str(self.y)+' '+str(30)+' 0 0 0 '+self.text+'\n')


class Design:  #Constructor of Design.
	shiftx = 0
	shifty = 0
	lines = []
	rects = []
	circles = []
	arcs = []
	texts = []  # Reads the whole design, makes Line, Circle, etc.objects and stores them in the appropriate container(appropriate vector)
	def __init__(self, input_stream):
		g = 0
		tmp = ''
		t = 0
		tint = ''
		tmp = input_stream.readline().strip()
		#print('Design->', tmp)
		if('@graphics' not in tmp):
			print('Design not found!')
			return
		#print('Graphics->',tmp.split())
		self.lines = []
		self.rects = []
		self.circles = []
		self.arcs = []
		self.texts = []
		tmp = tmp.split()
		tint,tint,tint,self.shiftx,self.shifty= map(str,tmp[:5])
		if len(tmp) > 5:
			tmp = ''.join(tmp[5:])
		self.shiftx = int(self.shiftx)*MULT  # print('shiftx->', self.shiftx, 'shifty->', self.shifty)
		self.shifty = int(self.shifty)*MULT
		#print('shiftx->',self.shiftx,'shifty->',self.shifty)
		while(t!= '*'):  #As long as we haven 't reached the description of the next Component continue reading the lib file.
			g  = input_stream.tell()  # Get the position of the read head, so that we can go back to this position
			t = input_stream.read(1) # Get the first character of the description, store in "t".This character gives what shape it is.
			if not t:
				break

			if t == 'v':
				#print('Line')
				input_stream.read(1)
				input_stream.read(1)
				input_stream.read(1)
				l = Line(input_stream, self.shiftx, self.shifty)
				self.lines.append(l)

			elif t == 'r':
				#print('Rect')
				input_stream.read(1)
				input_stream.read(1)
				input_stream.read(1)
				r = Rectangle(input_stream, self.shiftx, self.shifty)
				self.rects.append(r)

			elif t == 'c':
				#print('Circle')
				input_stream.read(1)
				input_stream.read(1)
				input_stream.read(1)
				c = Circle(input_stream, self.shiftx, self.shifty)
				self.circles.append(c)

			elif t == 'a':
				#print('Arc')
				input_stream.read(1)
				input_stream.read(1)
				input_stream.read(1)
				a = Arc(input_stream, self.shiftx, self.shifty)
				self.arcs.append(a)

			elif t == 'z':
				#print('Text')
				input_stream.read(1)
				input_stream.read(1)
				input_stream.read(1)
				z = Text(input_stream, self.shiftx, self.shifty)
				self.texts.append(z)

			else:   #If t is neither 'v', 'r', 'c'
				tmp = input_stream.readline().strip()
				g = input_stream.tell()

		input_stream.seek(g)


	def print(self, output_stream):
		for i in range(len(self.lines)):
			self.lines[i].print(output_stream)
		for i in range(len(self.rects)):
			self.rects[i].print(output_stream)
		for i in range(len(self.circles)):
			self.circles[i].print(output_stream)
		for i in range(len(self.arcs)):
			self.arcs[i].print(output_stream)
		for i in range(len(self.texts)):
			self.texts[i].print(output_stream)
