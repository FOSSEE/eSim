# =========================================================================
#  Written by : Laurent CHARRIER
#  Original Repository: https://github.com/laurentc2/LTspice2Kicad
# =========================================================================

# =========================================================================
#          FILE: sch_LTspice2Kicad.py
#
#         USAGE: ---
#
#   DESCRIPTION: This is LTspice to Kicad .lib Converter file for eSim
# 				 It converts to KiCad 4.0.7 .lib format
#
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Sumanto Kar, jeetsumanto123@gmail.com
#      MODIFIED: Sumanto Kar, jeetsumanto123@gmail.com
#  ORGANIZATION: eSim Team at FOSSEE, IIT Bombay
#       CREATED: Thursday 28 May 2020
#      REVISION: Thursday 27 July 2023
# =========================================================================

import sys,re,os,codecs

# function to find locaion of each space character in each line
def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub) # use start += 1 to find overlapping matches

# Always go 1 level up from the given path
directory = os.path.abspath(os.path.join(sys.argv[1], ".."))
if directory=="." : directory = os.getcwd()
if not os.path.isdir(directory):
    print(f"ERROR: '{directory}' is not a valid directory.")
    sys.exit(1)

# out_file = sys.argv[2]

dir = os.listdir(directory)
comp = []
for component in dir:
	if (component[-4:]==".asy") : comp.append(component)

base_name = os.path.basename(os.path.normpath(directory))  # Get last folder name
out_file = os.path.join(directory, "LTspice_" + base_name + ".lib")
print("Output Lib File: ", out_file)
outfl = codecs.open(out_file,"w");
outfl.write("EESchema-LIBRARY Version 2.3\n#encoding utf-8\n#\n")

