EESchema Schematic File Version 2
LIBS:power
LIBS:texas
LIBS:intel
LIBS:audio
LIBS:interface
LIBS:digital-audio
LIBS:philips
LIBS:display
LIBS:cypress
LIBS:siliconi
LIBS:opto
LIBS:atmel
LIBS:contrib
LIBS:valves
LIBS:eSim_Analog
LIBS:eSim_Devices
LIBS:eSim_Digital
LIBS:eSim_Hybrid
LIBS:eSim_Miscellaneous
LIBS:eSim_Plot
LIBS:eSim_Power
LIBS:eSim_PSpice
LIBS:eSim_Sources
LIBS:eSim_Subckt
LIBS:eSim_User
LIBS:3_and-cache
EELAYER 25 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L d_and U2
U 1 1 5C9A24D8
P 4250 2700
F 0 "U2" H 4250 2700 60  0000 C CNN
F 1 "d_and" H 4300 2800 60  0000 C CNN
F 2 "" H 4250 2700 60  0000 C CNN
F 3 "" H 4250 2700 60  0000 C CNN
	1    4250 2700
	1    0    0    -1  
$EndComp
$Comp
L d_and U3
U 1 1 5C9A2538
P 5150 2900
F 0 "U3" H 5150 2900 60  0000 C CNN
F 1 "d_and" H 5200 3000 60  0000 C CNN
F 2 "" H 5150 2900 60  0000 C CNN
F 3 "" H 5150 2900 60  0000 C CNN
	1    5150 2900
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 1 1 5C9A259A
P 3050 2600
F 0 "U1" H 3100 2700 30  0000 C CNN
F 1 "PORT" H 3050 2600 30  0000 C CNN
F 2 "" H 3050 2600 60  0000 C CNN
F 3 "" H 3050 2600 60  0000 C CNN
	1    3050 2600
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 2 1 5C9A25D9
P 3050 2800
F 0 "U1" H 3100 2900 30  0000 C CNN
F 1 "PORT" H 3050 2800 30  0000 C CNN
F 2 "" H 3050 2800 60  0000 C CNN
F 3 "" H 3050 2800 60  0000 C CNN
	2    3050 2800
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 3 1 5C9A260A
P 3050 3100
F 0 "U1" H 3100 3200 30  0000 C CNN
F 1 "PORT" H 3050 3100 30  0000 C CNN
F 2 "" H 3050 3100 60  0000 C CNN
F 3 "" H 3050 3100 60  0000 C CNN
	3    3050 3100
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 4 1 5C9A2637
P 6900 2850
F 0 "U1" H 6950 2950 30  0000 C CNN
F 1 "PORT" H 6900 2850 30  0000 C CNN
F 2 "" H 6900 2850 60  0000 C CNN
F 3 "" H 6900 2850 60  0000 C CNN
	4    6900 2850
	-1   0    0    1   
$EndComp
Wire Wire Line
	4700 2650 4700 2800
Wire Wire Line
	5600 2850 6650 2850
Wire Wire Line
	3800 2600 3300 2600
Wire Wire Line
	3800 2700 3300 2700
Wire Wire Line
	3300 2700 3300 2800
Wire Wire Line
	3300 3100 4700 3100
Wire Wire Line
	4700 3100 4700 2900
Text Notes 3500 2600 0    60   ~ 12
in1
Text Notes 3450 2800 0    60   ~ 12
in2\n
Text Notes 3500 3100 0    60   ~ 12
in3
Text Notes 6100 2850 0    60   ~ 12
out
$EndSCHEMATC
