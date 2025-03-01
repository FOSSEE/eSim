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
LIBS:sn55461-cache
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
L resistor R3
U 1 1 67B0155B
P 1650 1450
F 0 "R3" H 1700 1580 50  0000 C CNN
F 1 "4k" H 1700 1400 50  0000 C CNN
F 2 "" H 1700 1430 30  0000 C CNN
F 3 "" V 1700 1500 30  0000 C CNN
	1    1650 1450
	0    1    1    0   
$EndComp
$Comp
L resistor R2
U 1 1 67B0157B
P 2850 1350
F 0 "R2" H 2900 1480 50  0000 C CNN
F 1 "1.6k" H 2900 1300 50  0000 C CNN
F 2 "" H 2900 1330 30  0000 C CNN
F 3 "" V 2900 1400 30  0000 C CNN
	1    2850 1350
	0    1    1    0   
$EndComp
$Comp
L resistor R1
U 1 1 67B015B5
P 3850 1300
F 0 "R1" H 3900 1430 50  0000 C CNN
F 1 "130" H 3900 1250 50  0000 C CNN
F 2 "" H 3900 1280 30  0000 C CNN
F 3 "" V 3900 1350 30  0000 C CNN
	1    3850 1300
	0    1    1    0   
$EndComp
$Comp
L eSim_NPN Q4
U 1 1 67B015F3
P 1400 2800
F 0 "Q4" H 1300 2850 50  0000 R CNN
F 1 "eSim_NPN" H 1350 2950 50  0000 R CNN
F 2 "" H 1600 2900 29  0000 C CNN
F 3 "" H 1400 2800 60  0000 C CNN
	1    1400 2800
	0    1    1    0   
$EndComp
$Comp
L eSim_NPN Q5
U 1 1 67B0165A
P 1900 2800
F 0 "Q5" H 1800 2850 50  0000 R CNN
F 1 "eSim_NPN" H 1850 2950 50  0000 R CNN
F 2 "" H 2100 2900 29  0000 C CNN
F 3 "" H 1900 2800 60  0000 C CNN
	1    1900 2800
	0    -1   1    0   
$EndComp
$Comp
L eSim_NPN Q3
U 1 1 67B017E1
P 2850 2750
F 0 "Q3" H 2750 2800 50  0000 R CNN
F 1 "eSim_NPN" H 2800 2900 50  0000 R CNN
F 2 "" H 3050 2850 29  0000 C CNN
F 3 "" H 2850 2750 60  0000 C CNN
	1    2850 2750
	1    0    0    -1  
$EndComp
$Comp
L resistor R8
U 1 1 67B019B4
P 2850 3500
F 0 "R8" H 2900 3630 50  0000 C CNN
F 1 "1k" H 2900 3450 50  0000 C CNN
F 2 "" H 2900 3480 30  0000 C CNN
F 3 "" V 2900 3550 30  0000 C CNN
	1    2850 3500
	0    1    1    0   
$EndComp
$Comp
L eSim_NPN Q1
U 1 1 67B01B07
P 3400 1950
F 0 "Q1" H 3300 2000 50  0000 R CNN
F 1 "eSim_NPN" H 3350 2100 50  0000 R CNN
F 2 "" H 3600 2050 29  0000 C CNN
F 3 "" H 3400 1950 60  0000 C CNN
	1    3400 1950
	1    0    0    -1  
$EndComp
$Comp
L eSim_Diode D3
U 1 1 67B01D8D
P 1000 3700
F 0 "D3" H 1000 3800 50  0000 C CNN
F 1 "eSim_Diode" H 1000 3600 50  0000 C CNN
F 2 "" H 1000 3700 60  0000 C CNN
F 3 "" H 1000 3700 60  0000 C CNN
	1    1000 3700
	0    -1   -1   0   
$EndComp
$Comp
L eSim_Diode D2
U 1 1 67B01EEF
P 2100 3650
F 0 "D2" H 2100 3750 50  0000 C CNN
F 1 "eSim_Diode" H 2100 3550 50  0000 C CNN
F 2 "" H 2100 3650 60  0000 C CNN
F 3 "" H 2100 3650 60  0000 C CNN
	1    2100 3650
	0    -1   -1   0   
