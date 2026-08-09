EESchema Schematic File Version 2
LIBS:4_and-rescue
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
LIBS:4_and-cache
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
L 3_and-RESCUE-4_and X1
U 1 1 5C9A2915
P 3700 3500
F 0 "X1" H 4600 3800 60  0000 C CNN
F 1 "3_and" H 4650 4000 60  0000 C CNN
F 2 "" H 3700 3500 60  0000 C CNN
F 3 "" H 3700 3500 60  0000 C CNN
	1    3700 3500
	1    0    0    -1  
$EndComp
$Comp
L d_and U2
U 1 1 5C9A2940
P 5450 3400
F 0 "U2" H 5450 3400 60  0000 C CNN
F 1 "d_and" H 5500 3500 60  0000 C CNN
F 2 "" H 5450 3400 60  0000 C CNN
F 3 "" H 5450 3400 60  0000 C CNN
	1    5450 3400
	1    0    0    -1  
$EndComp
Wire Wire Line
	5000 3100 5000 3300
Wire Wire Line
	4150 3000 4150 2700
Wire Wire Line
	4150 2700 3200 2700
Wire Wire Line
	4150 3100 4000 3100
Wire Wire Line
	4000 3100 4000 3000
Wire Wire Line
	4000 3000 3200 3000
Wire Wire Line
	4150 3200 4150 3300
Wire Wire Line
	4150 3300 3250 3300
Wire Wire Line
	5000 3400 5000 3550
Wire Wire Line
	5000 3550 3250 3550
Wire Wire Line
	5900 3350 6500 3350
$Comp
L PORT U1
U 1 1 5C9A29B1
P 2950 2700
F 0 "U1" H 3000 2800 30  0000 C CNN
F 1 "PORT" H 2950 2700 30  0000 C CNN
F 2 "" H 2950 2700 60  0000 C CNN
F 3 "" H 2950 2700 60  0000 C CNN
	1    2950 2700
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 2 1 5C9A29E9
P 2950 3000
F 0 "U1" H 3000 3100 30  0000 C CNN
F 1 "PORT" H 2950 3000 30  0000 C CNN
F 2 "" H 2950 3000 60  0000 C CNN
F 3 "" H 2950 3000 60  0000 C CNN
	2    2950 3000
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 3 1 5C9A2A0D
P 3000 3300
F 0 "U1" H 3050 3400 30  0000 C CNN
F 1 "PORT" H 3000 3300 30  0000 C CNN
F 2 "" H 3000 3300 60  0000 C CNN
F 3 "" H 3000 3300 60  0000 C CNN
	3    3000 3300
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 4 1 5C9A2A3C
P 3000 3550
F 0 "U1" H 3050 3650 30  0000 C CNN
F 1 "PORT" H 3000 3550 30  0000 C CNN
F 2 "" H 3000 3550 60  0000 C CNN
F 3 "" H 3000 3550 60  0000 C CNN
	4    3000 3550
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 5 1 5C9A2A68
P 6750 3350
F 0 "U1" H 6800 3450 30  0000 C CNN
F 1 "PORT" H 6750 3350 30  0000 C CNN
F 2 "" H 6750 3350 60  0000 C CNN
F 3 "" H 6750 3350 60  0000 C CNN
	5    6750 3350
	-1   0    0    1   
$EndComp
Text Notes 3450 2650 0    60   ~ 12
in1
Text Notes 3450 2950 0    60   ~ 12
in2
Text Notes 3500 3300 0    60   ~ 12
in3
Text Notes 3500 3550 0    60   ~ 12
in4
Text Notes 6150 3350 0    60   ~ 12
out
$EndSCHEMATC
