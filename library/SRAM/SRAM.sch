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
LIBS:SRAM-cache
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
L pulse v1
U 1 1 664DBAB1
P 2400 4550
F 0 "v1" H 2200 4650 60  0000 C CNN
F 1 "pulse" H 2200 4500 60  0000 C CNN
F 2 "R1" H 2100 4550 60  0000 C CNN
F 3 "" H 2400 4550 60  0000 C CNN
	1    2400 4550
	1    0    0    -1  
$EndComp
$Comp
L pulse v2
U 1 1 664DBAE4
P 2950 4550
F 0 "v2" H 2750 4650 60  0000 C CNN
F 1 "pulse" H 2750 4500 60  0000 C CNN
F 2 "R1" H 2650 4550 60  0000 C CNN
F 3 "" H 2950 4550 60  0000 C CNN
	1    2950 4550
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR01
U 1 1 664DBC0B
P 2400 5100
F 0 "#PWR01" H 2400 4850 50  0001 C CNN
F 1 "GND" H 2400 4950 50  0000 C CNN
F 2 "" H 2400 5100 50  0001 C CNN
F 3 "" H 2400 5100 50  0001 C CNN
	1    2400 5100
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR02
U 1 1 664DBC2A
P 2950 5100
F 0 "#PWR02" H 2950 4850 50  0001 C CNN
F 1 "GND" H 2950 4950 50  0000 C CNN
F 2 "" H 2950 5100 50  0001 C CNN
F 3 "" H 2950 5100 50  0001 C CNN
	1    2950 5100
	1    0    0    -1  
$EndComp
$Comp
L DC v3
U 1 1 664DBC81
P 5250 3400
F 0 "v3" H 5050 3500 60  0000 C CNN
F 1 "DC" H 5050 3350 60  0000 C CNN
F 2 "R1" H 4950 3400 60  0000 C CNN
F 3 "" H 5250 3400 60  0000 C CNN
	1    5250 3400
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR03
U 1 1 664DBCEF
P 5250 3900
F 0 "#PWR03" H 5250 3650 50  0001 C CNN
F 1 "GND" H 5250 3750 50  0000 C CNN
F 2 "" H 5250 3900 50  0001 C CNN
F 3 "" H 5250 3900 50  0001 C CNN
	1    5250 3900
	1    0    0    -1  
$EndComp
Text GLabel 2550 4050 1    60   Input ~ 0
WL
Text GLabel 3350 4300 1    60   Input ~ 0
BL
Text GLabel 5650 4150 1    60   Input ~ 0
NOT_BL
Text GLabel 5000 3950 1    60   Input ~ 0
Q
Text GLabel 5000 4350 1    60   Input ~ 0
NOT_Q
$Comp
L GND #PWR04
U 1 1 664DBEF2
P 5150 4900
F 0 "#PWR04" H 5150 4650 50  0001 C CNN
F 1 "GND" H 5150 4750 50  0000 C CNN
F 2 "" H 5150 4900 50  0001 C CNN
F 3 "" H 5150 4900 50  0001 C CNN
	1    5150 4900
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U1
U 1 1 664DC3DB
P 2850 4050
F 0 "U1" H 2850 4550 60  0000 C CNN
F 1 "plot_v1" H 3050 4400 60  0000 C CNN
F 2 "" H 2850 4050 60  0000 C CNN
F 3 "" H 2850 4050 60  0000 C CNN
	1    2850 4050
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U2
U 1 1 664DC45C
P 3350 4050
F 0 "U2" H 3350 4550 60  0000 C CNN
F 1 "plot_v1" H 3550 4400 60  0000 C CNN
F 2 "" H 3350 4050 60  0000 C CNN
F 3 "" H 3350 4050 60  0000 C CNN
	1    3350 4050
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U5
U 1 1 664DC493
P 5800 4300
F 0 "U5" H 5800 4800 60  0000 C CNN
F 1 "plot_v1" H 6000 4650 60  0000 C CNN
F 2 "" H 5800 4300 60  0000 C CNN
F 3 "" H 5800 4300 60  0000 C CNN
	1    5800 4300
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U4
U 1 1 664DC567
P 5150 4250
F 0 "U4" H 5150 4750 60  0000 C CNN
F 1 "plot_v1" H 5350 4600 60  0000 C CNN
F 2 "" H 5150 4250 60  0000 C CNN
F 3 "" H 5150 4250 60  0000 C CNN
	1    5150 4250
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U3
U 1 1 664DC5C6
P 4950 4350
F 0 "U3" H 4950 4850 60  0000 C CNN
F 1 "plot_v1" H 4900 4600 60  0000 C CNN
F 2 "" H 4950 4350 60  0000 C CNN
F 3 "" H 4950 4350 60  0000 C CNN
	1    4950 4350
	0    1    1    0   