$EndComp
$Comp
L eSim_NPN Q6
U 1 1 67B01F4B
P 3500 3150
F 0 "Q6" H 3400 3200 50  0000 R CNN
F 1 "eSim_NPN" H 3450 3300 50  0000 R CNN
F 2 "" H 3700 3250 29  0000 C CNN
F 3 "" H 3500 3150 60  0000 C CNN
	1    3500 3150
	1    0    0    -1  
$EndComp
$Comp
L eSim_Diode D1
U 1 1 67B01FA6
P 3500 2500
F 0 "D1" H 3500 2600 50  0000 C CNN
F 1 "eSim_Diode" H 3500 2400 50  0000 C CNN
F 2 "" H 3500 2500 60  0000 C CNN
F 3 "" H 3500 2500 60  0000 C CNN
	1    3500 2500
	0    1    1    0   
$EndComp
$Comp
L resistor R4
U 1 1 67B02014
P 4100 3150
F 0 "R4" H 4150 3280 50  0000 C CNN
F 1 "500" H 4150 3100 50  0000 C CNN
F 2 "" H 4150 3130 30  0000 C CNN
F 3 "" V 4150 3200 30  0000 C CNN
	1    4100 3150
	0    1    1    0   
$EndComp
$Comp
L eSim_NPN Q2
U 1 1 67B02075
P 4550 2650
F 0 "Q2" H 4450 2700 50  0000 R CNN
F 1 "eSim_NPN" H 4500 2800 50  0000 R CNN
F 2 "" H 4750 2750 29  0000 C CNN
F 3 "" H 4550 2650 60  0000 C CNN
	1    4550 2650
	1    0    0    -1  
$EndComp
$Comp
L GNDPWR #PWR01
U 1 1 67B020E9
P 4500 4500
F 0 "#PWR01" H 4500 4300 50  0001 C CNN
F 1 "GNDPWR" H 4500 4370 50  0000 C CNN
F 2 "" H 4500 4450 50  0001 C CNN
F 3 "" H 4500 4450 50  0001 C CNN
	1    4500 4500
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 2 1 67B022AA
P 5200 2400
F 0 "U1" H 5250 2500 30  0000 C CNN
F 1 "PORT" H 5200 2400 30  0000 C CNN
F 2 "" H 5200 2400 60  0000 C CNN
F 3 "" H 5200 2400 60  0000 C CNN
	2    5200 2400
	-1   0    0    1   
$EndComp
$Comp
L PORT U1
U 3 1 67B0239D
P 600 2950
F 0 "U1" H 650 3050 30  0000 C CNN
F 1 "PORT" H 600 2950 30  0000 C CNN
F 2 "" H 600 2950 60  0000 C CNN
F 3 "" H 600 2950 60  0000 C CNN
	3    600  2950
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 4 1 67B026E1
P 600 3300
F 0 "U1" H 650 3400 30  0000 C CNN
F 1 "PORT" H 600 3300 30  0000 C CNN
F 2 "" H 600 3300 60  0000 C CNN
F 3 "" H 600 3300 60  0000 C CNN
	4    600  3300
	1    0    0    -1  
$EndComp
$Comp
L resistor R7
U 1 1 67B03BE7
P 9650 3400
F 0 "R7" H 9700 3530 50  0000 C CNN
F 1 "4k" H 9700 3350 50  0000 C CNN
F 2 "" H 9700 3380 30  0000 C CNN
F 3 "" V 9700 3450 30  0000 C CNN
	1    9650 3400
	0    -1   1    0   
$EndComp
$Comp
L resistor R6
U 1 1 67B03BED
P 8450 3300
F 0 "R6" H 8500 3430 50  0000 C CNN
F 1 "1.6k" H 8500 3250 50  0000 C CNN
F 2 "" H 8500 3280 30  0000 C CNN
F 3 "" V 8500 3350 30  0000 C CNN
	1    8450 3300
	0    -1   1    0   
$EndComp
$Comp
L resistor R5
U 1 1 67B03BF3
P 7450 3250
F 0 "R5" H 7500 3380 50  0000 C CNN
F 1 "130" H 7500 3200 50  0000 C CNN
F 2 "" H 7500 3230 30  0000 C CNN
F 3 "" V 7500 3300 30  0000 C CNN
	1    7450 3250
	0    -1   1    0   
