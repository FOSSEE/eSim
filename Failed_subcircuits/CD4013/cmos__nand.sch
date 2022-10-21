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
LIBS:cmos__nand-cache
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
L mosfet_p M1
U 1 1 62DA9263
P 5400 2750
F 0 "M1" H 5350 2800 50  0000 R CNN
F 1 "mosfet_p" H 5450 2900 50  0000 R CNN
F 2 "" H 5650 2850 29  0000 C CNN
F 3 "" H 5450 2750 60  0000 C CNN
	1    5400 2750
	1    0    0    1   
$EndComp
$Comp
L mosfet_p M4
U 1 1 62DA9264
P 6350 2750
F 0 "M4" H 6300 2800 50  0000 R CNN
F 1 "mosfet_p" H 6400 2900 50  0000 R CNN
F 2 "" H 6600 2850 29  0000 C CNN
F 3 "" H 6400 2750 60  0000 C CNN
	1    6350 2750
	-1   0    0    1   
$EndComp
$Comp
L mosfet_n M2
U 1 1 62DA9265
P 5700 3250
F 0 "M2" H 5700 3100 50  0000 R CNN
F 1 "mosfet_n" H 5800 3200 50  0000 R CNN
F 2 "" H 6000 2950 29  0000 C CNN
F 3 "" H 5800 3050 60  0000 C CNN
	1    5700 3250
	1    0    0    -1  
$EndComp
$Comp
L mosfet_n M3
U 1 1 62DA9266
P 6100 3750
F 0 "M3" H 6100 3600 50  0000 R CNN
F 1 "mosfet_n" H 6200 3700 50  0000 R CNN
F 2 "" H 6400 3450 29  0000 C CNN
F 3 "" H 6200 3550 60  0000 C CNN
	1    6100 3750
	-1   0    0    -1  
$EndComp
Wire Wire Line
	5550 2950 5550 3050
Wire Wire Line
	5550 3050 6200 3050
Wire Wire Line
	6200 3050 6200 2950
Wire Wire Line
	5900 3050 5900 3250
Connection ~ 5900 3050
Wire Wire Line
	5900 3650 5900 3750
Wire Wire Line
	5900 4150 5900 4450
Wire Wire Line
	5800 4100 5800 4250
Wire Wire Line
	5700 4250 5900 4250
Connection ~ 5900 4250
Wire Wire Line
	6000 3600 6000 3700
Wire Wire Line
	6000 3700 5700 3700
Wire Wire Line
	5700 3700 5700 4250
Connection ~ 5800 4250
Wire Wire Line
	5550 2550 5550 2400
Wire Wire Line
	5550 2400 6200 2400
Wire Wire Line
	6200 2400 6200 2550
Wire Wire Line
	5650 2600 5650 2400
Connection ~ 5650 2400
Wire Wire Line
	6100 2600 6100 2400
Connection ~ 6100 2400
Wire Wire Line
	5900 2400 5900 2200
Connection ~ 5900 2400
Wire Wire Line
	5250 2750 5250 3450
Wire Wire Line
	5250 3450 5600 3450
Wire Wire Line
	6500 2750 6500 3950
Wire Wire Line
	6500 3950 6200 3950
Wire Wire Line
	6500 3350 7150 3350
Connection ~ 6500 3350
Wire Wire Line
	5250 3050 4900 3050
Connection ~ 5250 3050
Wire Wire Line
	5900 3150 6800 3150
Connection ~ 5900 3150
$Comp
L PORT U1
U 1 1 62DA9267
P 4650 3050
F 0 "U1" H 4700 3150 30  0000 C CNN
F 1 "PORT" H 4650 3050 30  0000 C CNN
F 2 "" H 4650 3050 60  0000 C CNN
F 3 "" H 4650 3050 60  0000 C CNN
	1    4650 3050
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 2 1 62DA9268
P 5900 1950
F 0 "U1" H 5950 2050 30  0000 C CNN
F 1 "PORT" H 5900 1950 30  0000 C CNN
F 2 "" H 5900 1950 60  0000 C CNN
F 3 "" H 5900 1950 60  0000 C CNN
	2    5900 1950
	0    1    1    0   
$EndComp
$Comp
L PORT U1
U 3 1 62DA9269
P 5900 4700
F 0 "U1" H 5950 4800 30  0000 C CNN
F 1 "PORT" H 5900 4700 30  0000 C CNN
F 2 "" H 5900 4700 60  0000 C CNN
F 3 "" H 5900 4700 60  0000 C CNN
	3    5900 4700
	0    -1   -1   0   
$EndComp
$Comp
L PORT U1
U 5 1 62DA926A
P 7400 3350
F 0 "U1" H 7450 3450 30  0000 C CNN
F 1 "PORT" H 7400 3350 30  0000 C CNN
F 2 "" H 7400 3350 60  0000 C CNN
F 3 "" H 7400 3350 60  0000 C CNN
	5    7400 3350
	-1   0    0    1   
$EndComp
$Comp
L PORT U1
U 4 1 62DA926B
P 7050 3150
F 0 "U1" H 7100 3250 30  0000 C CNN
F 1 "PORT" H 7050 3150 30  0000 C CNN
F 2 "" H 7050 3150 60  0000 C CNN
F 3 "" H 7050 3150 60  0000 C CNN
	4    7050 3150
	-1   0    0    1   
$EndComp
$EndSCHEMATC
