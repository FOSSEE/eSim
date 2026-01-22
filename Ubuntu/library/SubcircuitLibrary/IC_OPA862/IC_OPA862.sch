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
LIBS:IC_OPA862-cache
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
L lm_741 X1
U 1 1 6405D910
P 4500 2950
F 0 "X1" H 4300 2950 60  0000 C CNN
F 1 "lm_741" H 4400 2700 60  0000 C CNN
F 2 "" H 4500 2950 60  0000 C CNN
F 3 "" H 4500 2950 60  0000 C CNN
	1    4500 2950
	1    0    0    -1  
$EndComp
$Comp
L lm_741 X2
U 1 1 6405D92B
P 5950 4700
F 0 "X2" H 5750 4700 60  0000 C CNN
F 1 "lm_741" H 5850 4450 60  0000 C CNN
F 2 "" H 5950 4700 60  0000 C CNN
F 3 "" H 5950 4700 60  0000 C CNN
	1    5950 4700
	1    0    0    -1  
$EndComp
$Comp
L resistor R1
U 1 1 6405D952
P 5150 4600
F 0 "R1" H 5200 4730 50  0000 C CNN
F 1 "1k" H 5200 4550 50  0000 C CNN
F 2 "" H 5200 4580 30  0000 C CNN
F 3 "" V 5200 4650 30  0000 C CNN
	1    5150 4600
	1    0    0    -1  
$EndComp
$Comp
L resistor R2
U 1 1 6405D971
P 5650 4000
F 0 "R2" H 5700 4130 50  0000 C CNN
F 1 "1k" H 5700 3950 50  0000 C CNN
F 2 "" H 5700 3980 30  0000 C CNN
F 3 "" V 5700 4050 30  0000 C CNN
	1    5650 4000
	1    0    0    -1  
$EndComp
$Comp
L capacitor C1
U 1 1 6405D98E
P 5700 3700
F 0 "C1" H 5725 3800 50  0000 L CNN
F 1 "4p" H 5725 3600 50  0000 L CNN
F 2 "" H 5738 3550 30  0000 C CNN
F 3 "" H 5700 3700 60  0000 C CNN
	1    5700 3700
	0    1    1    0   
$EndComp
$Comp
L PORT U1
U 1 1 6405DEE9
P 3550 2800
F 0 "U1" H 3600 2900 30  0000 C CNN
F 1 "PORT" H 3550 2800 30  0000 C CNN
F 2 "" H 3550 2800 60  0000 C CNN
F 3 "" H 3550 2800 60  0000 C CNN
	1    3550 2800
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 2 1 6405DF14
P 3550 3050
F 0 "U1" H 3600 3150 30  0000 C CNN
F 1 "PORT" H 3550 3050 30  0000 C CNN
F 2 "" H 3550 3050 60  0000 C CNN
F 3 "" H 3550 3050 60  0000 C CNN
	2    3550 3050
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 3 1 6405DF3B
P 3900 4800
F 0 "U1" H 3950 4900 30  0000 C CNN
F 1 "PORT" H 3900 4800 30  0000 C CNN
F 2 "" H 3900 4800 60  0000 C CNN
F 3 "" H 3900 4800 60  0000 C CNN
	3    3900 4800
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 5 1 6405E150
P 6450 2200
F 0 "U1" H 6500 2300 30  0000 C CNN
F 1 "PORT" H 6450 2200 30  0000 C CNN
F 2 "" H 6450 2200 60  0000 C CNN
F 3 "" H 6450 2200 60  0000 C CNN
	5    6450 2200
	-1   0    0    1   
$EndComp
$Comp
L PORT U1
U 4 1 6405E212
P 4350 5600
F 0 "U1" H 4400 5700 30  0000 C CNN
F 1 "PORT" H 4350 5600 30  0000 C CNN
F 2 "" H 4350 5600 60  0000 C CNN
F 3 "" H 4350 5600 60  0000 C CNN
	4    4350 5600
	0    -1   -1   0   
$EndComp
Wire Wire Line
	5050 2950 5050 4550
Wire Wire Line
	5550 3950 5400 3950
Wire Wire Line
	5400 3700 5400 4550
Wire Wire Line
	5400 4550 5350 4550
Wire Wire Line
	5550 3700 5400 3700
Connection ~ 5400 3950
Wire Wire Line
	5850 3950 6500 3950
Wire Wire Line
	6500 3700 6500 4700
Wire Wire Line
	5850 3700 6500 3700
Connection ~ 6500 3950
Wire Wire Line
	5050 2950 7250 2950
Wire Wire Line
	6500 4700 7250 4700
Wire Wire Line
	4350 2500 4350 2200
Wire Wire Line
	4350 2200 6200 2200
Wire Wire Line
	6100 2200 6100 4250
Wire Wire Line
	6100 4250 5800 4250
Wire Wire Line
	4350 3400 4350 5350
Wire Wire Line
	4350 5250 5800 5250
Wire Wire Line
	5800 5250 5800 5150
Wire Wire Line
	3800 2800 3950 2800
Wire Wire Line
	3800 3050 3950 3050
Wire Wire Line
	4150 4800 5400 4800
Connection ~ 4350 5250
Connection ~ 6100 2200
$Comp
L PORT U1
U 6 1 6405E6DC
P 7500 2950
F 0 "U1" H 7550 3050 30  0000 C CNN
F 1 "PORT" H 7500 2950 30  0000 C CNN
F 2 "" H 7500 2950 60  0000 C CNN
F 3 "" H 7500 2950 60  0000 C CNN
	6    7500 2950
	-1   0    0    1   
$EndComp
$Comp
L PORT U1
U 7 1 6405E70F
P 7500 4700
F 0 "U1" H 7550 4800 30  0000 C CNN
F 1 "PORT" H 7500 4700 30  0000 C CNN
F 2 "" H 7500 4700 60  0000 C CNN
F 3 "" H 7500 4700 60  0000 C CNN
	7    7500 4700
	-1   0    0    1   
$EndComp
Connection ~ 6950 2950
Connection ~ 6950 4700
$EndSCHEMATC
