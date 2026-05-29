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
L 74HC279 X1
U 1 1 69424832
P 2900 5850
F 0 "X1" H 5800 7900 60  0000 C CNN
F 1 "74HC279" H 5800 8000 60  0000 C CNN
F 2 "" H 5800 7900 60  0001 C CNN
F 3 "" H 5800 7900 60  0001 C CNN
	1    2900 5850
	1    0    0    -1  
$EndComp
$Comp
L adc_bridge_4 U3
U 1 1 694248B1
P 3550 3850
F 0 "U3" H 3550 3850 60  0000 C CNN
F 1 "adc_bridge_4" H 3550 4150 60  0000 C CNN
F 2 "" H 3550 3850 60  0000 C CNN
F 3 "" H 3550 3850 60  0000 C CNN
	1    3550 3850
	1    0    0    -1  
$EndComp
Wire Wire Line
	4100 3650 4100 3350
Wire Wire Line
	4100 3350 5200 3350
Wire Wire Line
	4400 3350 4400 4050
Wire Wire Line
	4400 4050 5200 4050
Connection ~ 4400 3350
Wire Wire Line
	4100 3750 4600 3750
Wire Wire Line
	4600 3750 4600 3550
Wire Wire Line
	4600 3550 5200 3550
Wire Wire Line
	4100 3850 5200 3850
Wire Wire Line
	5200 3850 5200 3800
Wire Wire Line
	4100 3950 4100 4250
Wire Wire Line
	4100 4250 5200 4250
Wire Wire Line
	3000 3650 3000 3000
Wire Wire Line
	3000 3000 2550 3000
Wire Wire Line
	3000 3750 2900 3750
Wire Wire Line
	2900 3750 2900 3600
Wire Wire Line
	2900 3600 2550 3600
Wire Wire Line
	3000 3850 2900 3850
Wire Wire Line
	2900 3850 2900 4350
Wire Wire Line
	2900 4350 2550 4350
Wire Wire Line
	3000 3950 3000 4850
Wire Wire Line
	3000 4850 2550 4850
$Comp
L dac_bridge_2 U4
U 1 1 694249DD
P 6950 3800
F 0 "U4" H 6950 3800 60  0000 C CNN
F 1 "dac_bridge_2" H 7000 3950 60  0000 C CNN
F 2 "" H 6950 3800 60  0000 C CNN
F 3 "" H 6950 3800 60  0000 C CNN
	1    6950 3800
	1    0    0    -1  
$EndComp
Wire Wire Line
	6400 3600 6500 3600
Wire Wire Line
	6500 3600 6500 3750
Wire Wire Line
	6400 4050 6500 4050
Wire Wire Line
	6500 4050 6500 3850
Wire Wire Line
	7500 3750 7500 3400
Wire Wire Line
	7500 3400 7750 3400
Wire Wire Line
	7500 3850 7500 4200
Wire Wire Line
	7500 4200 7750 4200
$Comp
L pulse v1
U 1 1 69424B07
P 2100 3000
F 0 "v1" H 1900 3100 60  0000 C CNN
F 1 "pulse" H 1900 2950 60  0000 C CNN
F 2 "R1" H 1800 3000 60  0000 C CNN
F 3 "" H 2100 3000 60  0000 C CNN
	1    2100 3000
	0    1    1    0   
$EndComp
$Comp
L pulse v2
U 1 1 69424B7E
P 2100 3600
F 0 "v2" H 1900 3700 60  0000 C CNN
F 1 "pulse" H 1900 3550 60  0000 C CNN
F 2 "R1" H 1800 3600 60  0000 C CNN
F 3 "" H 2100 3600 60  0000 C CNN
	1    2100 3600
	0    1    1    0   
$EndComp
$Comp
L pulse v3
U 1 1 69424BDD
P 2100 4350
F 0 "v3" H 1900 4450 60  0000 C CNN
F 1 "pulse" H 1900 4300 60  0000 C CNN
F 2 "R1" H 1800 4350 60  0000 C CNN
F 3 "" H 2100 4350 60  0000 C CNN
	1    2100 4350
	0    1    1    0   
$EndComp
$Comp
L pulse v4
U 1 1 69424C16
P 2100 4850
F 0 "v4" H 1900 4950 60  0000 C CNN
F 1 "pulse" H 1900 4800 60  0000 C CNN
F 2 "R1" H 1800 4850 60  0000 C CNN
F 3 "" H 2100 4850 60  0000 C CNN
	1    2100 4850
	0    1    1    0   
$EndComp
Wire Wire Line
	1650 3000 1300 3000
Wire Wire Line
	1300 3000 1300 4850
Wire Wire Line
	1300 4850 1650 4850
Wire Wire Line
	1650 4350 1300 4350
Connection ~ 1300 4350
Wire Wire Line
	1650 3600 1300 3600
Connection ~ 1300 3600
Wire Wire Line
	1300 3950 1100 3950
Connection ~ 1300 3950
$Comp
L plot_v1 U5
U 1 1 69424DA6
P 7550 3400
F 0 "U5" H 7550 3900 60  0000 C CNN
F 1 "plot_v1" H 7750 3750 60  0000 C CNN
F 2 "" H 7550 3400 60  0000 C CNN
F 3 "" H 7550 3400 60  0000 C CNN
	1    7550 3400
	0    1    1    0   
$EndComp
$Comp
L plot_v1 U6
U 1 1 69424DEF
P 7550 4200
F 0 "U6" H 7550 4700 60  0000 C CNN
F 1 "plot_v1" H 7750 4550 60  0000 C CNN
F 2 "" H 7550 4200 60  0000 C CNN
F 3 "" H 7550 4200 60  0000 C CNN
	1    7550 4200
	0    1    1    0   
$EndComp
$Comp
L plot_v1 U1
U 1 1 69424EA5
P 2700 3100
F 0 "U1" H 2700 3600 60  0000 C CNN
F 1 "plot_v1" H 2900 3450 60  0000 C CNN
F 2 "" H 2700 3100 60  0000 C CNN
F 3 "" H 2700 3100 60  0000 C CNN
	1    2700 3100
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U2
U 1 1 69424EEE
P 2750 3750
F 0 "U2" H 2750 4250 60  0000 C CNN
F 1 "plot_v1" H 2950 4100 60  0000 C CNN
F 2 "" H 2750 3750 60  0000 C CNN
F 3 "" H 2750 3750 60  0000 C CNN
	1    2750 3750
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR01
U 1 1 69424FB6
P 1100 3950
F 0 "#PWR01" H 1100 3700 50  0001 C CNN
F 1 "GND" H 1100 3800 50  0000 C CNN
F 2 "" H 1100 3950 50  0001 C CNN
F 3 "" H 1100 3950 50  0001 C CNN
	1    1100 3950
	1    0    0    -1  
$EndComp
Text GLabel 3050 3100 2    60   Input ~ 0
Rbar
Wire Wire Line
	2700 2900 2700 3000
Connection ~ 2700 3000
Text GLabel 2600 3550 1    60   Input ~ 0
Sbar
Wire Wire Line
	2600 3550 2600 3600
Connection ~ 2600 3600
Wire Wire Line
	2750 3550 2750 3600
Connection ~ 2750 3600
Wire Wire Line
	3050 3100 3000 3100
Connection ~ 3000 3100
Text GLabel 7600 3300 1    60   Input ~ 0
Q
Text GLabel 7600 4050 1    60   Input ~ 0
Q1
Wire Wire Line
	7600 3300 7600 3400
Connection ~ 7600 3400
Wire Wire Line
	7600 4050 7600 4200
Connection ~ 7600 4200
$EndSCHEMATC
