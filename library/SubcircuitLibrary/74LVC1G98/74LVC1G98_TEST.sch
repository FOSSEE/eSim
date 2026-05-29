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
L 74LVC1G98 X1
U 1 1 69180B4F
P 3250 5850
F 0 "X1" H 6000 8000 60  0000 C CNN
F 1 "74LVC1G98" H 6000 8100 60  0000 C CNN
F 2 "" H 6000 8000 60  0001 C CNN
F 3 "" H 6000 8000 60  0001 C CNN
	1    3250 5850
	1    0    0    -1  
$EndComp
$Comp
L adc_bridge_3 U4
U 1 1 69180BA3
P 4650 3550
F 0 "U4" H 4650 3550 60  0000 C CNN
F 1 "adc_bridge_3" H 4650 3700 60  0000 C CNN
F 2 "" H 4650 3550 60  0000 C CNN
F 3 "" H 4650 3550 60  0000 C CNN
	1    4650 3550
	1    0    0    -1  
$EndComp
$Comp
L dac_bridge_1 U5
U 1 1 69180BDE
P 7300 3650
F 0 "U5" H 7300 3650 60  0000 C CNN
F 1 "dac_bridge_1" H 7300 3800 60  0000 C CNN
F 2 "" H 7300 3650 60  0000 C CNN
F 3 "" H 7300 3650 60  0000 C CNN
	1    7300 3650
	1    0    0    -1  
$EndComp
$Comp
L pulse v1
U 1 1 69180C21
P 2850 2900
F 0 "v1" H 2650 3000 60  0000 C CNN
F 1 "pulse" H 2650 2850 60  0000 C CNN
F 2 "R1" H 2550 2900 60  0000 C CNN
F 3 "" H 2850 2900 60  0000 C CNN
	1    2850 2900
	0    1    1    0   
$EndComp
$Comp
L pulse v2
U 1 1 69180C68
P 2850 3600
F 0 "v2" H 2650 3700 60  0000 C CNN
F 1 "pulse" H 2650 3550 60  0000 C CNN
F 2 "R1" H 2550 3600 60  0000 C CNN
F 3 "" H 2850 3600 60  0000 C CNN
	1    2850 3600
	0    1    1    0   
$EndComp
$Comp
L pulse v3
U 1 1 69180CC6
P 2850 4300
F 0 "v3" H 2650 4400 60  0000 C CNN
F 1 "pulse" H 2650 4250 60  0000 C CNN
F 2 "R1" H 2550 4300 60  0000 C CNN
F 3 "" H 2850 4300 60  0000 C CNN
	1    2850 4300
	0    1    1    0   
$EndComp
$Comp
L GND #PWR01
U 1 1 69180E01
P 2050 3450
F 0 "#PWR01" H 2050 3200 50  0001 C CNN
F 1 "GND" H 2050 3300 50  0000 C CNN
F 2 "" H 2050 3450 50  0001 C CNN
F 3 "" H 2050 3450 50  0001 C CNN
	1    2050 3450
	0    1    1    0   
$EndComp
$Comp
L plot_v1 U1
U 1 1 69180E21
P 3450 2950
F 0 "U1" H 3450 3450 60  0000 C CNN
F 1 "plot_v1" H 3650 3300 60  0000 C CNN
F 2 "" H 3450 2950 60  0000 C CNN
F 3 "" H 3450 2950 60  0000 C CNN
	1    3450 2950
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U2
U 1 1 69180E58
P 3450 3750
F 0 "U2" H 3450 4250 60  0000 C CNN
F 1 "plot_v1" H 3650 4100 60  0000 C CNN
F 2 "" H 3450 3750 60  0000 C CNN
F 3 "" H 3450 3750 60  0000 C CNN
	1    3450 3750
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U3
U 1 1 69180E95
P 3450 4450
F 0 "U3" H 3450 4950 60  0000 C CNN
F 1 "plot_v1" H 3650 4800 60  0000 C CNN
F 2 "" H 3450 4450 60  0000 C CNN
F 3 "" H 3450 4450 60  0000 C CNN
	1    3450 4450
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U6
U 1 1 69180EF4
P 8000 3600
F 0 "U6" H 8000 4100 60  0000 C CNN
F 1 "plot_v1" H 8200 3950 60  0000 C CNN
F 2 "" H 8000 3600 60  0000 C CNN
F 3 "" H 8000 3600 60  0000 C CNN
	1    8000 3600
	0    1    1    0   
$EndComp
Text GLabel 3950 2800 1    60   Input ~ 0
A
Text GLabel 3900 3500 1    60   Input ~ 0
B
Text GLabel 3900 4200 1    60   Input ~ 0
C
Text GLabel 8050 3500 1    60   Input ~ 0
Y
Wire Wire Line
	3300 2900 4050 2900
Wire Wire Line
	4050 2900 4050 3500
Wire Wire Line
	3300 3600 4050 3600
Wire Wire Line
	4050 3700 4050 4300
Wire Wire Line
	4050 4300 3300 4300
Wire Wire Line
	2400 4300 2200 4300
Wire Wire Line
	2200 4300 2200 2900
Wire Wire Line
	2200 2900 2400 2900
Wire Wire Line
	2400 3600 2200 3600
Connection ~ 2200 3600
Wire Wire Line
	5200 3500 5200 3450
Wire Wire Line
	5200 3450 5450 3450
Wire Wire Line
	5200 3600 5450 3600
Wire Wire Line
	5200 3700 5200 3800
Wire Wire Line
	5200 3800 5450 3800
Wire Wire Line
	6550 3600 6700 3600
Wire Wire Line
	7850 3600 8200 3600
Wire Wire Line
	3450 2750 3450 2900
Connection ~ 3450 2900
Wire Wire Line
	3450 3550 3450 3600
Connection ~ 3450 3600
Wire Wire Line
	3450 4250 3450 4300
Connection ~ 3450 4300
Wire Wire Line
	3950 2800 3950 2900
Connection ~ 3950 2900
Wire Wire Line
	3900 3500 3900 3600
Connection ~ 3900 3600
Wire Wire Line
	3900 4200 3900 4300
Connection ~ 3900 4300
Wire Wire Line
	2050 3450 2200 3450
Connection ~ 2200 3450
Wire Wire Line
	8050 3500 8050 3600
Connection ~ 8050 3600
$EndSCHEMATC
