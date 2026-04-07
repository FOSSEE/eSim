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
LIBS:device
LIBS:transistors
LIBS:conn
LIBS:linear
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
LIBS:eSim_User
LIBS:eSim_Plot
LIBS:eSim_PSpice
LIBS:74LS04-test-cache
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
L DC v2
U 1 1 5E1D63E6
P 5400 3400
F 0 "v2" H 5200 3500 60  0000 C CNN
F 1 "DC" H 5200 3350 60  0000 C CNN
F 2 "R1" H 5100 3400 60  0000 C CNN
F 3 "" H 5400 3400 60  0000 C CNN
	1    5400 3400
	0    1    1    0   
$EndComp
$Comp
L pulse v1
U 1 1 5E1D6488
P 3200 2150
F 0 "v1" H 3000 2250 60  0000 C CNN
F 1 "pulse" H 3000 2100 60  0000 C CNN
F 2 "R1" H 2900 2150 60  0000 C CNN
F 3 "" H 3200 2150 60  0000 C CNN
	1    3200 2150
	0    1    1    0   
$EndComp
$Comp
L eSim_R R2
U 1 1 5E1D64F5
P 3900 2200
F 0 "R2" H 3950 2330 50  0000 C CNN
F 1 "1k" H 3950 2150 50  0000 C CNN
F 2 "" H 3950 2180 30  0000 C CNN
F 3 "" V 3950 2250 30  0000 C CNN
	1    3900 2200
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U2
U 1 1 5E1D6966
P 4650 2400
F 0 "U2" H 4650 2900 60  0000 C CNN
F 1 "plot_v1" H 4850 2750 60  0000 C CNN
F 2 "" H 4650 2400 60  0000 C CNN
F 3 "" H 4650 2400 60  0000 C CNN
	1    4650 2400
	1    0    0    -1  
$EndComp
Text GLabel 4300 2350 0    60   Input ~ 0
out1
$Comp
L plot_v1 U1
U 1 1 5E1D6B17
P 3750 2200
F 0 "U1" H 3750 2700 60  0000 C CNN
F 1 "plot_v1" H 3950 2550 60  0000 C CNN
F 2 "" H 3750 2200 60  0000 C CNN
F 3 "" H 3750 2200 60  0000 C CNN
	1    3750 2200
	1    0    0    -1  
$EndComp
Text GLabel 3650 2050 0    60   Input ~ 0
in1
Wire Wire Line
	6100 2150 6100 3400
Wire Wire Line
	2650 3050 4950 3050
Wire Wire Line
	4850 3050 4850 3400
Wire Wire Line
	4850 3400 4950 3400
Wire Wire Line
	6100 3400 5850 3400
Wire Wire Line
	4100 2150 4950 2150
Wire Wire Line
	3650 2150 3800 2150
Wire Wire Line
	3750 2000 3750 2150
Connection ~ 3750 2150
Wire Wire Line
	3650 2050 3700 2050
Wire Wire Line
	3700 2050 3700 2150
Connection ~ 3700 2150
$Comp
L GND #PWR01
U 1 1 5E1D7F75
P 3850 3400
F 0 "#PWR01" H 3850 3150 50  0001 C CNN
F 1 "GND" H 3850 3250 50  0000 C CNN
F 2 "" H 3850 3400 50  0001 C CNN
F 3 "" H 3850 3400 50  0001 C CNN
	1    3850 3400
	1    0    0    -1  
$EndComp
Connection ~ 4850 3050
Wire Wire Line
	3850 3400 3850 3050
Connection ~ 3850 3050
Wire Wire Line
	4650 2200 4650 2300
Connection ~ 4650 2300
$Comp
L eSim_R R1
U 1 1 5E1D823A
P 4400 2600
F 0 "R1" H 4450 2730 50  0000 C CNN
F 1 "2k" H 4450 2550 50  0000 C CNN
F 2 "" H 4450 2580 30  0000 C CNN
F 3 "" V 4450 2650 30  0000 C CNN
	1    4400 2600
	0    1    1    0   
$EndComp
Wire Wire Line
	4450 2500 4450 2300
Wire Wire Line
	4450 2800 4450 3050
Connection ~ 4450 3050
Wire Wire Line
	4450 2300 4950 2300
Wire Wire Line
	2750 2150 2650 2150
Wire Wire Line
	2650 2150 2650 3050
Wire Wire Line
	4300 2350 4450 2350
Connection ~ 4450 2350
$Comp
L eSim_74LS04 X1
U 1 1 5E1D88C9
P 5500 2600
F 0 "X1" H 5500 2700 60  0000 C CNN
F 1 "eSim_74LS04" H 5500 2600 60  0000 C CNN
F 2 "" H 5500 2600 60  0001 C CNN
F 3 "" H 5500 2600 60  0001 C CNN
	1    5500 2600
	1    0    0    -1  
$EndComp
Wire Wire Line
	6050 2150 6100 2150
$EndSCHEMATC
