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
LIBS:IC_LM386-cache
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
U 1 1 641FE287
P 4300 3050
F 0 "R1" H 4350 3180 50  0000 C CNN
F 1 "15k" H 4350 3000 50  0000 C CNN
F 2 "" H 4350 3030 30  0000 C CNN
F 3 "" V 4350 3100 30  0000 C CNN
	1    4300 3050
	0    1    1    0   
$EndComp
$Comp
L resistor R2
U 1 1 641FE2A0
P 4300 3550
F 0 "R2" H 4350 3680 50  0000 C CNN
F 1 "15k" H 4350 3500 50  0000 C CNN
F 2 "" H 4350 3530 30  0000 C CNN
F 3 "" V 4350 3600 30  0000 C CNN
	1    4300 3550
	0    1    1    0   
$EndComp
$Comp
L resistor R3
U 1 1 641FE2C1
P 4600 4050
F 0 "R3" H 4650 4180 50  0000 C CNN
F 1 "150" H 4650 4000 50  0000 C CNN
F 2 "" H 4650 4030 30  0000 C CNN
F 3 "" V 4650 4100 30  0000 C CNN
	1    4600 4050
	1    0    0    -1  
$EndComp
$Comp
L resistor R4
U 1 1 641FE2E0
P 5150 4050
F 0 "R4" H 5200 4180 50  0000 C CNN
F 1 "1.35k" H 5200 4000 50  0000 C CNN
F 2 "" H 5200 4030 30  0000 C CNN
F 3 "" V 5200 4100 30  0000 C CNN
	1    5150 4050
	1    0    0    -1  
$EndComp
$Comp
L resistor R5
U 1 1 641FE3C5
P 6250 4050
F 0 "R5" H 6300 4180 50  0000 C CNN
F 1 "15k" H 6300 4000 50  0000 C CNN
F 2 "" H 6300 4030 30  0000 C CNN
F 3 "" V 6300 4100 30  0000 C CNN
	1    6250 4050
	1    0    0    -1  
$EndComp
$Comp
L eSim_PNP Q2
U 1 1 641FE3EC
P 4250 4450
F 0 "Q2" H 4150 4500 50  0000 R CNN
F 1 "eSim_PNP" H 4200 4600 50  0000 R CNN
F 2 "" H 4450 4550 29  0000 C CNN
F 3 "" H 4250 4450 60  0000 C CNN
	1    4250 4450
	1    0    0    1   
$EndComp
$Comp
L eSim_PNP Q1
U 1 1 641FE423
P 3700 4850
F 0 "Q1" H 3600 4900 50  0000 R CNN
F 1 "eSim_PNP" H 3650 5000 50  0000 R CNN
F 2 "" H 3900 4950 29  0000 C CNN
F 3 "" H 3700 4850 60  0000 C CNN
	1    3700 4850
	1    0    0    1   
$EndComp
$Comp
L eSim_PNP Q5
U 1 1 641FE44A
P 5650 4450
F 0 "Q5" H 5550 4500 50  0000 R CNN
F 1 "eSim_PNP" H 5600 4600 50  0000 R CNN
F 2 "" H 5850 4550 29  0000 C CNN
F 3 "" H 5650 4450 60  0000 C CNN
	1    5650 4450
	-1   0    0    1   
$EndComp
$Comp
L eSim_PNP Q6
U 1 1 641FE47B
P 6150 4850
F 0 "Q6" H 6050 4900 50  0000 R CNN
F 1 "eSim_PNP" H 6100 5000 50  0000 R CNN
F 2 "" H 6350 4950 29  0000 C CNN
F 3 "" H 6150 4850 60  0000 C CNN
	1    6150 4850
	-1   0    0    1   
$EndComp
$Comp
L eSim_NPN Q3
U 1 1 641FE52E
P 4450 5600
F 0 "Q3" H 4350 5650 50  0000 R CNN
F 1 "eSim_NPN" H 4400 5750 50  0000 R CNN
F 2 "" H 4650 5700 29  0000 C CNN
F 3 "" H 4450 5600 60  0000 C CNN
	1    4450 5600
	-1   0    0    -1  
$EndComp
$Comp
L eSim_NPN Q4
U 1 1 641FE561
P 5450 5600
F 0 "Q4" H 5350 5650 50  0000 R CNN
F 1 "eSim_NPN" H 5400 5750 50  0000 R CNN
F 2 "" H 5650 5700 29  0000 C CNN
F 3 "" H 5450 5600 60  0000 C CNN
	1    5450 5600
	1    0    0    -1  
