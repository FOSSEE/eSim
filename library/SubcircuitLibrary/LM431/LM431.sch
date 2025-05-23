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
LIBS:LM431-cache
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
L resistor R1
U 1 1 674F6B71
P 2850 3250
F 0 "R1" H 2900 3380 50  0000 C CNN
F 1 "12k" H 2900 3200 50  0000 C CNN
F 2 "" H 2900 3230 30  0000 C CNN
F 3 "" V 2900 3300 30  0000 C CNN
	1    2850 3250
	0    1    1    0   
$EndComp
$Comp
L resistor R2
U 1 1 674F6B72
P 3600 4200
F 0 "R2" H 3650 4330 50  0000 C CNN
F 1 "800" H 3650 4150 50  0000 C CNN
F 2 "" H 3650 4180 30  0000 C CNN
F 3 "" V 3650 4250 30  0000 C CNN
	1    3600 4200
	1    0    0    -1  
$EndComp
$Comp
L eSim_NPN Q2
U 1 1 674F6B73
P 3000 4150
F 0 "Q2" H 2900 4200 50  0000 R CNN
F 1 "eSim_NPN" H 2950 4300 50  0000 R CNN
F 2 "" H 3200 4250 29  0000 C CNN
F 3 "" H 3000 4150 60  0000 C CNN
	1    3000 4150
	-1   0    0    -1  
$EndComp
$Comp
L resistor R3
U 1 1 674F6B74
P 4250 3250
F 0 "R3" H 4300 3380 50  0000 C CNN
F 1 "12k" H 4300 3200 50  0000 C CNN
F 2 "" H 4300 3230 30  0000 C CNN
F 3 "" V 4300 3300 30  0000 C CNN
	1    4250 3250
	0    1    1    0   
$EndComp
$Comp
L eSim_NPN Q3
U 1 1 674F6B75
P 4200 4150
F 0 "Q3" H 4100 4200 50  0000 R CNN
F 1 "eSim_NPN" H 4150 4300 50  0000 R CNN
F 2 "" H 4400 4250 29  0000 C CNN
F 3 "" H 4200 4150 60  0000 C CNN
	1    4200 4150
	1    0    0    -1  
$EndComp
$Comp
L resistor R4
U 1 1 674F6B76
P 4250 4850
F 0 "R4" H 4300 4980 50  0000 C CNN
F 1 "640" H 4300 4800 50  0000 C CNN
F 2 "" H 4300 4830 30  0000 C CNN
F 3 "" V 4300 4900 30  0000 C CNN
	1    4250 4850
	0    1    1    0   
$EndComp
$Comp
L resistor R5
U 1 1 674F6B77
P 4750 3700
F 0 "R5" H 4800 3830 50  0000 C CNN
F 1 "2.5k" H 4800 3650 50  0000 C CNN
F 2 "" H 4800 3680 30  0000 C CNN
F 3 "" V 4800 3750 30  0000 C CNN
	1    4750 3700
	1    0    0    -1  
$EndComp
$Comp
L capacitor_polarised C1
U 1 1 674F6B78
P 5350 3350
F 0 "C1" H 5375 3450 50  0000 L CNN
F 1 "0.1nF" H 5375 3250 50  0000 L CNN
F 2 "" H 5350 3350 50  0001 C CNN
F 3 "" H 5350 3350 50  0001 C CNN
	1    5350 3350
	0    -1   -1   0   
$EndComp
$Comp
L eSim_NPN Q4
U 1 1 674F6B79
P 5550 3650
F 0 "Q4" H 5450 3700 50  0000 R CNN
F 1 "eSim_NPN" H 5500 3800 50  0000 R CNN
F 2 "" H 5750 3750 29  0000 C CNN
F 3 "" H 5550 3650 60  0000 C CNN
	1    5550 3650
	1    0    0    -1  
$EndComp
$Comp
L eSim_PNP Q5
U 1 1 674F6B7A
P 5900 3150
F 0 "Q5" H 5800 3200 50  0000 R CNN
F 1 "eSim_PNP" H 5850 3300 50  0000 R CNN
F 2 "" H 6100 3250 29  0000 C CNN
F 3 "" H 5900 3150 60  0000 C CNN
	1    5900 3150
	1    0    0    1   
$EndComp
$Comp
L capacitor_polarised C2
U 1 1 674F6B7B
P 6600 3150
F 0 "C2" H 6625 3250 50  0000 L CNN
F 1 "0.1nF" H 6625 3050 50  0000 L CNN
F 2 "" H 6600 3150 50  0001 C CNN
F 3 "" H 6600 3150 50  0001 C CNN
	1    6600 3150
	1    0    0    -1  
$EndComp
$Comp
L eSim_NPN Q6
U 1 1 674F6B7C
P 6850 3650
F 0 "Q6" H 6750 3700 50  0000 R CNN
F 1 "eSim_NPN" H 6800 3800 50  0000 R CNN
F 2 "" H 7050 3750 29  0000 C CNN
F 3 "" H 6850 3650 60  0000 C CNN
	1    6850 3650
	1    0    0    -1  
$EndComp
$Comp
L resistor R6
U 1 1 674F6B7D
P 6900 4850
F 0 "R6" H 6950 4980 50  0000 C CNN
F 1 "1k" H 6950 4800 50  0000 C CNN
F 2 "" H 6950 4830 30  0000 C CNN
F 3 "" V 6950 4900 30  0000 C CNN
	1    6900 4850
	0    1    1    0   
