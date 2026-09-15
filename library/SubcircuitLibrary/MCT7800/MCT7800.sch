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
LIBS:MCT7800-cache
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
U 1 1 683733D3
P 1400 2350
F 0 "R1" H 1450 2480 50  0000 C CNN
F 1 "100" H 1450 2300 50  0000 C CNN
F 2 "" H 1450 2330 30  0000 C CNN
F 3 "" V 1450 2400 30  0000 C CNN
	1    1400 2350
	0    1    1    0   
$EndComp
$Comp
L resistor R2
U 1 1 6837345D
P 2450 2100
F 0 "R2" H 2500 2230 50  0000 C CNN
F 1 "500" H 2500 2050 50  0000 C CNN
F 2 "" H 2500 2080 30  0000 C CNN
F 3 "" V 2500 2150 30  0000 C CNN
	1    2450 2100
	0    1    1    0   
$EndComp
$Comp
L eSim_NPN Q1
U 1 1 683734A6
P 2400 3150
F 0 "Q1" H 2300 3200 50  0000 R CNN
F 1 "eSim_NPN" H 2350 3300 50  0000 R CNN
F 2 "" H 2600 3250 29  0000 C CNN
F 3 "" H 2400 3150 60  0000 C CNN
	1    2400 3150
	1    0    0    -1  
$EndComp
$Comp
L resistor R3
U 1 1 6837359D
P 2450 3850
F 0 "R3" H 2500 3980 50  0000 C CNN
F 1 "3.3K" H 2500 3800 50  0000 C CNN
F 2 "" H 2500 3830 30  0000 C CNN
F 3 "" V 2500 3900 30  0000 C CNN
	1    2450 3850
	0    1    1    0   
$EndComp
$Comp
L resistor R4
U 1 1 683735FC
P 2450 5150
F 0 "R4" H 2500 5280 50  0000 C CNN
F 1 "2.7K" H 2500 5100 50  0000 C CNN
F 2 "" H 2500 5130 30  0000 C CNN
F 3 "" V 2500 5200 30  0000 C CNN
	1    2450 5150
	0    1    1    0   
$EndComp
$Comp
L resistor R5
U 1 1 68373671
P 2450 6300
F 0 "R5" H 2500 6430 50  0000 C CNN
F 1 "500" H 2500 6250 50  0000 C CNN
F 2 "" H 2500 6280 30  0000 C CNN
F 3 "" V 2500 6350 30  0000 C CNN
	1    2450 6300
	0    1    1    0   
$EndComp
$Comp
L eSim_Diode D1
U 1 1 683737CF
P 1450 4400
F 0 "D1" H 1450 4500 50  0000 C CNN
F 1 "eSim_Diode" H 1450 4300 50  0000 C CNN
F 2 "" H 1450 4400 60  0000 C CNN
F 3 "" H 1450 4400 60  0000 C CNN
	1    1450 4400
	0    -1   -1   0   
$EndComp
$Comp
L eSim_PNP Q8
U 1 1 68373CF4
P 5050 1700
F 0 "Q8" H 4950 1750 50  0000 R CNN
F 1 "eSim_PNP" H 5000 1850 50  0000 R CNN
F 2 "" H 5250 1800 29  0000 C CNN
F 3 "" H 5050 1700 60  0000 C CNN
	1    5050 1700
	-1   0    0    1   
$EndComp
$Comp
L eSim_PNP Q12
U 1 1 68373DC1
P 6250 1700
F 0 "Q12" H 6150 1750 50  0000 R CNN
F 1 "eSim_PNP" H 6200 1850 50  0000 R CNN
F 2 "" H 6450 1800 29  0000 C CNN
F 3 "" H 6250 1700 60  0000 C CNN
	1    6250 1700
	1    0    0    1   
$EndComp
$Comp
L resistor R13
U 1 1 68373E8C
P 6300 1150
F 0 "R13" H 6350 1280 50  0000 C CNN
F 1 "100K" H 6350 1100 50  0000 C CNN
F 2 "" H 6350 1130 30  0000 C CNN
F 3 "" V 6350 1200 30  0000 C CNN
	1    6300 1150
	0    1    1    0   
