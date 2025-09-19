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
LIBS:M5223_My-cache
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
L eSim_NPN Q4
U 1 1 683DAB4D
P 4500 4850
F 0 "Q4" H 4400 4900 50  0000 R CNN
F 1 "eSim_NPN" H 4450 5000 50  0000 R CNN
F 2 "" H 4700 4950 29  0000 C CNN
F 3 "" H 4500 4850 60  0000 C CNN
	1    4500 4850
	1    0    0    -1  
$EndComp
$Comp
L eSim_PNP Q2
U 1 1 683DABA1
P 3550 2850
F 0 "Q2" H 3450 2900 50  0000 R CNN
F 1 "eSim_PNP" H 3500 3000 50  0000 R CNN
F 2 "" H 3750 2950 29  0000 C CNN
F 3 "" H 3550 2850 60  0000 C CNN
	1    3550 2850
	1    0    0    1   
$EndComp
$Comp
L eSim_PNP Q1
U 1 1 683DABE1
P 3100 3300
F 0 "Q1" H 3000 3350 50  0000 R CNN
F 1 "eSim_PNP" H 3050 3450 50  0000 R CNN
F 2 "" H 3300 3400 29  0000 C CNN
F 3 "" H 3100 3300 60  0000 C CNN
	1    3100 3300
	1    0    0    1   
$EndComp
$Comp
L eSim_PNP Q5
U 1 1 683DABFE
P 4650 2850
F 0 "Q5" H 4550 2900 50  0000 R CNN
F 1 "eSim_PNP" H 4600 3000 50  0000 R CNN
F 2 "" H 4850 2950 29  0000 C CNN
F 3 "" H 4650 2850 60  0000 C CNN
	1    4650 2850
	-1   0    0    1   
$EndComp
$Comp
L eSim_PNP Q6
U 1 1 683DAC31
P 5050 3300
F 0 "Q6" H 4950 3350 50  0000 R CNN
F 1 "eSim_PNP" H 5000 3450 50  0000 R CNN
F 2 "" H 5250 3400 29  0000 C CNN
F 3 "" H 5050 3300 60  0000 C CNN
	1    5050 3300
	-1   0    0    1   
$EndComp
$Comp
L eSim_NPN Q3
U 1 1 683DACF6
P 3800 4850
F 0 "Q3" H 3700 4900 50  0000 R CNN
F 1 "eSim_NPN" H 3750 5000 50  0000 R CNN
F 2 "" H 4000 4950 29  0000 C CNN
F 3 "" H 3800 4850 60  0000 C CNN
	1    3800 4850
	-1   0    0    -1  
$EndComp
$Comp
L eSim_GND #PWR01
U 1 1 683DAE76
P 3200 3600
F 0 "#PWR01" H 3200 3350 50  0001 C CNN
F 1 "eSim_GND" H 3200 3450 50  0000 C CNN
F 2 "" H 3200 3600 50  0001 C CNN
F 3 "" H 3200 3600 50  0001 C CNN
	1    3200 3600
	1    0    0    -1  
$EndComp
$Comp
L eSim_GND #PWR02
U 1 1 683DAE9A
P 4950 3600
F 0 "#PWR02" H 4950 3350 50  0001 C CNN
F 1 "eSim_GND" H 4950 3450 50  0000 C CNN
F 2 "" H 4950 3600 50  0001 C CNN
F 3 "" H 4950 3600 50  0001 C CNN
	1    4950 3600
	1    0    0    -1  
$EndComp
$Comp
L dc I1
U 1 1 683DAF62
P 4150 1950
F 0 "I1" H 3950 2050 60  0000 C CNN
F 1 "dc" H 3950 1900 60  0000 C CNN
F 2 "R1" H 3850 1950 60  0000 C CNN
F 3 "" H 4150 1950 60  0000 C CNN
	1    4150 1950
	1    0    0    -1  
$EndComp
$Comp
L eSim_NPN Q11
U 1 1 683DB0D0
P 7800 2700
F 0 "Q11" H 7700 2750 50  0000 R CNN
F 1 "eSim_NPN" H 7750 2850 50  0000 R CNN
F 2 "" H 8000 2800 29  0000 C CNN
F 3 "" H 7800 2700 60  0000 C CNN
	1    7800 2700
	1    0    0    -1  
$EndComp
$Comp
L eSim_NPN Q12
U 1 1 683DB150
P 8200 3000
F 0 "Q12" H 8100 3050 50  0000 R CNN
F 1 "eSim_NPN" H 8150 3150 50  0000 R CNN
F 2 "" H 8400 3100 29  0000 C CNN
F 3 "" H 8200 3000 60  0000 C CNN
	1    8200 3000
	1    0    0    -1  
$EndComp
$Comp
L eSim_PNP Q7
U 1 1 683DB25B
P 5450 4450
F 0 "Q7" H 5350 4500 50  0000 R CNN
F 1 "eSim_PNP" H 5400 4600 50  0000 R CNN
F 2 "" H 5650 4550 29  0000 C CNN
F 3 "" H 5450 4450 60  0000 C CNN
	1    5450 4450
	1    0    0    1   
