# =========================================================================
#          FILE: sch_convert.py
#
#         USAGE: ---
#
#   DESCRIPTION: This is program to create a batch file
#		 Used to convert schematics in bulk
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

import sys,re,os,time
directory = os.getcwd()
lines= os.listdir(directory)
infl = open("convert.bat","w");
lnn=0
for line1 in lines:
	lnn = lnn + 1
	line1 = line1.rstrip('\n')	
	line1 = line1.rstrip('\r')
	if line1.find('.asc')!=-1:
		infl.write("python3 sch_LTspice2Kicad.py "+line1+"\n")

infl.close()

	
