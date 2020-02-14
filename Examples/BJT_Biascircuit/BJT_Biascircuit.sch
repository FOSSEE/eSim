EESchema Schematic File Version 2
LIBS:BJT_Biascircuit-rescue
LIBS:eSim_Analog
LIBS:eSim_Devices
LIBS:eSim_Digital
LIBS:eSim_Hybrid
LIBS:eSim_Miscellaneous
LIBS:eSim_Power
LIBS:eSim_Sources
LIBS:eSim_Subckt
LIBS:eSim_User
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
LIBS:power
LIBS:device
LIBS:transistors
LIBS:conn
LIBS:linear
LIBS:regul
LIBS:74xx
LIBS:cmos4000
LIBS:eSim_Plot
LIBS:BJT_Biascircuit-cache
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
L DC-RESCUE-BJT_Biascircuit v1
U 1 1 56A86D0E
P 6600 3050
F 0 "v1" H 6400 3150 60  0000 C CNN
F 1 "DC" H 6400 3000 60  0000 C CNN
F 2 "R1" H 6300 3050 60  0000 C CNN
F 3 "" H 6600 3050 60  0000 C CNN
	1    6600 3050
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR01
U 1 1 56A86D80
P 5450 4300
F 0 "#PWR01" H 5450 4050 50  0001 C CNN
F 1 "GND" H 5450 4150 50  0000 C CNN
F 2 "" H 5450 4300 50  0000 C CNN
F 3 "" H 5450 4300 50  0000 C CNN
	1    5450 4300
	1    0    0    -1  
$EndComp
Text GLabel 4150 3100 0    60   Input ~ 0
ib
Text GLabel 6550 2350 2    60   Input ~ 0
vce
$Comp
L R-RESCUE-BJT_Biascircuit R1
U 1 1 56C44AD7
P 5400 2650
F 0 "R1" H 5450 2780 50  0000 C CNN
F 1 "1k" H 5450 2700 50  0000 C CNN
F 2 "" H 5450 2630 30  0000 C CNN
F 3 "" V 5450 2700 30  0000 C CNN
	1    5400 2650
	0    1    1    0   
$EndComp
$Comp
L R-RESCUE-BJT_Biascircuit R2
U 1 1 56C44C4B
P 4800 3150
F 0 "R2" H 4850 3280 50  0000 C CNN
F 1 "1k" H 4850 3200 50  0000 C CNN
F 2 "" H 4850 3130 30  0000 C CNN
F 3 "" V 4850 3200 30  0000 C CNN
	1    4800 3150
	-1   0    0    1   
$EndComp
Wire Wire Line
	4150 3200 4150 3350
Wire Wire Line
	5450 3400 5450 4300
Wire Wire Line
	4150 4250 6600 4250
Connection ~ 5450 4250
Wire Wire Line
	6600 2450 6600 2600
Wire Wire Line
	6600 4250 6600 3500
Wire Wire Line
	6550 2350 6500 2350
Wire Wire Line
	6500 2350 6500 2450
Connection ~ 6500 2450
Wire Wire Line
	4150 3100 4300 3100
Wire Wire Line
	4300 3100 4300 3200
Connection ~ 4300 3200
Wire Wire Line
	6450 2450 6600 2450
Wire Wire Line
	5450 2450 5850 2450
Wire Wire Line
	5450 2550 5450 2450
Wire Wire Line
	5450 2850 5450 3000
Wire Wire Line
	5150 3200 4900 3200
Wire Wire Line
	4150 3200 4600 3200
$Comp
L plot_i2 U1
U 1 1 56D4411B
P 6150 2700
F 0 "U1" H 6150 3100 60  0000 C CNN
F 1 "plot_i2" H 6150 2800 60  0000 C CNN
F 2 "" H 6150 2700 60  0000 C CNN
F 3 "" H 6150 2700 60  0000 C CNN
	1    6150 2700
	-1   0    0    -1  
$EndComp
$Comp
L dc I1
U 1 1 56D441DD
P 4150 3800
F 0 "I1" H 3950 3900 60  0000 C CNN
F 1 "dc" H 3950 3750 60  0000 C CNN
F 2 "R1" H 3850 3800 60  0000 C CNN
F 3 "" H 4150 3800 60  0000 C CNN
	1    4150 3800
	1    0    0    -1  
$EndComp
$Comp
L eSim_NPN Q1
U 1 1 5D5CEC51
P 5350 3200
F 0 "Q1" H 5250 3250 50  0000 R CNN
F 1 "eSim_NPN" H 5300 3350 50  0000 R CNN
F 2 "" H 5550 3300 29  0000 C CNN
F 3 "" H 5350 3200 60  0000 C CNN
	1    5350 3200
	1    0    0    -1  
$EndComp
$Comp
L PWR_FLAG #FLG02
U 1 1 5D665114
P 5600 4150
F 0 "#FLG02" H 5600 4225 50  0001 C CNN
F 1 "PWR_FLAG" H 5600 4300 50  0000 C CNN
F 2 "" H 5600 4150 50  0001 C CNN
F 3 "" H 5600 4150 50  0001 C CNN
	1    5600 4150
	1    0    0    -1  
$EndComp
Wire Wire Line
	5600 4150 5600 4250
Connection ~ 5600 4250
$EndSCHEMATC
