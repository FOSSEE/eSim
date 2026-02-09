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
L 74HC126 X1
U 1 1 694F6AE4
P 4700 5100
F 0 "X1" H 6300 6150 60  0000 C CNN
F 1 "74HC126" H 6300 6250 60  0000 C CNN
F 2 "" H 6300 6150 60  0001 C CNN
F 3 "" H 6300 6150 60  0001 C CNN
	1    4700 5100
	1    0    0    -1  
$EndComp
$Comp
L adc_bridge_2 U3
U 1 1 694F6B3F
P 5100 3950
F 0 "U3" H 5100 3950 60  0000 C CNN
F 1 "adc_bridge_2" H 5100 4100 60  0000 C CNN
F 2 "" H 5100 3950 60  0000 C CNN
F 3 "" H 5100 3950 60  0000 C CNN
	1    5100 3950
	1    0    0    -1  
$EndComp
$Comp
L dac_bridge_1 U4
U 1 1 694F6B92
P 7700 3950
F 0 "U4" H 7700 3950 60  0000 C CNN
F 1 "dac_bridge_1" H 7700 4100 60  0000 C CNN
F 2 "" H 7700 3950 60  0000 C CNN
F 3 "" H 7700 3950 60  0000 C CNN
	1    7700 3950
	1    0    0    -1  
$EndComp
Wire Wire Line
	5650 3900 5650 3750
Wire Wire Line
	5650 3750 5700 3750
Wire Wire Line
	5650 4000 5650 4150
Wire Wire Line
	5650 4150 5700 4150
Wire Wire Line
	6900 3900 7100 3900
Wire Wire Line
	8250 3900 8550 3900
Wire Wire Line
	4500 3900 4500 3600
Wire Wire Line
	4500 3600 4200 3600
Wire Wire Line
	4500 4000 4500 4400
Wire Wire Line
	4500 4250 4200 4250
$Comp
L pulse v1
U 1 1 694F6C63
P 3750 3600
F 0 "v1" H 3550 3700 60  0000 C CNN
F 1 "pulse" H 3550 3550 60  0000 C CNN
F 2 "R1" H 3450 3600 60  0000 C CNN
F 3 "" H 3750 3600 60  0000 C CNN
	1    3750 3600
	0    1    1    0   
$EndComp
$Comp
L pulse v2
U 1 1 694F6C9A
P 3750 4250
F 0 "v2" H 3550 4350 60  0000 C CNN
F 1 "pulse" H 3550 4200 60  0000 C CNN
F 2 "R1" H 3450 4250 60  0000 C CNN
F 3 "" H 3750 4250 60  0000 C CNN
	1    3750 4250
	0    1    1    0   
$EndComp
Wire Wire Line
	3300 3600 3050 3600
Wire Wire Line
	3050 3600 3050 4250
Wire Wire Line
	3050 4250 3300 4250
Wire Wire Line
	3050 3900 2950 3900
Connection ~ 3050 3900
$Comp
L plot_v1 U1
U 1 1 694F6D47
P 4450 3700
F 0 "U1" H 4450 4200 60  0000 C CNN
F 1 "plot_v1" H 4650 4050 60  0000 C CNN
F 2 "" H 4450 3700 60  0000 C CNN
F 3 "" H 4450 3700 60  0000 C CNN
	1    4450 3700
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U2
U 1 1 694F6D88
P 4500 4200
F 0 "U2" H 4500 4700 60  0000 C CNN
F 1 "plot_v1" H 4700 4550 60  0000 C CNN
F 2 "" H 4500 4200 60  0000 C CNN
F 3 "" H 4500 4200 60  0000 C CNN
	1    4500 4200
	-1   0    0    1   
$EndComp
$Comp
L plot_v1 U5
U 1 1 694F6E04
P 8350 3900
F 0 "U5" H 8350 4400 60  0000 C CNN
F 1 "plot_v1" H 8550 4250 60  0000 C CNN
F 2 "" H 8350 3900 60  0000 C CNN
F 3 "" H 8350 3900 60  0000 C CNN
	1    8350 3900
	0    1    1    0   
$EndComp
Text GLabel 8400 3800 1    60   Input ~ 0
Y
Text GLabel 4300 4350 3    60   Input ~ 0
OEbar
Text GLabel 4300 3500 1    60   Input ~ 0
A
Wire Wire Line
	4300 3500 4300 3600
Connection ~ 4300 3600
Wire Wire Line
	4450 3500 4450 3600
Connection ~ 4450 3600
Wire Wire Line
	4300 4350 4300 4250
Connection ~ 4300 4250
Connection ~ 4500 4250
Wire Wire Line
	8400 3800 8400 3900
Connection ~ 8400 3900
$Comp
L GND #PWR01
U 1 1 694F7078
P 2950 3900
F 0 "#PWR01" H 2950 3650 50  0001 C CNN
F 1 "GND" H 2950 3750 50  0000 C CNN
F 2 "" H 2950 3900 50  0001 C CNN
F 3 "" H 2950 3900 50  0001 C CNN
	1    2950 3900
	0    1    1    0   
$EndComp
$EndSCHEMATC
