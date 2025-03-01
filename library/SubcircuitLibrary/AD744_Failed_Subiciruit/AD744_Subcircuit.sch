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
LIBS:AD744_Subcircuit-cache
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
L dc I1
U 1 1 675D32E0
P 2650 1450
F 0 "I1" H 2450 1550 60  0000 C CNN
F 1 "400uA" H 2450 1400 60  0000 C CNN
F 2 "R1" H 2350 1450 60  0000 C CNN
F 3 "" H 2650 1450 60  0000 C CNN
	1    2650 1450
	-1   0    0    1   
$EndComp
$Comp
L resistor R1
U 1 1 675D3313
P 2200 2550
F 0 "R1" H 2250 2680 50  0000 C CNN
F 1 "300" H 2250 2500 50  0000 C CNN
F 2 "" H 2250 2530 30  0000 C CNN
F 3 "" V 2250 2600 30  0000 C CNN
	1    2200 2550
	0    1    1    0   
$EndComp
$Comp
L resistor R3
U 1 1 675D3334
P 3000 2550
F 0 "R3" H 3050 2680 50  0000 C CNN
F 1 "300" H 3050 2500 50  0000 C CNN
F 2 "" H 3050 2530 30  0000 C CNN
F 3 "" V 3050 2600 30  0000 C CNN
	1    3000 2550
	0    1    1    0   
$EndComp
$Comp
L resistor R2
U 1 1 675D33EF
P 2200 5950
F 0 "R2" H 2250 6080 50  0000 C CNN
F 1 "1k" H 2250 5900 50  0000 C CNN
F 2 "" H 2250 5930 30  0000 C CNN
F 3 "" V 2250 6000 30  0000 C CNN
	1    2200 5950
	0    1    1    0   
$EndComp
$Comp
L eSim_NPN Q2
U 1 1 675D34CD
P 2950 4700
F 0 "Q2" H 2850 4750 50  0000 R CNN
F 1 "eSim_NPN" H 2900 4850 50  0000 R CNN
F 2 "" H 3150 4800 29  0000 C CNN
F 3 "" H 2950 4700 60  0000 C CNN
	1    2950 4700
	1    0    0    -1  
$EndComp
$Comp
L resistor R4
U 1 1 675D3518
P 3000 5950
F 0 "R4" H 3050 6080 50  0000 C CNN
F 1 "1k" H 3050 5900 50  0000 C CNN
F 2 "" H 3050 5930 30  0000 C CNN
F 3 "" V 3050 6000 30  0000 C CNN
	1    3000 5950
	0    1    1    0   
$EndComp
$Comp
L eSim_NPN Q4
U 1 1 675D35FA
P 5500 4750
F 0 "Q4" H 5400 4800 50  0000 R CNN
F 1 "eSim_NPN" H 5450 4900 50  0000 R CNN
F 2 "" H 5700 4850 29  0000 C CNN
F 3 "" H 5500 4750 60  0000 C CNN
	1    5500 4750
	1    0    0    -1  
$EndComp
$Comp
L capacitor C1
U 1 1 675D3664
P 6100 4150
F 0 "C1" H 6125 4250 50  0000 L CNN
F 1 "5pF" H 6125 4050 50  0000 L CNN
F 2 "" H 6138 4000 30  0000 C CNN
F 3 "" H 6100 4150 60  0000 C CNN
	1    6100 4150
	0    1    1    0   
$EndComp
$Comp
L eSim_NPN Q5
U 1 1 675D36DD
P 6500 5300
F 0 "Q5" H 6400 5350 50  0000 R CNN
F 1 "eSim_NPN" H 6450 5450 50  0000 R CNN
F 2 "" H 6700 5400 29  0000 C CNN
F 3 "" H 6500 5300 60  0000 C CNN
	1    6500 5300
	1    0    0    -1  
$EndComp
$Comp
L resistor R5
U 1 1 675D3759
P 5550 5950
F 0 "R5" H 5600 6080 50  0000 C CNN
F 1 "8k" H 5600 5900 50  0000 C CNN
F 2 "" H 5600 5930 30  0000 C CNN
F 3 "" V 5600 6000 30  0000 C CNN
	1    5550 5950
	0    1    1    0   
$EndComp
$Comp
L dc I2
U 1 1 675D37F9
P 7100 1450
F 0 "I2" H 6900 1550 60  0000 C CNN
F 1 "2mA" H 6900 1400 60  0000 C CNN
F 2 "R1" H 6800 1450 60  0000 C CNN
F 3 "" H 7100 1450 60  0000 C CNN
	1    7100 1450
	-1   0    0    1   
