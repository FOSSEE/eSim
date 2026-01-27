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
LIBS:device
LIBS:transistors
LIBS:conn
LIBS:linear
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
LIBS:eSim_User
LIBS:eSim_Plot
LIBS:eSim_PSpice
LIBS:eSim_Subckt
LIBS:INVCMOS-cache
EELAYER 25 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date "29 apr 2015"
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
Wire Wire Line
	5900 4000 5900 4150
Connection ~ 5800 2450
Connection ~ 5800 4150
Wire Wire Line
	5900 4150 5800 4150
Connection ~ 5050 3350
Wire Wire Line
	4000 3350 5050 3350
Wire Wire Line
	5050 3850 5500 3850
Wire Wire Line
	5050 2700 5050 3850
Wire Wire Line
	5050 2700 5500 2700
Wire Wire Line
	5800 3650 5800 2900
Wire Wire Line
	5800 2500 5800 2300
Connection ~ 4200 3350
$Comp
L PORT U1
U 1 1 5D6263BC
P 3750 3350
F 0 "U1" H 3800 3450 30  0000 C CNN
F 1 "PORT" H 3750 3350 30  0000 C CNN
F 2 "" H 3750 3350 60  0000 C CNN
F 3 "" H 3750 3350 60  0000 C CNN
	1    3750 3350
	1    0    0    -1  
$EndComp
Wire Wire Line
	6050 3250 5800 3250
Connection ~ 5800 3250
Wire Wire Line
	5800 4050 5800 4550
$Comp
L eSim_MOS_N M1
U 1 1 5D6265DB
P 5600 3650
F 0 "M1" H 5600 3500 50  0000 R CNN
F 1 "eSim_MOS_N" H 5700 3600 50  0000 R CNN
F 2 "" H 5900 3350 29  0000 C CNN
F 3 "" H 5700 3450 60  0000 C CNN
	1    5600 3650
	1    0    0    -1  
$EndComp
$Comp
L eSim_MOS_P M2
U 1 1 5D626659
P 5650 2700
F 0 "M2" H 5600 2750 50  0000 R CNN
F 1 "eSim_MOS_P" H 5700 2850 50  0000 R CNN
F 2 "" H 5900 2800 29  0000 C CNN
F 3 "" H 5700 2700 60  0000 C CNN
	1    5650 2700
	1    0    0    -1  
$EndComp
Wire Wire Line
	5900 2850 6050 2850
Wire Wire Line
	6050 2850 6050 2450
Wire Wire Line
	6050 2450 5800 2450
Connection ~ 6000 3250
Connection ~ 5800 4300
$Comp
L GND #PWR1
U 1 1 5D626C59
P 5800 4550
F 0 "#PWR1" H 5800 4300 50  0001 C CNN
F 1 "GND" H 5800 4400 50  0000 C CNN
F 2 "" H 5800 4550 50  0001 C CNN
F 3 "" H 5800 4550 50  0001 C CNN
	1    5800 4550
	1    0    0    -1  
$EndComp
$Comp
L DC v1
U 1 1 5D626C7F
P 6250 2300
F 0 "v1" H 6050 2400 60  0000 C CNN
F 1 "5" H 6050 2250 60  0000 C CNN
F 2 "R1" H 5950 2300 60  0000 C CNN
F 3 "" H 6250 2300 60  0000 C CNN
	1    6250 2300
	0    -1   -1   0   
$EndComp
$Comp
L GND #PWR2
U 1 1 5D626CF6
P 6850 2300
F 0 "#PWR2" H 6850 2050 50  0001 C CNN
F 1 "GND" H 6850 2150 50  0000 C CNN
F 2 "" H 6850 2300 50  0001 C CNN
F 3 "" H 6850 2300 50  0001 C CNN
	1    6850 2300
	1    0    0    -1  
$EndComp
Wire Wire Line
	6850 2300 6700 2300
$Comp
L PORT U1
U 2 1 5D626DCB
P 6300 3250
F 0 "U1" H 6350 3350 30  0000 C CNN
F 1 "PORT" H 6300 3250 30  0000 C CNN
F 2 "" H 6300 3250 60  0000 C CNN
F 3 "" H 6300 3250 60  0000 C CNN
	2    6300 3250
	-1   0    0    1   
$EndComp
$Comp
L eSim_C C1
U 1 1 5D62796C
P 6050 3850
F 0 "C1" H 6075 3950 50  0000 L CNN
F 1 "1u" H 6075 3750 50  0000 L CNN
F 2 "" H 6088 3700 30  0000 C CNN
F 3 "" H 6050 3850 60  0000 C CNN
	1    6050 3850
	1    0    0    -1  
$EndComp
Wire Wire Line
	6050 3700 6050 3400
Wire Wire Line
	6050 3400 6000 3400
Wire Wire Line
	6000 3400 6000 3250
Wire Wire Line
	6050 4000 6050 4300
Wire Wire Line
	6050 4300 5800 4300
$EndSCHEMATC
