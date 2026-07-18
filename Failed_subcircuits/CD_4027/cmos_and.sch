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
LIBS:cmos_and-cache
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
U 1 1 62DA96A4
P 3450 2700
F 0 "M1" H 3400 2750 50  0000 R CNN
F 1 "mosfet_p" H 3500 2850 50  0000 R CNN
F 2 "" H 3700 2800 29  0000 C CNN
F 3 "" H 3500 2700 60  0000 C CNN
	1    3450 2700
	1    0    0    1   
$EndComp
$Comp
L mosfet_p M4
U 1 1 62DA96A5
P 4400 2700
F 0 "M4" H 4350 2750 50  0000 R CNN
F 1 "mosfet_p" H 4450 2850 50  0000 R CNN
F 2 "" H 4650 2800 29  0000 C CNN
F 3 "" H 4450 2700 60  0000 C CNN
	1    4400 2700
	-1   0    0    1   
$EndComp
$Comp
L mosfet_n M2
U 1 1 62DA96A6
P 3750 3200
F 0 "M2" H 3750 3050 50  0000 R CNN
F 1 "mosfet_n" H 3850 3150 50  0000 R CNN
F 2 "" H 4050 2900 29  0000 C CNN
F 3 "" H 3850 3000 60  0000 C CNN
	1    3750 3200
	1    0    0    -1  
$EndComp
$Comp
L mosfet_n M3
U 1 1 62DA96A7
P 4150 3700
F 0 "M3" H 4150 3550 50  0000 R CNN
F 1 "mosfet_n" H 4250 3650 50  0000 R CNN
F 2 "" H 4450 3400 29  0000 C CNN
F 3 "" H 4250 3500 60  0000 C CNN
	1    4150 3700
	-1   0    0    -1  
$EndComp
Wire Wire Line
	3600 2900 3600 3000
Wire Wire Line
	3600 3000 4250 3000
Wire Wire Line
	4250 3000 4250 2900
Wire Wire Line
	3950 3000 3950 3200
Connection ~ 3950 3000
Wire Wire Line
	3950 3600 3950 3700
Wire Wire Line
	3950 4100 3950 4400
Wire Wire Line
	3850 4050 3850 4200
Wire Wire Line
	3750 4200 3950 4200
Connection ~ 3950 4200
Wire Wire Line
	4050 3550 4050 3650
Wire Wire Line
	4050 3650 3750 3650
Wire Wire Line
	3750 3650 3750 4200
Connection ~ 3850 4200
Wire Wire Line
	3600 2500 3600 2350
Wire Wire Line
	3600 2350 4250 2350
Wire Wire Line
	4250 2350 4250 2500
Wire Wire Line
	3700 2550 3700 2350
Connection ~ 3700 2350
Wire Wire Line
	4150 2550 4150 2350
Connection ~ 4150 2350
Wire Wire Line
	3950 2350 3950 2050
Connection ~ 3950 2350
Wire Wire Line
	3300 2700 3300 3400
Wire Wire Line
	3300 3400 3650 3400
Wire Wire Line
	4550 2700 4550 3900
Wire Wire Line
	4550 3900 4250 3900
Wire Wire Line
	4550 3300 5200 3300
Connection ~ 4550 3300
Wire Wire Line
	3300 3000 2950 3000
Connection ~ 3300 3000
Wire Wire Line
	3950 3100 5950 3100
Connection ~ 3950 3100
$Comp
L PORT U1
U 1 1 62DA96A8
P 2700 3000
F 0 "U1" H 2750 3100 30  0000 C CNN
F 1 "PORT" H 2700 3000 30  0000 C CNN
F 2 "" H 2700 3000 60  0000 C CNN
F 3 "" H 2700 3000 60  0000 C CNN
	1    2700 3000
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 4 1 62DA96A9
P 5450 3300
F 0 "U1" H 5500 3400 30  0000 C CNN
F 1 "PORT" H 5450 3300 30  0000 C CNN
F 2 "" H 5450 3300 60  0000 C CNN
F 3 "" H 5450 3300 60  0000 C CNN
	4    5450 3300
	-1   0    0    1   
$EndComp
$Comp
L mosfet_p M6
U 1 1 62DA96AA
P 6300 2700
F 0 "M6" H 6250 2750 50  0000 R CNN
F 1 "mosfet_p" H 6350 2850 50  0000 R CNN
F 2 "" H 6550 2800 29  0000 C CNN
F 3 "" H 6350 2700 60  0000 C CNN
	1    6300 2700
	1    0    0    1   
$EndComp
$Comp
L mosfet_n M5
U 1 1 62DA96AB
P 6250 3300
F 0 "M5" H 6250 3150 50  0000 R CNN
F 1 "mosfet_n" H 6350 3250 50  0000 R CNN
F 2 "" H 6550 3000 29  0000 C CNN
F 3 "" H 6350 3100 60  0000 C CNN
	1    6250 3300
	1    0    0    -1  
$EndComp
Wire Wire Line
	6450 2050 6450 2500
Wire Wire Line
	6450 2300 6550 2300
Wire Wire Line
	6550 2300 6550 2550
Connection ~ 6450 2300
Wire Wire Line
	6450 4400 6450 3700
Wire Wire Line
	6550 3650 6550 3850
Wire Wire Line
	6550 3850 6450 3850
Connection ~ 6450 3850
Wire Wire Line
	6150 2700 5950 2700
Wire Wire Line
	5950 2700 5950 3500
Wire Wire Line
	5950 3500 6150 3500
Wire Wire Line
	6450 2900 6450 3300
Wire Wire Line
	6450 3100 7050 3100
Connection ~ 6450 3100
Connection ~ 5950 3100
$Comp
L PORT U1
U 5 1 62DA96AC
P 7300 3100
F 0 "U1" H 7350 3200 30  0000 C CNN
F 1 "PORT" H 7300 3100 30  0000 C CNN
F 2 "" H 7300 3100 60  0000 C CNN
F 3 "" H 7300 3100 60  0000 C CNN
	5    7300 3100
	-1   0    0    1   
$EndComp
$Comp
L PORT U1
U 2 1 62DA96AD
P 5150 5050
F 0 "U1" H 5200 5150 30  0000 C CNN
F 1 "PORT" H 5150 5050 30  0000 C CNN
F 2 "" H 5150 5050 60  0000 C CNN
F 3 "" H 5150 5050 60  0000 C CNN
	2    5150 5050
	0    -1   -1   0   
$EndComp
$Comp
L PORT U1
U 3 1 62DA96AE
P 5250 1350
F 0 "U1" H 5300 1450 30  0000 C CNN
F 1 "PORT" H 5250 1350 30  0000 C CNN
F 2 "" H 5250 1350 60  0000 C CNN
F 3 "" H 5250 1350 60  0000 C CNN
	3    5250 1350
	0    1    1    0   
$EndComp
Wire Wire Line
	3950 2050 6450 2050
Wire Wire Line
	3950 4400 6450 4400
Wire Wire Line
	5150 4800 5150 4400
Connection ~ 5150 4400
Wire Wire Line
	5250 1600 5250 2050
Connection ~ 5250 2050
$EndSCHEMATC
