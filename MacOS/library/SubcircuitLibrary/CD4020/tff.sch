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
LIBS:asw-cache
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
L d_tff U3
U 1 1 6815E4DD
P 8150 2800
F 0 "U3" H 8150 2800 60  0000 C CNN
F 1 "d_tff" H 8150 2950 60  0000 C CNN
F 2 "" H 8150 2800 60  0000 C CNN
F 3 "" H 8150 2800 60  0000 C CNN
	1    8150 2800
	1    0    0    -1  
$EndComp
$Comp
L adc_bridge_4 U1
U 1 1 6815E4DE
P 5050 2800
F 0 "U1" H 5050 2800 60  0000 C CNN
F 1 "adc_bridge_4" H 5050 3100 60  0000 C CNN
F 2 "" H 5050 2800 60  0000 C CNN
F 3 "" H 5050 2800 60  0000 C CNN
	1    5050 2800
	1    0    0    -1  
$EndComp
$Comp
L dac_bridge_1 U5
U 1 1 6815E4DF
P 9350 2500
F 0 "U5" H 9350 2500 60  0000 C CNN
F 1 "dac_bridge_1" H 9350 2650 60  0000 C CNN
F 2 "" H 9350 2500 60  0000 C CNN
F 3 "" H 9350 2500 60  0000 C CNN
	1    9350 2500
	1    0    0    -1  
$EndComp
$Comp
L dac_bridge_1 U4
U 1 1 6815E4E0
P 9300 3150
F 0 "U4" H 9300 3150 60  0000 C CNN
F 1 "dac_bridge_1" H 9300 3300 60  0000 C CNN
F 2 "" H 9300 3150 60  0000 C CNN
F 3 "" H 9300 3150 60  0000 C CNN
	1    9300 3150
	1    0    0    -1  
$EndComp
Text GLabel 9900 2450 2    60   Input ~ 0
q
Text GLabel 9850 3100 2    60   Input ~ 0
qb
Text GLabel 4500 2600 1    60   Input ~ 0
t
Text GLabel 4500 2700 0    60   Input ~ 0
clk
Text GLabel 4500 2900 0    60   Input ~ 0
reset
$Comp
L GND #PWR1
U 1 1 6815E4E1
P 4500 2800
F 0 "#PWR1" H 4500 2550 50  0001 C CNN
F 1 "GND" H 4500 2650 50  0000 C CNN
F 2 "" H 4500 2800 50  0001 C CNN
F 3 "" H 4500 2800 50  0001 C CNN
	1    4500 2800
	0    1    1    0   
$EndComp
Text GLabel 8700 2400 1    60   Input ~ 0
a1
Wire Wire Line
	7250 3400 8150 3400
Wire Wire Line
	7250 2900 7250 3400
Wire Wire Line
	7600 2700 7600 3100
Wire Wire Line
	7250 2700 7600 2700
Wire Wire Line
	7600 2600 7600 2450
Wire Wire Line
	8700 2450 8750 2450
Wire Wire Line
	5600 2600 6400 2600
Wire Wire Line
	6400 2600 6400 2650
Wire Wire Line
	7300 2600 7600 2600
Wire Wire Line
	5600 2700 6400 2700
Wire Wire Line
	6400 2700 6400 2750
Wire Wire Line
	7250 2750 7250 2700
Wire Wire Line
	5600 2800 5850 2800
Wire Wire Line
	5850 2800 5850 1750
Wire Wire Line
	5850 1750 8150 1750
Wire Wire Line
	8150 1750 8150 2150
Wire Wire Line
	5600 2900 7250 2900
Wire Wire Line
	8700 2450 8700 2400
Wire Wire Line
	6400 2650 7300 2650
Wire Wire Line
	7300 2650 7300 2600
$Comp
L d_inverter U2
U 1 1 6815E4E2
P 6850 2750
F 0 "U2" H 6850 2650 60  0000 C CNN
F 1 "d_inverter" H 6850 2900 60  0000 C CNN
F 2 "" H 6900 2700 60  0000 C CNN
F 3 "" H 6900 2700 60  0000 C CNN
	1    6850 2750
	1    0    0    -1  
$EndComp
Wire Wire Line
	6400 2750 6550 2750
Wire Wire Line
	7150 2750 7250 2750
$EndSCHEMATC
