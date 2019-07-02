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
L SPEAKER X1
U 1 1 5D1B061E
P 6900 3550
F 0 "X1" H 6700 3650 60  0000 C CNN
F 1 "SPEAKER" H 6300 3650 60  0000 C CNN
F 2 "" H 6900 3550 60  0001 C CNN
F 3 "" H 6900 3550 60  0001 C CNN
	1    6900 3550
	1    0    0    -1  
$EndComp
$Comp
L AC v1
U 1 1 5D1B061F
P 4350 3550
F 0 "v1" H 4150 3650 60  0000 C CNN
F 1 "AC" H 4150 3500 60  0000 C CNN
F 2 "R1" H 4050 3550 60  0000 C CNN
F 3 "" H 4350 3550 60  0000 C CNN
	1    4350 3550
	1    0    0    -1  
$EndComp
$Comp
L eSim_R R1
U 1 1 5D1B0620
P 4650 2850
F 0 "R1" H 4700 2980 50  0000 C CNN
F 1 "10" H 4700 2900 50  0000 C CNN
F 2 "" H 4700 2830 30  0000 C CNN
F 3 "" V 4700 2900 30  0000 C CNN
	1    4650 2850
	1    0    0    -1  
$EndComp
Wire Wire Line
	4350 3100 4350 2800
Wire Wire Line
	4350 2800 4550 2800
Wire Wire Line
	6700 2800 6700 2900
Wire Wire Line
	4850 2800 5050 2800
Wire Wire Line
	5650 2800 6700 2800
Wire Wire Line
	6650 4450 6650 4050
Wire Wire Line
	4350 4450 6650 4450
Wire Wire Line
	4350 4450 4350 4000
$Comp
L eSim_GND #PWR01
U 1 1 5D1B0621
P 5300 4600
F 0 "#PWR01" H 5300 4350 50  0001 C CNN
F 1 "eSim_GND" H 5300 4450 50  0000 C CNN
F 2 "" H 5300 4600 50  0001 C CNN
F 3 "" H 5300 4600 50  0001 C CNN
	1    5300 4600
	1    0    0    -1  
$EndComp
Wire Wire Line
	5300 4600 5300 4450
Connection ~ 5300 4450
$Comp
L plot_v1 U2
U 1 1 5D1B0622
P 6350 2900
F 0 "U2" H 6350 3400 60  0000 C CNN
F 1 "plot_v1" H 6550 3250 60  0000 C CNN
F 2 "" H 6350 2900 60  0000 C CNN
F 3 "" H 6350 2900 60  0000 C CNN
	1    6350 2900
	1    0    0    -1  
$EndComp
Wire Wire Line
	6350 2700 6350 2800
Connection ~ 6350 2800
Text GLabel 6600 2800 1    60   Input ~ 0
v_vr
$Comp
L plot_i2 U1
U 1 1 5D1B0623
P 5350 3050
F 0 "U1" H 5350 3450 60  0000 C CNN
F 1 "plot_i2" H 5350 3150 60  0000 C CNN
F 2 "" H 5350 3050 60  0000 C CNN
F 3 "" H 5350 3050 60  0000 C CNN
	1    5350 3050
	1    0    0    -1  
$EndComp
$EndSCHEMATC
