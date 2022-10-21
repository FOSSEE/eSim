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
LIBS:cmos_buffer-cache
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
L mosfet_p M4
U 1 1 62DA98C4
P 5800 2950
F 0 "M4" H 5750 3000 50  0000 R CNN
F 1 "mosfet_p" H 5850 3100 50  0000 R CNN
F 2 "" H 6050 3050 29  0000 C CNN
F 3 "" H 5850 2950 60  0000 C CNN
	1    5800 2950
	1    0    0    1   
$EndComp
$Comp
L mosfet_n M3
U 1 1 62DA98C5
P 5750 3550
F 0 "M3" H 5750 3400 50  0000 R CNN
F 1 "mosfet_n" H 5850 3500 50  0000 R CNN
F 2 "" H 6050 3250 29  0000 C CNN
F 3 "" H 5850 3350 60  0000 C CNN
	1    5750 3550
	1    0    0    -1  
$EndComp
Wire Wire Line
	5950 2500 5950 2750
Wire Wire Line
	5950 2650 6050 2650
Wire Wire Line
	6050 2650 6050 2800
Connection ~ 5950 2650
Wire Wire Line
	5950 4200 5950 3950
Wire Wire Line
	6050 3900 6050 4100
Wire Wire Line
	6050 4100 5950 4100
Connection ~ 5950 4100
Wire Wire Line
	5650 2950 5650 3750
Wire Wire Line
	5950 3150 5950 3550
Wire Wire Line
	5950 3350 6050 3350
Connection ~ 5950 3350
Wire Wire Line
	5050 3350 5650 3350
Connection ~ 5650 3350
$Comp
L PORT U1
U 2 1 62DA98C6
P 5500 2050
F 0 "U1" H 5550 2150 30  0000 C CNN
F 1 "PORT" H 5500 2050 30  0000 C CNN
F 2 "" H 5500 2050 60  0000 C CNN
F 3 "" H 5500 2050 60  0000 C CNN
	2    5500 2050
	0    1    1    0   
$EndComp
$Comp
L PORT U1
U 3 1 62DA98C7
P 5500 4600
F 0 "U1" H 5550 4700 30  0000 C CNN
F 1 "PORT" H 5500 4600 30  0000 C CNN
F 2 "" H 5500 4600 60  0000 C CNN
F 3 "" H 5500 4600 60  0000 C CNN
	3    5500 4600
	0    -1   -1   0   
$EndComp
$Comp
L PORT U1
U 4 1 62DA98C8
P 6300 3350
F 0 "U1" H 6350 3450 30  0000 C CNN
F 1 "PORT" H 6300 3350 30  0000 C CNN
F 2 "" H 6300 3350 60  0000 C CNN
F 3 "" H 6300 3350 60  0000 C CNN
	4    6300 3350
	-1   0    0    1   
$EndComp
$Comp
L mosfet_p M2
U 1 1 62DA98C9
P 4900 2950
F 0 "M2" H 4850 3000 50  0000 R CNN
F 1 "mosfet_p" H 4950 3100 50  0000 R CNN
F 2 "" H 5150 3050 29  0000 C CNN
F 3 "" H 4950 2950 60  0000 C CNN
	1    4900 2950
	1    0    0    1   
$EndComp
$Comp
L mosfet_n M1
U 1 1 62DA98CA
P 4850 3550
F 0 "M1" H 4850 3400 50  0000 R CNN
F 1 "mosfet_n" H 4950 3500 50  0000 R CNN
F 2 "" H 5150 3250 29  0000 C CNN
F 3 "" H 4950 3350 60  0000 C CNN
	1    4850 3550
	1    0    0    -1  
$EndComp
Wire Wire Line
	5050 2500 5050 2750
Wire Wire Line
	5050 2650 5150 2650
Wire Wire Line
	5150 2650 5150 2800
Connection ~ 5050 2650
Wire Wire Line
	5050 3950 5050 4200
Wire Wire Line
	5150 3900 5150 4100
Wire Wire Line
	5150 4100 5050 4100
Connection ~ 5050 4100
Wire Wire Line
	4750 2950 4750 3750
Wire Wire Line
	5050 3150 5050 3550
Connection ~ 5050 3350
Wire Wire Line
	4750 3350 4600 3350
Connection ~ 4750 3350
$Comp
L PORT U1
U 1 1 62DA98CB
P 4350 3350
F 0 "U1" H 4400 3450 30  0000 C CNN
F 1 "PORT" H 4350 3350 30  0000 C CNN
F 2 "" H 4350 3350 60  0000 C CNN
F 3 "" H 4350 3350 60  0000 C CNN
	1    4350 3350
	1    0    0    -1  
$EndComp
Wire Wire Line
	5050 4200 5950 4200
Wire Wire Line
	5500 4350 5500 4200
Connection ~ 5500 4200
Wire Wire Line
	5050 2500 5950 2500
Wire Wire Line
	5500 2300 5500 2500
Connection ~ 5500 2500
$EndSCHEMATC