$EndComp
$Comp
L eSim_NPN Q11
U 1 1 67B03BF9
P 9900 4750
F 0 "Q11" H 9800 4800 50  0000 R CNN
F 1 "eSim_NPN" H 9850 4900 50  0000 R CNN
F 2 "" H 10100 4850 29  0000 C CNN
F 3 "" H 9900 4750 60  0000 C CNN
	1    9900 4750
	0    -1   1    0   
$EndComp
$Comp
L eSim_NPN Q10
U 1 1 67B03BFF
P 9400 4750
F 0 "Q10" H 9300 4800 50  0000 R CNN
F 1 "eSim_NPN" H 9350 4900 50  0000 R CNN
F 2 "" H 9600 4850 29  0000 C CNN
F 3 "" H 9400 4750 60  0000 C CNN
	1    9400 4750
	0    1    1    0   
$EndComp
$Comp
L eSim_NPN Q9
U 1 1 67B03C05
P 8450 4700
F 0 "Q9" H 8350 4750 50  0000 R CNN
F 1 "eSim_NPN" H 8400 4850 50  0000 R CNN
F 2 "" H 8650 4800 29  0000 C CNN
F 3 "" H 8450 4700 60  0000 C CNN
	1    8450 4700
	-1   0    0    -1  
$EndComp
$Comp
L resistor R10
U 1 1 67B03C0B
P 8450 5450
F 0 "R10" H 8500 5580 50  0000 C CNN
F 1 "1k" H 8500 5400 50  0000 C CNN
F 2 "" H 8500 5430 30  0000 C CNN
F 3 "" V 8500 5500 30  0000 C CNN
	1    8450 5450
	0    -1   1    0   
$EndComp
$Comp
L eSim_NPN Q7
U 1 1 67B03C11
P 7900 3900
F 0 "Q7" H 7800 3950 50  0000 R CNN
F 1 "eSim_NPN" H 7850 4050 50  0000 R CNN
F 2 "" H 8100 4000 29  0000 C CNN
F 3 "" H 7900 3900 60  0000 C CNN
	1    7900 3900
	-1   0    0    -1  
$EndComp
$Comp
L eSim_Diode D6
U 1 1 67B03C17
P 10300 5650
F 0 "D6" H 10300 5750 50  0000 C CNN
F 1 "eSim_Diode" H 10300 5550 50  0000 C CNN
F 2 "" H 10300 5650 60  0000 C CNN
F 3 "" H 10300 5650 60  0000 C CNN
	1    10300 5650
	0    1    -1   0   
$EndComp
$Comp
L eSim_Diode D5
U 1 1 67B03C1D
P 9200 5600
F 0 "D5" H 9200 5700 50  0000 C CNN
F 1 "eSim_Diode" H 9200 5500 50  0000 C CNN
F 2 "" H 9200 5600 60  0000 C CNN
F 3 "" H 9200 5600 60  0000 C CNN
	1    9200 5600
	0    1    -1   0   
$EndComp
$Comp
L eSim_NPN Q12
U 1 1 67B03C23
P 7800 5100
F 0 "Q12" H 7700 5150 50  0000 R CNN
F 1 "eSim_NPN" H 7750 5250 50  0000 R CNN
F 2 "" H 8000 5200 29  0000 C CNN
F 3 "" H 7800 5100 60  0000 C CNN
	1    7800 5100
	-1   0    0    -1  
$EndComp
$Comp
L eSim_Diode D4
U 1 1 67B03C29
P 7800 4450
F 0 "D4" H 7800 4550 50  0000 C CNN
F 1 "eSim_Diode" H 7800 4350 50  0000 C CNN
F 2 "" H 7800 4450 60  0000 C CNN
F 3 "" H 7800 4450 60  0000 C CNN
	1    7800 4450
	0    -1   1    0   
$EndComp
$Comp
L resistor R9
U 1 1 67B03C2F
P 7200 5100
F 0 "R9" H 7250 5230 50  0000 C CNN
F 1 "500" H 7250 5050 50  0000 C CNN
F 2 "" H 7250 5080 30  0000 C CNN
F 3 "" V 7250 5150 30  0000 C CNN
	1    7200 5100
	0    -1   1    0   
