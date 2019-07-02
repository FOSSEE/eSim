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
LIBS:eSim_Miscellaneous
LIBS:eSim_Plot
LIBS:eSim_Power
LIBS:eSim_Sources
LIBS:eSim_Subckt
LIBS:eSim_User
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
L d_and U3
U 1 1 5AB62CE3
P 5050 2550
F 0 "U3" H 5050 2550 60  0000 C CNN
F 1 "d_and" H 5100 2650 60  0000 C CNN
F 2 "" H 5050 2550 60  0000 C CNN
F 3 "" H 5050 2550 60  0000 C CNN
	1    5050 2550
	1    0    0    -1  
$EndComp
$Comp
L d_and U4
U 1 1 5AB62D59
P 5050 3400
F 0 "U4" H 5050 3400 60  0000 C CNN
F 1 "d_and" H 5100 3500 60  0000 C CNN
F 2 "" H 5050 3400 60  0000 C CNN
F 3 "" H 5050 3400 60  0000 C CNN
	1    5050 3400
	1    0    0    -1  
$EndComp
$Comp
L d_or U5
U 1 1 5AB62DBD
P 6300 2950
F 0 "U5" H 6300 2950 60  0000 C CNN
F 1 "d_or" H 6300 3050 60  0000 C CNN
F 2 "" H 6300 2950 60  0000 C CNN
F 3 "" H 6300 2950 60  0000 C CNN
	1    6300 2950
	1    0    0    -1  
$EndComp
Wire Wire Line
	5500 2500 5550 2500
Wire Wire Line
	5550 2500 5550 2850
Wire Wire Line
	5550 2850 5850 2850
Wire Wire Line
	5500 3350 5550 3350
Wire Wire Line
	5550 3350 5550 2950
Wire Wire Line
	5550 2950 5850 2950
$Comp
L d_inverter U2
U 1 1 5AB62FFA
P 4200 2550
F 0 "U2" H 4200 2450 60  0000 C CNN
F 1 "d_inverter" H 4200 2700 60  0000 C CNN
F 2 "" H 4250 2500 60  0000 C CNN
F 3 "" H 4250 2500 60  0000 C CNN
	1    4200 2550
	1    0    0    -1  
$EndComp
Wire Wire Line
	4500 2550 4600 2550
$Comp
L PORT U1
U 1 1 5AB6307B
P 3450 3300
F 0 "U1" H 3500 3400 30  0000 C CNN
F 1 "PORT" H 3450 3300 30  0000 C CNN
F 2 "" H 3450 3300 60  0000 C CNN
F 3 "" H 3450 3300 60  0000 C CNN
	1    3450 3300
	1    0    0    -1  
$EndComp
Wire Wire Line
	3900 2550 3900 3300
Wire Wire Line
	3700 3300 4600 3300
Connection ~ 3900 3300
$Comp
L PORT U1
U 2 1 5AB631BF
P 4100 2050
F 0 "U1" H 4150 2150 30  0000 C CNN
F 1 "PORT" H 4100 2050 30  0000 C CNN
F 2 "" H 4100 2050 60  0000 C CNN
F 3 "" H 4100 2050 60  0000 C CNN
	2    4100 2050
	1    0    0    -1  
$EndComp
Wire Wire Line
	4350 2050 4600 2050
Wire Wire Line
	4600 2050 4600 2450
$Comp
L PORT U1
U 3 1 5AB6340B
P 4200 3850
F 0 "U1" H 4250 3950 30  0000 C CNN
F 1 "PORT" H 4200 3850 30  0000 C CNN
F 2 "" H 4200 3850 60  0000 C CNN
F 3 "" H 4200 3850 60  0000 C CNN
	3    4200 3850
	1    0    0    -1  
$EndComp
Wire Wire Line
	4600 3400 4600 3850
Wire Wire Line
	4600 3850 4450 3850
$Comp
L PORT U1
U 4 1 5AB63737
P 7100 2900
F 0 "U1" H 7150 3000 30  0000 C CNN
F 1 "PORT" H 7100 2900 30  0000 C CNN
F 2 "" H 7100 2900 60  0000 C CNN
F 3 "" H 7100 2900 60  0000 C CNN
	4    7100 2900
	-1   0    0    1   
$EndComp
Wire Wire Line
	6750 2900 6850 2900
$EndSCHEMATC