$EndComp
$Comp
L eSim_Diode D1
U 1 1 675D38D8
P 2250 5200
F 0 "D1" H 2250 5300 50  0000 C CNN
F 1 "eSim_Diode" H 2250 5100 50  0000 C CNN
F 2 "" H 2250 5200 60  0000 C CNN
F 3 "" H 2250 5200 60  0000 C CNN
	1    2250 5200
	0    1    1    0   
$EndComp
$Comp
L eSim_Diode D2
U 1 1 675D3987
P 7100 2600
F 0 "D2" H 7100 2700 50  0000 C CNN
F 1 "eSim_Diode" H 7100 2500 50  0000 C CNN
F 2 "" H 7100 2600 60  0000 C CNN
F 3 "" H 7100 2600 60  0000 C CNN
	1    7100 2600
	0    1    1    0   
$EndComp
$Comp
L eSim_Diode D3
U 1 1 675D39DB
P 7100 3300
F 0 "D3" H 7100 3400 50  0000 C CNN
F 1 "eSim_Diode" H 7100 3200 50  0000 C CNN
F 2 "" H 7100 3300 60  0000 C CNN
F 3 "" H 7100 3300 60  0000 C CNN
	1    7100 3300
	0    1    1    0   
$EndComp
$Comp
L eSim_PNP Q7
U 1 1 675D3A5D
P 7900 4300
F 0 "Q7" H 7800 4350 50  0000 R CNN
F 1 "eSim_PNP" H 7850 4450 50  0000 R CNN
F 2 "" H 8100 4400 29  0000 C CNN
F 3 "" H 7900 4300 60  0000 C CNN
	1    7900 4300
	1    0    0    1   
$EndComp
$Comp
L eSim_NPN Q6
U 1 1 675D3ACF
P 7900 2850
F 0 "Q6" H 7800 2900 50  0000 R CNN
F 1 "eSim_NPN" H 7850 3000 50  0000 R CNN
F 2 "" H 8100 2950 29  0000 C CNN
F 3 "" H 7900 2850 60  0000 C CNN
	1    7900 2850
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 1 1 675D3B54
P 1100 3650
F 0 "U1" H 1150 3750 30  0000 C CNN
F 1 "PORT" H 1100 3650 30  0000 C CNN
F 2 "" H 1100 3650 60  0000 C CNN
F 3 "" H 1100 3650 60  0000 C CNN
	1    1100 3650
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 4 1 675D3C0E
P 4150 3650
F 0 "U1" H 4200 3750 30  0000 C CNN
F 1 "PORT" H 4150 3650 30  0000 C CNN
F 2 "" H 4150 3650 60  0000 C CNN
F 3 "" H 4150 3650 60  0000 C CNN
	4    4150 3650
	-1   0    0    1   
$EndComp
$Comp
L PORT U1
U 2 1 675D3CE7
P 1100 4100
F 0 "U1" H 1150 4200 30  0000 C CNN
F 1 "PORT" H 1100 4100 30  0000 C CNN
F 2 "" H 1100 4100 60  0000 C CNN
F 3 "" H 1100 4100 60  0000 C CNN
	2    1100 4100
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 3 1 675D3E3D
P 1100 4800
F 0 "U1" H 1150 4900 30  0000 C CNN
F 1 "PORT" H 1100 4800 30  0000 C CNN
F 2 "" H 1100 4800 60  0000 C CNN
F 3 "" H 1100 4800 60  0000 C CNN
	3    1100 4800
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 5 1 675D4098
P 8850 700
F 0 "U1" H 8900 800 30  0000 C CNN
F 1 "PORT" H 8850 700 30  0000 C CNN
F 2 "" H 8850 700 60  0000 C CNN
F 3 "" H 8850 700 60  0000 C CNN
	5    8850 700 
	-1   0    0    1   
$EndComp
$Comp
L PORT U1
U 6 1 675D427B
P 8900 3550
F 0 "U1" H 8950 3650 30  0000 C CNN
F 1 "PORT" H 8900 3550 30  0000 C CNN
F 2 "" H 8900 3550 60  0000 C CNN
F 3 "" H 8900 3550 60  0000 C CNN
	6    8900 3550
	-1   0    0    1   
