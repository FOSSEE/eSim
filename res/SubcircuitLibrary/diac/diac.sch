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
LIBS:analogSpice
LIBS:eSim_Analog
LIBS:eSim_Devices
LIBS:eSim_Digital
LIBS:eSim_Hybrid
LIBS:eSim_Miscellaneous
LIBS:eSim_Sources
LIBS:eSim_Subckt
LIBS:eSim_User
EELAYER 25 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date "22 sep 2014"
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
Wire Wire Line
	4150 2750 4150 4300
Connection ~ 4400 3750
Wire Wire Line
	4400 4450 5050 4450
Wire Wire Line
	4400 4450 4400 3450
Wire Wire Line
	5500 3350 5500 4050
Connection ~ 4600 3400
Wire Wire Line
	4600 4050 4600 2750
Wire Wire Line
	4600 2750 4150 2750
Wire Wire Line
	4400 3450 4150 3450
Connection ~ 4150 3450
Wire Wire Line
	4400 3750 5050 3750
$Comp
L PWR_FLAG #FLG01
U 1 1 5417D647
P 4150 4300
F 0 "#FLG01" H 4150 4570 30  0001 C CNN
F 1 "PWR_FLAG" H 4150 4530 30  0000 C CNN
F 2 "" H 4150 4300 60  0001 C CNN
F 3 "" H 4150 4300 60  0001 C CNN
	1    4150 4300
	0    1    1    0   
$EndComp
$Comp
L PORT U3
U 2 1 5417D62C
P 5750 3350
F 0 "U3" H 5750 3300 30  0000 C CNN
F 1 "PORT" H 5750 3350 30  0000 C CNN
F 2 "" H 5750 3350 60  0001 C CNN
F 3 "" H 5750 3350 60  0001 C CNN
	2    5750 3350
	-1   0    0    1   
$EndComp
$Comp
L PORT U3
U 1 1 5417D624
P 4150 2500
F 0 "U3" H 4150 2450 30  0000 C CNN
F 1 "PORT" H 4150 2500 30  0000 C CNN
F 2 "" H 4150 2500 60  0001 C CNN
F 3 "" H 4150 2500 60  0001 C CNN
	1    4150 2500
	0    1    1    0   
$EndComp
$Comp
L GND #PWR02
U 1 1 5417D5DC
P 4150 4300
F 0 "#PWR02" H 4150 4300 30  0001 C CNN
F 1 "GND" H 4150 4230 30  0001 C CNN
F 2 "" H 4150 4300 60  0001 C CNN
F 3 "" H 4150 4300 60  0001 C CNN
	1    4150 4300
	1    0    0    -1  
$EndComp
$Comp
L aswitch U1
U 1 1 56669812
P 4600 3550
F 0 "U1" H 5050 3850 60  0000 C CNN
F 1 "aswitch" H 5050 3750 60  0000 C CNN
F 2 "" H 5050 3650 60  0000 C CNN
F 3 "" H 5050 3650 60  0000 C CNN
	1    4600 3550
	1    0    0    -1  
$EndComp
$Comp
L aswitch U2
U 1 1 5666987C
P 4600 4200
F 0 "U2" H 5050 4500 60  0000 C CNN
F 1 "aswitch" H 5050 4400 60  0000 C CNN
F 2 "" H 5050 4300 60  0000 C CNN
F 3 "" H 5050 4300 60  0000 C CNN
	1    4600 4200
	1    0    0    -1  
$EndComp
Wire Wire Line
	5050 4450 5050 4300
Wire Wire Line
	5050 3750 5050 3650
Wire Wire Line
	5500 4050 5450 4050
Wire Wire Line
	5500 3400 5450 3400
Connection ~ 5500 3400
$EndSCHEMATC
