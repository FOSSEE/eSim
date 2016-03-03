EESchema Schematic File Version 2
LIBS:eSim_Analog
LIBS:eSim_Devices
LIBS:eSim_Digital
LIBS:eSim_Hybrid
LIBS:eSim_Miscellaneous
LIBS:eSim_Plot
LIBS:eSim_Power
LIBS:eSim_Sources
LIBS:eSim_Subckt
LIBS:eSim_User
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
LIBS:FET_Characteristic-cache
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
L NJF J1
U 1 1 56C45BB2
P 5700 3300
F 0 "J1" H 5600 3350 50  0000 R CNN
F 1 "NJF" H 5650 3450 50  0000 R CNN
F 2 "" H 5900 3400 29  0000 C CNN
F 3 "" H 5700 3300 60  0000 C CNN
	1    5700 3300
	1    0    0    -1  
$EndComp
$Comp
L DC vds1
U 1 1 56C45C58
P 7200 3300
F 0 "vds1" H 7000 3400 60  0000 C CNN
F 1 "DC" H 7000 3250 60  0000 C CNN
F 2 "R1" H 6900 3300 60  0000 C CNN
F 3 "" H 7200 3300 60  0000 C CNN
	1    7200 3300
	1    0    0    -1  
$EndComp
$Comp
L DC vgs1
U 1 1 56C45CAD
P 4450 3800
F 0 "vgs1" H 4250 3900 60  0000 C CNN
F 1 "DC" H 4250 3750 60  0000 C CNN
F 2 "R1" H 4150 3800 60  0000 C CNN
F 3 "" H 4450 3800 60  0000 C CNN
	1    4450 3800
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR01
U 1 1 56C45DD7
P 5800 4300
F 0 "#PWR01" H 5800 4050 50  0001 C CNN
F 1 "GND" H 5800 4150 50  0000 C CNN
F 2 "" H 5800 4300 50  0000 C CNN
F 3 "" H 5800 4300 50  0000 C CNN
	1    5800 4300
	1    0    0    -1  
$EndComp
Wire Wire Line
	5500 3300 4450 3300
Wire Wire Line
	4450 3300 4450 3350
Wire Wire Line
	4450 4250 7200 4250
Wire Wire Line
	7200 4250 7200 3750
Wire Wire Line
	5800 3500 5800 4300
Connection ~ 5800 4250
Wire Wire Line
	5800 3100 5800 2200
Wire Wire Line
	5800 2200 6450 2200
Wire Wire Line
	7050 2200 7200 2200
Wire Wire Line
	7200 2200 7200 2850
$Comp
L plot_i2 U_id1
U 1 1 56D85998
P 6750 2450
F 0 "U_id1" H 6750 2850 60  0000 C CNN
F 1 "plot_i2" H 6750 2550 60  0000 C CNN
F 2 "" H 6750 2450 60  0000 C CNN
F 3 "" H 6750 2450 60  0000 C CNN
	1    6750 2450
	-1   0    0    -1  
$EndComp
Text GLabel 6150 2100 1    60   Input ~ 0
id
Wire Wire Line
	6150 2100 6150 2200
Connection ~ 6150 2200
$EndSCHEMATC
