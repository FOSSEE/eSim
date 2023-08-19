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
LIBS:LOG101-cache
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
U 1 1 63EA744D
P 5100 4650
F 0 "X1" H 4900 4650 60  0000 C CNN
F 1 "lm_741" H 5000 4400 60  0000 C CNN
F 2 "" H 5100 4650 60  0000 C CNN
F 3 "" H 5100 4650 60  0000 C CNN
	1    5100 4650
	1    0    0    -1  
$EndComp
$Comp
L lm_741 X2
U 1 1 63EA74D9
P 7000 4250
F 0 "X2" H 6800 4250 60  0000 C CNN
F 1 "lm_741" H 6900 4000 60  0000 C CNN
F 2 "" H 7000 4250 60  0000 C CNN
F 3 "" H 7000 4250 60  0000 C CNN
	1    7000 4250
	1    0    0    -1  
$EndComp
$Comp
L eSim_NPN Q1
U 1 1 63EA7516
P 5050 3650
F 0 "Q1" H 4950 3700 50  0000 R CNN
F 1 "eSim_NPN" H 5000 3800 50  0000 R CNN
F 2 "" H 5250 3750 29  0000 C CNN
F 3 "" H 5050 3650 60  0000 C CNN
	1    5050 3650
	0    -1   -1   0   
$EndComp
Wire Wire Line
	4200 3550 4850 3550
Wire Wire Line
	4550 4500 4550 3550
Connection ~ 4550 3550
Wire Wire Line
	5250 3550 5450 3550
Wire Wire Line
	5650 4650 5650 4150
Wire Wire Line
	5650 4150 5350 4150
Wire Wire Line
	5350 4150 5350 3550
Connection ~ 5350 3550
Wire Wire Line
	5850 3550 6100 3550
Wire Wire Line
	6100 3000 6100 4100
Wire Wire Line
	6100 4100 6450 4100
$Comp
L capacitor C1
U 1 1 63EA766F
P 6500 3000
F 0 "C1" H 6525 3100 50  0000 L CNN
F 1 "100p" H 6525 2900 50  0000 L CNN
F 2 "" H 6538 2850 30  0000 C CNN
F 3 "" H 6500 3000 60  0000 C CNN
	1    6500 3000
	0    1    1    0   
$EndComp
Wire Wire Line
	4150 3000 6350 3000
Connection ~ 6100 3000
Connection ~ 6100 3550
$Comp
L resistor R1
U 1 1 63EA76F2
P 7500 4600
F 0 "R1" H 7550 4730 50  0000 C CNN
F 1 "15.72k" H 7550 4550 50  0000 C CNN
F 2 "" H 7550 4580 30  0000 C CNN
F 3 "" V 7550 4650 30  0000 C CNN
	1    7500 4600
	0    1    1    0   
$EndComp
$Comp
L resistor R2
U 1 1 63EA771B
P 7500 5150
F 0 "R2" H 7550 5280 50  0000 C CNN
F 1 "1k" H 7550 5100 50  0000 C CNN
F 2 "" H 7550 5130 30  0000 C CNN
F 3 "" V 7550 5200 30  0000 C CNN
	1    7500 5150
	0    1    1    0   
$EndComp
Wire Wire Line
	7550 5050 7550 4800
Wire Wire Line
	5050 3850 5050 4000
Wire Wire Line
	5050 4000 6000 4000
Wire Wire Line
	6000 4000 6000 4950
Wire Wire Line
	6000 4950 7550 4950
Connection ~ 7550 4950
Wire Wire Line
	7550 3000 7550 4500
Wire Wire Line
	6650 3000 7550 3000
Connection ~ 7550 4250
$Comp
L eSim_GND #PWR01
U 1 1 63EA785A
P 4400 4900
F 0 "#PWR01" H 4400 4650 50  0001 C CNN
F 1 "eSim_GND" H 4400 4750 50  0000 C CNN
F 2 "" H 4400 4900 50  0001 C CNN
F 3 "" H 4400 4900 50  0001 C CNN
	1    4400 4900
	1    0    0    -1  
$EndComp
$Comp
L eSim_GND #PWR02
U 1 1 63EA7880
P 7550 5500
F 0 "#PWR02" H 7550 5250 50  0001 C CNN
F 1 "eSim_GND" H 7550 5350 50  0000 C CNN
F 2 "" H 7550 5500 50  0001 C CNN
F 3 "" H 7550 5500 50  0001 C CNN
	1    7550 5500
	1    0    0    -1  
$EndComp
$Comp
L eSim_GND #PWR03
U 1 1 63EA78A6
P 5850 3900
F 0 "#PWR03" H 5850 3650 50  0001 C CNN
F 1 "eSim_GND" H 5850 3750 50  0000 C CNN
F 2 "" H 5850 3900 50  0001 C CNN
F 3 "" H 5850 3900 50  0001 C CNN
	1    5850 3900
	1    0    0    -1  