$EndComp
$Comp
L eSim_Diode D1
U 1 1 641FE592
P 7050 3650
F 0 "D1" H 7050 3750 50  0000 C CNN
F 1 "eSim_Diode" H 7050 3550 50  0000 C CNN
F 2 "" H 7050 3650 60  0000 C CNN
F 3 "" H 7050 3650 60  0000 C CNN
	1    7050 3650
	0    1    1    0   
$EndComp
$Comp
L eSim_Diode D2
U 1 1 641FE5C3
P 7050 4400
F 0 "D2" H 7050 4500 50  0000 C CNN
F 1 "eSim_Diode" H 7050 4300 50  0000 C CNN
F 2 "" H 7050 4400 60  0000 C CNN
F 3 "" H 7050 4400 60  0000 C CNN
	1    7050 4400
	0    1    1    0   
$EndComp
$Comp
L eSim_NPN Q7
U 1 1 6420528C
P 6950 5600
F 0 "Q7" H 6850 5650 50  0000 R CNN
F 1 "eSim_NPN" H 6900 5750 50  0000 R CNN
F 2 "" H 7150 5700 29  0000 C CNN
F 3 "" H 6950 5600 60  0000 C CNN
	1    6950 5600
	1    0    0    -1  
$EndComp
$Comp
L eSim_PNP Q8
U 1 1 642052CF
P 7400 4800
F 0 "Q8" H 7300 4850 50  0000 R CNN
F 1 "eSim_PNP" H 7350 4950 50  0000 R CNN
F 2 "" H 7600 4900 29  0000 C CNN
F 3 "" H 7400 4800 60  0000 C CNN
	1    7400 4800
	1    0    0    1   
$EndComp
$Comp
L eSim_NPN Q9
U 1 1 64205306
P 7750 3500
F 0 "Q9" H 7650 3550 50  0000 R CNN
F 1 "eSim_NPN" H 7700 3650 50  0000 R CNN
F 2 "" H 7950 3600 29  0000 C CNN
F 3 "" H 7750 3500 60  0000 C CNN
	1    7750 3500
	1    0    0    -1  
$EndComp
$Comp
L eSim_NPN Q10
U 1 1 64205357
P 7750 5350
F 0 "Q10" H 7650 5400 50  0000 R CNN
F 1 "eSim_NPN" H 7700 5500 50  0000 R CNN
F 2 "" H 7950 5450 29  0000 C CNN
F 3 "" H 7750 5350 60  0000 C CNN
	1    7750 5350
	1    0    0    -1  
$EndComp
Wire Wire Line
	4350 3750 4350 4250
Wire Wire Line
	4350 4000 4500 4000
Wire Wire Line
	4800 4000 5050 4000
Wire Wire Line
	5350 4000 6150 4000
Wire Wire Line
	6450 4000 8100 4000
Wire Wire Line
	7050 3800 7050 4250
Connection ~ 7050 4000
Connection ~ 4350 4000
Wire Wire Line
	5550 3850 5550 4250
Connection ~ 5550 4000
Wire Wire Line
	3800 4650 3800 4450
Wire Wire Line
	3800 4450 4050 4450
Wire Wire Line
	5850 4450 6050 4450
Wire Wire Line
	6050 4450 6050 4650
Wire Wire Line
	4350 5400 4350 4650
Wire Wire Line
	5550 5400 5550 4650
Wire Wire Line
	4650 5600 5250 5600
Wire Wire Line
	4350 5150 4750 5150
Wire Wire Line
	4750 5150 4750 5600
Connection ~ 4750 5600
Connection ~ 4350 5150
Wire Wire Line
	3800 5050 3800 6050
Wire Wire Line
	3800 6050 8100 6050
Wire Wire Line
	4350 6050 4350 5800
Wire Wire Line
	7850 3700 7850 5150
Wire Wire Line
	7500 4600 7500 4500
Wire Wire Line
	7500 4500 7850 4500
Connection ~ 7850 4500
Wire Wire Line
	7050 4550 7050 5400
Wire Wire Line
	7200 4800 7050 4800
Connection ~ 7050 4800
Wire Wire Line
	7500 5000 7500 5350
Wire Wire Line
	7500 5350 7550 5350
Wire Wire Line
	7850 6050 7850 5550
Connection ~ 4350 6050
Wire Wire Line
	5550 5800 5550 6050
Connection ~ 5550 6050
Wire Wire Line
	6050 5050 6050 6050
Connection ~ 6050 6050
$Comp
L resistor R6
U 1 1 64205A0B
P 6300 5350
F 0 "R6" H 6350 5480 50  0000 C CNN
F 1 "50k" H 6350 5300 50  0000 C CNN
F 2 "" H 6350 5330 30  0000 C CNN
F 3 "" V 6350 5400 30  0000 C CNN
	1    6300 5350
	0    1    1    0   