$EndComp
$Comp
L eSim_NPN Q7
U 1 1 674F6B7E
P 7400 4150
F 0 "Q7" H 7300 4200 50  0000 R CNN
F 1 "eSim_NPN" H 7350 4300 50  0000 R CNN
F 2 "" H 7600 4250 29  0000 C CNN
F 3 "" H 7400 4150 60  0000 C CNN
	1    7400 4150
	1    0    0    -1  
$EndComp
$Comp
L resistor R7
U 1 1 674F6B7F
P 7450 4850
F 0 "R7" H 7500 4980 50  0000 C CNN
F 1 "3.3" H 7500 4800 50  0000 C CNN
F 2 "" H 7500 4830 30  0000 C CNN
F 3 "" V 7500 4900 30  0000 C CNN
	1    7450 4850
	0    1    1    0   
$EndComp
$Comp
L eSim_NPN Q1
U 1 1 674F6B80
P 2800 2750
F 0 "Q1" H 2700 2800 50  0000 R CNN
F 1 "eSim_NPN" H 2750 2900 50  0000 R CNN
F 2 "" H 3000 2850 29  0000 C CNN
F 3 "" H 2800 2750 60  0000 C CNN
	1    2800 2750
	1    0    0    -1  
$EndComp
Wire Wire Line
	2900 2950 2900 3150
Wire Wire Line
	4300 3150 4300 3050
Wire Wire Line
	4300 3050 2900 3050
Connection ~ 2900 3050
Wire Wire Line
	3200 4150 3500 4150
Wire Wire Line
	3800 4150 4000 4150
Wire Wire Line
	3900 4150 3900 3650
Wire Wire Line
	3900 3650 2900 3650
Connection ~ 2900 3650
Connection ~ 3900 4150
Wire Wire Line
	4300 4350 4300 4750
Wire Wire Line
	2900 3450 2900 3950
Wire Wire Line
	2900 4350 2900 5050
Wire Wire Line
	2900 5050 7850 5050
Wire Wire Line
	4300 3450 4300 3950
Wire Wire Line
	4650 3650 4300 3650
Connection ~ 4300 3650
Wire Wire Line
	4950 3650 5350 3650
Wire Wire Line
	5200 3350 5050 3350
Wire Wire Line
	5050 3350 5050 3650
Connection ~ 5050 3650
Wire Wire Line
	5650 2850 5650 3450
Wire Wire Line
	5650 3150 5700 3150
Wire Wire Line
	5500 3350 5650 3350
Connection ~ 5650 3350
Wire Wire Line
	6000 3350 6000 3450
Wire Wire Line
	6000 3450 5650 3450
Wire Wire Line
	2900 2550 2900 2350
Wire Wire Line
	2900 2350 7800 2350
Wire Wire Line
	6000 2950 6000 2350
Connection ~ 6000 2350
Wire Wire Line
	6950 3450 6950 2350
Connection ~ 6950 2350
Wire Wire Line
	6950 3850 6950 4750
Wire Wire Line
	7200 4150 6950 4150
Connection ~ 6950 4150
Wire Wire Line
	7500 4350 7500 4750
Wire Wire Line
	7500 3950 7500 2350
Connection ~ 7500 2350
Connection ~ 4300 5050
Connection ~ 6950 5050
Wire Wire Line
	5650 3850 5650 5050
Connection ~ 5650 5050
Connection ~ 7500 5050
$Comp
L PORT U1
U 1 1 674F6B81
P 2350 2750
F 0 "U1" H 2400 2850 30  0000 C CNN
F 1 "PORT" H 2350 2750 30  0000 C CNN
F 2 "" H 2350 2750 60  0000 C CNN
F 3 "" H 2350 2750 60  0000 C CNN
	1    2350 2750
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 2 1 674F6B82
P 8050 2350
F 0 "U1" H 8100 2450 30  0000 C CNN
F 1 "PORT" H 8050 2350 30  0000 C CNN
F 2 "" H 8050 2350 60  0000 C CNN
F 3 "" H 8050 2350 60  0000 C CNN
	2    8050 2350
	-1   0    0    1   
$EndComp
$Comp
L PORT U1
U 3 1 674F6B83
P 8100 5050
F 0 "U1" H 8150 5150 30  0000 C CNN
F 1 "PORT" H 8100 5050 30  0000 C CNN
F 2 "" H 8100 5050 60  0000 C CNN
F 3 "" H 8100 5050 60  0000 C CNN
	3    8100 5050
	-1   0    0    1   
$EndComp
$Comp
L eSim_PNP Q8
U 1 1 675DDD31
P 6300 3150
F 0 "Q8" H 6200 3200 50  0000 R CNN
F 1 "eSim_PNP" H 6250 3300 50  0000 R CNN
F 2 "" H 6500 3250 29  0000 C CNN
F 3 "" H 6300 3150 60  0000 C CNN
	1    6300 3150
	1    0    0    1   
$EndComp
Wire Wire Line
	6600 3000 6600 2350
Wire Wire Line
	6400 2350 6400 2950
Wire Wire Line
	6600 3300 6600 3650
Connection ~ 6600 3650
Wire Wire Line
	6400 3650 6650 3650
Connection ~ 6600 2350
Connection ~ 6400 2350
Wire Wire Line
	6400 3350 6400 3650
Wire Wire Line
	6100 3150 6100 2850
Wire Wire Line
	6100 2850 5650 2850
Connection ~ 5650 3150
$EndSCHEMATC