$EndComp
$Comp
L eSim_NPN Q8
U 1 1 683DB381
P 6500 3850
F 0 "Q8" H 6400 3900 50  0000 R CNN
F 1 "eSim_NPN" H 6450 4000 50  0000 R CNN
F 2 "" H 6700 3950 29  0000 C CNN
F 3 "" H 6500 3850 60  0000 C CNN
	1    6500 3850
	1    0    0    -1  
$EndComp
$Comp
L eSim_NPN Q9
U 1 1 683DB3D6
P 6950 4100
F 0 "Q9" H 6850 4150 50  0000 R CNN
F 1 "eSim_NPN" H 6900 4250 50  0000 R CNN
F 2 "" H 7150 4200 29  0000 C CNN
F 3 "" H 6950 4100 60  0000 C CNN
	1    6950 4100
	1    0    0    -1  
$EndComp
$Comp
L dc I2
U 1 1 683DB4B0
P 5550 2100
F 0 "I2" H 5350 2200 60  0000 C CNN
F 1 "dc" H 5350 2050 60  0000 C CNN
F 2 "R1" H 5250 2100 60  0000 C CNN
F 3 "" H 5550 2100 60  0000 C CNN
	1    5550 2100
	1    0    0    -1  
$EndComp
$Comp
L dc I3
U 1 1 683DB798
P 7000 2100
F 0 "I3" H 6800 2200 60  0000 C CNN
F 1 "dc" H 6800 2050 60  0000 C CNN
F 2 "R1" H 6700 2100 60  0000 C CNN
F 3 "" H 7000 2100 60  0000 C CNN
	1    7000 2100
	1    0    0    -1  
$EndComp
$Comp
L eSim_NPN Q10
U 1 1 683DBB6B
P 7750 3400
F 0 "Q10" H 7650 3450 50  0000 R CNN
F 1 "eSim_NPN" H 7700 3550 50  0000 R CNN
F 2 "" H 7950 3500 29  0000 C CNN
F 3 "" H 7750 3400 60  0000 C CNN
	1    7750 3400
	-1   0    0    -1  
$EndComp
$Comp
L dc I4
U 1 1 683DBD28
P 7650 4400
F 0 "I4" H 7450 4500 60  0000 C CNN
F 1 "dc" H 7450 4350 60  0000 C CNN
F 2 "R1" H 7350 4400 60  0000 C CNN
F 3 "" H 7650 4400 60  0000 C CNN
	1    7650 4400
	1    0    0    -1  
$EndComp
$Comp
L eSim_PNP Q13
U 1 1 683DBED0
P 8200 3900
F 0 "Q13" H 8100 3950 50  0000 R CNN
F 1 "eSim_PNP" H 8150 4050 50  0000 R CNN
F 2 "" H 8400 4000 29  0000 C CNN
F 3 "" H 8200 3900 60  0000 C CNN
	1    8200 3900
	1    0    0    1   
$EndComp
$Comp
L resistor R3
U 1 1 683DBF22
P 8400 3450
F 0 "R3" H 8450 3580 50  0000 C CNN
F 1 "500" H 8450 3400 50  0000 C CNN
F 2 "" H 8450 3430 30  0000 C CNN
F 3 "" V 8450 3500 30  0000 C CNN
	1    8400 3450
	0    1    1    0   
$EndComp
$Comp
L capacitor C1
U 1 1 683DB935
P 5400 2900
F 0 "C1" H 5425 3000 50  0000 L CNN
F 1 "15p" H 5425 2800 50  0000 L CNN
F 2 "" H 5438 2750 30  0000 C CNN
F 3 "" H 5400 2900 60  0000 C CNN
	1    5400 2900
	1    0    0    -1  
$EndComp
Wire Wire Line
	3650 3050 3650 4650
Wire Wire Line
	3650 4650 3700 4650
Wire Wire Line
	4550 3050 4550 4650
Wire Wire Line
	4550 4650 4600 4650
Wire Wire Line
	4000 4850 4300 4850
Wire Wire Line
	4150 4850 4150 4350
Wire Wire Line
	4150 4350 3650 4350
Connection ~ 3650 4350
Connection ~ 4150 4850
Wire Wire Line
	3350 2850 3200 2850
Wire Wire Line
	3200 2850 3200 3100
Wire Wire Line
	4850 2850 4950 2850
Wire Wire Line
	4950 2850 4950 3100
Wire Wire Line
	3200 3500 3200 3600
Wire Wire Line
	4950 3500 4950 3600
Wire Wire Line
	3650 2650 4550 2650
Wire Wire Line
	4150 2400 4150 2650
Connection ~ 4150 2650
Wire Wire Line
	1700 3300 2900 3300
Wire Wire Line
	5250 4050 5250 3300
Wire Wire Line
	7900 2900 7900 3000
Wire Wire Line
	7900 3000 8000 3000
