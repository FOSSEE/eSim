EESchema Schematic File Version 2
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
LIBS:eSim_Plot
LIBS:transistors
LIBS:conn
LIBS:eSim_User
LIBS:regul
LIBS:74xx
LIBS:cmos4000
LIBS:eSim_Analog
LIBS:eSim_Devices
LIBS:eSim_Digital
LIBS:eSim_Hybrid
LIBS:eSim_Miscellaneous
LIBS:eSim_Power
LIBS:eSim_Sources
LIBS:eSim_Subckt
LIBS:eSim_Nghdl
LIBS:eSim_Ngveri
LIBS:eSim_SKY130
LIBS:eSim_SKY130_Subckts
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
L d_inverter U3
U 1 1 666DFBF0
P 3350 2900
F 0 "U3" H 3350 2800 60  0000 C CNN
F 1 "d_inverter" H 3350 3050 60  0000 C CNN
F 2 "" H 3400 2850 60  0000 C CNN
F 3 "" H 3400 2850 60  0000 C CNN
	1    3350 2900
	1    0    0    -1  
$EndComp
$Comp
L d_and U8
U 1 1 666DFC27
P 5150 2500
F 0 "U8" H 5150 2500 60  0000 C CNN
F 1 "d_and" H 5200 2600 60  0000 C CNN
F 2 "" H 5150 2500 60  0000 C CNN
F 3 "" H 5150 2500 60  0000 C CNN
	1    5150 2500
	1    0    0    -1  
$EndComp
$Comp
L d_inverter U6
U 1 1 666DFC6E
P 4400 2400
F 0 "U6" H 4400 2300 60  0000 C CNN
F 1 "d_inverter" H 4400 2550 60  0000 C CNN
F 2 "" H 4450 2350 60  0000 C CNN
F 3 "" H 4450 2350 60  0000 C CNN
	1    4400 2400
	1    0    0    -1  
$EndComp
$Comp
L d_or U10
U 1 1 666DFCAC
P 6050 2750
F 0 "U10" H 6050 2750 60  0000 C CNN
F 1 "d_or" H 6050 2850 60  0000 C CNN
F 2 "" H 6050 2750 60  0000 C CNN
F 3 "" H 6050 2750 60  0000 C CNN
	1    6050 2750
	1    0    0    -1  
$EndComp
$Comp
L d_and U9
U 1 1 666DFD21
P 5150 3000
F 0 "U9" H 5150 3000 60  0000 C CNN
F 1 "d_and" H 5200 3100 60  0000 C CNN
F 2 "" H 5150 3000 60  0000 C CNN
F 3 "" H 5150 3000 60  0000 C CNN
	1    5150 3000
	1    0    0    -1  
$EndComp
$Comp
L d_inverter U7
U 1 1 666DFD27
P 4400 2900
F 0 "U7" H 4400 2800 60  0000 C CNN
F 1 "d_inverter" H 4400 3050 60  0000 C CNN
F 2 "" H 4450 2850 60  0000 C CNN
F 3 "" H 4450 2850 60  0000 C CNN
	1    4400 2900
	1    0    0    -1  
$EndComp
$Comp
L d_inverter U2
U 1 1 666DFD59
P 3350 2400
F 0 "U2" H 3350 2300 60  0000 C CNN
F 1 "d_inverter" H 3350 2550 60  0000 C CNN
F 2 "" H 3400 2350 60  0000 C CNN
F 3 "" H 3400 2350 60  0000 C CNN
	1    3350 2400
	1    0    0    -1  
$EndComp
$Comp
L d_inverter U4
U 1 1 666DFD92
P 3350 3400
F 0 "U4" H 3350 3300 60  0000 C CNN
F 1 "d_inverter" H 3350 3550 60  0000 C CNN
F 2 "" H 3400 3350 60  0000 C CNN
F 3 "" H 3400 3350 60  0000 C CNN
	1    3350 3400
	1    0    0    -1  
$EndComp
$Comp
L d_inverter U5
U 1 1 666DFDE2
P 4100 3400
F 0 "U5" H 4100 3300 60  0000 C CNN
F 1 "d_inverter" H 4100 3550 60  0000 C CNN
F 2 "" H 4150 3350 60  0000 C CNN
F 3 "" H 4150 3350 60  0000 C CNN
	1    4100 3400
	1    0    0    -1  
$EndComp
Wire Wire Line
	3650 3400 3800 3400
Wire Wire Line
	4100 2900 3650 2900
Wire Wire Line
	3650 2400 4100 2400
Wire Wire Line
	4700 2500 4600 2500
Wire Wire Line
	4600 2500 4600 3400
Wire Wire Line
	4600 3400 4400 3400
Wire Wire Line
	4700 3000 3750 3000
Wire Wire Line
	3750 3000 3750 3400
Connection ~ 3750 3400
Wire Wire Line
	5600 2650 5600 2650
Wire Wire Line
	5600 2650 5600 2450
Wire Wire Line
	5600 2750 5600 2750
Wire Wire Line
	5600 2750 5600 2950
$Comp
L PORT U1
U 4 1 666DFEB3
P 6750 2700
F 0 "U1" H 6800 2800 30  0000 C CNN
F 1 "PORT" H 6750 2700 30  0000 C CNN
F 2 "" H 6750 2700 60  0000 C CNN
F 3 "" H 6750 2700 60  0000 C CNN
	4    6750 2700
	-1   0    0    1   
$EndComp
$Comp
L PORT U1
U 1 1 666E01B8
P 3050 2150
F 0 "U1" H 3100 2250 30  0000 C CNN
F 1 "PORT" H 3050 2150 30  0000 C CNN
F 2 "" H 3050 2150 60  0000 C CNN
F 3 "" H 3050 2150 60  0000 C CNN
	1    3050 2150
	0    1    1    0   
$EndComp
$Comp
L PORT U1
U 2 1 666E0201
P 3050 2650
F 0 "U1" H 3100 2750 30  0000 C CNN
F 1 "PORT" H 3050 2650 30  0000 C CNN
F 2 "" H 3050 2650 60  0000 C CNN
F 3 "" H 3050 2650 60  0000 C CNN
	2    3050 2650
	0    1    1    0   
$EndComp
$Comp
L PORT U1
U 3 1 666E023A
P 3050 3150
F 0 "U1" H 3100 3250 30  0000 C CNN
F 1 "PORT" H 3050 3150 30  0000 C CNN
F 2 "" H 3050 3150 60  0000 C CNN
F 3 "" H 3050 3150 60  0000 C CNN
	3    3050 3150
	0    1    1    0   
$EndComp
$EndSCHEMATC
