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
LIBS:cmos_or-cache
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
L mosfet_p M2
U 1 1 62DA9496
P 4150 2400
F 0 "M2" H 4100 2450 50  0000 R CNN
F 1 "mosfet_p" H 4200 2550 50  0000 R CNN
F 2 "" H 4400 2500 29  0000 C CNN
F 3 "" H 4200 2400 60  0000 C CNN
	1    4150 2400
	1    0    0    1   
$EndComp
$Comp
L mosfet_p M3
U 1 1 62DA9497
P 4450 3150
F 0 "M3" H 4400 3200 50  0000 R CNN
F 1 "mosfet_p" H 4500 3300 50  0000 R CNN
F 2 "" H 4700 3250 29  0000 C CNN
F 3 "" H 4500 3150 60  0000 C CNN
	1    4450 3150
	-1   0    0    1   
$EndComp
$Comp
L mosfet_n M1
U 1 1 62DA9498
P 3650 3800
F 0 "M1" H 3650 3650 50  0000 R CNN
F 1 "mosfet_n" H 3750 3750 50  0000 R CNN
F 2 "" H 3950 3500 29  0000 C CNN
F 3 "" H 3750 3600 60  0000 C CNN
	1    3650 3800
	1    0    0    -1  
$EndComp
$Comp
L mosfet_n M4
U 1 1 62DA9499
P 4950 3800
F 0 "M4" H 4950 3650 50  0000 R CNN
F 1 "mosfet_n" H 5050 3750 50  0000 R CNN
F 2 "" H 5250 3500 29  0000 C CNN
F 3 "" H 5050 3600 60  0000 C CNN
	1    4950 3800
	-1   0    0    -1  
$EndComp
Wire Wire Line
	4300 2600 4300 2950
Wire Wire Line
	4300 3350 4300 3600
Wire Wire Line
	3850 3600 4750 3600
Wire Wire Line
	3850 3600 3850 3800
Wire Wire Line
	4750 3600 4750 3800
Connection ~ 4300 3600
Wire Wire Line
	4300 1850 4300 2200
Wire Wire Line
	4300 2150 4500 2150
Wire Wire Line
	4400 2150 4400 2250
Connection ~ 4300 2150
Wire Wire Line
	4200 3000 4200 2900
Wire Wire Line
	4200 2900 4500 2900
Wire Wire Line
	4500 2900 4500 2150
Connection ~ 4400 2150
Wire Wire Line
	3850 4200 3850 4350
Wire Wire Line
	4750 4350 3850 4350
Wire Wire Line
	4750 4200 4750 4350
Wire Wire Line
	3950 4150 3950 4250
Wire Wire Line
	3950 4250 3850 4250
Connection ~ 3850 4250
Wire Wire Line
	4650 4150 4650 4250
Wire Wire Line
	4650 4250 4750 4250
Connection ~ 4750 4250
Wire Wire Line
	4000 2400 3550 2400
Wire Wire Line
	3550 2400 3550 4000
Wire Wire Line
	4600 3150 5050 3150
Wire Wire Line
	5050 3150 5050 4000
Wire Wire Line
	5050 3550 5550 3550
Connection ~ 5050 3550
Wire Wire Line
	3550 3050 3100 3050
Connection ~ 3550 3050
Wire Wire Line
	4300 3450 4850 3450
Wire Wire Line
	4850 3450 4850 2900
Wire Wire Line
	4850 2900 6850 2900
Connection ~ 4300 3450
Wire Wire Line
	4300 4350 4300 4600
Connection ~ 4300 4350
$Comp
L PORT U1
U 1 1 62DA949A
P 2850 3050
F 0 "U1" H 2900 3150 30  0000 C CNN
F 1 "PORT" H 2850 3050 30  0000 C CNN
F 2 "" H 2850 3050 60  0000 C CNN
F 3 "" H 2850 3050 60  0000 C CNN
	1    2850 3050
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 2 1 62DA949B
P 5800 3550
F 0 "U1" H 5850 3650 30  0000 C CNN
F 1 "PORT" H 5800 3550 30  0000 C CNN
F 2 "" H 5800 3550 60  0000 C CNN
F 3 "" H 5800 3550 60  0000 C CNN
	2    5800 3550
	-1   0    0    1   
$EndComp
$Comp
L mosfet_p M6
U 1 1 62DA949C
P 7200 2500
F 0 "M6" H 7150 2550 50  0000 R CNN
F 1 "mosfet_p" H 7250 2650 50  0000 R CNN
F 2 "" H 7450 2600 29  0000 C CNN
F 3 "" H 7250 2500 60  0000 C CNN
	1    7200 2500
	1    0    0    1   
$EndComp
$Comp
L mosfet_n M5
U 1 1 62DA949D
P 7150 3100
F 0 "M5" H 7150 2950 50  0000 R CNN
F 1 "mosfet_n" H 7250 3050 50  0000 R CNN
F 2 "" H 7450 2800 29  0000 C CNN
F 3 "" H 7250 2900 60  0000 C CNN
	1    7150 3100
	1    0    0    -1  
$EndComp
Wire Wire Line
	7350 1850 7350 2300
Wire Wire Line
	7350 2100 7450 2100
Wire Wire Line
	7450 2100 7450 2350
Connection ~ 7350 2100
Wire Wire Line
	7350 4600 7350 3500
Wire Wire Line
	7450 3450 7450 3650
Wire Wire Line
	7450 3650 7350 3650
Connection ~ 7350 3650
Wire Wire Line
	7050 2500 6850 2500
Wire Wire Line
	6850 2500 6850 3300
Wire Wire Line
	6850 3300 7050 3300
Wire Wire Line
	7350 2700 7350 3100
Wire Wire Line
	7350 2900 7950 2900
Connection ~ 7350 2900
Connection ~ 6850 2900
$Comp
L PORT U1
U 5 1 62DA949E
P 8200 2900
F 0 "U1" H 8250 3000 30  0000 C CNN
F 1 "PORT" H 8200 2900 30  0000 C CNN
F 2 "" H 8200 2900 60  0000 C CNN
F 3 "" H 8200 2900 60  0000 C CNN
	5    8200 2900
	-1   0    0    1   
$EndComp
Wire Wire Line
	7350 1850 4300 1850
Wire Wire Line
	4300 4600 7350 4600
Wire Wire Line
	5800 4600 5800 5100
Connection ~ 5800 4600
Wire Wire Line
	5850 1850 5850 1450
Connection ~ 5850 1850
$Comp
L PORT U1
U 4 1 62DA949F
P 5850 1200
F 0 "U1" H 5900 1300 30  0000 C CNN
F 1 "PORT" H 5850 1200 30  0000 C CNN
F 2 "" H 5850 1200 60  0000 C CNN
F 3 "" H 5850 1200 60  0000 C CNN
	4    5850 1200
	0    1    1    0   
$EndComp
$Comp
L PORT U1
U 3 1 62DA94A0
P 5800 5350
F 0 "U1" H 5850 5450 30  0000 C CNN
F 1 "PORT" H 5800 5350 30  0000 C CNN
F 2 "" H 5800 5350 60  0000 C CNN
F 3 "" H 5800 5350 60  0000 C CNN
	3    5800 5350
	0    -1   -1   0   
$EndComp
$EndSCHEMATC
