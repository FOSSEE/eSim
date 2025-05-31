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
LIBS:c_origin-cache
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
L PORT U1
U 1 1 67F4E33E
P 2350 1300
F 0 "U1" H 2400 1400 30  0000 C CNN
F 1 "PORT" H 2350 1300 30  0000 C CNN
F 2 "" H 2350 1300 60  0000 C CNN
F 3 "" H 2350 1300 60  0000 C CNN
	1    2350 1300
	0    -1   1    0   
$EndComp
$Comp
L PORT U1
U 2 1 67F4E33F
P 3100 1300
F 0 "U1" H 3150 1400 30  0000 C CNN
F 1 "PORT" H 3100 1300 30  0000 C CNN
F 2 "" H 3100 1300 60  0000 C CNN
F 3 "" H 3100 1300 60  0000 C CNN
	2    3100 1300
	0    -1   1    0   
$EndComp
$Comp
L PORT U1
U 3 1 67F4E340
P 3850 1300
F 0 "U1" H 3900 1400 30  0000 C CNN
F 1 "PORT" H 3850 1300 30  0000 C CNN
F 2 "" H 3850 1300 60  0000 C CNN
F 3 "" H 3850 1300 60  0000 C CNN
	3    3850 1300
	0    -1   1    0   
$EndComp
$Comp
L PORT U1
U 4 1 67F4E341
P 4450 1300
F 0 "U1" H 4500 1400 30  0000 C CNN
F 1 "PORT" H 4450 1300 30  0000 C CNN
F 2 "" H 4450 1300 60  0000 C CNN
F 3 "" H 4450 1300 60  0000 C CNN
	4    4450 1300
	0    -1   1    0   
$EndComp
Text Label 2350 1650 3    60   ~ 0
w
Text Label 3100 1700 3    60   ~ 0
x
Text Label 3850 1700 3    60   ~ 0
y
Text Label 4450 1700 3    60   ~ 0
z
$Comp
L d_inverter U2
U 1 1 67F4E342
P 2600 2450
F 0 "U2" H 2600 2350 60  0000 C CNN
F 1 "d_inverter" H 2600 2600 60  0000 C CNN
F 2 "" H 2650 2400 60  0000 C CNN
F 3 "" H 2650 2400 60  0000 C CNN
	1    2600 2450
	0    1    1    0   
$EndComp
$Comp
L d_inverter U3
U 1 1 67F4E343
P 3450 2450
F 0 "U3" H 3450 2350 60  0000 C CNN
F 1 "d_inverter" H 3450 2600 60  0000 C CNN
F 2 "" H 3500 2400 60  0000 C CNN
F 3 "" H 3500 2400 60  0000 C CNN
	1    3450 2450
	0    1    1    0   
$EndComp
$Comp
L d_inverter U4
U 1 1 67F4E344
P 4100 2400
F 0 "U4" H 4100 2300 60  0000 C CNN
F 1 "d_inverter" H 4100 2550 60  0000 C CNN
F 2 "" H 4150 2350 60  0000 C CNN
F 3 "" H 4150 2350 60  0000 C CNN
	1    4100 2400
	0    1    1    0   
$EndComp
Wire Wire Line
	2350 2100 2600 2100
Wire Wire Line
	2600 2100 2600 2150
Connection ~ 2350 2100
Wire Wire Line
	3100 2100 3450 2100
Wire Wire Line
	3450 2100 3450 2150
Connection ~ 3100 2100
Wire Wire Line
	4100 2050 4100 2100
Connection ~ 4450 1950
Wire Wire Line
	3100 1550 3100 3800
Wire Wire Line
	2350 1550 2350 2100
Wire Wire Line
	3450 2900 5400 2900
Connection ~ 3450 2900
Wire Wire Line
	4100 3000 5400 3000
Connection ~ 4100 3000
Wire Wire Line
	3450 3200 5400 3200
Connection ~ 3450 3200
Wire Wire Line
	4450 3300 5400 3300
Connection ~ 4450 3300
Wire Wire Line
	2600 3700 5400 3700
Connection ~ 2600 3700
Wire Wire Line
	3100 3800 5400 3800
Wire Wire Line
	3450 3200 3450 2750
Wire Wire Line
	2600 3700 2600 2750
Wire Wire Line
	4100 3000 4100 2700
Wire Wire Line
	4450 3300 4450 1550
Wire Wire Line
	4100 2050 3850 2050
Wire Wire Line
	3850 2050 3850 1550
$Comp
L d_and U5
U 1 1 67F4E64B
P 5850 3000
F 0 "U5" H 5850 3000 60  0000 C CNN
F 1 "d_and" H 5900 3100 60  0000 C CNN
F 2 "" H 5850 3000 60  0000 C CNN
F 3 "" H 5850 3000 60  0000 C CNN
	1    5850 3000
	1    0    0    -1  
$EndComp
$Comp
L d_and U6
U 1 1 67F4E6B2
P 5850 3300
F 0 "U6" H 5850 3300 60  0000 C CNN
F 1 "d_and" H 5900 3400 60  0000 C CNN
F 2 "" H 5850 3300 60  0000 C CNN
F 3 "" H 5850 3300 60  0000 C CNN
	1    5850 3300
	1    0    0    -1  
$EndComp
$Comp
L d_and U7
U 1 1 67F4E707
P 5850 3800
F 0 "U7" H 5850 3800 60  0000 C CNN
F 1 "d_and" H 5900 3900 60  0000 C CNN
F 2 "" H 5850 3800 60  0000 C CNN
F 3 "" H 5850 3800 60  0000 C CNN
	1    5850 3800
	1    0    0    -1  
$EndComp
$Comp
L d_or U8
U 1 1 67F4E744
P 6750 3050
F 0 "U8" H 6750 3050 60  0000 C CNN
F 1 "d_or" H 6750 3150 60  0000 C CNN
F 2 "" H 6750 3050 60  0000 C CNN
F 3 "" H 6750 3050 60  0000 C CNN
	1    6750 3050
	1    0    0    -1  
$EndComp
Wire Wire Line
	6300 3050 6300 3250
$Comp
L d_or U9
U 1 1 67F4E7EF
P 7650 3100
F 0 "U9" H 7650 3100 60  0000 C CNN
F 1 "d_or" H 7650 3200 60  0000 C CNN
F 2 "" H 7650 3100 60  0000 C CNN
F 3 "" H 7650 3100 60  0000 C CNN
	1    7650 3100
	1    0    0    -1  
$EndComp
Wire Wire Line
	6300 3750 7200 3750
Wire Wire Line
	7200 3750 7200 3100
$Comp
L PORT U1
U 5 1 67F4E938
P 8350 3050
F 0 "U1" H 8400 3150 30  0000 C CNN
F 1 "PORT" H 8350 3050 30  0000 C CNN
F 2 "" H 8350 3050 60  0000 C CNN
F 3 "" H 8350 3050 60  0000 C CNN
	5    8350 3050
	-1   0    0    1   
$EndComp
$EndSCHEMATC
