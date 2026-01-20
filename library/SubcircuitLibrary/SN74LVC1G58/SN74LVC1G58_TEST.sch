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
L SN74LVC1G58 X1
U 1 1 69180873
P 3600 5250
F 0 "X1" H 5750 6850 60  0000 C CNN
F 1 "SN74LVC1G58" H 5750 6950 60  0000 C CNN
F 2 "" H 5750 6850 60  0001 C CNN
F 3 "" H 5750 6850 60  0001 C CNN
	1    3600 5250
	1    0    0    -1  
$EndComp
$Comp
L adc_bridge_3 U4
U 1 1 691808BC
P 4300 3550
F 0 "U4" H 4300 3550 60  0000 C CNN
F 1 "adc_bridge_3" H 4300 3700 60  0000 C CNN
F 2 "" H 4300 3550 60  0000 C CNN
F 3 "" H 4300 3550 60  0000 C CNN
	1    4300 3550
	1    0    0    -1  
$EndComp
$Comp
L dac_bridge_1 U5
U 1 1 69180921
P 7150 3650
F 0 "U5" H 7150 3650 60  0000 C CNN
F 1 "dac_bridge_1" H 7150 3800 60  0000 C CNN
F 2 "" H 7150 3650 60  0000 C CNN
F 3 "" H 7150 3650 60  0000 C CNN
	1    7150 3650
	1    0    0    -1  
$EndComp
Wire Wire Line
	4850 3500 4850 3350
Wire Wire Line
	4850 3350 5150 3350
Wire Wire Line
	4850 3600 5150 3600
Wire Wire Line
	4850 3700 4850 3850
Wire Wire Line
	4850 3850 5150 3850
Wire Wire Line
	6350 3600 6550 3600
$Comp
L pulse v1
U 1 1 691809BE
P 2450 2800
F 0 "v1" H 2250 2900 60  0000 C CNN
F 1 "pulse" H 2250 2750 60  0000 C CNN
F 2 "R1" H 2150 2800 60  0000 C CNN
F 3 "" H 2450 2800 60  0000 C CNN
	1    2450 2800
	0    1    1    0   
$EndComp
$Comp
L pulse v2
U 1 1 69180A27
P 2450 3600
F 0 "v2" H 2250 3700 60  0000 C CNN
F 1 "pulse" H 2250 3550 60  0000 C CNN
F 2 "R1" H 2150 3600 60  0000 C CNN
F 3 "" H 2450 3600 60  0000 C CNN
	1    2450 3600
	0    1    1    0   
$EndComp
$Comp
L pulse v3
U 1 1 69180A56
P 2450 4300
F 0 "v3" H 2250 4400 60  0000 C CNN
F 1 "pulse" H 2250 4250 60  0000 C CNN
F 2 "R1" H 2150 4300 60  0000 C CNN
F 3 "" H 2450 4300 60  0000 C CNN
	1    2450 4300
	0    1    1    0   
$EndComp
Wire Wire Line
	2900 2800 3700 2800
Wire Wire Line
	3700 2800 3700 3500
Wire Wire Line
	2900 3600 3700 3600
Wire Wire Line
	2900 4300 3700 4300
Wire Wire Line
	3700 4300 3700 3700
Wire Wire Line
	1750 4300 2000 4300
Wire Wire Line
	1750 2800 2000 2800
Wire Wire Line
	1750 3600 2000 3600
Connection ~ 1750 3600
Wire Wire Line
	1750 2800 1750 4300
Wire Wire Line
	7700 3600 8050 3600
Wire Wire Line
	1500 3450 1750 3450
Connection ~ 1750 3450
$Comp
L plot_v1 U3
U 1 1 69180BB2
P 3300 2950
F 0 "U3" H 3300 3450 60  0000 C CNN
F 1 "plot_v1" H 3500 3300 60  0000 C CNN
F 2 "" H 3300 2950 60  0000 C CNN
F 3 "" H 3300 2950 60  0000 C CNN
	1    3300 2950
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U2
U 1 1 69180BF5
P 3050 3700
F 0 "U2" H 3050 4200 60  0000 C CNN
F 1 "plot_v1" H 3250 4050 60  0000 C CNN
F 2 "" H 3050 3700 60  0000 C CNN
F 3 "" H 3050 3700 60  0000 C CNN
	1    3050 3700
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U1
U 1 1 69180C26
P 3000 4400
F 0 "U1" H 3000 4900 60  0000 C CNN
F 1 "plot_v1" H 3200 4750 60  0000 C CNN
F 2 "" H 3000 4400 60  0000 C CNN
F 3 "" H 3000 4400 60  0000 C CNN
	1    3000 4400
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U6
U 1 1 69180CA2
P 7850 3600
F 0 "U6" H 7850 4100 60  0000 C CNN
F 1 "plot_v1" H 8050 3950 60  0000 C CNN
F 2 "" H 7850 3600 60  0000 C CNN
F 3 "" H 7850 3600 60  0000 C CNN
	1    7850 3600
	0    1    1    0   
$EndComp
Text GLabel 3050 2700 1    60   Input ~ 0
A
Text GLabel 3550 3500 1    60   Input ~ 0
B
Text GLabel 3500 4250 1    60   Input ~ 0
C
Text GLabel 7850 3500 1    60   Input ~ 0
Y
$Comp
L GND #PWR01
U 1 1 69180E88
P 1500 3450
F 0 "#PWR01" H 1500 3200 50  0001 C CNN
F 1 "GND" H 1500 3300 50  0000 C CNN
F 2 "" H 1500 3450 50  0001 C CNN
F 3 "" H 1500 3450 50  0001 C CNN
	1    1500 3450
	1    0    0    -1  
$EndComp
Wire Wire Line
	3050 2700 3050 2800
Connection ~ 3050 2800
Wire Wire Line
	3300 2750 3300 2800
Connection ~ 3300 2800
Wire Wire Line
	3050 3500 3050 3600
Connection ~ 3050 3600
Wire Wire Line
	3550 3500 3550 3600
Connection ~ 3550 3600
Wire Wire Line
	3000 4200 3000 4300
Connection ~ 3000 4300
Wire Wire Line
	3500 4250 3500 4300
Connection ~ 3500 4300
Wire Wire Line
	7850 3500 7850 3600
Connection ~ 7850 3600
$EndSCHEMATC
