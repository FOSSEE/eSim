EESchema Schematic File Version 2
LIBS:power
LIBS:device
LIBS:transistors
LIBS:conn
LIBS:linear
LIBS:regul
LIBS:74xx
LIBS:cmos4000
LIBS:adc-dac
LIBS:memory
LIBS:xilinx
LIBS:special
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
LIBS:valves
LIBS:eSim_Analog
LIBS:eSim_Devices
LIBS:eSim_Digital
LIBS:eSim_Hybrid
LIBS:eSim_Sources
LIBS:eSim_Subckt
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
L d_xor U2
U 1 1 558A946A
P 5650 3050
F 0 "U2" H 5650 3050 60  0000 C CNN
F 1 "d_xor" H 5700 3150 47  0000 C CNN
F 2 "" H 5650 3050 60  0000 C CNN
F 3 "" H 5650 3050 60  0000 C CNN
	1    5650 3050
	1    0    0    -1  
$EndComp
$Comp
L d_and U3
U 1 1 558A94D5
P 5700 3800
F 0 "U3" H 5700 3800 60  0000 C CNN
F 1 "d_and" H 5750 3900 60  0000 C CNN
F 2 "" H 5700 3800 60  0000 C CNN
F 3 "" H 5700 3800 60  0000 C CNN
	1    5700 3800
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 1 1 558A94F6
P 4150 3000
F 0 "U1" H 4200 3100 30  0000 C CNN
F 1 "PORT" H 4150 3000 30  0000 C CNN
F 2 "" H 4150 3000 60  0000 C CNN
F 3 "" H 4150 3000 60  0000 C CNN
	1    4150 3000
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 2 1 558A9543
P 4150 3450
F 0 "U1" H 4200 3550 30  0000 C CNN
F 1 "PORT" H 4150 3450 30  0000 C CNN
F 2 "" H 4150 3450 60  0000 C CNN
F 3 "" H 4150 3450 60  0000 C CNN
	2    4150 3450
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 3 1 558A9573
P 6650 3000
F 0 "U1" H 6700 3100 30  0000 C CNN
F 1 "PORT" H 6650 3000 30  0000 C CNN
F 2 "" H 6650 3000 60  0000 C CNN
F 3 "" H 6650 3000 60  0000 C CNN
	3    6650 3000
	-1   0    0    1   
$EndComp
$Comp
L PORT U1
U 4 1 558A9606
P 6700 3750
F 0 "U1" H 6750 3850 30  0000 C CNN
F 1 "PORT" H 6700 3750 30  0000 C CNN
F 2 "" H 6700 3750 60  0000 C CNN
F 3 "" H 6700 3750 60  0000 C CNN
	4    6700 3750
	-1   0    0    1   
$EndComp
Wire Wire Line
	5200 2950 4450 2950
Wire Wire Line
	4450 2950 4450 3000
Wire Wire Line
	4450 3000 4400 3000
Wire Wire Line
	4400 3450 4550 3450
Wire Wire Line
	4550 3450 4550 3050
Wire Wire Line
	4550 3050 5200 3050
Wire Wire Line
	5250 3700 5000 3700
Wire Wire Line
	5000 3700 5000 2950
Connection ~ 5000 2950
Wire Wire Line
	5250 3800 4850 3800
Wire Wire Line
	4850 3800 4850 3050
Connection ~ 4850 3050
Wire Wire Line
	6100 3000 6400 3000
Wire Wire Line
	6150 3750 6450 3750
Text Notes 4550 2950 0    60   ~ 0
IN1\n\n
Text Notes 4600 3150 0    60   ~ 0
IN2
Text Notes 6200 2950 0    60   ~ 0
SUM\n
Text Notes 6200 3650 0    60   ~ 0
COUT\n
$EndSCHEMATC