$EndComp
$Comp
L GND #PWR05
U 1 1 664DBB89
P 4450 4750
F 0 "#PWR05" H 4450 4500 50  0001 C CNN
F 1 "GND" H 4450 4600 50  0000 C CNN
F 2 "" H 4450 4750 50  0001 C CNN
F 3 "" H 4450 4750 50  0001 C CNN
	1    4450 4750
	1    0    0    -1  
$EndComp
$Comp
L resistor R1
U 1 1 664F2152
P 4950 4550
F 0 "R1" H 5000 4680 50  0000 C CNN
F 1 "1000k" H 5000 4500 50  0000 C CNN
F 2 "" H 5000 4530 30  0000 C CNN
F 3 "" V 5000 4600 30  0000 C CNN
	1    4950 4550
	0    1    1    0   
$EndComp
$Comp
L resistor R2
U 1 1 664F2198
P 5250 4550
F 0 "R2" H 5300 4680 50  0000 C CNN
F 1 "1000k" H 5300 4500 50  0000 C CNN
F 2 "" H 5300 4530 30  0000 C CNN
F 3 "" V 5300 4600 30  0000 C CNN
	1    5250 4550
	0    1    1    0   
$EndComp
Wire Wire Line
	4450 4750 4450 4650
Wire Wire Line
	5850 4150 5000 4150
Wire Wire Line
	2950 5100 2950 5000
Wire Wire Line
	2400 5100 2400 5000
Wire Wire Line
	2950 4100 3150 4100
Wire Wire Line
	3150 4100 3150 4300
Wire Wire Line
	3150 4300 3950 4300
Wire Wire Line
	3950 4050 2400 4050
Wire Wire Line
	2400 4050 2400 4100
Wire Wire Line
	5250 3900 5250 3850
Wire Wire Line
	5250 2950 4450 2950
Wire Wire Line
	4450 2950 4450 3600
Wire Wire Line
	5000 3950 5000 4100
Wire Wire Line
	5000 4100 5300 4100
Wire Wire Line
	5300 4100 5300 4450
Wire Wire Line
	5000 4450 5000 4350
Wire Wire Line
	5300 4900 5300 4750
Wire Wire Line
	5000 4900 5300 4900
Wire Wire Line
	5000 4750 5000 4900
Connection ~ 5150 4900
Wire Wire Line
	5150 4050 5150 4100
Connection ~ 5150 4100
Wire Wire Line
	5150 4350 5150 4400
Wire Wire Line
	5150 4400 5000 4400
Connection ~ 5000 4400
Wire Wire Line
	5800 4100 5800 4150
Connection ~ 5800 4150
Wire Wire Line
	2850 3850 2850 4050
Connection ~ 2850 4050
Wire Wire Line
	3350 3850 3650 3850
Wire Wire Line
	3650 3850 3650 4300
Connection ~ 3650 4300
Wire Wire Line
	5850 5150 5850 5050
$Comp
L GND #PWR06
U 1 1 664DBBE8
P 5850 5150
F 0 "#PWR06" H 5850 4900 50  0001 C CNN
F 1 "GND" H 5850 5000 50  0000 C CNN
F 2 "" H 5850 5150 50  0001 C CNN
F 3 "" H 5850 5150 50  0001 C CNN
	1    5850 5150
	1    0    0    -1  
$EndComp
$Comp
L pulse v4
U 1 1 664DBB35
P 5850 4600
F 0 "v4" H 5650 4700 60  0000 C CNN
F 1 "pulse" H 5650 4550 60  0000 C CNN
F 2 "R1" H 5550 4600 60  0000 C CNN
F 3 "" H 5850 4600 60  0000 C CNN
	1    5850 4600
	1    0    0    -1  
$EndComp
$Comp
L SRAM_Cell X1
U 1 1 665033ED
P 3550 4450
F 0 "X1" H 4600 4400 60  0000 C CNN
F 1 "SRAM_Cell" H 4500 5150 60  0000 C CNN
F 2 "" H 3550 4450 60  0001 C CNN
F 3 "" H 3550 4450 60  0001 C CNN
	1    3550 4450
	1    0    0    -1  
$EndComp
$EndSCHEMATC
