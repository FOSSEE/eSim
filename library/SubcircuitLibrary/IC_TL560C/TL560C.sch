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
LIBS:TL560C-cache
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
L eSim_NPN Q1
U 1 1 68492C39
P 2000 4100
F 0 "Q1" H 1900 4150 50  0000 R CNN
F 1 "eSim_NPN" H 1950 4250 50  0000 R CNN
F 2 "" H 2200 4200 29  0000 C CNN
F 3 "" H 2000 4100 60  0000 C CNN
	1    2000 4100
	1    0    0    -1  
$EndComp
$Comp
L eSim_NPN Q3
U 1 1 68492C73
P 3000 4100
F 0 "Q3" H 2900 4150 50  0000 R CNN
F 1 "eSim_NPN" H 2950 4250 50  0000 R CNN
F 2 "" H 3200 4200 29  0000 C CNN
F 3 "" H 3000 4100 60  0000 C CNN
	1    3000 4100
	-1   0    0    -1  
$EndComp
$Comp
L resistor R1
U 1 1 68492CCD
P 2450 4950
F 0 "R1" H 2500 5080 50  0000 C CNN
F 1 "5k" H 2500 4900 50  0000 C CNN
F 2 "" H 2500 4930 30  0000 C CNN
F 3 "" V 2500 5000 30  0000 C CNN
	1    2450 4950
	0    1    1    0   
$EndComp
$Comp
L eSim_PNP Q2
U 1 1 68492D46
P 2550 2250
F 0 "Q2" H 2450 2300 50  0000 R CNN
F 1 "eSim_PNP" H 2500 2400 50  0000 R CNN
F 2 "" H 2750 2350 29  0000 C CNN
F 3 "" H 2550 2250 60  0000 C CNN
	1    2550 2250
	1    0    0    1   
$EndComp
$Comp
L eSim_PNP Q4
U 1 1 68492D98
P 3300 2250
F 0 "Q4" H 3200 2300 50  0000 R CNN
F 1 "eSim_PNP" H 3250 2400 50  0000 R CNN
F 2 "" H 3500 2350 29  0000 C CNN
F 3 "" H 3300 2250 60  0000 C CNN
	1    3300 2250
	1    0    0    1   
$EndComp
$Comp
L resistor R2
U 1 1 68492DFC
P 4050 4850
F 0 "R2" H 4100 4980 50  0000 C CNN
F 1 "1.3k" H 4100 4800 50  0000 C CNN
F 2 "" H 4100 4830 30  0000 C CNN
F 3 "" V 4100 4900 30  0000 C CNN
	1    4050 4850
	-1   0    0    1   
$EndComp
$Comp
L eSim_NPN Q6
U 1 1 68492E7D
P 4900 4900
F 0 "Q6" H 4800 4950 50  0000 R CNN
F 1 "eSim_NPN" H 4850 5050 50  0000 R CNN
F 2 "" H 5100 5000 29  0000 C CNN
F 3 "" H 4900 4900 60  0000 C CNN
	1    4900 4900
	1    0    0    -1  
$EndComp
$Comp
L eSim_NPN Q5
U 1 1 68492F3A
P 3700 2700
F 0 "Q5" H 3600 2750 50  0000 R CNN
F 1 "eSim_NPN" H 3650 2850 50  0000 R CNN
F 2 "" H 3900 2800 29  0000 C CNN
F 3 "" H 3700 2700 60  0000 C CNN
	1    3700 2700
	1    0    0    -1  
$EndComp
Wire Wire Line
	2100 4300 2100 4400
Wire Wire Line
	2100 4400 2900 4400
Wire Wire Line
	2900 4400 2900 4300
Wire Wire Line
	2500 4400 2500 4850
Connection ~ 2500 4400
Wire Wire Line
	2500 5150 2500 5850
Wire Wire Line
	1250 5850 8900 5850
Wire Wire Line
	2100 3900 2100 2250
Wire Wire Line
	2100 2250 2350 2250