$EndComp
$Comp
L resistor R8
U 1 1 68373EF9
P 4900 1150
F 0 "R8" H 4950 1280 50  0000 C CNN
F 1 "100" H 4950 1100 50  0000 C CNN
F 2 "" H 4950 1130 30  0000 C CNN
F 3 "" V 4950 1200 30  0000 C CNN
	1    4900 1150
	0    1    1    0   
$EndComp
$Comp
L eSim_NPN Q2
U 1 1 683742CA
P 3700 4350
F 0 "Q2" H 3600 4400 50  0000 R CNN
F 1 "eSim_NPN" H 3650 4500 50  0000 R CNN
F 2 "" H 3900 4450 29  0000 C CNN
F 3 "" H 3700 4350 60  0000 C CNN
	1    3700 4350
	1    0    0    -1  
$EndComp
$Comp
L eSim_NPN Q10
U 1 1 6837491E
P 5800 2500
F 0 "Q10" H 5700 2550 50  0000 R CNN
F 1 "eSim_NPN" H 5750 2650 50  0000 R CNN
F 2 "" H 6000 2600 29  0000 C CNN
F 3 "" H 5800 2500 60  0000 C CNN
	1    5800 2500
	1    0    0    -1  
$EndComp
$Comp
L eSim_NPN Q3
U 1 1 68374F77
P 3900 6400
F 0 "Q3" H 3800 6450 50  0000 R CNN
F 1 "eSim_NPN" H 3850 6550 50  0000 R CNN
F 2 "" H 4100 6500 29  0000 C CNN
F 3 "" H 3900 6400 60  0000 C CNN
	1    3900 6400
	-1   0    0    -1  
$EndComp
$Comp
L resistor R6
U 1 1 683753C8
P 3750 5550
F 0 "R6" H 3800 5680 50  0000 C CNN
F 1 "1.4K" H 3800 5500 50  0000 C CNN
F 2 "" H 3800 5530 30  0000 C CNN
F 3 "" V 3800 5600 30  0000 C CNN
	1    3750 5550
	0    1    1    0   
$EndComp
$Comp
L eSim_NPN Q7
U 1 1 683756E3
P 4850 6400
F 0 "Q7" H 4750 6450 50  0000 R CNN
F 1 "eSim_NPN" H 4800 6550 50  0000 R CNN
F 2 "" H 5050 6500 29  0000 C CNN
F 3 "" H 4850 6400 60  0000 C CNN
	1    4850 6400
	1    0    0    -1  
$EndComp
$Comp
L resistor R7
U 1 1 68375756
P 4300 6850
F 0 "R7" H 4350 6980 50  0000 C CNN
F 1 "6.0K" H 4350 6800 50  0000 C CNN
F 2 "" H 4350 6830 30  0000 C CNN
F 3 "" V 4350 6900 30  0000 C CNN
	1    4300 6850
	0    1    1    0   
$EndComp
$Comp
L resistor R11
U 1 1 683757BF
P 4900 6900
F 0 "R11" H 4950 7030 50  0000 C CNN
F 1 "1.0K" H 4950 6850 50  0000 C CNN
F 2 "" H 4950 6880 30  0000 C CNN
F 3 "" V 4950 6950 30  0000 C CNN
	1    4900 6900
	0    1    1    0   
$EndComp
$Comp
L eSim_NPN Q4
U 1 1 68375D06
P 4100 5950
F 0 "Q4" H 4000 6000 50  0000 R CNN
F 1 "eSim_NPN" H 4050 6100 50  0000 R CNN
F 2 "" H 4300 6050 29  0000 C CNN
F 3 "" H 4100 5950 60  0000 C CNN
	1    4100 5950
	1    0    0    -1  
$EndComp
$Comp
L resistor R10
U 1 1 68376041
P 4900 5550
F 0 "R10" H 4950 5680 50  0000 C CNN
F 1 "28K" H 4950 5500 50  0000 C CNN
F 2 "" H 4950 5530 30  0000 C CNN
F 3 "" V 4950 5600 30  0000 C CNN
	1    4900 5550
	0    1    1    0   