$EndComp
Wire Wire Line
	6350 4850 6350 5250
Wire Wire Line
	6750 5600 5750 5600
Wire Wire Line
	5750 5600 5750 5200
Wire Wire Line
	5750 5200 5550 5200
Connection ~ 5550 5200
Wire Wire Line
	6350 5550 6350 6050
Connection ~ 6350 6050
$Comp
L resistor R7
U 1 1 64205F94
P 7000 3050
F 0 "R7" H 7050 3180 50  0000 C CNN
F 1 "5k" H 7050 3000 50  0000 C CNN
F 2 "" H 7050 3030 30  0000 C CNN
F 3 "" V 7050 3100 30  0000 C CNN
	1    7000 3050
	0    1    1    0   
$EndComp
Wire Wire Line
	4350 2950 4350 2700
Wire Wire Line
	4350 2700 8100 2700
Wire Wire Line
	7850 2700 7850 3300
Wire Wire Line
	7050 2950 7050 2700
Connection ~ 7050 2700
Wire Wire Line
	4350 3250 4350 3450
Wire Wire Line
	7050 3250 7050 3500
Wire Wire Line
	7050 3500 7550 3500
Connection ~ 7850 4000
Wire Wire Line
	7050 5800 7050 6050
Connection ~ 7050 6050
$Comp
L PORT U1
U 2 1 64207110
P 3850 3350
F 0 "U1" H 3900 3450 30  0000 C CNN
F 1 "PORT" H 3850 3350 30  0000 C CNN
F 2 "" H 3850 3350 60  0000 C CNN
F 3 "" H 3850 3350 60  0000 C CNN
	2    3850 3350
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 1 1 6420714F
P 3050 4850
F 0 "U1" H 3100 4950 30  0000 C CNN
F 1 "PORT" H 3050 4850 30  0000 C CNN
F 2 "" H 3050 4850 60  0000 C CNN
F 3 "" H 3050 4850 60  0000 C CNN
	1    3050 4850
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 6 1 642071DE
P 8350 2700
F 0 "U1" H 8400 2800 30  0000 C CNN
F 1 "PORT" H 8350 2700 30  0000 C CNN
F 2 "" H 8350 2700 60  0000 C CNN
F 3 "" H 8350 2700 60  0000 C CNN
	6    8350 2700
	-1   0    0    1   
$EndComp
$Comp
L PORT U1
U 7 1 64207223
P 8350 4000
F 0 "U1" H 8400 4100 30  0000 C CNN
F 1 "PORT" H 8350 4000 30  0000 C CNN
F 2 "" H 8350 4000 60  0000 C CNN
F 3 "" H 8350 4000 60  0000 C CNN
	7    8350 4000
	-1   0    0    1   
$EndComp
$Comp
L PORT U1
U 8 1 6420728A
P 8350 6050
F 0 "U1" H 8400 6150 30  0000 C CNN
F 1 "PORT" H 8350 6050 30  0000 C CNN
F 2 "" H 8350 6050 60  0000 C CNN
F 3 "" H 8350 6050 60  0000 C CNN
	8    8350 6050
	-1   0    0    1   
$EndComp
$Comp
L PORT U1
U 3 1 6420731D
P 4950 3600
F 0 "U1" H 5000 3700 30  0000 C CNN
F 1 "PORT" H 4950 3600 30  0000 C CNN
F 2 "" H 4950 3600 60  0000 C CNN
F 3 "" H 4950 3600 60  0000 C CNN
	3    4950 3600
	0    1    1    0   
$EndComp
$Comp
L PORT U1
U 4 1 6420736E
P 5550 3600
F 0 "U1" H 5600 3700 30  0000 C CNN
F 1 "PORT" H 5550 3600 30  0000 C CNN
F 2 "" H 5550 3600 60  0000 C CNN
F 3 "" H 5550 3600 60  0000 C CNN
	4    5550 3600
	0    1    1    0   
$EndComp
Connection ~ 7850 6050
Wire Wire Line
	4950 3850 4950 4000
Connection ~ 4950 4000
Wire Wire Line
	3300 4850 3500 4850
Wire Wire Line
	4100 3350 4350 3350
Connection ~ 4350 3350
Connection ~ 7850 2700
$Comp
L PORT U1
U 5 1 6420A0F6
P 6750 4850
F 0 "U1" H 6800 4950 30  0000 C CNN
F 1 "PORT" H 6750 4850 30  0000 C CNN
F 2 "" H 6750 4850 60  0000 C CNN
F 3 "" H 6750 4850 60  0000 C CNN
	5    6750 4850
	-1   0    0    1   
$EndComp
Wire Wire Line
	6500 4850 6350 4850
$EndSCHEMATC
