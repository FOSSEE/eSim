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
L d_xor U3
U 1 1 5C7FDDA3
P 4400 3150
F 0 "U3" H 4400 3150 60  0000 C CNN
F 1 "d_xor" H 4450 3250 47  0000 C CNN
F 2 "" H 4400 3150 60  0000 C CNN
F 3 "" H 4400 3150 60  0000 C CNN
	1    4400 3150
	1    0    0    -1  
$EndComp
$Comp
L d_inverter U2
U 1 1 5C7FDDD8
P 3400 3750
F 0 "U2" H 3400 3650 60  0000 C CNN
F 1 "d_inverter" H 3400 3900 60  0000 C CNN
F 2 "" H 3450 3700 60  0000 C CNN
F 3 "" H 3450 3700 60  0000 C CNN
	1    3400 3750
	1    0    0    -1  
$EndComp
$Comp
L d_and U4
U 1 1 5C7FDE57
P 4450 3750
F 0 "U4" H 4450 3750 60  0000 C CNN
F 1 "d_and" H 4500 3850 60  0000 C CNN
F 2 "" H 4450 3750 60  0000 C CNN
F 3 "" H 4450 3750 60  0000 C CNN
	1    4450 3750
	1    0    0    -1  
$EndComp
Wire Wire Line
	3950 3150 3950 3650
Wire Wire Line
	3950 3650 4000 3650
Wire Wire Line
	3700 3750 4000 3750
Wire Wire Line
	3100 3750 3100 3050
Wire Wire Line
	2950 3050 3950 3050
$Comp
L PORT U1
U 1 1 5C7FDF5A
P 2700 3050
F 0 "U1" H 2750 3150 30  0000 C CNN
F 1 "PORT" H 2700 3050 30  0000 C CNN
F 2 "" H 2700 3050 60  0000 C CNN
F 3 "" H 2700 3050 60  0000 C CNN
	1    2700 3050
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 2 1 5C7FDF97
P 3500 3350
F 0 "U1" H 3550 3450 30  0000 C CNN
F 1 "PORT" H 3500 3350 30  0000 C CNN
F 2 "" H 3500 3350 60  0000 C CNN
F 3 "" H 3500 3350 60  0000 C CNN
	2    3500 3350
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 3 1 5C7FE00A
P 5300 3100
F 0 "U1" H 5350 3200 30  0000 C CNN
F 1 "PORT" H 5300 3100 30  0000 C CNN
F 2 "" H 5300 3100 60  0000 C CNN
F 3 "" H 5300 3100 60  0000 C CNN
	3    5300 3100
	-1   0    0    1   
$EndComp
$Comp
L PORT U1
U 4 1 5C7FE064
P 5350 3700
F 0 "U1" H 5400 3800 30  0000 C CNN
F 1 "PORT" H 5350 3700 30  0000 C CNN
F 2 "" H 5350 3700 60  0000 C CNN
F 3 "" H 5350 3700 60  0000 C CNN
	4    5350 3700
	-1   0    0    1   
$EndComp
Connection ~ 3100 3050
Wire Wire Line
	3750 3350 3950 3350
Connection ~ 3950 3350
Wire Wire Line
	4850 3100 5050 3100
Wire Wire Line
	4900 3700 5100 3700
$EndSCHEMATC