$EndComp
$Comp
L resistor R9
U 1 1 68376321
P 4900 5000
F 0 "R9" H 4950 5130 50  0000 C CNN
F 1 "6.0K" H 4950 4950 50  0000 C CNN
F 2 "" H 4950 4980 30  0000 C CNN
F 3 "" V 4950 5050 30  0000 C CNN
	1    4900 5000
	0    1    1    0   
$EndComp
$Comp
L eSim_NPN Q6
U 1 1 683771FE
P 4600 4500
F 0 "Q6" H 4500 4550 50  0000 R CNN
F 1 "eSim_NPN" H 4550 4650 50  0000 R CNN
F 2 "" H 4800 4600 29  0000 C CNN
F 3 "" H 4600 4500 60  0000 C CNN
	1    4600 4500
	-1   0    0    -1  
$EndComp
$Comp
L eSim_NPN Q5
U 1 1 68377293
P 4600 3450
F 0 "Q5" H 4500 3500 50  0000 R CNN
F 1 "eSim_NPN" H 4550 3600 50  0000 R CNN
F 2 "" H 4800 3550 29  0000 C CNN
F 3 "" H 4600 3450 60  0000 C CNN
	1    4600 3450
	-1   0    0    -1  
$EndComp
$Comp
L eSim_NPN Q9
U 1 1 6837732F
P 5050 3950
F 0 "Q9" H 4950 4000 50  0000 R CNN
F 1 "eSim_NPN" H 5000 4100 50  0000 R CNN
F 2 "" H 5250 4050 29  0000 C CNN
F 3 "" H 5050 3950 60  0000 C CNN
	1    5050 3950
	-1   0    0    -1  
$EndComp
$Comp
L capacitor_polarised C1
U 1 1 68378529
P 5500 5850
F 0 "C1" H 5525 5950 50  0000 L CNN
F 1 "30p" H 5525 5750 50  0000 L CNN
F 2 "" H 5500 5850 50  0001 C CNN
F 3 "" H 5500 5850 50  0001 C CNN
	1    5500 5850
	0    -1   -1   0   
$EndComp
$Comp
L eSim_NPN Q11
U 1 1 68378606
P 5850 6150
F 0 "Q11" H 5750 6200 50  0000 R CNN
F 1 "eSim_NPN" H 5800 6300 50  0000 R CNN
F 2 "" H 6050 6250 29  0000 C CNN
F 3 "" H 5850 6150 60  0000 C CNN
	1    5850 6150
	1    0    0    -1  
$EndComp
$Comp
L eSim_PNP Q14
U 1 1 68378E51
P 6550 5150
F 0 "Q14" H 6450 5200 50  0000 R CNN
F 1 "eSim_PNP" H 6500 5300 50  0000 R CNN
F 2 "" H 6750 5250 29  0000 C CNN
F 3 "" H 6550 5150 60  0000 C CNN
	1    6550 5150
	1    0    0    1   
$EndComp
$Comp
L resistor R14
U 1 1 68378EF1
P 6300 4600
F 0 "R14" H 6350 4730 50  0000 C CNN
F 1 "2.0K" H 6350 4550 50  0000 C CNN
F 2 "" H 6350 4580 30  0000 C CNN
F 3 "" V 6350 4650 30  0000 C CNN
	1    6300 4600
	0    1    1    0   
$EndComp
$Comp
L resistor R12
U 1 1 68379769
P 5700 6900
F 0 "R12" H 5750 7030 50  0000 C CNN
F 1 "5.0K" H 5750 6850 50  0000 C CNN
F 2 "" H 5750 6880 30  0000 C CNN
F 3 "" V 5750 6950 30  0000 C CNN
	1    5700 6900
	0    1    1    0   
$EndComp
$Comp
L eSim_NPN Q13
U 1 1 68379995
P 6250 6500
F 0 "Q13" H 6150 6550 50  0000 R CNN
F 1 "eSim_NPN" H 6200 6650 50  0000 R CNN
F 2 "" H 6450 6600 29  0000 C CNN
F 3 "" H 6250 6500 60  0000 C CNN
	1    6250 6500
	1    0    0    -1  
$EndComp
$Comp
L eSim_NPN Q16
U 1 1 6837A706
P 8000 2250
F 0 "Q16" H 7900 2300 50  0000 R CNN
F 1 "eSim_NPN" H 7950 2400 50  0000 R CNN
F 2 "" H 8200 2350 29  0000 C CNN
F 3 "" H 8000 2250 60  0000 C CNN
	1    8000 2250
	1    0    0    -1  
