#The MIT License (MIT)

#PSpice to Oscad Schematic Converter
#This code is written by Suryavamshi Tenneti, FOSSEE, IIT Bombay
#The code is modified by Sumanto Kar and Gloria Nandihal, FOSSEE, IIT Bombay


from header import *						#Importing header file from PythonLib folder
from component_instance import *				#Importing component_instance file from PythonLib folder
from wire import *						#Importing header file from PythonLib folder
							
import sys							#Importing python sys module						
import os							#Importing python os module
					
from misc import *						#Importing misc file from PythonLib folder



files = sys.argv[1:]
input_file = files[0]						#input file(Pspice Schematic) location
new_location = files[1]						#new file(KiCAD file) location
new_directory = os.path.dirname(new_location)			#Creating new directory path(where KiCAD files are to be stored
base_name = os.path.basename(new_location)			#Addding base name to the new directory



if not os.path.exists(new_location):				#If the directory does not already exists, then making new directory
	os.makedirs(new_location)



#current_location = os.getcwd()
file = open(input_file, 'r+')					#opening a file in read and write mode
os.chdir(new_location)						#changing to the new directory location
fprojname = base_name + '.proj'					#Creating name for the new KiCAD project
fproname = base_name + '.pro'					#Creating name for the new KiCAD project
fschname = base_name + '.sch'					#Creating name for the new EESchema schematic





#Creating a String of the libraries and library names to be added in the EESchema and project file respectively
descr = 'EESchema Schematic File Version 2  date \nLIBS:power\nLIBS:device\nLIBS:transistors\nLIBS:conn\nLIBS:linear\nLIBS:regul\nLIBS:74xx\nLIBS:cmos4000\nLIBS:adc-dac\nLIBS:memory\nLIBS:xilinx\nLIBS:special\nLIBS:microcontrollers\nLIBS:dsp\nLIBS:microchip\nLIBS:analog_switches\nLIBS:motorola\nLIBS:texas\nLIBS:intel\nLIBS:audio\nLIBS:interface\nLIBS:digital-audio\nLIBS:philips\nLIBS:display\nLIBS:cypress\nLIBS:siliconi\nLIBS:opto\nLIBS:atmel\nLIBS:contrib\nLIBS:valves\nEELAYER 25  0\nEELAYER END\n$Descr A4 11700 8267\nencoding utf-8\nSheet 1 1\nTitle \"\"\nDate \"\"\nRev \"\"\nComp \"\"\nComment1 \"\"\nComment2 \"\"\nComment3 \"\"\nComment4 \"\"\n$EndDescr\n'





proDescr = 'update= \nlast_client=eeschema\n[eeschema]\nversion=1\nLibDir=\nNetFmt=1\nHPGLSpd=20\nHPGLDm=15\nHPGLNum=1\noffX_A4=0\noffY_A4=0\noffX_A3=0\noffY_A3=0\noffX_A2=0\noffY_A2=0\noffX_A1=0\noffY_A1=0\noffX_A0=0\noffY_A0=0\noffX_A=0\noffY_A=0\noffX_B=0\noffY_B=0\noffX_C=0\noffY_C=0\noffX_D=0\noffY_D=0\noffX_E=0\noffY_E=0\nRptD_X=0\nRptD_Y=100\nRptLab=1\nLabSize=60\n[eeschema/libraries]\nLibName1=power\nLibName2=device\nLibName3=transistors\nLibName4=conn\nLibName5=linear\nLibName6=regul\nLibName7=74xx\nLibName8=cmos4000\nLibName9=adc-dac\nLibName10=memory\nLibName11=xilinx\nLibName12=special\nLibName13=microcontrollers\nLibName14=dsp\nLibName15=microchip\nLibName16=analog_switches\nLibName17=motorola\nLibName18=texas\nLibName19=intel\nLibName20=audio\nLibName21=interface\nLibName22=digital-audio\nLibName23=philips\nLibName24=display\nLibName25=cypress\nLibName26=siliconi\nLibName27=opto\nLibName28=atmel\nLibName29=contrib\nLibName30=valves'




nameAppend = '_PSPICE'				                #name to be appended with the Pspice Components                
REMOVEDCOMPONENTS = ['TITLEBLK', 'PARAM', 'readme', 'VIEWPOINT', 'LIB', 'copyright', 'WATCH1', 'VECTOR', 'NODESET1']
								# Components to be removed  


											
