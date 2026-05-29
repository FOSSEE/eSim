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
LIBS:IC_MC1445L(2)-cache
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
L MC1445L X1
U 1 1 68405103
P 5650 3450
F 0 "X1" H 5750 2850 60  0000 C CNN
F 1 "MC1445L" H 5750 3850 60  0000 C CNN
F 2 "" H 5650 3450 60  0001 C CNN
F 3 "" H 5650 3450 60  0001 C CNN
	1    5650 3450
	1    0    0    -1  
$EndComp
$Comp
L sine v1
U 1 1 68405122
P 3100 3650
F 0 "v1" H 2900 3750 60  0000 C CNN
F 1 "sine" H 2900 3600 60  0000 C CNN
F 2 "R1" H 2800 3650 60  0000 C CNN
F 3 "" H 3100 3650 60  0000 C CNN
	1    3100 3650
	1    0    0    -1  
$EndComp
$Comp
L resistor R1
U 1 1 6840517B
P 3500 3600
F 0 "R1" H 3550 3730 50  0000 C CNN
F 1 "51" H 3550 3550 50  0000 C CNN
F 2 "" H 3550 3580 30  0000 C CNN
F 3 "" V 3550 3650 30  0000 C CNN
	1    3500 3600
	0    1    1    0   
$EndComp
$Comp
L DC v2
U 1 1 68405396
P 4800 5200
F 0 "v2" H 4600 5300 60  0000 C CNN
F 1 "DC" H 4600 5150 60  0000 C CNN
F 2 "R1" H 4500 5200 60  0000 C CNN
F 3 "" H 4800 5200 60  0000 C CNN
	1    4800 5200
	1    0    0    -1  
$EndComp
$Comp
L DC v3
U 1 1 68405403
P 5350 5400
F 0 "v3" H 5150 5500 60  0000 C CNN
F 1 "DC" H 5150 5350 60  0000 C CNN
F 2 "R1" H 5050 5400 60  0000 C CNN
F 3 "" H 5350 5400 60  0000 C CNN
	1    5350 5400
	1    0    0    -1  
$EndComp
$Comp
L plot_db U1
U 1 1 68405466
P 7150 2950
F 0 "U1" H 7150 3450 60  0000 C CNN
F 1 "plot_db" H 7350 3300 60  0000 C CNN
F 2 "" H 7150 2950 60  0000 C CNN
F 3 "" H 7150 2950 60  0000 C CNN
	1    7150 2950
	0    1    1    0   
$EndComp
$Comp
L plot_db U2
U 1 1 68405501
P 7150 3450
F 0 "U2" H 7150 3950 60  0000 C CNN
F 1 "plot_db" H 7350 3800 60  0000 C CNN
F 2 "" H 7150 3450 60  0000 C CNN
F 3 "" H 7150 3450 60  0000 C CNN
	1    7150 3450
	0    1    1    0   
$EndComp
$Comp
L GND #PWR01
U 1 1 68405650
P 3300 4200
F 0 "#PWR01" H 3300 3950 50  0001 C CNN
F 1 "GND" H 3300 4050 50  0000 C CNN
F 2 "" H 3300 4200 50  0001 C CNN
F 3 "" H 3300 4200 50  0001 C CNN
	1    3300 4200
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR02
U 1 1 68405677
P 4550 3850
F 0 "#PWR02" H 4550 3600 50  0001 C CNN
F 1 "GND" H 4550 3700 50  0000 C CNN
F 2 "" H 4550 3850 50  0001 C CNN
F 3 "" H 4550 3850 50  0001 C CNN
	1    4550 3850
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR03
U 1 1 68405697
P 4650 4300
F 0 "#PWR03" H 4650 4050 50  0001 C CNN
F 1 "GND" H 4650 4150 50  0000 C CNN
F 2 "" H 4650 4300 50  0001 C CNN
F 3 "" H 4650 4300 50  0001 C CNN
	1    4650 4300
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR04
U 1 1 684056B7
P 4800 5800
F 0 "#PWR04" H 4800 5550 50  0001 C CNN
F 1 "GND" H 4800 5650 50  0000 C CNN
F 2 "" H 4800 5800 50  0001 C CNN
F 3 "" H 4800 5800 50  0001 C CNN
	1    4800 5800
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR05
U 1 1 684056F3
P 5350 5950
F 0 "#PWR05" H 5350 5700 50  0001 C CNN
F 1 "GND" H 5350 5800 50  0000 C CNN
F 2 "" H 5350 5950 50  0001 C CNN
F 3 "" H 5350 5950 50  0001 C CNN
	1    5350 5950
	1    0    0    -1  