$EndComp
$Comp
L eSim_NPN Q8
U 1 1 67B03C35
P 6750 4600
F 0 "Q8" H 6650 4650 50  0000 R CNN
F 1 "eSim_NPN" H 6700 4750 50  0000 R CNN
F 2 "" H 6950 4700 29  0000 C CNN
F 3 "" H 6750 4600 60  0000 C CNN
	1    6750 4600
	-1   0    0    -1  
$EndComp
$Comp
L GNDPWR #PWR02
U 1 1 67B03C3B
P 6800 6400
F 0 "#PWR02" H 6800 6200 50  0001 C CNN
F 1 "GNDPWR" H 6800 6270 50  0000 C CNN
F 2 "" H 6800 6350 50  0001 C CNN
F 3 "" H 6800 6350 50  0001 C CNN
	1    6800 6400
	-1   0    0    -1  
$EndComp
$Comp
L PORT U1
U 5 1 67B03C41
P 6100 4350
F 0 "U1" H 6150 4450 30  0000 C CNN
F 1 "PORT" H 6100 4350 30  0000 C CNN
F 2 "" H 6100 4350 60  0000 C CNN
F 3 "" H 6100 4350 60  0000 C CNN
	5    6100 4350
	1    0    0    1   
$EndComp
$Comp
L PORT U1
U 6 1 67B03C47
P 10700 4900
F 0 "U1" H 10750 5000 30  0000 C CNN
F 1 "PORT" H 10700 4900 30  0000 C CNN
F 2 "" H 10700 4900 60  0000 C CNN
F 3 "" H 10700 4900 60  0000 C CNN
	6    10700 4900
	-1   0    0    -1  
$EndComp
$Comp
L PORT U1
U 7 1 67B03C4D
P 10700 5250
F 0 "U1" H 10750 5350 30  0000 C CNN
F 1 "PORT" H 10700 5250 30  0000 C CNN
F 2 "" H 10700 5250 60  0000 C CNN
F 3 "" H 10700 5250 60  0000 C CNN
	7    10700 5250
	-1   0    0    -1  
$EndComp
$Comp
L PORT U1
U 1 1 67B04090
P 8700 1450
F 0 "U1" H 8750 1550 30  0000 C CNN
F 1 "PORT" H 8700 1450 30  0000 C CNN
F 2 "" H 8700 1450 60  0000 C CNN
F 3 "" H 8700 1450 60  0000 C CNN
	1    8700 1450
	-1   0    0    1   
$EndComp
$Comp
L PORT U1
U 8 1 67B0436C
P 5400 4850
F 0 "U1" H 5450 4950 30  0000 C CNN
F 1 "PORT" H 5400 4850 30  0000 C CNN
F 2 "" H 5400 4850 60  0000 C CNN
F 3 "" H 5400 4850 60  0000 C CNN
	8    5400 4850
	-1   0    0    1   
$EndComp
Wire Wire Line
	1600 2900 1700 2900
Wire Wire Line
	1400 2600 1900 2600
Wire Wire Line
	2950 2950 2950 3400
Wire Wire Line
	2950 3400 2900 3400
Wire Wire Line
	2950 1550 2950 2550
Wire Wire Line
	2950 1550 2900 1550
Wire Wire Line
	2950 1950 3200 1950
Connection ~ 2950 1950
Wire Wire Line
	3500 1750 3900 1750
Wire Wire Line
	3900 1750 3900 1500
Wire Wire Line
	2900 1250 2900 1050
Wire Wire Line
	1700 1050 6500 1050
Wire Wire Line
	3900 1050 3900 1200
Wire Wire Line
	1700 1050 1700 1350
Connection ~ 2900 1050
Wire Wire Line
	850  3300 2100 3300
Wire Wire Line
	2100 2900 2100 3500
Connection ~ 2100 3300
Wire Wire Line
	1000 3550 1000 2950
Connection ~ 1000 2950
Wire Wire Line
	1700 1650 1700 2600
Connection ~ 1700 2600
Wire Wire Line
	1200 2950 1200 2900
Wire Wire Line
	850  2950 1200 2950
Wire Wire Line
	1650 2900 1650 3100
Wire Wire Line
	1650 3100 2650 3100
Wire Wire Line
	2650 3100 2650 2750
Connection ~ 1650 2900
Wire Wire Line
	3500 2150 3500 2350
Wire Wire Line
	3500 2650 4350 2650
