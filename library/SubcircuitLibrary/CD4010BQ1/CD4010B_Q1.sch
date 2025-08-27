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
LIBS:CD4010B_Q1-cache
LIBS:CD4010B-cache
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
U 1 1 6852B46F
P 4000 2750
F 0 "M2" H 3950 2800 50  0000 R CNN
F 1 "mosfet_p" H 4050 2900 50  0000 R CNN
F 2 "" H 4250 2850 29  0000 C CNN
F 3 "" H 4050 2750 60  0000 C CNN
	1    4000 2750
	1    0    0    -1  
$EndComp
$Comp
L mosfet_n M1
U 1 1 6852B470
P 3950 3450
F 0 "M1" H 3950 3300 50  0000 R CNN
F 1 "mosfet_n" H 4050 3400 50  0000 R CNN
F 2 "" H 4250 3150 29  0000 C CNN
F 3 "" H 4050 3250 60  0000 C CNN
	1    3950 3450
	1    0    0    -1  
$EndComp
$Comp
L mosfet_p M5
U 1 1 6852B471
P 5750 2700
F 0 "M5" H 5700 2750 50  0000 R CNN
F 1 "mosfet_p" H 5800 2850 50  0000 R CNN
F 2 "" H 6000 2800 29  0000 C CNN
F 3 "" H 5800 2700 60  0000 C CNN
	1    5750 2700
	1    0    0    -1  
$EndComp
$Comp
L mosfet_n M4
U 1 1 6852B472
P 4850 3500
F 0 "M4" H 4850 3350 50  0000 R CNN
F 1 "mosfet_n" H 4950 3450 50  0000 R CNN
F 2 "" H 5150 3200 29  0000 C CNN
F 3 "" H 4950 3300 60  0000 C CNN
	1    4850 3500
	1    0    0    -1  
$EndComp
$Comp
L mosfet_n M3
U 1 1 6852B473
P 4850 2550
F 0 "M3" H 4850 2400 50  0000 R CNN
F 1 "mosfet_n" H 4950 2500 50  0000 R CNN
F 2 "" H 5150 2250 29  0000 C CNN
F 3 "" H 4950 2350 60  0000 C CNN
	1    4850 2550
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 1 1 6852B69C
P 2400 3300
F 0 "U1" H 2450 3400 30  0000 C CNN
F 1 "PORT" H 2400 3300 30  0000 C CNN
F 2 "" H 2400 3300 60  0000 C CNN
F 3 "" H 2400 3300 60  0000 C CNN
	1    2400 3300
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 5 1 6852B759
P 4850 4200
F 0 "U1" H 4900 4300 30  0000 C CNN
F 1 "PORT" H 4850 4200 30  0000 C CNN
F 2 "" H 4850 4200 60  0000 C CNN
F 3 "" H 4850 4200 60  0000 C CNN
	5    4850 4200
	-1   0    0    1   
$EndComp
$Comp
L PORT U1
U 4 1 6852B7E3
P 3300 1800
F 0 "U1" H 3350 1900 30  0000 C CNN
F 1 "PORT" H 3300 1800 30  0000 C CNN
F 2 "" H 3300 1800 60  0000 C CNN
F 3 "" H 3300 1800 60  0000 C CNN
	4    3300 1800
	0    -1   -1   0   
$EndComp
$Comp
L PORT U1
U 2 1 6852B9FE
P 7100 3050
F 0 "U1" H 7150 3150 30  0000 C CNN
F 1 "PORT" H 7100 3050 30  0000 C CNN
F 2 "" H 7100 3050 60  0000 C CNN
F 3 "" H 7100 3050 60  0000 C CNN
	2    7100 3050
	-1   0    0    1   
$EndComp
$Comp
L PORT U1
U 3 1 6852BB2C
P 5500 1300
F 0 "U1" H 5550 1400 30  0000 C CNN
F 1 "PORT" H 5500 1300 30  0000 C CNN
F 2 "" H 5500 1300 60  0000 C CNN
F 3 "" H 5500 1300 60  0000 C CNN
	3    5500 1300
	0    -1   -1   0   
$EndComp
Wire Wire Line
	4150 2950 4150 3450
Wire Wire Line
	4250 2900 4350 2900
Wire Wire Line
	4350 2900 4350 2550
Wire Wire Line
	4350 2550 4150 2550
Wire Wire Line
	5050 2950 5050 3500
Wire Wire Line
	5150 4050 5150 3850
Wire Wire Line
	4150 4050 5150 4050
Wire Wire Line
	5050 4050 5050 3900
Wire Wire Line
	6000 2850 6200 2850
Wire Wire Line
	6200 2850 6200 2300
Wire Wire Line
	6200 2300 4150 2300
Wire Wire Line
	4150 2550 4150 1550
Wire Wire Line
	4150 3850 4150 4050
Wire Wire Line
	4250 4050 4250 3800
Connection ~ 5050 4050
Connection ~ 4250 4050
Wire Wire Line
	3850 2750 3500 2750
Wire Wire Line
	3500 2750 3500 3650
Wire Wire Line
	3500 3650 3850 3650
Wire Wire Line
	4150 1550 3300 1550
Connection ~ 4150 2300
Wire Wire Line
	5900 2500 5900 1050
Wire Wire Line
	5900 1050 5500 1050
Wire Wire Line
	4150 3250 5600 3250
Wire Wire Line
	4700 3250 4700 3700
Wire Wire Line
	4700 3700 4750 3700
Connection ~ 4150 3250
Wire Wire Line
	5600 3250 5600 2700
Connection ~ 4700 3250
Wire Wire Line
	4750 2750 4750 3150
Wire Wire Line
	4750 3150 3500 3150
Connection ~ 3500 3150
Wire Wire Line
	5050 2550 5050 2150
Wire Wire Line
	5050 2150 5900 2150
Connection ~ 5900 2150
Wire Wire Line
	5150 2900 5150 3050
Wire Wire Line
	5050 3050 6850 3050
Connection ~ 5050 3050
Wire Wire Line
	5900 3050 5900 2900
Connection ~ 5150 3050
Wire Wire Line
	2650 3300 3500 3300
Connection ~ 3500 3300
Connection ~ 5900 3050
Connection ~ 4600 4050
Wire Wire Line
	4600 4200 4600 4050
$EndSCHEMATC
