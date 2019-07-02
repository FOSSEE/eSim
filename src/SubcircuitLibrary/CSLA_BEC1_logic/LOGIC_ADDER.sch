EESchema Schematic File Version 2
LIBS:power
LIBS:device
LIBS:transistors
LIBS:conn
LIBS:linear
LIBS:regul
LIBS:74xx
LIBS:cmos4000
LIBS:adc-dac
LIBS:memory
LIBS:xilinx
LIBS:microcontrollers
LIBS:dsp
LIBS:microchip
LIBS:analog_switches
LIBS:motorola
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
LIBS:eSim_Sources
LIBS:eSim_Subckt
LIBS:eSim_User
LIBS:LOGIC_ADDER-cache
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
U 1 1 5AB647D1
P 4100 2200
F 0 "U2" H 4100 2200 60  0000 C CNN
F 1 "d_and" H 4150 2300 60  0000 C CNN
F 2 "" H 4100 2200 60  0000 C CNN
F 3 "" H 4100 2200 60  0000 C CNN
	1    4100 2200
	1    0    0    -1  
$EndComp
$Comp
L d_and U4
U 1 1 5AB648AD
P 5250 2300
F 0 "U4" H 5250 2300 60  0000 C CNN
F 1 "d_and" H 5300 2400 60  0000 C CNN
F 2 "" H 5250 2300 60  0000 C CNN
F 3 "" H 5250 2300 60  0000 C CNN
	1    5250 2300
	1    0    0    -1  
$EndComp
$Comp
L d_xor U3
U 1 1 5AB648E7
P 4100 2750
F 0 "U3" H 4100 2750 60  0000 C CNN
F 1 "d_xor" H 4150 2850 47  0000 C CNN
F 2 "" H 4100 2750 60  0000 C CNN
F 3 "" H 4100 2750 60  0000 C CNN
	1    4100 2750
	1    0    0    -1  
$EndComp
$Comp
L d_xor U5
U 1 1 5AB6498F
P 5250 2600
F 0 "U5" H 5250 2600 60  0000 C CNN
F 1 "d_xor" H 5300 2700 47  0000 C CNN
F 2 "" H 5250 2600 60  0000 C CNN
F 3 "" H 5250 2600 60  0000 C CNN
	1    5250 2600
	1    0    0    -1  
$EndComp
$Comp
L d_or U6
U 1 1 5AB64A11
P 6250 2250
F 0 "U6" H 6250 2250 60  0000 C CNN
F 1 "d_or" H 6250 2350 60  0000 C CNN
F 2 "" H 6250 2250 60  0000 C CNN
F 3 "" H 6250 2250 60  0000 C CNN
	1    6250 2250
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 1 1 5AB64A78
P 2650 2100
F 0 "U1" H 2700 2200 30  0000 C CNN
F 1 "PORT" H 2650 2100 30  0000 C CNN
F 2 "" H 2650 2100 60  0000 C CNN
F 3 "" H 2650 2100 60  0000 C CNN
	1    2650 2100
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 2 1 5AB64BE9
P 2650 2300
F 0 "U1" H 2700 2400 30  0000 C CNN
F 1 "PORT" H 2650 2300 30  0000 C CNN
F 2 "" H 2650 2300 60  0000 C CNN
F 3 "" H 2650 2300 60  0000 C CNN
	2    2650 2300
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 4 1 5AB64C18
P 6300 2550
F 0 "U1" H 6350 2650 30  0000 C CNN
F 1 "PORT" H 6300 2550 30  0000 C CNN
F 2 "" H 6300 2550 60  0000 C CNN
F 3 "" H 6300 2550 60  0000 C CNN
	4    6300 2550
	-1   0    0    1   
$EndComp
$Comp
L PORT U1
U 3 1 5AB64C59
P 2650 2900
F 0 "U1" H 2700 3000 30  0000 C CNN
F 1 "PORT" H 2650 2900 30  0000 C CNN
F 2 "" H 2650 2900 60  0000 C CNN
F 3 "" H 2650 2900 60  0000 C CNN
	3    2650 2900
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 5 1 5AB64C94
P 7150 2200
F 0 "U1" H 7200 2300 30  0000 C CNN
F 1 "PORT" H 7150 2200 30  0000 C CNN
F 2 "" H 7150 2200 60  0000 C CNN
F 3 "" H 7150 2200 60  0000 C CNN
	5    7150 2200
	-1   0    0    1   
$EndComp
Wire Wire Line
	2900 2100 3650 2100
Wire Wire Line
	2900 2250 3650 2250
Wire Wire Line
	3650 2250 3650 2200
Wire Wire Line
	3400 2100 3400 2650
Wire Wire Line
	3400 2650 3650 2650
Connection ~ 3400 2100
Wire Wire Line
	3150 2250 3150 2750
Wire Wire Line
	3150 2750 3650 2750
Connection ~ 3150 2250
Wire Wire Line
	4550 2700 4550 2500
Wire Wire Line
	4550 2500 4800 2500
Wire Wire Line
	2900 2900 4800 2900
Wire Wire Line
	4800 2900 4800 2600
Wire Wire Line
	4700 2500 4700 2200
Wire Wire Line
	4700 2200 4800 2200
Connection ~ 4700 2500
Wire Wire Line
	4800 2300 4600 2300
Wire Wire Line
	4600 2300 4600 2900
Connection ~ 4600 2900
Wire Wire Line
	5700 2250 5800 2250
Wire Wire Line
	4550 2150 4550 2000
Wire Wire Line
	4550 2000 5800 2000
Wire Wire Line
	5800 2000 5800 2150
Wire Wire Line
	5700 2550 6050 2550
Wire Wire Line
	6700 2200 6900 2200
Wire Wire Line
	2900 2250 2900 2300
Text GLabel 3000 1850 0    60   Input ~ 0
A
Text GLabel 3000 2500 0    60   Input ~ 0
B
Text GLabel 3000 3250 0    60   Input ~ 0
CIN
Wire Wire Line
	3000 3250 3050 3250
Wire Wire Line
	3050 3250 3050 2900
Connection ~ 3050 2900
Wire Wire Line
	3000 1850 3100 1850
Wire Wire Line
	3100 1850 3100 2100
Connection ~ 3100 2100
Wire Wire Line
	3000 2500 3000 2250
Connection ~ 3000 2250
Text GLabel 6750 1700 0    60   Output ~ 0
CARRY
Text GLabel 5950 2800 0    60   Output ~ 0
SUM
Wire Wire Line
	6750 1700 6800 1700
Wire Wire Line
	6800 1700 6800 2200
Connection ~ 6800 2200
Wire Wire Line
	5950 2550 5950 2800
Connection ~ 5950 2550
$EndSCHEMATC