Wire Wire Line
	3600 2650 3600 2950
Wire Wire Line
	3300 3150 2950 3150
Connection ~ 2950 3150
Connection ~ 3600 2650
Wire Wire Line
	4150 2650 4150 3050
Connection ~ 4150 2650
Wire Wire Line
	4650 2450 4950 2450
Wire Wire Line
	4950 2450 4950 2400
Wire Wire Line
	4650 4100 4650 2850
Wire Wire Line
	1000 4100 4950 4100
Wire Wire Line
	4150 3350 4150 4100
Connection ~ 4650 4100
Wire Wire Line
	3600 3350 3600 4100
Connection ~ 4150 4100
Wire Wire Line
	2900 3700 2900 4100
Connection ~ 3600 4100
Wire Wire Line
	2100 3800 2100 4100
Connection ~ 2900 4100
Wire Wire Line
	1000 3850 1000 4100
Connection ~ 2100 4100
Connection ~ 3900 1050
Wire Wire Line
	9600 4850 9700 4850
Wire Wire Line
	9400 4550 9900 4550
Wire Wire Line
	8350 4900 8350 5350
Wire Wire Line
	8350 5350 8400 5350
Wire Wire Line
	8350 3500 8350 4500
Wire Wire Line
	8350 3500 8400 3500
Wire Wire Line
	8350 3900 8100 3900
Connection ~ 8350 3900
Wire Wire Line
	7800 3700 7400 3700
Wire Wire Line
	7400 3700 7400 3450
Wire Wire Line
	8400 3200 8400 3000
Wire Wire Line
	6150 3000 9600 3000
Wire Wire Line
	7400 3000 7400 3150
Wire Wire Line
	9600 3000 9600 3300
Connection ~ 8400 3000
Wire Wire Line
	10450 5250 9200 5250
Wire Wire Line
	9200 4850 9200 5450
Connection ~ 9200 5250
Wire Wire Line
	10300 5500 10300 4900
Connection ~ 10300 4900
Wire Wire Line
	9600 3600 9600 4550
Connection ~ 9600 4550
Wire Wire Line
	10100 4900 10100 4850
Wire Wire Line
	10100 4900 10450 4900
Wire Wire Line
	9650 4850 9650 5050
Wire Wire Line
	9650 5050 8650 5050
Wire Wire Line
	8650 5050 8650 4700
Connection ~ 9650 4850
Wire Wire Line
	7800 4100 7800 4300
Wire Wire Line
	6950 4600 7800 4600
Wire Wire Line
	7700 4600 7700 4900
Wire Wire Line
	8000 5100 8350 5100
Connection ~ 8350 5100
Connection ~ 7700 4600
Wire Wire Line
	7150 4600 7150 5000
Connection ~ 7150 4600
Wire Wire Line
	6650 4400 6350 4400
Wire Wire Line
	6350 4400 6350 4350
Wire Wire Line
	6650 4800 6650 6050
Wire Wire Line
	4950 6050 10300 6050
Wire Wire Line
	7150 5300 7150 6050
Connection ~ 6650 6050
Wire Wire Line
	6800 6050 6800 6400
Wire Wire Line
	7700 5300 7700 6050
Connection ~ 7150 6050
Wire Wire Line
	8400 5650 8400 6050
Connection ~ 7700 6050
Wire Wire Line
	9200 5750 9200 6050
Connection ~ 8400 6050
Wire Wire Line
	10300 6050 10300 5800
Connection ~ 9200 6050
Connection ~ 7400 3000
Wire Wire Line
	7650 1450 8450 1450
Wire Wire Line
	6500 1050 6500 1300
Wire Wire Line
	4950 4850 5150 4850
Wire Wire Line
	4500 4500 4500 4100
Connection ~ 4500 4100
Connection ~ 6800 6050
Text GLabel 7650 1450 0    60   Input ~ 0
vcc
Text GLabel 6500 1300 3    60   Input ~ 0
vcc
Text GLabel 6150 3000 0    60   Input ~ 0
vcc
Text GLabel 4950 4100 2    60   Input ~ 0
gnd1
Text GLabel 4950 4850 0    60   Input ~ 0
gnd1
Text GLabel 4950 6050 0    60   Input ~ 0
gnd1
$EndSCHEMATC