$EndComp
$Comp
L eSim_NPN Q17
U 1 1 6837A79F
P 9450 2600
F 0 "Q17" H 9350 2650 50  0000 R CNN
F 1 "eSim_NPN" H 9400 2750 50  0000 R CNN
F 2 "" H 9650 2700 29  0000 C CNN
F 3 "" H 9450 2600 60  0000 C CNN
	1    9450 2600
	1    0    0    -1  
$EndComp
$Comp
L eSim_Diode D2
U 1 1 6837A926
P 7450 1800
F 0 "D2" H 7450 1900 50  0000 C CNN
F 1 "eSim_Diode" H 7450 1700 50  0000 C CNN
F 2 "" H 7450 1800 60  0000 C CNN
F 3 "" H 7450 1800 60  0000 C CNN
	1    7450 1800
	0    -1   -1   0   
$EndComp
$Comp
L resistor R15
U 1 1 6837AA35
P 7400 1200
F 0 "R15" H 7450 1330 50  0000 C CNN
F 1 "10K" H 7450 1150 50  0000 C CNN
F 2 "" H 7450 1180 30  0000 C CNN
F 3 "" V 7450 1250 30  0000 C CNN
	1    7400 1200
	0    1    1    0   
$EndComp
$Comp
L eSim_NPN Q15
U 1 1 6837AE59
P 7200 2900
F 0 "Q15" H 7100 2950 50  0000 R CNN
F 1 "eSim_NPN" H 7150 3050 50  0000 R CNN
F 2 "" H 7400 3000 29  0000 C CNN
F 3 "" H 7200 2900 60  0000 C CNN
	1    7200 2900
	-1   0    0    -1  
$EndComp
$Comp
L resistor R16
U 1 1 6837B14E
P 8050 3100
F 0 "R16" H 8100 3230 50  0000 C CNN
F 1 "200" H 8100 3050 50  0000 C CNN
F 2 "" H 8100 3080 30  0000 C CNN
F 3 "" V 8100 3150 30  0000 C CNN
	1    8050 3100
	0    1    1    0   
$EndComp
$Comp
L resistor R20
U 1 1 6837B3E1
P 9600 3200
F 0 "R20" H 9650 3330 50  0000 C CNN
F 1 "0.3" H 9650 3150 50  0000 C CNN
F 2 "" H 9650 3180 30  0000 C CNN
F 3 "" V 9650 3250 30  0000 C CNN
	1    9600 3200
	0    -1   -1   0   
$EndComp
$Comp
L resistor R19
U 1 1 6837B589
P 8750 2950
F 0 "R19" H 8800 3080 50  0000 C CNN
F 1 "240" H 8800 2900 50  0000 C CNN
F 2 "" H 8800 2930 30  0000 C CNN
F 3 "" V 8800 3000 30  0000 C CNN
	1    8750 2950
	1    0    0    -1  
$EndComp
$Comp
L resistor R17
U 1 1 6837D366
P 8650 4200
F 0 "R17" H 8700 4330 50  0000 C CNN
F 1 "0.25K" H 8700 4150 50  0000 C CNN
F 2 "" H 8700 4180 30  0000 C CNN
F 3 "" V 8700 4250 30  0000 C CNN
	1    8650 4200
	0    1    1    0   
$EndComp
$Comp
L resistor R18
U 1 1 6837D3FF
P 8650 5500
F 0 "R18" H 8700 5630 50  0000 C CNN
F 1 "5.0K" H 8700 5450 50  0000 C CNN
F 2 "" H 8700 5480 30  0000 C CNN
F 3 "" V 8700 5550 30  0000 C CNN
	1    8650 5500
	0    1    1    0   
$EndComp
Wire Wire Line
	1450 2250 1450 1350
Wire Wire Line
	1450 1350 3900 1350
Wire Wire Line
	2200 3150 1450 3150
Wire Wire Line
	1450 2550 1450 4250
Wire Wire Line
	2500 2950 2500 2300
Wire Wire Line
	2500 1350 2500 2000