Wire Wire Line
	2900 3900 2900 2250
Wire Wire Line
	2900 2250 3100 2250
Wire Wire Line
	2650 2450 2650 3400
Wire Wire Line
	2650 3400 3650 3400
Wire Wire Line
	3650 3400 3650 4900
Wire Wire Line
	3650 4900 3850 4900
Wire Wire Line
	4150 4900 4700 4900
Wire Wire Line
	1800 4100 1100 4100
Wire Wire Line
	2650 2050 2650 1600
Wire Wire Line
	1200 1600 8350 1600
Wire Wire Line
	3400 1600 3400 2050
Connection ~ 2650 1600
Wire Wire Line
	3400 2450 3400 2700
Wire Wire Line
	3400 2700 3500 2700
Wire Wire Line
	3800 2500 3800 2000
Wire Wire Line
	3800 2000 6950 2000
Wire Wire Line
	3800 2900 3800 4650
Wire Wire Line
	3800 4650 2500 4650
Connection ~ 2500 4650
Wire Wire Line
	3200 4100 5250 4100
Wire Wire Line
	5000 4100 5000 4700
$Comp
L resistor R3
U 1 1 68493136
P 5450 4050
F 0 "R3" H 5500 4180 50  0000 C CNN
F 1 "2.5k" H 5500 4000 50  0000 C CNN
F 2 "" H 5500 4030 30  0000 C CNN
F 3 "" V 5500 4100 30  0000 C CNN
	1    5450 4050
	-1   0    0    1   
$EndComp
Connection ~ 5000 4100
Wire Wire Line
	5550 4100 6950 4100
Wire Wire Line
	5000 5850 5000 5100
Connection ~ 2500 5850
$Comp
L resistor R5
U 1 1 684932D4
P 6400 4750
F 0 "R5" H 6450 4880 50  0000 C CNN
F 1 "3k" H 6450 4700 50  0000 C CNN
F 2 "" H 6450 4730 30  0000 C CNN
F 3 "" V 6450 4800 30  0000 C CNN
	1    6400 4750
	0    -1   -1   0   
$EndComp
Wire Wire Line
	6350 3200 6350 4550
Connection ~ 6350 5850
Connection ~ 5000 5850
$Comp
L resistor R4
U 1 1 68493443
P 6400 3100
F 0 "R4" H 6450 3230 50  0000 C CNN
F 1 "1.7k" H 6450 3050 50  0000 C CNN
F 2 "" H 6450 3080 30  0000 C CNN
F 3 "" V 6450 3150 30  0000 C CNN
	1    6400 3100
	0    -1   -1   0   
$EndComp
Connection ~ 6350 4100
Wire Wire Line
	6350 1600 6350 2900
Connection ~ 3400 1600
$Comp
L eSim_PNP Q7
U 1 1 684935BD
P 7150 2000
F 0 "Q7" H 7050 2050 50  0000 R CNN
F 1 "eSim_PNP" H 7100 2150 50  0000 R CNN
F 2 "" H 7350 2100 29  0000 C CNN
F 3 "" H 7150 2000 60  0000 C CNN
	1    7150 2000
	1    0    0    1   
$EndComp
Wire Wire Line
	7250 1600 7250 1800
Connection ~ 6350 1600
Wire Wire Line
	8350 1600 8350 2000
Connection ~ 7250 1600
$Comp
L resistor R6
U 1 1 68493704
P 8400 2200
F 0 "R6" H 8450 2330 50  0000 C CNN
F 1 "0.3k" H 8450 2150 50  0000 C CNN
F 2 "" H 8450 2180 30  0000 C CNN
F 3 "" V 8450 2250 30  0000 C CNN
	1    8400 2200
	0    -1   -1   0   
$EndComp
$Comp
L eSim_NPN Q8
U 1 1 684937E9
P 8250 2700
F 0 "Q8" H 8150 2750 50  0000 R CNN
F 1 "eSim_NPN" H 8200 2850 50  0000 R CNN
F 2 "" H 8450 2800 29  0000 C CNN
F 3 "" H 8250 2700 60  0000 C CNN
	1    8250 2700
	1    0    0    -1  
