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
LIBS:74V1G14-cache
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
L mosfet_n M1
U 1 1 62E8D877
P 3550 3950
F 0 "M1" H 3550 3800 50  0000 R CNN
F 1 "mosfet_n" H 3650 3900 50  0000 R CNN
F 2 "" H 3850 3650 29  0000 C CNN
F 3 "" H 3650 3750 60  0000 C CNN
	1    3550 3950
	1    0    0    -1  
$EndComp
$Comp
L mosfet_n M2
U 1 1 62E8D878
P 3550 5300
F 0 "M2" H 3550 5150 50  0000 R CNN
F 1 "mosfet_n" H 3650 5250 50  0000 R CNN
F 2 "" H 3850 5000 29  0000 C CNN
F 3 "" H 3650 5100 60  0000 C CNN
	1    3550 5300
	1    0    0    -1  
$EndComp
$Comp
L mosfet_p M3
U 1 1 62E8D879
P 3650 1600
F 0 "M3" H 3600 1650 50  0000 R CNN
F 1 "mosfet_p" H 3700 1750 50  0000 R CNN
F 2 "" H 3900 1700 29  0000 C CNN
F 3 "" H 3700 1600 60  0000 C CNN
	1    3650 1600
	1    0    0    -1  
$EndComp
$Comp
L mosfet_p M4
U 1 1 62E8D87A
P 3650 2650
F 0 "M4" H 3600 2700 50  0000 R CNN
F 1 "mosfet_p" H 3700 2800 50  0000 R CNN
F 2 "" H 3900 2750 29  0000 C CNN
F 3 "" H 3700 2650 60  0000 C CNN
	1    3650 2650
	1    0    0    -1  
$EndComp
$Comp
L mosfet_p M5
U 1 1 62E8D87B
P 7250 2100
F 0 "M5" H 7200 2150 50  0000 R CNN
F 1 "mosfet_p" H 7300 2250 50  0000 R CNN
F 2 "" H 7500 2200 29  0000 C CNN
F 3 "" H 7300 2100 60  0000 C CNN
	1    7250 2100
	0    1    -1   0   
$EndComp
$Comp
L mosfet_n M6
U 1 1 62E8D87C
P 7450 4850
F 0 "M6" H 7450 4700 50  0000 R CNN
F 1 "mosfet_n" H 7550 4800 50  0000 R CNN
F 2 "" H 7750 4550 29  0000 C CNN
F 3 "" H 7550 4650 60  0000 C CNN
	1    7450 4850
	0    1    1    0   
$EndComp
Wire Wire Line
	3800 1800 3800 2450
Wire Wire Line
	3800 2850 3800 3950
Wire Wire Line
	3800 3950 3750 3950
Wire Wire Line
	3750 4350 3750 5300
Wire Wire Line
	7050 1950 3800 1950
Connection ~ 3800 1950
Wire Wire Line
	7100 1750 7100 1850
Wire Wire Line
	3800 850  3800 1400
Wire Wire Line
	3800 1300 4550 1300
Wire Wire Line
	4550 1300 4550 2900
Wire Wire Line
	4550 2900 3900 2900
Wire Wire Line
	3900 2900 3900 2800
Connection ~ 3800 1300
Wire Wire Line
	3900 1750 7100 1750
Connection ~ 4550 1750
Wire Wire Line
	3750 5700 3750 6200
Wire Wire Line
	3850 5650 3850 5850
Wire Wire Line
	3850 5850 3750 5850
Connection ~ 3750 5850
Wire Wire Line
	3850 5700 4150 5700
Wire Wire Line
	4150 5700 4150 4300
Wire Wire Line
	4150 4300 3850 4300
Connection ~ 3850 5700
Wire Wire Line
	4150 5250 7100 5250
Wire Wire Line
	7100 5250 7100 5150
Connection ~ 4150 5250
Wire Wire Line
	7050 5050 3750 5050
Connection ~ 3750 5050
Wire Wire Line
	7450 5050 9450 5050
Wire Wire Line
	3800 3350 9200 3350
Connection ~ 3800 3350
Wire Wire Line
	2750 1600 2750 5500
Wire Wire Line
	2750 5500 3450 5500
Wire Wire Line
	3500 2650 3500 2550
Wire Wire Line
	3500 2550 2750 2550
Connection ~ 2750 2550
Connection ~ 2750 4150
Wire Wire Line
	2100 3300 2750 3300
Connection ~ 2750 3300
Wire Wire Line
	7450 1950 9700 1950
Wire Wire Line
	9700 1950 9700 6050
Wire Wire Line
	9700 6050 3750 6050
Connection ~ 3750 6050
Wire Wire Line
	3500 1600 2750 1600
Wire Wire Line
	3450 4150 2750 4150
Wire Wire Line
	3600 850  9450 850 
Wire Wire Line
	9450 850  9450 5050
Connection ~ 3800 850 
Text Label 3600 850  0    60   ~ 0
Vcc
Text Label 9100 3350 0    60   ~ 0
Vout
Text Label 3750 6150 0    60   ~ 0
GND
Text Label 2300 3300 0    60   ~ 0
Inp
Text Label 2300 4100 0    60   ~ 0
NC
NoConn ~ 2300 4100
$Comp
L PORT U1
U 2 1 62E8E2E7
P 1850 3300
F 0 "U1" H 1900 3400 30  0000 C CNN
F 1 "PORT" H 1850 3300 30  0000 C CNN
F 2 "" H 1850 3300 60  0000 C CNN
F 3 "" H 1850 3300 60  0000 C CNN
	2    1850 3300
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 1 1 62E8E33C
P 2050 4100
F 0 "U1" H 2100 4200 30  0000 C CNN
F 1 "PORT" H 2050 4100 30  0000 C CNN
F 2 "" H 2050 4100 60  0000 C CNN
F 3 "" H 2050 4100 60  0000 C CNN
	1    2050 4100
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 4 1 62E8E47F
P 9450 3350
F 0 "U1" H 9500 3450 30  0000 C CNN
F 1 "PORT" H 9450 3350 30  0000 C CNN
F 2 "" H 9450 3350 60  0000 C CNN
F 3 "" H 9450 3350 60  0000 C CNN
	4    9450 3350
	-1   0    0    1   
$EndComp
$Comp
L PORT U1
U 5 1 62E8E9EE
P 3350 850
F 0 "U1" H 3400 950 30  0000 C CNN
F 1 "PORT" H 3350 850 30  0000 C CNN
F 2 "" H 3350 850 60  0000 C CNN
F 3 "" H 3350 850 60  0000 C CNN
	5    3350 850 
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 3 1 62E8ECBB
P 3500 6200
F 0 "U1" H 3550 6300 30  0000 C CNN
F 1 "PORT" H 3500 6200 30  0000 C CNN
F 2 "" H 3500 6200 60  0000 C CNN
F 3 "" H 3500 6200 60  0000 C CNN
	3    3500 6200
	1    0    0    -1  
$EndComp
Wire Wire Line
	7250 2250 6900 2250
Wire Wire Line
	6900 2250 6900 3350
Connection ~ 6900 3350
Wire Wire Line
	7250 4750 7250 3350
Connection ~ 7250 3350
$EndSCHEMATC