Wire Wire Line
	8300 1500 8300 2800
Wire Wire Line
	5250 4450 4550 4450
Connection ~ 4550 4450
Wire Wire Line
	3700 5050 8300 5050
Wire Wire Line
	5550 5050 5550 4650
Connection ~ 4600 5050
Wire Wire Line
	5550 2550 5550 4250
Wire Wire Line
	6300 3850 5550 3850
Connection ~ 5550 3850
Wire Wire Line
	6600 4050 6600 4100
Wire Wire Line
	6600 4100 6750 4100
Wire Wire Line
	7050 5050 7050 4300
Connection ~ 5550 5050
Wire Wire Line
	4150 1500 8300 1500
Wire Wire Line
	5550 1500 5550 1650
Connection ~ 8300 2500
Connection ~ 5550 1500
Wire Wire Line
	6600 1500 6600 3650
Connection ~ 6600 1500
Wire Wire Line
	7000 2550 7000 3900
Wire Wire Line
	7000 3900 8000 3900
Wire Wire Line
	7000 1650 7000 1500
Connection ~ 7000 1500
Wire Wire Line
	5400 3050 5400 4300
Wire Wire Line
	5400 4300 5200 4300
Wire Wire Line
	5200 4300 5200 4450
Connection ~ 5200 4450
Wire Wire Line
	5400 2750 7600 2750
Wire Wire Line
	7600 2750 7600 2700
Wire Wire Line
	8300 3200 8300 3400
Wire Wire Line
	8300 3400 7950 3400
Wire Wire Line
	7650 3200 7000 3200
Connection ~ 7000 3200
Wire Wire Line
	7650 3600 7650 3950
Wire Wire Line
	7650 5050 7650 4850
Connection ~ 7050 5050
Wire Wire Line
	8300 3300 8450 3300
Wire Wire Line
	8450 3300 8450 3350
Connection ~ 8300 3300
Wire Wire Line
	8450 3650 8450 3700
Connection ~ 8450 3700
Connection ~ 8300 3700
Connection ~ 7650 3700
Connection ~ 7050 3900
Wire Wire Line
	8300 5050 8300 4100
Connection ~ 7650 5050
Wire Wire Line
	6300 5050 6300 5350
Connection ~ 6300 5050
Wire Wire Line
	8800 1050 7750 1050
Wire Wire Line
	7750 1050 7750 1500
Connection ~ 7750 1500
Connection ~ 9100 3700
Connection ~ 3200 3550
Connection ~ 9200 3700
Wire Wire Line
	2400 4050 5250 4050
Wire Wire Line
	7650 3700 9500 3700
Wire Wire Line
	7900 2500 7900 1500
Connection ~ 7900 1500
Connection ~ 7000 2750
$Comp
L PORT U?
U 1 1 6840A0F8
P 1450 3300
F 0 "U?" H 1500 3400 30  0000 C CNN
F 1 "PORT" H 1450 3300 30  0000 C CNN
F 2 "" H 1450 3300 60  0000 C CNN
F 3 "" H 1450 3300 60  0000 C CNN
	1    1450 3300
	1    0    0    -1  
$EndComp
$Comp
L PORT U?
U 1 1 6840A1F1
P 2150 4050
F 0 "U?" H 2200 4150 30  0000 C CNN
F 1 "PORT" H 2150 4050 30  0000 C CNN
F 2 "" H 2150 4050 60  0000 C CNN
F 3 "" H 2150 4050 60  0000 C CNN
	1    2150 4050
	1    0    0    -1  
$EndComp
$Comp
L PORT U?
U 1 1 6840A266
P 5950 5350
F 0 "U?" H 6000 5450 30  0000 C CNN
F 1 "PORT" H 5950 5350 30  0000 C CNN
F 2 "" H 5950 5350 60  0000 C CNN
F 3 "" H 5950 5350 60  0000 C CNN
	1    5950 5350
	1    0    0    -1  
$EndComp
$Comp
L PORT U?
U 1 1 6840A3EC
P 9250 3900
F 0 "U?" H 9300 4000 30  0000 C CNN
F 1 "PORT" H 9250 3900 30  0000 C CNN
F 2 "" H 9250 3900 60  0000 C CNN
F 3 "" H 9250 3900 60  0000 C CNN
	1    9250 3900
	1    0    0    -1  
$EndComp
$Comp
L PORT U?
U 1 1 6840A51B
P 8500 1250
F 0 "U?" H 8550 1350 30  0000 C CNN
F 1 "PORT" H 8500 1250 30  0000 C CNN
F 2 "" H 8500 1250 60  0000 C CNN
F 3 "" H 8500 1250 60  0000 C CNN
	1    8500 1250
	1    0    0    -1  
$EndComp
Wire Wire Line
	6300 5350 6200 5350
Wire Wire Line
	9500 3700 9500 3900
Wire Wire Line
	8750 1250 8800 1250
Wire Wire Line
	8800 1250 8800 1050
$EndSCHEMATC