$EndComp
$Comp
L PORT U1
U 7 1 675D4484
P 8900 4950
F 0 "U1" H 8950 5050 30  0000 C CNN
F 1 "PORT" H 8900 4950 30  0000 C CNN
F 2 "" H 8900 4950 60  0000 C CNN
F 3 "" H 8900 4950 60  0000 C CNN
	7    8900 4950
	-1   0    0    1   
$EndComp
$Comp
L PORT U1
U 8 1 675D48E8
P 8900 6400
F 0 "U1" H 8950 6500 30  0000 C CNN
F 1 "PORT" H 8900 6400 30  0000 C CNN
F 2 "" H 8900 6400 60  0000 C CNN
F 3 "" H 8900 6400 60  0000 C CNN
	8    8900 6400
	-1   0    0    1   
$EndComp
Wire Wire Line
	8600 700  2650 700 
Wire Wire Line
	2650 700  2650 1000
Wire Wire Line
	2250 2450 2250 2150
Wire Wire Line
	2250 2150 3050 2150
Wire Wire Line
	3050 2150 3050 2450
Wire Wire Line
	2650 1900 2650 2150
Connection ~ 2650 2150
Wire Wire Line
	2250 2750 2250 3450
Wire Wire Line
	2250 3850 2250 5050
Wire Wire Line
	3050 3850 3050 4500
Wire Wire Line
	2750 4700 1400 4700
Wire Wire Line
	1400 4700 1400 4800
Wire Wire Line
	1400 4800 1350 4800
Wire Wire Line
	2250 5850 2250 5350
Wire Wire Line
	3050 5850 3050 4900
Wire Wire Line
	8650 6400 2250 6400
Wire Wire Line
	2250 6400 2250 6150
Wire Wire Line
	1350 3650 1950 3650
Wire Wire Line
	3900 3650 3350 3650
Wire Wire Line
	3050 2750 3050 3450
Wire Wire Line
	5950 4150 1450 4150
Wire Wire Line
	1450 4150 1450 4100
Wire Wire Line
	1450 4100 1350 4100
Wire Wire Line
	3050 6150 3050 6400
Connection ~ 3050 6400
Wire Wire Line
	5300 4750 4150 4750
Wire Wire Line
	4150 4750 4150 4350
Wire Wire Line
	4150 4350 3050 4350
Connection ~ 3050 4350
Wire Wire Line
	5600 4550 5600 700 
Connection ~ 5600 700 
Wire Wire Line
	5600 5850 5600 4950
Wire Wire Line
	5600 6150 5600 6400
Connection ~ 5600 6400
Wire Wire Line
	6250 4150 6600 4150
Wire Wire Line
	6600 4150 6600 5100
Wire Wire Line
	6300 5300 5600 5300
Connection ~ 5600 5300
Wire Wire Line
	7700 4300 6600 4300
Connection ~ 6600 4300
Wire Wire Line
	7100 3450 7100 4950
Connection ~ 7100 4300
Wire Wire Line
	7100 2750 7100 3150
Wire Wire Line
	7100 1900 7100 2450
Wire Wire Line
	7100 1000 7100 700 
Connection ~ 7100 700 
Wire Wire Line
	7100 4950 8650 4950
Wire Wire Line
	8000 4100 8000 3050
Wire Wire Line
	8650 3550 8000 3550
Connection ~ 8000 3550
Wire Wire Line
	8000 2650 8000 700 
Connection ~ 8000 700 
Wire Wire Line
	8000 4500 8000 6400
Connection ~ 8000 6400
Wire Wire Line
	7700 2850 7700 2150
Wire Wire Line
	7700 2150 7100 2150
Connection ~ 7100 2150
Wire Wire Line
	6600 5500 6600 6400
Connection ~ 6600 6400
$Comp
L eSim_NPN Q3
U 1 1 675D339B
P 3150 3650
F 0 "Q3" H 3050 3700 50  0000 R CNN
F 1 "eSim_NPN" H 3100 3800 50  0000 R CNN
F 2 "" H 3350 3750 29  0000 C CNN
F 3 "" H 3150 3650 60  0000 C CNN
	1    3150 3650
	-1   0    0    -1  
$EndComp
$Comp
L eSim_NPN Q1
U 1 1 675D3372
P 2150 3650
F 0 "Q1" H 2050 3700 50  0000 R CNN
F 1 "eSim_NPN" H 2100 3800 50  0000 R CNN
F 2 "" H 2350 3750 29  0000 C CNN
F 3 "" H 2150 3650 60  0000 C CNN
	1    2150 3650
	1    0    0    -1  
$EndComp
$EndSCHEMATC