for component in comp :
	print(component)
	in_file = directory + "\\" + component

	#if (component == "ADA4807.asy" or component == "ADA4895.asy") :  # I don't know how to detect automatically the file encoding UTF-16-LE with Python

	#	infl = codecs.open(in_file,"r",'utf-16-le');

	#else : infl = open(in_file,"r");
	infl = codecs.open(in_file,"r");
	lines = infl.readlines()
	infl.close()

	drw_lin = list()
	# pins stuffs
	pin_pos = []
	pin_orient = []
	pin_justif=[]
	pin_name = []
	pin_order = []
	pin_off=[]
	
	Value = "Value"
	Value_XY = "0 0"
	Value_orient = "H"
	Value_justif = "L"
	Prefix = ""
	Prefix_XY = "0 0"
	Prefix_orient = "H"
	Prefix_justif = "L"
	Description = ""
	SpiceModel = ""

	# read the LTspice library line by line :
	for line1 in lines:
		line1 = line1.rstrip('\n')
		line1 = line1.rstrip('\r')
		# print(line1)
		spc = list(find_all(line1," "))  # find all space locations to split the variables of the line
		if re.match(r"^SYMATTR Prefix *", line1) is not None: 
			Prefix = line1[15:]
		if re.match(r"^WINDOW 0 *", line1) is not None: 
			Prefix_XY = str(int(3.125*int(line1[spc[1]:spc[2]]))) + " " + str(int(-3.125*int(line1[spc[2]:spc[3]])))
			Prefix_orient = "H"
			Prefix_justif = line1[spc[3]+1:spc[3]+2]
			if Prefix_justif=="V" :
				Prefix_orient = "V"
				Prefix_justif = line1[spc[3]+2:spc[3]+3]
		if re.match(r"^SYMATTR Value *", line1) is not None: 
			Value = line1[14:]
		if re.match(r"^SYMATTR Value2 *", line1) is not None: 
			Value = line1[15:]
		if re.match(r"^WINDOW 3 *", line1) is not None: 
			Value_XY = str(int(3.125*int(line1[spc[1]:spc[2]]))) + " " + str(int(-3.125*int(line1[spc[2]:spc[3]])))
			Value_orient = "H"
			Value_justif = line1[spc[3]+1:spc[3]+2]
			if Value_justif=="V" :
				Value_orient = "V"
				Value_justif = line1[spc[3]+2:spc[3]+3]
		if re.match(r"^SYMATTR Description *", line1) is not None: 
			Description = line1[19:]
		if re.match(r"^SYMATTR SpiceModel *", line1) is not None: 
			SpiceModel = line1[18:]
		
		if re.match(r"^LINE *", line1) is not None: 
			if len(spc)==5 :
				drw_lin.append("P 2 0 0 0 " + str(int(3.125*int(line1[spc[1]:spc[2]]))) + " " + str(int(-3.125*int(line1[spc[2]:spc[3]]))) + " " + str(int(3.125*int(line1[spc[3]:spc[4]]))) + " " + str(int(-3.125*int(line1[spc[4]:]))))
			else :
				drw_lin.append("P 2 0 0 0 " + str(int(3.125*int(line1[spc[1]:spc[2]]))) + " " + str(int(-3.125*int(line1[spc[2]:spc[3]]))) + " " + str(int(3.125*int(line1[spc[3]:spc[4]]))) + " " + str(int(-3.125*int(line1[spc[4]:spc[5]]))))
				
		if re.match(r"^RECTANGLE *", line1) is not None: 
			if len(spc)==5 :
				drw_lin.append("S " + str(int(3.125*int(line1[spc[1]:spc[2]]))) + " " + str(int(-3.125*int(line1[spc[2]:spc[3]]))) + " " + str(int(3.125*int(line1[spc[3]:spc[4]]))) + " " + str(int(-3.125*int(line1[spc[4]:]))) + " 0 0 0 f")
			else :
				drw_lin.append("S " + str(int(3.125*int(line1[spc[1]:spc[2]]))) + " " + str(int(-3.125*int(line1[spc[2]:spc[3]]))) + " " + str(int(3.125*int(line1[spc[3]:spc[4]]))) + " " + str(int(-3.125*int(line1[spc[4]:spc[5]]))) + " 0 0 0 f")
		
		if re.match(r"^CIRCLE *", line1) is not None: 
			if len(spc)==5 :
				drw_lin.append("C " + str(int(0.5*3.125*(int(line1[spc[1]:spc[2]]) + int(line1[spc[3]:spc[4]])))) + " " + str(int(0.5*-3.125*(int(line1[spc[2]:spc[3]]) + int(line1[spc[4]:])))) + " " + str(int(0.5*3.125*abs(int(line1[spc[1]:spc[2]]) - int(line1[spc[3]:spc[4]])))) + " 0 0 0 N")
			else :
				drw_lin.append("C " + str(int(0.5*3.125*(int(line1[spc[1]:spc[2]]) + int(line1[spc[3]:spc[4]])))) + " " + str(int(0.5*-3.125*(int(line1[spc[2]:spc[3]]) + int(line1[spc[4]:spc[5]])))) + " " + str(int(0.5*3.125*abs(int(line1[spc[1]:spc[2]]) - int(line1[spc[3]:spc[4]])))) + " 0 0 0 N")
		
		if re.match(r"^ARC *", line1) is not None: 
			if len(spc)==9 : 
				drw_lin.append("A " + str(int(0.5*3.125*(int(line1[spc[1]:spc[2]]) + int(line1[spc[3]:spc[4]])))) + " " + str(int(0.5*-3.125*(int(line1[spc[2]:spc[3]]) + int(line1[spc[4]:spc[5]])))) + " " + str(int(0.5*3.125*abs(int(line1[spc[1]:spc[2]]) - int(line1[spc[3]:spc[4]])))) + " 0 900 0 0 0 N " + str(int(3.125*int(line1[spc[5]:spc[6]]))) + " " + str(int(-3.125*int(line1[spc[6]:spc[7]]))) + " " + str(int(3.125*int(line1[spc[7]:spc[8]]))) + " " + str(int(-3.125*int(line1[spc[8]:]))))
			else : 
				drw_lin.append("A " + str(int(0.5*3.125*(int(line1[spc[1]:spc[2]]) + int(line1[spc[3]:spc[4]])))) + " " + str(int(0.5*-3.125*(int(line1[spc[2]:spc[3]]) + int(line1[spc[4]:spc[5]])))) + " " + str(int(0.5*3.125*abs(int(line1[spc[1]:spc[2]]) - int(line1[spc[3]:spc[4]])))) + " 0 900 0 0 0 N " + str(int(3.125*int(line1[spc[5]:spc[6]]))) + " " + str(int(-3.125*int(line1[spc[6]:spc[7]]))) + " " + str(int(3.125*int(line1[spc[7]:spc[8]]))) + " " + str(int(-3.125*int(line1[spc[8]:spc[9]]))))
				
		if re.match(r"^TEXT *", line1) is not None: 
			if (line1[spc[3]+1:spc[3]+2]=="V"):
				text_orient = "1 "
				text_justif = line1[spc[3]+2:spc[3]+3]
			else :
				text_orient = "0 "
				text_justif = line1[spc[3]+1:spc[3]+2]
			drw_lin.append("T " + text_orient + str(int(3.125*int(line1[spc[0]:spc[1]]))) + " " + str(int(-3.125*int(line1[spc[1]:spc[2]]))) + " 50 0 0 1 " + line1[spc[4]:])
			# drw_lin.append("T " + text_orient + str(int(3.125*int(line1[spc[0]:spc[1]]))) + " " + str(int(-3.125*int(line1[spc[1]:spc[2]]))) + " 0 0 1 " + line1[spc[4]:] + " N N " + text_justif)

		if ((re.match(r"^PIN *", line1) is not None) and not(re.match(r"^PINATTR *", line1) is not None)): 
			pin_pos.append(str(int(3.125*int(line1[spc[0]:spc[1]]))) + " " + str(int(-3.125*int(line1[spc[1]:spc[2]]))))
			pin_off.append(str(int(3.125*int(line1[spc[3]:]))))
			if (line1[spc[2]+1:spc[2]+2]=="V") :
				pin_orient.append("V")
				pin_justif.append(line1[spc[2]+2:spc[2]+3])
			else :
				pin_orient.append("H")
				pin_justif.append(line1[spc[2]+1:spc[2]+2])
		if re.match(r"^PINATTR SpiceOrder *", line1) is not None:
			pin_order.append(line1[spc[1]:])
		if re.match(r"^PINATTR PinName *", line1) is not None:
			pin_name.append(line1[spc[1]:])
	if Description != "":
		# output the data in Kicad format
		outfl.write("#   " + component[0:len(component)-4] + "\n")
		#if Description != "":
		outfl.write("# " + Description + "\n")
		#if SpiceModel != "":
		outfl.write("# SpiceModel : " + SpiceModel + "\n")
		outfl.write("#\n")
		if (Prefix=="B" or Prefix=="E" or Prefix=="F" or Prefix=="G" or Prefix=="H" or Prefix=="I" or Prefix=="V") : Pow="P"
		else : Pow="N" 
		if (Prefix=="X" or Prefix=="U"): ViewPin = "Y"
		else : ViewPin = "N"
		if (component.find("voltage")!=-1 or component.find("current")!=-1):
			outfl.write("DEF " + component[0:len(component)-4] + " " + Prefix + " 0 1 Y Y 1 F N\n")
		else : 
			outfl.write("DEF " + component[0:len(component)-4] + " " + Prefix + " 0 1 N " + ViewPin + " 1 F " + Pow + "\n")
		if ((Prefix_justif == "B") or (Prefix_justif == "T")):
			outfl.write("F0 \"" + Prefix + "\" " + Prefix_XY + " 50 " + Prefix_orient + " V C " + Prefix_justif + "NN\n")
		else :
			outfl.write("F0 \"" + Prefix + "\" " + Prefix_XY + " 50 " + Prefix_orient + " V " + Prefix_justif + " CNN\n")
	
		if ((Value_justif == "B") or (Value_justif == "T")):
			outfl.write("F1 \"" + component[0:len(component)-4] + "\" " + Value_XY + " 50 " + Value_orient + " V C " + Value_justif + "NN\n")
		else :
			outfl.write("F1 \"" + component[0:len(component)-4] + "\" " + Value_XY + " 50 " + Value_orient + " V " + Value_justif + " CNN\n")
	
		# the value is transferd to F5 instead of F1 because F1 text should be the component name 
		if Value != "Value" :
			if ((Value_justif == "B") or (Value_justif == "T")):
				outfl.write("F5 \"" + Value + "\" " + Value_XY + " 50 " + Value_orient + " I C " + Value_justif + "NN\n")
			else :
				outfl.write("F5 \"" + Value + "\" " + Value_XY + " 50 " + Value_orient + " I " + Value_justif + " CNN\n")
		
			if (Pow=="N") : outfl.write("$FPLIST\n " + Prefix + "_*\n$ENDFPLIST\n")
	
		#DRAWINGS and PINS
		outfl.write("DRAW\n")
		for i in range(0,len(drw_lin)) :
			outfl.write(drw_lin[i] + "\n")

		for i in range(0,len(pin_name)) :
			pinjustif = pin_justif[i]
			if pin_justif[i] == "L" : pinjustif = "R"
			if pin_justif[i] == "R" : pinjustif = "L"
			if pin_justif[i] == "T" : pinjustif = "D"
			if pin_justif[i] == "B" : pinjustif = "U"
			outfl.write("X " + pin_name[i].replace(" ","") + " " + pin_order[i] + " " + pin_pos[i] + " 0 " + pinjustif + " 50 50 1 1 U\n")
		
		outfl.write("ENDDRAW\nENDDEF\n#\n")

outfl.close()
