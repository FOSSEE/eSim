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
NoConn ~ 6350 2800
NoConn ~ 6350 3250
$Comp
L DC v2
U 1 1 6838486C
P 5000 2250
F 0 "v2" H 4800 2350 60  0000 C CNN
F 1 "DC" H 4800 2200 60  0000 C CNN
F 2 "R1" H 4700 2250 60  0000 C CNN
F 3 "" H 5000 2250 60  0000 C CNN
	1    5000 2250
	1    0    0    1   
$EndComp
$Comp
L eSim_GND #PWR01
U 1 1 683848C0
P 5150 1800
F 0 "#PWR01" H 5150 1550 50  0001 C CNN
F 1 "eSim_GND" H 5150 1650 50  0000 C CNN
F 2 "" H 5150 1800 50  0001 C CNN
F 3 "" H 5150 1800 50  0001 C CNN
	1    5150 1800
	1    0    0    -1  
$EndComp
$Comp
L eSim_GND #PWR02
U 1 1 683848DE
P 5050 3800
F 0 "#PWR02" H 5050 3550 50  0001 C CNN
F 1 "eSim_GND" H 5050 3650 50  0000 C CNN
F 2 "" H 5050 3800 50  0001 C CNN
F 3 "" H 5050 3800 50  0001 C CNN
	1    5050 3800
	1    0    0    -1  
$EndComp
NoConn ~ 6350 2950
NoConn ~ 6350 3100
NoConn ~ 6350 3400
NoConn ~ 6350 3550
NoConn ~ 6350 3700
NoConn ~ 6350 3800
NoConn ~ 5150 3700
NoConn ~ 5150 3550
NoConn ~ 5150 3400
NoConn ~ 5150 3250
$Comp
L pulse v1
U 1 1 6838493F
P 4800 3550
F 0 "v1" H 4600 3650 60  0000 C CNN
F 1 "pulse" H 4600 3500 60  0000 C CNN
F 2 "R1" H 4500 3550 60  0000 C CNN
F 3 "" H 4800 3550 60  0000 C CNN
	1    4800 3550
	1    0    0    -1  
$EndComp
$Comp
L eSim_GND #PWR03
U 1 1 68384996
P 4800 4100
F 0 "#PWR03" H 4800 3850 50  0001 C CNN
F 1 "eSim_GND" H 4800 3950 50  0000 C CNN
F 2 "" H 4800 4100 50  0001 C CNN
F 3 "" H 4800 4100 50  0001 C CNN
	1    4800 4100
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U1
U 1 1 68384C0C
P 4700 3150
F 0 "U1" H 4700 3650 60  0000 C CNN
F 1 "plot_v1" H 4900 3500 60  0000 C CNN
F 2 "" H 4700 3150 60  0000 C CNN
F 3 "" H 4700 3150 60  0000 C CNN
	1    4700 3150
	1    0    0    -1  
$EndComp
Text GLabel 4650 3050 0    60   Input ~ 0
OUT
$Comp
L CD4049 X1
U 1 1 683876A4
P 5750 4000
F 0 "X1" H 5750 4050 60  0000 C CNN
F 1 "CD4049" H 5700 5400 60  0000 C CNN
F 2 "" H 5750 4750 60  0001 C CNN
F 3 "" H 5750 4750 60  0001 C CNN
	1    5750 4000
	1    0    0    -1  
$EndComp
Text GLabel 3850 3350 0    60   Input ~ 0
in
$Comp
L plot_v1 U2
U 1 1 6838A23B
P 4150 3500
F 0 "U2" H 4150 4000 60  0000 C CNN
F 1 "plot_v1" H 4350 3850 60  0000 C CNN
F 2 "" H 4150 3500 60  0000 C CNN
F 3 "" H 4150 3500 60  0000 C CNN
	1    4150 3500
	1    0    0    -1  
$EndComp
Wire Wire Line
	5000 2700 5000 2800
Wire Wire Line
	5000 2800 5150 2800
Wire Wire Line
	5000 1800 5150 1800
Wire Wire Line
	5050 3800 5150 3800
Wire Wire Line
	4800 3100 5150 3100
Wire Wire Line
	4800 4000 4800 4100
Wire Wire Line
	4700 2950 5150 2950
Wire Wire Line
	4650 3050 4850 3050
Wire Wire Line
	4850 3050 4850 2950
Connection ~ 4850 2950
Wire Wire Line
	4150 3300 4950 3300
Wire Wire Line
	4950 3300 4950 3100
Connection ~ 4950 3100
Wire Wire Line
	3850 3350 4400 3350
Wire Wire Line
	4400 3350 4400 3300
Connection ~ 4400 3300
$EndSCHEMATC