$EndComp
$Comp
L resistor R2
U 1 1 68405803
P 6800 2450
F 0 "R2" H 6850 2580 50  0000 C CNN
F 1 "2.5k" H 6850 2400 50  0000 C CNN
F 2 "" H 6850 2430 30  0000 C CNN
F 3 "" V 6850 2500 30  0000 C CNN
	1    6800 2450
	0    1    1    0   
$EndComp
$Comp
L resistor R3
U 1 1 684058B1
P 6800 3700
F 0 "R3" H 6850 3830 50  0000 C CNN
F 1 "2.5k" H 6850 3650 50  0000 C CNN
F 2 "" H 6850 3680 30  0000 C CNN
F 3 "" V 6850 3750 30  0000 C CNN
	1    6800 3700
	0    1    1    0   
$EndComp
$Comp
L GND #PWR06
U 1 1 68405AF4
P 6450 2500
F 0 "#PWR06" H 6450 2250 50  0001 C CNN
F 1 "GND" H 6450 2350 50  0000 C CNN
F 2 "" H 6450 2500 50  0001 C CNN
F 3 "" H 6450 2500 50  0001 C CNN
	1    6450 2500
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR07
U 1 1 68405B59
P 6850 4350
F 0 "#PWR07" H 6850 4100 50  0001 C CNN
F 1 "GND" H 6850 4200 50  0000 C CNN
F 2 "" H 6850 4350 50  0001 C CNN
F 3 "" H 6850 4350 50  0001 C CNN
	1    6850 4350
	1    0    0    -1  
$EndComp
Text GLabel 7150 2800 1    60   Input ~ 0
OUT(-)
Text GLabel 7150 3650 3    60   Input ~ 0
OUT(+)
Wire Wire Line
	3100 3200 5150 3200
Wire Wire Line
	3550 3200 3550 3500
Wire Wire Line
	3100 4100 3550 4100
Wire Wire Line
	3550 4100 3550 3800
Connection ~ 3550 3200
Wire Wire Line
	5150 3300 4550 3300
Wire Wire Line
	4550 3300 4550 3850
Wire Wire Line
	4550 3400 5150 3400
Wire Wire Line
	4550 3650 5150 3650
Connection ~ 4550 3400
Connection ~ 4550 3650
Wire Wire Line
	5150 3750 4650 3750
Wire Wire Line
	4650 3750 4650 4300
Wire Wire Line
	5150 3850 4800 3850
Wire Wire Line
	4800 3850 4800 4750
Wire Wire Line
	5150 3950 4900 3950
Wire Wire Line
	4900 3950 4900 4950
Wire Wire Line
	4900 4950 5350 4950
Wire Wire Line
	6200 3200 6200 2950
Wire Wire Line
	6200 2950 7350 2950
Wire Wire Line
	6200 3300 6200 3450
Wire Wire Line
	6200 3450 7350 3450
Wire Wire Line
	5350 5850 5350 5950
Wire Wire Line
	4800 5650 4800 5800
Wire Wire Line
	3300 4100 3300 4200
Connection ~ 3300 4100
Wire Wire Line
	6850 3450 6850 3600
Connection ~ 6850 3450
Wire Wire Line
	6850 3900 6850 4350
Wire Wire Line
	6850 2650 6850 2950
Connection ~ 6850 2950
Wire Wire Line
	6850 2350 6850 2250
Wire Wire Line
	6850 2250 6450 2250
Wire Wire Line
	6450 2250 6450 2500
Wire Wire Line
	7150 3650 7150 3450
Connection ~ 7150 3450
Wire Wire Line
	7150 2800 7150 2950
Connection ~ 7150 2950
$EndSCHEMATC