Wire Wire Line
	2500 3750 2500 3350
Wire Wire Line
	2500 4050 2500 5050
Wire Wire Line
	2500 5350 2500 6200
Connection ~ 1450 3150
Wire Wire Line
	2500 6500 2500 6700
Wire Wire Line
	1450 6700 1450 4550
Connection ~ 2500 6700
Wire Wire Line
	4950 1050 4950 950 
Wire Wire Line
	4950 1350 4950 1500
Wire Wire Line
	6350 1500 6350 1350
Wire Wire Line
	6350 950  6350 1050
Wire Wire Line
	5250 1700 6050 1700
Wire Wire Line
	3800 2900 3800 4150
Wire Wire Line
	4950 2900 4950 1900
Wire Wire Line
	5650 1700 5650 2100
Wire Wire Line
	5650 2100 4950 2100
Connection ~ 4950 2100
Connection ~ 5650 1700
Wire Wire Line
	3500 4350 2500 4350
Connection ~ 2500 4350
Wire Wire Line
	5900 2300 5900 2200
Wire Wire Line
	5900 2200 6350 2200
Connection ~ 6350 2200
Wire Wire Line
	3000 2500 3000 5800
Wire Wire Line
	3000 5800 2500 5800
Connection ~ 2500 5800
Wire Wire Line
	3150 6700 3150 2700
Connection ~ 3150 6700
Wire Wire Line
	3800 6600 3800 7350
Wire Wire Line
	3800 5750 3800 6200
Wire Wire Line
	3800 4550 3800 5450
Wire Wire Line
	4100 6400 4650 6400
Wire Wire Line
	4350 6750 4350 6400
Connection ~ 4350 6400
Wire Wire Line
	4950 6600 4950 6800
Wire Wire Line
	4950 7350 4950 7100
Wire Wire Line
	4350 7050 4350 7350
Wire Wire Line
	4200 6150 4200 6350
Wire Wire Line
	4200 6350 4250 6350
Wire Wire Line
	4250 6350 4250 6400
Connection ~ 4250 6400
Wire Wire Line
	3900 5950 3800 5950
Connection ~ 3800 5950
Wire Wire Line
	4950 6200 4950 5750
Wire Wire Line
	4950 5200 4950 5450
Wire Wire Line
	3800 5300 4950 5300
Connection ~ 3800 5300
Wire Wire Line
	4200 5750 4200 5300
Connection ~ 4200 5300
Connection ~ 4950 5300
Wire Wire Line
	4950 4900 4950 4150
Wire Wire Line
	4800 4500 4950 4500
Connection ~ 4950 4500
Wire Wire Line
	4500 4300 4500 3650
Wire Wire Line
	3800 2900 4950 2900
Wire Wire Line
	4500 2900 4500 3250
Connection ~ 4500 2900
Wire Wire Line
	3000 2500 5600 2500
Wire Wire Line
	3150 2700 5900 2700
Wire Wire Line
	4800 3450 9950 3450
Wire Wire Line
	4950 3750 4950 3450
Connection ~ 4950 3450
Wire Wire Line
	5250 3950 8000 3950
Wire Wire Line
	8000 3950 8000 5050
Wire Wire Line
	8000 5050 8700 5050
Wire Wire Line
	5350 5850 4950 5850
Connection ~ 4950 5850
Wire Wire Line
	5650 6150 5100 6150
Wire Wire Line
	5100 6150 5100 6050
Wire Wire Line
	5100 6050 4950 6050
Connection ~ 4950 6050
Wire Wire Line
	5650 5850 5850 5850
Wire Wire Line
	5850 5850 5850 5750
Wire Wire Line
	5850 5750 6350 5750
Wire Wire Line
	5950 5950 5950 5750
Connection ~ 5950 5750
Wire Wire Line
	6350 4800 6350 6300
Connection ~ 6350 5150
Wire Wire Line
	6350 1900 6350 4500
Wire Wire Line
	6650 4950 6650 4250
Wire Wire Line
	6650 4250 6350 4250
Connection ~ 6350 4250
Wire Wire Line
	6650 5350 7000 5350
Wire Wire Line
	7000 5350 7000 6350
Wire Wire Line
	5950 6350 5950 6650
