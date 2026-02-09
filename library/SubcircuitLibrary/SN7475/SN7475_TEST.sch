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
LIBS:SN7475_TEST-cache
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
L adc_bridge_2 U3
U 1 1 6900D15C
P 4350 3750
F 0 "U3" H 4350 3750 60  0000 C CNN
F 1 "adc_bridge_2" H 4350 3900 60  0000 C CNN
F 2 "" H 4350 3750 60  0000 C CNN
F 3 "" H 4350 3750 60  0000 C CNN
	1    4350 3750
	1    0    0    -1  
$EndComp
$Comp
L pulse v1
U 1 1 6900D1A1
P 2450 3200
F 0 "v1" H 2250 3300 60  0000 C CNN
F 1 "pulse" H 2250 3150 60  0000 C CNN
F 2 "R1" H 2150 3200 60  0000 C CNN
F 3 "" H 2450 3200 60  0000 C CNN
	1    2450 3200
	0    1    1    0   
$EndComp
$Comp
L pulse v2
U 1 1 6900D1E0
P 2450 4400
F 0 "v2" H 2250 4500 60  0000 C CNN
F 1 "pulse" H 2250 4350 60  0000 C CNN
F 2 "R1" H 2150 4400 60  0000 C CNN
F 3 "" H 2450 4400 60  0000 C CNN
	1    2450 4400
	0    1    1    0   
$EndComp
Wire Wire Line
	2900 3200 3750 3200
Wire Wire Line
	3750 3200 3750 3700
Wire Wire Line
	2900 4400 3750 4400
Wire Wire Line
	3750 4400 3750 3800
Wire Wire Line
	2000 3200 1850 3200
Wire Wire Line
	1850 3200 1850 4400
Wire Wire Line
	1850 4400 2000 4400
Wire Wire Line
	1850 3700 1650 3700
Connection ~ 1850 3700
Wire Wire Line
	4900 3700 4900 3650
Wire Wire Line
	4900 3650 5050 3650
Wire Wire Line
	4900 3800 4900 3900
$Comp
L dac_bridge_2 U4
U 1 1 6900D286
P 6750 3750
F 0 "U4" H 6750 3750 60  0000 C CNN
F 1 "dac_bridge_2" H 6800 3900 60  0000 C CNN
F 2 "" H 6750 3750 60  0000 C CNN
F 3 "" H 6750 3750 60  0000 C CNN
	1    6750 3750
	1    0    0    -1  
$EndComp
Wire Wire Line
	6150 3650 6300 3650
Wire Wire Line
	6300 3650 6300 3700
Wire Wire Line
	6300 3800 6300 3900
Wire Wire Line
	7300 3700 7300 3450
Wire Wire Line
	7300 3450 7850 3450
Wire Wire Line
	7300 3800 7300 3950
Wire Wire Line
	7300 3950 7850 3950
$Comp
L plot_v1 U1
U 1 1 6900D33F
P 3050 3350
F 0 "U1" H 3050 3850 60  0000 C CNN
F 1 "plot_v1" H 3250 3700 60  0000 C CNN
F 2 "" H 3050 3350 60  0000 C CNN
F 3 "" H 3050 3350 60  0000 C CNN
	1    3050 3350
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U2
U 1 1 6900D39C
P 3100 4300
F 0 "U2" H 3100 4800 60  0000 C CNN
F 1 "plot_v1" H 3300 4650 60  0000 C CNN
F 2 "" H 3100 4300 60  0000 C CNN
F 3 "" H 3100 4300 60  0000 C CNN
	1    3100 4300
	-1   0    0    1   
$EndComp
$Comp
L plot_v1 U5
U 1 1 6900D3FE
P 7650 3450
F 0 "U5" H 7650 3950 60  0000 C CNN
F 1 "plot_v1" H 7850 3800 60  0000 C CNN
F 2 "" H 7650 3450 60  0000 C CNN
F 3 "" H 7650 3450 60  0000 C CNN
	1    7650 3450
	0    1    1    0   
$EndComp
$Comp
L plot_v1 U6
U 1 1 6900D457
P 7650 3950
F 0 "U6" H 7650 4450 60  0000 C CNN
F 1 "plot_v1" H 7850 4300 60  0000 C CNN
F 2 "" H 7650 3950 60  0000 C CNN
F 3 "" H 7650 3950 60  0000 C CNN
	1    7650 3950
	0    1    1    0   
$EndComp
Text GLabel 3600 3050 1    60   Input ~ 0
C
Text GLabel 3600 4550 3    60   Input ~ 0
D
Text GLabel 7600 3350 1    60   Input ~ 0
Q
Text GLabel 7600 4050 3    60   Input ~ 0
Qbar
Wire Wire Line
	3050 3150 3050 3200
Connection ~ 3050 3200
Wire Wire Line
	3600 3050 3600 3200
Connection ~ 3600 3200
Wire Wire Line
	3100 4500 3100 4400
Connection ~ 3100 4400
Wire Wire Line
	3600 4550 3600 4400
Connection ~ 3600 4400
Wire Wire Line
	7600 3350 7600 3450
Connection ~ 7600 3450
Wire Wire Line
	7600 4050 7600 3950
Connection ~ 7600 3950
$Comp
L GND #PWR01
U 1 1 6900D653
P 1650 3700
F 0 "#PWR01" H 1650 3450 50  0001 C CNN
F 1 "GND" H 1650 3550 50  0000 C CNN
F 2 "" H 1650 3700 50  0001 C CNN
F 3 "" H 1650 3700 50  0001 C CNN
	1    1650 3700
	0    1    1    0   
$EndComp
$Comp
L SN74LS75 X1
U 1 1 6900DA76
P 4500 4700
F 0 "X1" H 5600 5550 60  0000 C CNN
F 1 "SN74LS75" H 5600 5650 60  0000 C CNN
F 2 "" H 5550 5550 60  0001 C CNN
F 3 "" H 5550 5550 60  0001 C CNN
	1    4500 4700
	1    0    0    -1  
$EndComp
Wire Wire Line
	4900 3900 5050 3900
Wire Wire Line
	6300 3900 6150 3900
$EndSCHEMATC
