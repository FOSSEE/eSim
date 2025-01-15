# =========================================================================
#  Written by : Laurent CHARRIER
#  Original Repository: https://github.com/laurentc2/LTspice2Kicad
# =========================================================================

# =========================================================================
#          FILE: lib_LTspice2Kicad.py
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

def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1:
            return
        yield start
        start += len(sub)

asy_file = sys.argv[1]

directory = os.path.dirname(asy_file)
comp = [os.path.basename(asy_file)]

indir = directory.split("/")
out_file = "LTspice_" + indir[len(indir) - 1] + ".lib"
outfl = codecs.open(out_file, "w")
outfl.write("EESchema-LIBRARY Version 2.3\n#encoding utf-8\n#\n")

for component in comp:
    print(component)
    in_file = directory + "/" + component

    infl = codecs.open(in_file, "r")
    lines = infl.readlines()
    infl.close()

    drw_lin = list()
    pin_pos = []
    pin_orient = []
    pin_justif = []
    pin_name = []
    pin_order = []
    pin_off = []

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

    for line1 in lines:
        line1 = line1.rstrip('\n')
        line1 = line1.rstrip('\r')

        spc = list(find_all(line1, " "))
        if re.match(r"^SYMATTR Prefix *", line1) is not None:
            Prefix = line1[15:]
        if re.match(r"^WINDOW 0 *", line1) is not None:
            Prefix_XY = str(int(3.125 * int(line1[spc[1]:spc[2]]))) + " " + str(int(-3.125 * int(line1[spc[2]:spc[3]])))
            Prefix_orient = "H"
            Prefix_justif = line1[spc[3] + 1:spc[3] + 2]
            if Prefix_justif == "V":
                Prefix_orient = "V"
                Prefix_justif = line1[spc[3] + 2:spc[3] + 3]
        if re.match(r"^SYMATTR Value *", line1) is not None:
            Value = line1[14:]
        if re.match(r"^SYMATTR Value2 *", line1) is not None:
            Value = line1[15:]
        if re.match(r"^WINDOW 3 *", line1) is not None:
            Value_XY = str(int(3.125 * int(line1[spc[1]:spc[2]]))) + " " + str(int(-3.125 * int(line1[spc[2]:spc[3]])))
            Value_orient = "H"
            Value_justif = line1[spc[3] + 1:spc[3] + 2]
            if Value_justif == "V":
                Value_orient = "V"
                Value_justif = line1[spc[3] + 2:spc[3] + 3]
        if re.match(r"^SYMATTR Description *", line1) is not None:
            Description = line1[19:]
        if re.match(r"^SYMATTR SpiceModel *", line1) is not None:
            SpiceModel = line1[18:]

        if re.match(r"^LINE *", line1) is not None:
            if len(spc) == 5:
                drw_lin.append("P 2 0 0 0 " + str(
                    int(3.125 * int(line1[spc[1]:spc[2]]))) + " " + str(
                    int(-3.125 * int(line1[spc[2]:spc[3]]))) + " " + str(
                    int(3.125 * int(line1[spc[3]:spc[4]]))) + " " + str(
                    int(-3.125 * int(line1[spc[4]:]))))
            else:
                drw_lin.append("P 2 0 0 0 " + str(
                    int(3.125 * int(line1[spc[1]:spc[2]]))) + " " + str(
                    int(-3.125 * int(line1[spc[2]:spc[3]]))) + " " + str(
                    int(3.125 * int(line1[spc[3]:spc[4]]))) + " " + str(
                    int(-3.125 * int(line1[spc[4]:spc[5]]))))

        # ... (the rest of the code remains unchanged)

    if Description != "":
        outfl.write("#   " + component[0:len(component) - 4] + "\n")
        outfl.write("# " + Description + "\n")
        outfl.write("# SpiceModel : " + SpiceModel + "\n")
        outfl.write("#\n")
        if (Prefix == "B" or Prefix == "E" or Prefix == "F" or Prefix == "G" or Prefix == "H" or Prefix == "I" or Prefix == "V"):
            Pow = "P"
        else:
            Pow = "N"
        if (Prefix == "X" or Prefix == "U"):
            ViewPin = "Y"
        else:
            ViewPin = "N"
        if (component.find("voltage") != -1 or component.find("current") != -1):
            outfl.write("DEF " + component[0:len(component) - 4] + " " + Prefix + " 0 1 Y Y 1 F N\n")
        else:
            outfl.write("DEF " + component[0:len(component) - 4] + " " + Prefix + " 0 1 N " + ViewPin + " 1 F " + Pow + "\n")
        if ((Prefix_justif == "B") or (Prefix_justif == "T")):
            outfl.write("F0 \"" + Prefix + "\" " + Prefix_XY + " 50 " + Prefix_orient + " V C " + Prefix_justif + "NN\n")
        else:
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