#print('opening .proj file')
fproj  = open(fprojname,'w+')					#opening the project KiCAD file in write mode, if not present creating it
fproj.write('schematicFile '+ base_name + '.sch.sch' + '\n')	#writing to the project file
fproj.close()							#closing the project file
#print('closing .proj file')




#print('opening .pro file')					
fpro = open(fproname, 'w+')					#opening the project KiCAD file in write mode, if not present creating it
fpro.write(proDescr + '\n')					#writing the library names to the project file
fpro.close()							#closing the project file
#print('closing .pro file')




textline = file.readline().strip()				#reading from the Pspice Schematic file until '@status' is reached
while('@status' not in textline):
	textline = file.readline().strip()
	#print(textline)

textline = file.readline().strip()




#print('opening .sch file')
fsch = open(fschname, 'w+')					#opening the EESchema file in write mode, if not present creating it
fsch.write(descr)						#writing the libraries to the project file

while('@ports' not in textline):				#reading from the Pspice Schematic file until '@ports' is reached
	textline = file.readline().strip()
	#print(textline)





componentInstances = []						#creating array of componentInstances for EESchema
g = file.tell()							#getting position of file handle
textline = file.readline().strip()
while(textline[:4] == 'port' and textline != ''):		#reading each port data from the Pspice schematic file
	#print('decoding ports')
	#print(textline)
	file.seek(g)						#setting the position of file handle
	ci = ComponentInstance(file)				#sending the 'file'object to ComponentInstance Constructor 
								#and storing the result in ci
	if ci.type_ == 'AGND' or ci.type_ == 'GND_ANALOG' or ci.type_ == 'GND_EARTH' or ci.type_ == 'EGND' or ci.type_ == '+5V' or ci.type_ == '-5V' :								#checking whether the type of ci is ground or power lines
		#print(ci.type_)
		fixInst(ci)					
		componentInstances.append(ci)			#appending ci to the array of componentInstances for EESchema

		componentInstances[-1].attrs[0].value = '#PWR'+str(len(componentInstances))
								#appending pwr to the array of componentInstances for EESchema

	g = file.tell()						#getting position of file handle
	textline = file.readline().strip()			

'''file.seek(g)
g = file.tell()
print(file.readline().strip())
file.seek(g)
print('**', textline, ('@parts' in textline))
'''




while('@parts' not in textline and textline!=''):		#reading each part data from the Pspice schematic file
	#print('parts')
	textline = file.readline().strip()
	#print(textline)
g = file.tell()							#getting position of file handle




#textline = file.readline().strip()
textline = file.readline().strip()				
#print('part->', textline)
while(textline[:4] == 'part' and textline != ''):
	file.seek(g)						#setting the position of file handle
	#print('part',file.readline().strip())
	file.seek(g)
	ci = ComponentInstance(file)				#sending the 'file' object to ComponentInstance Constructor 
								#in ComponentInstance.py and storing the result in ci
	fixInst(ci)
	ci.type_ = ci.type_ + nameAppend			#appending _PSPIE stored in nameAppend to ci.type 
	componentInstances.append(ci)				#appending ci to the array of componentInstances for EESchema
	g = file.tell()						#getting position of file handle
	textline = file.readline().strip()





file.seek(g)							#setting the position of file handle
#print('len of componentInstances = ', len(componentInstances))
for i in range(0, len(componentInstances)):			#printing the componentInstances array to the EESchema Schematic file
	componentInstances[i].print(fsch)

while('@conn' not in textline and textline != ''):		#reading each part data from the Pspice schematic file
	textline = file.readline().strip()			




wires = []							#creating an array wires
file.readline().strip()
parseWire(file, wires)						#sending the 'file' object to parseWire  function in wire.py
								#and storing the result in wires

for i in range(0, len(wires)):					#printing the wires array to the EESchema Schematic file
	wires[i].print(fsch)




conns = []							
parseConn(file, conns)						#sending the 'file' object to parseConn  function in wire.py
								#and storing the result in conns

for i in range(0, len(conns)):					#printing the conns array to the EESchema Schematic file
	conns[i].print(fsch)




fsch.write('$EndSCHEMATC\n')					#writing '$EndSCHEMATIC' to EESchema Schematic
fsch.close()							#closing the EESchema Schematic