$EndComp
$Comp
L eSim_GND #PWR04
U 1 1 63EA78D5
P 6350 4550
F 0 "#PWR04" H 6350 4300 50  0001 C CNN
F 1 "eSim_GND" H 6350 4400 50  0000 C CNN
F 2 "" H 6350 4550 50  0001 C CNN
F 3 "" H 6350 4550 50  0001 C CNN
	1    6350 4550
	1    0    0    -1  
$EndComp
Wire Wire Line
	4550 4750 4400 4750
Wire Wire Line
	4400 4750 4400 4900
Wire Wire Line
	7550 5500 7550 5350
Wire Wire Line
	6450 4350 6350 4350
Wire Wire Line
	6350 4350 6350 4550
Wire Wire Line
	5650 3850 5850 3850
Wire Wire Line
	5850 3850 5850 3900
$Comp
L PORT U1
U 1 1 63EA7BBF
P 3900 3000
F 0 "U1" H 3950 3100 30  0000 C CNN
F 1 "PORT" H 3900 3000 30  0000 C CNN
F 2 "" H 3900 3000 60  0000 C CNN
F 3 "" H 3900 3000 60  0000 C CNN
	1    3900 3000
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 6 1 63EA7EC1
P 7950 4250
F 0 "U1" H 8000 4350 30  0000 C CNN
F 1 "PORT" H 7950 4250 30  0000 C CNN
F 2 "" H 7950 4250 60  0000 C CNN
F 3 "" H 7950 4250 60  0000 C CNN
	6    7950 4250
	-1   0    0    1   
$EndComp
$Comp
L PORT U1
U 2 1 63EA7EEC
P 3950 3550
F 0 "U1" H 4000 3650 30  0000 C CNN
F 1 "PORT" H 3950 3550 30  0000 C CNN
F 2 "" H 3950 3550 60  0000 C CNN
F 3 "" H 3950 3550 60  0000 C CNN
	2    3950 3550
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 5 1 63EA8093
P 7900 5400
F 0 "U1" H 7950 5500 30  0000 C CNN
F 1 "PORT" H 7900 5400 30  0000 C CNN
F 2 "" H 7900 5400 60  0000 C CNN
F 3 "" H 7900 5400 60  0000 C CNN
	5    7900 5400
	-1   0    0    1   
$EndComp
$Comp
L PORT U1
U 3 1 63EA8382
P 5200 5800
F 0 "U1" H 5250 5900 30  0000 C CNN
F 1 "PORT" H 5200 5800 30  0000 C CNN
F 2 "" H 5200 5800 60  0000 C CNN
F 3 "" H 5200 5800 60  0000 C CNN
	3    5200 5800
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 4 1 63EA83BF
P 6250 5800
F 0 "U1" H 6300 5900 30  0000 C CNN
F 1 "PORT" H 6250 5800 30  0000 C CNN
F 2 "" H 6250 5800 60  0000 C CNN
F 3 "" H 6250 5800 60  0000 C CNN
	4    6250 5800
	-1   0    0    1   
$EndComp
Text GLabel 5500 5500 0    60   Input ~ 0
V+
Text GLabel 5900 5500 2    60   Input ~ 0
V-
Wire Wire Line
	5550 5500 5500 5500
Wire Wire Line
	5550 5500 5550 5800
Connection ~ 5550 5800
Wire Wire Line
	5900 5500 5850 5500
Wire Wire Line
	5850 5500 5850 5800
Connection ~ 5850 5800
Text GLabel 5100 4150 2    60   Input ~ 0
V+
Text GLabel 7000 3650 2    60   Input ~ 0
V+
Text GLabel 5100 5250 2    60   Input ~ 0
V-
Text GLabel 7000 4800 2    60   Input ~ 0
V-
Wire Wire Line
	5100 4150 4950 4150
Wire Wire Line
	4950 4150 4950 4200
Wire Wire Line
	5100 5250 4950 5250
Wire Wire Line
	4950 5250 4950 5100
Wire Wire Line
	7000 3650 6850 3650
Wire Wire Line
	6850 3650 6850 3800
Wire Wire Line
	7000 4800 6850 4800
Wire Wire Line
	6850 4800 6850 4700
Wire Wire Line
	7650 5400 7550 5400
Connection ~ 7550 5400
Wire Wire Line
	7700 4250 7550 4250
$Comp
L eSim_NPN Q2
U 1 1 63EA92EA
P 5650 3650
F 0 "Q2" H 5550 3700 50  0000 R CNN
F 1 "eSim_NPN" H 5600 3800 50  0000 R CNN
F 2 "" H 5850 3750 29  0000 C CNN
F 3 "" H 5650 3650 60  0000 C CNN
	1    5650 3650
	0    1    -1   0   
$EndComp
Wire Wire Line
	5550 5800 5450 5800
Wire Wire Line
	5850 5800 6000 5800
$EndSCHEMATC
