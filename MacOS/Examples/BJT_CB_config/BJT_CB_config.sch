EESchema Schematic File Version 2
LIBS:BJT_CB_config-rescue
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
LIBS:BJT_CB_config-cache
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
L DC-RESCUE-BJT_CB_config v1
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
Text GLabel 4250 3000 0    60   Input ~ 0
ie
Text GLabel 6750 2300 2    60   Input ~ 0
vcb
$Comp
L R-RESCUE-BJT_CB_config R1
U 1 1 56C44AD7
P 5600 2750
F 0 "R1" H 5650 2880 50  0000 C CNN
F 1 "1k" H 5650 2800 50  0000 C CNN
F 2 "" H 5650 2730 30  0000 C CNN
F 3 "" V 5650 2800 30  0000 C CNN
	1    5600 2750
	0    1    1    0   
$EndComp
$Comp
L R-RESCUE-BJT_CB_config R2
U 1 1 56C44C4B
P 4900 3050
F 0 "R2" H 4950 3180 50  0000 C CNN
F 1 "1k" H 4950 3100 50  0000 C CNN
F 2 "" H 4950 3030 30  0000 C CNN
F 3 "" V 4950 3100 30  0000 C CNN
	1    4900 3050
	-1   0    0    1   
$EndComp
Wire Wire Line
	5450 3400 5450 4300
Wire Wire Line
	4150 4250 6600 4250
Connection ~ 5450 4250
Wire Wire Line
	6600 4250 6600 3500
Wire Wire Line
	6750 2300 6700 2300
Wire Wire Line
	4250 3000 4400 3000
Wire Wire Line
	4400 3000 4400 3100
Connection ~ 4400 3100
Wire Wire Line
	5650 2450 5650 2650
Wire Wire Line
	5650 2950 5650 3100
Wire Wire Line
	5250 3100 5000 3100
Wire Wire Line
	4150 3100 4700 3100
Wire Wire Line
	6550 2450 6600 2450
Wire Wire Line
	6600 2450 6600 2600
Wire Wire Line
	6700 2300 6700 2500
Wire Wire Line
	6700 2500 6600 2500
Connection ~ 6600 2500
Wire Wire Line
	4150 3350 4150 3100
$Comp
L plot_i2 U_ic1
U 1 1 56CC385D
P 6250 2200
F 0 "U_ic1" H 6250 2600 60  0000 C CNN
F 1 "plot_i2" H 6250 2300 60  0000 C CNN
F 2 "" H 6250 2200 60  0000 C CNN
F 3 "" H 6250 2200 60  0000 C CNN
	1    6250 2200
	-1   0    0    1   
$EndComp
Wire Wire Line
	5650 2450 5950 2450
$Comp
L dc I1
U 1 1 56CC3A22
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
U 1 1 5D5CEEB2
P 5450 3200
F 0 "Q1" H 5350 3250 50  0000 R CNN
F 1 "eSim_NPN" H 5400 3350 50  0000 R CNN
F 2 "" H 5650 3300 29  0000 C CNN
F 3 "" H 5450 3200 60  0000 C CNN
	1    5450 3200
	0    1    -1   0   
$EndComp
$Comp
L PWR_FLAG #FLG02
U 1 1 5D665163
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