$EndComp
Wire Wire Line
	7250 2200 7250 2700
Wire Wire Line
	7250 2700 8050 2700
Wire Wire Line
	8350 2500 8350 2300
Wire Wire Line
	8350 2900 8350 3400
$Comp
L resistor R7
U 1 1 68493AB1
P 8400 3600
F 0 "R7" H 8450 3730 50  0000 C CNN
F 1 "0.2k" H 8450 3550 50  0000 C CNN
F 2 "" H 8450 3580 30  0000 C CNN
F 3 "" V 8450 3650 30  0000 C CNN
	1    8400 3600
	0    -1   -1   0   
$EndComp
$Comp
L eSim_NPN Q9
U 1 1 68493BA0
P 8800 4050
F 0 "Q9" H 8700 4100 50  0000 R CNN
F 1 "eSim_NPN" H 8750 4200 50  0000 R CNN
F 2 "" H 9000 4150 29  0000 C CNN
F 3 "" H 8800 4050 60  0000 C CNN
	1    8800 4050
	1    0    0    -1  
$EndComp
Wire Wire Line
	8350 3700 8350 4450
Wire Wire Line
	8350 4050 8600 4050
Wire Wire Line
	8900 3850 8900 3500
Wire Wire Line
	8900 3500 9350 3500
$Comp
L resistor R8
U 1 1 68493CF2
P 8400 4650
F 0 "R8" H 8450 4780 50  0000 C CNN
F 1 "3k" H 8450 4600 50  0000 C CNN
F 2 "" H 8450 4630 30  0000 C CNN
F 3 "" V 8450 4700 30  0000 C CNN
	1    8400 4650
	0    -1   -1   0   
$EndComp
Connection ~ 8350 4050
Wire Wire Line
	8350 5850 8350 4750
Wire Wire Line
	6350 4850 6350 5850
Wire Wire Line
	6950 4100 6950 6000
$Comp
L PORT U1
U 2 1 68494358
P 950 1600
F 0 "U1" H 1000 1700 30  0000 C CNN
F 1 "PORT" H 950 1600 30  0000 C CNN
F 2 "" H 950 1600 60  0000 C CNN
F 3 "" H 950 1600 60  0000 C CNN
	2    950  1600
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 1 1 68494439
P 850 4100
F 0 "U1" H 900 4200 30  0000 C CNN
F 1 "PORT" H 850 4100 30  0000 C CNN
F 2 "" H 850 4100 60  0000 C CNN
F 3 "" H 850 4100 60  0000 C CNN
	1    850  4100
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 3 1 684944FF
P 1000 5850
F 0 "U1" H 1050 5950 30  0000 C CNN
F 1 "PORT" H 1000 5850 30  0000 C CNN
F 2 "" H 1000 5850 60  0000 C CNN
F 3 "" H 1000 5850 60  0000 C CNN
	3    1000 5850
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 4 1 6849469E
P 6950 6250
F 0 "U1" H 7000 6350 30  0000 C CNN
F 1 "PORT" H 6950 6250 30  0000 C CNN
F 2 "" H 6950 6250 60  0000 C CNN
F 3 "" H 6950 6250 60  0000 C CNN
	4    6950 6250
	0    -1   -1   0   
$EndComp
$Comp
L PORT U1
U 5 1 68494763
P 9600 3500
F 0 "U1" H 9650 3600 30  0000 C CNN
F 1 "PORT" H 9600 3500 30  0000 C CNN
F 2 "" H 9600 3500 60  0000 C CNN
F 3 "" H 9600 3500 60  0000 C CNN
	5    9600 3500
	-1   0    0    1   
$EndComp
Wire Wire Line
	8900 5850 8900 4250
Connection ~ 8350 5850
$EndSCHEMATC
