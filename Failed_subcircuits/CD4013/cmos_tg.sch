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
LIBS:cmos_tg-cache
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
U 1 1 62DA99E3
P 5850 2700
F 0 "M2" H 5800 2750 50  0000 R CNN
F 1 "mosfet_p" H 5900 2850 50  0000 R CNN
F 2 "" H 6100 2800 29  0000 C CNN
F 3 "" H 5900 2700 60  0000 C CNN
	1    5850 2700
	0    1    1    0   
$EndComp
$Comp
L mosfet_n M1
U 1 1 62DA99E4
P 5650 3850
F 0 "M1" H 5650 3700 50  0000 R CNN
F 1 "mosfet_n" H 5750 3800 50  0000 R CNN
F 2 "" H 5950 3550 29  0000 C CNN
F 3 "" H 5750 3650 60  0000 C CNN
	1    5650 3850
	0    -1   -1   0   
$EndComp
Wire Wire Line
	5400 3650 5650 3650
Wire Wire Line
	5400 2850 5400 3650
Wire Wire Line
	5400 2850 5650 2850
Wire Wire Line
	6300 3650 6050 3650
Wire Wire Line
	6300 2850 6300 3650
Wire Wire Line
	6300 2850 6050 2850
Wire Wire Line
	6300 3250 6500 3250
Connection ~ 6300 3250
Wire Wire Line
	5400 3200 5200 3200
Connection ~ 5400 3200
Wire Wire Line
	5850 2550 5850 2350
Wire Wire Line
	5850 3950 5850 4200
$Comp
L GND #PWR1
U 1 1 62DA99E5
P 6150 3550
F 0 "#PWR1" H 6150 3300 50  0001 C CNN
F 1 "GND" H 6150 3400 50  0000 C CNN
F 2 "" H 6150 3550 50  0001 C CNN
F 3 "" H 6150 3550 50  0001 C CNN
	1    6150 3550
	-1   0    0    1   
$EndComp
Wire Wire Line
	6150 3550 6000 3550
Wire Wire Line
	5700 2950 5550 2950
Wire Wire Line
	5550 2950 5550 4000
Wire Wire Line
	5550 4000 5850 4000
Connection ~ 5850 4000
$Comp
L PORT U1
U 1 1 62DA99E6
P 4950 3200
F 0 "U1" H 5000 3300 30  0000 C CNN
F 1 "PORT" H 4950 3200 30  0000 C CNN
F 2 "" H 4950 3200 60  0000 C CNN
F 3 "" H 4950 3200 60  0000 C CNN
	1    4950 3200
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 2 1 62DA99E7
P 5850 2100
F 0 "U1" H 5900 2200 30  0000 C CNN
F 1 "PORT" H 5850 2100 30  0000 C CNN
F 2 "" H 5850 2100 60  0000 C CNN
F 3 "" H 5850 2100 60  0000 C CNN
	2    5850 2100
	0    1    1    0   
$EndComp
$Comp
L PORT U1
U 3 1 62DA99E8
P 5850 4450
F 0 "U1" H 5900 4550 30  0000 C CNN
F 1 "PORT" H 5850 4450 30  0000 C CNN
F 2 "" H 5850 4450 60  0000 C CNN
F 3 "" H 5850 4450 60  0000 C CNN
	3    5850 4450
	0    -1   -1   0   
$EndComp
$Comp
L PORT U1
U 4 1 62DA99E9
P 6750 3250
F 0 "U1" H 6800 3350 30  0000 C CNN
F 1 "PORT" H 6750 3250 30  0000 C CNN
F 2 "" H 6750 3250 60  0000 C CNN
F 3 "" H 6750 3250 60  0000 C CNN
	4    6750 3250
	-1   0    0    1   
$EndComp
$EndSCHEMATC