Wire Wire Line
	5750 6650 6000 6650
Wire Wire Line
	5750 6650 5750 6800
Connection ~ 6350 5750
Wire Wire Line
	6050 6500 6000 6500
Wire Wire Line
	6000 6500 6000 6650
Connection ~ 5950 6650
Wire Wire Line
	6350 7350 6350 6700
Wire Wire Line
	5750 7350 5750 7100
Wire Wire Line
	3900 1350 3900 950 
Wire Wire Line
	3900 950  9200 950 
Connection ~ 2500 1350
Connection ~ 4950 950 
Wire Wire Line
	9200 950  9200 1000
Connection ~ 6350 950 
Wire Wire Line
	7800 2250 6650 2250
Wire Wire Line
	6650 2250 6650 2050
Wire Wire Line
	6650 2050 6350 2050
Connection ~ 6350 2050
Wire Wire Line
	7100 3100 7100 3450
Connection ~ 7100 3450
Wire Wire Line
	8650 2900 7400 2900
Wire Wire Line
	7450 1950 7450 2800
Wire Wire Line
	7450 2800 7550 2800
Wire Wire Line
	7550 2800 7550 2900
Connection ~ 7550 2900
Wire Wire Line
	7450 1400 7450 1650
Wire Wire Line
	7450 1100 7450 950 
Connection ~ 7450 950 
Wire Wire Line
	8100 2050 8100 950 
Connection ~ 8100 950 
Wire Wire Line
	8100 2450 8100 3000
Wire Wire Line
	8100 3300 8100 3450
Connection ~ 8100 3450
Wire Wire Line
	9550 2800 9550 3000
Wire Wire Line
	9550 3300 9550 3450
Connection ~ 9550 3450
Wire Wire Line
	9250 2600 8100 2600
Connection ~ 8100 2600
Wire Wire Line
	8950 2900 9550 2900
Connection ~ 9550 2900
Wire Wire Line
	9550 2400 9550 1000
Wire Wire Line
	9200 1000 9850 1000
Connection ~ 9550 1000
Wire Wire Line
	8700 4400 8700 5400
Connection ~ 8700 5050
Wire Wire Line
	8700 6350 8700 5700
Wire Wire Line
	8700 4100 8700 3450
Connection ~ 8700 3450
Wire Wire Line
	4500 4700 4500 5300
Connection ~ 4500 5300
Wire Wire Line
	1450 6700 3550 6700
Wire Wire Line
	3550 6700 3550 6900
Wire Wire Line
	3550 6900 3800 6900
Wire Wire Line
	3800 7350 6700 7350
Connection ~ 3800 6900
Connection ~ 4350 7350
Connection ~ 4950 7350
Connection ~ 5750 7350
Wire Wire Line
	6700 7350 6700 6350
Wire Wire Line
	6700 6350 9700 6350
Connection ~ 6350 7350
Connection ~ 7000 6350
Connection ~ 8700 6350
$Comp
L PORT U1
U 2 1 683804D4
P 9950 6350
F 0 "U1" H 10000 6450 30  0000 C CNN
F 1 "PORT" H 9950 6350 30  0000 C CNN
F 2 "" H 9950 6350 60  0000 C CNN
F 3 "" H 9950 6350 60  0000 C CNN
	2    9950 6350
	-1   0    0    1   
$EndComp
$Comp
L PORT U1
U 1 1 6838073F
P 10100 1000
F 0 "U1" H 10150 1100 30  0000 C CNN
F 1 "PORT" H 10100 1000 30  0000 C CNN
F 2 "" H 10100 1000 60  0000 C CNN
F 3 "" H 10100 1000 60  0000 C CNN
	1    10100 1000
	-1   0    0    1   
$EndComp
$Comp
L PORT U1
U 3 1 6838098E
P 10200 3450
F 0 "U1" H 10250 3550 30  0000 C CNN
F 1 "PORT" H 10200 3450 30  0000 C CNN
F 2 "" H 10200 3450 60  0000 C CNN
F 3 "" H 10200 3450 60  0000 C CNN
	3    10200 3450
	-1   0    0    1   
$EndComp
Wire Wire Line
	7100 2700 7100 2250
Connection ~ 7100 2250
$EndSCHEMATC
