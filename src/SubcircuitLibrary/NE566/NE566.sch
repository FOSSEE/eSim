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
LIBS:eSim_Analog
LIBS:eSim_Devices
LIBS:eSim_Digital
LIBS:eSim_Hybrid
LIBS:eSim_Miscellaneous
LIBS:eSim_Plot
LIBS:eSim_Power
LIBS:eSim_PSpice
LIBS:eSim_Sources
LIBS:eSim_Subckt
LIBS:eSim_User
LIBS:NE566-cache
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
U 1 1 5C9D1243
P 1650 1650
F 0 "Q1" H 1550 1700 50  0000 R CNN
F 1 "eSim_NPN" H 1600 1800 50  0000 R CNN
F 2 "" H 1850 1750 29  0000 C CNN
F 3 "" H 1650 1650 60  0000 C CNN
	1    1650 1650
	1    0    0    -1  
$EndComp
$Comp
L eSim_NPN Q2
U 1 1 5C9D1262
P 1850 2450
F 0 "Q2" H 1750 2500 50  0000 R CNN
F 1 "eSim_NPN" H 1800 2600 50  0000 R CNN
F 2 "" H 2050 2550 29  0000 C CNN
F 3 "" H 1850 2450 60  0000 C CNN
	1    1850 2450
	-1   0    0    -1  
$EndComp
$Comp
L eSim_NPN Q5
U 1 1 5C9D1293
P 2650 2450
F 0 "Q5" H 2550 2500 50  0000 R CNN
F 1 "eSim_NPN" H 2600 2600 50  0000 R CNN
F 2 "" H 2850 2550 29  0000 C CNN
F 3 "" H 2650 2450 60  0000 C CNN
	1    2650 2450
	1    0    0    -1  
$EndComp
$Comp
L eSim_Diode D1
U 1 1 5C9D12F5
P 1750 3150
F 0 "D1" H 1750 3250 50  0000 C CNN
F 1 "eSim_Diode" H 1750 3050 50  0000 C CNN
F 2 "" H 1750 3150 60  0000 C CNN
F 3 "" H 1750 3150 60  0000 C CNN
	1    1750 3150
	0    1    1    0   
$EndComp
$Comp
L eSim_Diode D3
U 1 1 5C9D136F
P 2750 3150
F 0 "D3" H 2750 3250 50  0000 C CNN
F 1 "eSim_Diode" H 2750 3050 50  0000 C CNN
F 2 "" H 2750 3150 60  0000 C CNN
F 3 "" H 2750 3150 60  0000 C CNN
	1    2750 3150
	0    1    1    0   
$EndComp
$Comp
L eSim_NPN Q6
U 1 1 5C9D13AA
P 2650 4100
F 0 "Q6" H 2550 4150 50  0000 R CNN
F 1 "eSim_NPN" H 2600 4250 50  0000 R CNN
F 2 "" H 2850 4200 29  0000 C CNN
F 3 "" H 2650 4100 60  0000 C CNN
	1    2650 4100
	1    0    0    -1  
$EndComp
$Comp
L eSim_NPN Q8
U 1 1 5C9D13D9
P 3550 3550
F 0 "Q8" H 3450 3600 50  0000 R CNN
F 1 "eSim_NPN" H 3500 3700 50  0000 R CNN
F 2 "" H 3750 3650 29  0000 C CNN
F 3 "" H 3550 3550 60  0000 C CNN
	1    3550 3550
	1    0    0    -1  
$EndComp
$Comp
L eSim_NPN Q7
U 1 1 5C9D13FE
P 2650 4900
F 0 "Q7" H 2550 4950 50  0000 R CNN
F 1 "eSim_NPN" H 2600 5050 50  0000 R CNN
F 2 "" H 2850 5000 29  0000 C CNN
F 3 "" H 2650 4900 60  0000 C CNN
	1    2650 4900
	1    0    0    -1  
$EndComp
$Comp
L eSim_NPN Q3
U 1 1 5C9D142B
P 1850 4900
F 0 "Q3" H 1750 4950 50  0000 R CNN
F 1 "eSim_NPN" H 1800 5050 50  0000 R CNN
F 2 "" H 2050 5000 29  0000 C CNN
F 3 "" H 1850 4900 60  0000 C CNN
	1    1850 4900
	-1   0    0    -1  
$EndComp
$Comp
L eSim_R R1
U 1 1 5C9D148A
P 1700 5550
F 0 "R1" H 1750 5680 50  0000 C CNN
F 1 "5k" H 1750 5600 50  0000 C CNN
F 2 "" H 1750 5530 30  0000 C CNN
F 3 "" V 1750 5600 30  0000 C CNN
	1    1700 5550
	0    1    1    0   
$EndComp
$Comp
L eSim_R R3
U 1 1 5C9D14C1
P 2700 5500
F 0 "R3" H 2750 5630 50  0000 C CNN
F 1 "5k" H 2750 5550 50  0000 C CNN
F 2 "" H 2750 5480 30  0000 C CNN
F 3 "" V 2750 5550 30  0000 C CNN
	1    2700 5500
	0    1    1    0   
$EndComp
$Comp
L eSim_Diode D4
U 1 1 5C9D153A
P 2750 6100
F 0 "D4" H 2750 6200 50  0000 C CNN
F 1 "eSim_Diode" H 2750 6000 50  0000 C CNN
F 2 "" H 2750 6100 60  0000 C CNN
F 3 "" H 2750 6100 60  0000 C CNN
	1    2750 6100
	0    -1   -1   0   
$EndComp
$Comp
L eSim_NPN Q4
U 1 1 5C9D156F
P 1850 6500
F 0 "Q4" H 1750 6550 50  0000 R CNN
F 1 "eSim_NPN" H 1800 6650 50  0000 R CNN
F 2 "" H 2050 6600 29  0000 C CNN
F 3 "" H 1850 6500 60  0000 C CNN
	1    1850 6500
	-1   0    0    -1  
$EndComp
$Comp
L eSim_Diode D2
U 1 1 5C9D15BE
P 2500 6500
F 0 "D2" H 2500 6600 50  0000 C CNN
F 1 "eSim_Diode" H 2500 6400 50  0000 C CNN
F 2 "" H 2500 6500 60  0000 C CNN
F 3 "" H 2500 6500 60  0000 C CNN
	1    2500 6500
	-1   0    0    1   
$EndComp
$Comp
L eSim_R R2
U 1 1 5C9D1601
P 2150 6750
F 0 "R2" H 2200 6880 50  0000 C CNN
F 1 "5k" H 2200 6800 50  0000 C CNN
F 2 "" H 2200 6730 30  0000 C CNN
F 3 "" V 2200 6800 30  0000 C CNN
	1    2150 6750
	0    1    1    0   
$EndComp
$Comp
L eSim_R R4
U 1 1 5C9D163C
P 3600 6750
F 0 "R4" H 3650 6880 50  0000 C CNN
F 1 "5k" H 3650 6800 50  0000 C CNN
F 2 "" H 3650 6730 30  0000 C CNN
F 3 "" V 3650 6800 30  0000 C CNN
	1    3600 6750
	0    1    1    0   
$EndComp
$Comp
L eSim_NPN Q10
U 1 1 5C9D172D
P 3850 4600
F 0 "Q10" H 3750 4650 50  0000 R CNN
F 1 "eSim_NPN" H 3800 4750 50  0000 R CNN
F 2 "" H 4050 4700 29  0000 C CNN
F 3 "" H 3850 4600 60  0000 C CNN
	1    3850 4600
	1    0    0    -1  
$EndComp
$Comp
L eSim_NPN Q9
U 1 1 5C9D17A2
P 3750 5900
F 0 "Q9" H 3650 5950 50  0000 R CNN
F 1 "eSim_NPN" H 3700 6050 50  0000 R CNN
F 2 "" H 3950 6000 29  0000 C CNN
F 3 "" H 3750 5900 60  0000 C CNN
	1    3750 5900
	-1   0    0    -1  
$EndComp
$Comp
L eSim_NPN Q11
U 1 1 5C9D17FB
P 4600 5900
F 0 "Q11" H 4500 5950 50  0000 R CNN
F 1 "eSim_NPN" H 4550 6050 50  0000 R CNN
F 2 "" H 4800 6000 29  0000 C CNN
F 3 "" H 4600 5900 60  0000 C CNN
	1    4600 5900
	-1   0    0    -1  
$EndComp
$Comp
L eSim_Diode D5
U 1 1 5C9D183E
P 4300 2950
F 0 "D5" H 4300 3050 50  0000 C CNN
F 1 "eSim_Diode" H 4300 2850 50  0000 C CNN
F 2 "" H 4300 2950 60  0000 C CNN
F 3 "" H 4300 2950 60  0000 C CNN
	1    4300 2950
	1    0    0    -1  
$EndComp
$Comp
L eSim_Diode D6
U 1 1 5C9D18B3
P 4300 3950
F 0 "D6" H 4300 4050 50  0000 C CNN
F 1 "eSim_Diode" H 4300 3850 50  0000 C CNN
F 2 "" H 4300 3950 60  0000 C CNN
F 3 "" H 4300 3950 60  0000 C CNN
	1    4300 3950
	1    0    0    -1  
$EndComp
$Comp
L eSim_NPN Q12
U 1 1 5C9D1968
P 4850 3950
F 0 "Q12" H 4750 4000 50  0000 R CNN
F 1 "eSim_NPN" H 4800 4100 50  0000 R CNN
F 2 "" H 5050 4050 29  0000 C CNN
F 3 "" H 4850 3950 60  0000 C CNN
	1    4850 3950
	1    0    0    -1  
$EndComp
$Comp
L eSim_Diode D8
U 1 1 5C9D19B5
P 5150 2350
F 0 "D8" H 5150 2450 50  0000 C CNN
F 1 "eSim_Diode" H 5150 2250 50  0000 C CNN
F 2 "" H 5150 2350 60  0000 C CNN
F 3 "" H 5150 2350 60  0000 C CNN
	1    5150 2350
	1    0    0    -1  
$EndComp
$Comp
L eSim_Diode D7
U 1 1 5C9D1A10
P 5200 3300
F 0 "D7" H 5200 3400 50  0000 C CNN
F 1 "eSim_Diode" H 5200 3200 50  0000 C CNN
F 2 "" H 5200 3300 60  0000 C CNN
F 3 "" H 5200 3300 60  0000 C CNN
	1    5200 3300
	1    0    0    -1  
$EndComp
$Comp
L eSim_R R6
U 1 1 5C9D1A5F
P 4900 1250
F 0 "R6" H 4950 1380 50  0000 C CNN
F 1 "5k" H 4950 1300 50  0000 C CNN
F 2 "" H 4950 1230 30  0000 C CNN
F 3 "" V 4950 1300 30  0000 C CNN
	1    4900 1250
	0    1    1    0   
$EndComp
$Comp
L eSim_R R8
U 1 1 5C9D1ABE
P 5900 1250
F 0 "R8" H 5950 1380 50  0000 C CNN
F 1 "5k" H 5950 1300 50  0000 C CNN
F 2 "" H 5950 1230 30  0000 C CNN
F 3 "" V 5950 1300 30  0000 C CNN
	1    5900 1250
	0    1    1    0   
$EndComp
$Comp
L eSim_NPN Q14
U 1 1 5C9D1B3D
P 6400 1850
F 0 "Q14" H 6300 1900 50  0000 R CNN
F 1 "eSim_NPN" H 6350 2000 50  0000 R CNN
F 2 "" H 6600 1950 29  0000 C CNN
F 3 "" H 6400 1850 60  0000 C CNN
	1    6400 1850
	1    0    0    -1  
$EndComp
$Comp
L eSim_NPN Q13
U 1 1 5C9D1C1E
P 5850 3300
F 0 "Q13" H 5750 3350 50  0000 R CNN
F 1 "eSim_NPN" H 5800 3450 50  0000 R CNN
F 2 "" H 6050 3400 29  0000 C CNN
F 3 "" H 5850 3300 60  0000 C CNN
	1    5850 3300
	1    0    0    -1  
$EndComp
$Comp
L eSim_R R7
U 1 1 5C9D1C7F
P 5450 3550
F 0 "R7" H 5500 3680 50  0000 C CNN
F 1 "5k" H 5500 3600 50  0000 C CNN
F 2 "" H 5500 3530 30  0000 C CNN
F 3 "" V 5500 3600 30  0000 C CNN
	1    5450 3550
	0    1    1    0   
$EndComp
$Comp
L eSim_PNP Q15
U 1 1 5C9D1DA7
P 7100 2750
F 0 "Q15" H 7000 2800 50  0000 R CNN
F 1 "eSim_PNP" H 7050 2900 50  0000 R CNN
F 2 "" H 7300 2850 29  0000 C CNN
F 3 "" H 7100 2750 60  0000 C CNN
	1    7100 2750
	1    0    0    1   
$EndComp
$Comp
L eSim_PNP Q16
U 1 1 5C9D1E16
P 8000 2750
F 0 "Q16" H 7900 2800 50  0000 R CNN
F 1 "eSim_PNP" H 7950 2900 50  0000 R CNN
F 2 "" H 8200 2850 29  0000 C CNN
F 3 "" H 8000 2750 60  0000 C CNN
	1    8000 2750
	-1   0    0    -1  
$EndComp
$Comp
L eSim_PNP Q17
U 1 1 5C9D1EFF
P 8650 2650
F 0 "Q17" H 8550 2700 50  0000 R CNN
F 1 "eSim_PNP" H 8600 2800 50  0000 R CNN
F 2 "" H 8850 2750 29  0000 C CNN
F 3 "" H 8650 2650 60  0000 C CNN
	1    8650 2650
	-1   0    0    1   
$EndComp
$Comp
L eSim_R R13
U 1 1 5C9D1FB4
P 9000 1400
F 0 "R13" H 9050 1530 50  0000 C CNN
F 1 "5k" H 9050 1450 50  0000 C CNN
F 2 "" H 9050 1380 30  0000 C CNN
F 3 "" V 9050 1450 30  0000 C CNN
	1    9000 1400
	0    1    1    0   
$EndComp
$Comp
L eSim_Diode D9
U 1 1 5C9D2065
P 8500 1450
F 0 "D9" H 8500 1550 50  0000 C CNN
F 1 "eSim_Diode" H 8500 1350 50  0000 C CNN
F 2 "" H 8500 1450 60  0000 C CNN
F 3 "" H 8500 1450 60  0000 C CNN
	1    8500 1450
	0    -1   -1   0   
$EndComp
$Comp
L eSim_R R15
U 1 1 5C9D20D8
P 10450 1750
F 0 "R15" H 10500 1880 50  0000 C CNN
F 1 "5k" H 10500 1800 50  0000 C CNN
F 2 "" H 10500 1730 30  0000 C CNN
F 3 "" V 10500 1800 30  0000 C CNN
	1    10450 1750
	0    1    1    0   
$EndComp
$Comp
L eSim_R R12
U 1 1 5C9D215D
P 8500 4200
F 0 "R12" H 8550 4330 50  0000 C CNN
F 1 "5k" H 8550 4250 50  0000 C CNN
F 2 "" H 8550 4180 30  0000 C CNN
F 3 "" V 8550 4250 30  0000 C CNN
	1    8500 4200
	0    1    1    0   
$EndComp
$Comp
L eSim_R R5
U 1 1 5C9D2300
P 4450 6750
F 0 "R5" H 4500 6880 50  0000 C CNN
F 1 "5k" H 4500 6800 50  0000 C CNN
F 2 "" H 4500 6730 30  0000 C CNN
F 3 "" V 4500 6800 30  0000 C CNN
	1    4450 6750
	0    1    1    0   
$EndComp
$Comp
L eSim_R R9
U 1 1 5C9D2395
P 5950 6750
F 0 "R9" H 6000 6880 50  0000 C CNN
F 1 "5k" H 6000 6800 50  0000 C CNN
F 2 "" H 6000 6730 30  0000 C CNN
F 3 "" V 6000 6800 30  0000 C CNN
	1    5950 6750
	0    1    1    0   
$EndComp
$Comp
L eSim_R R10
U 1 1 5C9D242E
P 6450 6750
F 0 "R10" H 6500 6880 50  0000 C CNN
F 1 "5k" H 6500 6800 50  0000 C CNN
F 2 "" H 6500 6730 30  0000 C CNN
F 3 "" V 6500 6800 30  0000 C CNN
	1    6450 6750
	0    1    1    0   
$EndComp
$Comp
L eSim_NPN Q18
U 1 1 5C9D24BF
P 9650 5900
F 0 "Q18" H 9550 5950 50  0000 R CNN
F 1 "eSim_NPN" H 9600 6050 50  0000 R CNN
F 2 "" H 9850 6000 29  0000 C CNN
F 3 "" H 9650 5900 60  0000 C CNN
	1    9650 5900
	-1   0    0    -1  
$EndComp
$Comp
L eSim_NPN Q19
U 1 1 5C9D2540
P 10350 5900
F 0 "Q19" H 10250 5950 50  0000 R CNN
F 1 "eSim_NPN" H 10300 6050 50  0000 R CNN
F 2 "" H 10550 6000 29  0000 C CNN
F 3 "" H 10350 5900 60  0000 C CNN
	1    10350 5900
	1    0    0    -1  
$EndComp
$Comp
L eSim_R R14
U 1 1 5C9D25BD
P 9500 6750
F 0 "R14" H 9550 6880 50  0000 C CNN
F 1 "5k" H 9550 6800 50  0000 C CNN
F 2 "" H 9550 6730 30  0000 C CNN
F 3 "" V 9550 6800 30  0000 C CNN
	1    9500 6750
	0    1    1    0   
$EndComp
$Comp
L eSim_R R16
U 1 1 5C9D2650
P 10450 6750
F 0 "R16" H 10500 6880 50  0000 C CNN
F 1 "5k" H 10500 6800 50  0000 C CNN
F 2 "" H 10500 6730 30  0000 C CNN
F 3 "" V 10500 6800 30  0000 C CNN
	1    10450 6750
	0    1    1    0   
$EndComp
$Comp
L PORT U1
U 5 1 5C9D2BB3
P 650 1650
F 0 "U1" H 700 1750 30  0000 C CNN
F 1 "PORT" H 650 1650 30  0000 C CNN
F 2 "" H 650 1650 60  0000 C CNN
F 3 "" H 650 1650 60  0000 C CNN
	5    650  1650
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 6 1 5C9D68D0
P 2100 800
F 0 "U1" H 2150 900 30  0000 C CNN
F 1 "PORT" H 2100 800 30  0000 C CNN
F 2 "" H 2100 800 60  0000 C CNN
F 3 "" H 2100 800 60  0000 C CNN
	6    2100 800 
	-1   0    0    1   
$EndComp
$Comp
L eSim_R R11
U 1 1 5C9D8B9B
P 7150 1350
F 0 "R11" H 7200 1480 50  0000 C CNN
F 1 "5k" H 7200 1400 50  0000 C CNN
F 2 "" H 7200 1330 30  0000 C CNN
F 3 "" V 7200 1400 30  0000 C CNN
	1    7150 1350
	0    1    1    0   
$EndComp
$Comp
L PORT U1
U 8 1 5C9D98CB
P 3650 550
F 0 "U1" H 3700 650 30  0000 C CNN
F 1 "PORT" H 3650 550 30  0000 C CNN
F 2 "" H 3650 550 60  0000 C CNN
F 3 "" H 3650 550 60  0000 C CNN
	8    3650 550 
	0    1    1    0   
$EndComp
$Comp
L PORT U1
U 7 1 5C9E5DF3
P 3150 3950
F 0 "U1" H 3200 4050 30  0000 C CNN
F 1 "PORT" H 3150 3950 30  0000 C CNN
F 2 "" H 3150 3950 60  0000 C CNN
F 3 "" H 3150 3950 60  0000 C CNN
	7    3150 3950
	0    -1   -1   0   
$EndComp
$Comp
L PORT U1
U 4 1 5C9E625B
P 4950 5150
F 0 "U1" H 5000 5250 30  0000 C CNN
F 1 "PORT" H 4950 5150 30  0000 C CNN
F 2 "" H 4950 5150 60  0000 C CNN
F 3 "" H 4950 5150 60  0000 C CNN
	4    4950 5150
	-1   0    0    1   
$EndComp
$Comp
L PORT U1
U 3 1 5C9E6ECC
P 6800 5100
F 0 "U1" H 6850 5200 30  0000 C CNN
F 1 "PORT" H 6800 5100 30  0000 C CNN
F 2 "" H 6800 5100 60  0000 C CNN
F 3 "" H 6800 5100 60  0000 C CNN
	3    6800 5100
	-1   0    0    1   
$EndComp
$Comp
L PORT U1
U 1 1 5C9E7FDD
P 11100 7250
F 0 "U1" H 11150 7350 30  0000 C CNN
F 1 "PORT" H 11100 7250 30  0000 C CNN
F 2 "" H 11100 7250 60  0000 C CNN
F 3 "" H 11100 7250 60  0000 C CNN
	1    11100 7250
	0    -1   -1   0   
$EndComp
Text Notes 500  1450 0    79   ~ 0
Modulation Input\n
Text Notes 2200 800  0    79   ~ 0
R1(External)
Text Notes 3300 5750 1    79   ~ 0
C1(External)\n
Text Notes 4500 5050 0    79   ~ 0
Triangle Wave Output
Text Notes 6500 5000 0    79   ~ 0
Square Wave Output\n
Text Notes 10950 7000 0    79   ~ 0
GND\n
Text Notes 3425 625  0    79   ~ 0
V+\n
$Comp
L eSim_Diode D10
U 1 1 5C9F4364
P 1300 1850
F 0 "D10" H 1300 1950 50  0000 C CNN
F 1 "eSim_Diode" H 1300 1750 50  0000 C CNN
F 2 "" H 1300 1850 60  0000 C CNN
F 3 "" H 1300 1850 60  0000 C CNN
	1    1300 1850
	0    -1   -1   0   
$EndComp
Text Notes 950  1650 0    79   ~ 0
Vc\n
Wire Wire Line
	1750 1850 1750 2250
Wire Wire Line
	900  1650 1450 1650
Wire Wire Line
	2750 2000 2750 2250
Wire Wire Line
	2050 2450 2450 2450
Wire Wire Line
	2750 2200 2250 2200
Wire Wire Line
	2250 2200 2250 2450
Connection ~ 2250 2450
Connection ~ 2750 2200
Wire Wire Line
	2100 1800 2450 1800
Wire Wire Line
	2100 2000 2100 1800
Wire Wire Line
	1300 2000 2100 2000
Connection ~ 1750 2000
Wire Wire Line
	2750 1450 1750 1450
Wire Wire Line
	2750 2650 2750 3000
Wire Wire Line
	1750 2650 1750 3000
Wire Wire Line
	2750 2850 1750 2850
Connection ~ 1750 2850
Connection ~ 2750 2850
Wire Wire Line
	2750 3300 2750 3900
Wire Wire Line
	2450 4100 1750 4100
Wire Wire Line
	1750 3300 1750 4700
Connection ~ 1750 4100
Wire Wire Line
	2750 4300 2750 4700
Wire Wire Line
	2050 4900 2450 4900
Wire Wire Line
	2750 3550 3350 3550
Connection ~ 2750 3550
Wire Wire Line
	2750 4500 2250 4500
Wire Wire Line
	2250 4500 2250 4900
Connection ~ 2250 4900
Connection ~ 2750 4500
Wire Wire Line
	2750 5100 2750 5400
Wire Wire Line
	2750 5700 2750 5950
Wire Wire Line
	1750 5100 1750 5450
Wire Wire Line
	1750 5750 1750 6300
Wire Wire Line
	1750 5900 2750 5900
Connection ~ 2750 5900
Connection ~ 1750 5900
Wire Wire Line
	2750 6250 2750 6500
Wire Wire Line
	2650 6500 8550 6500
Wire Wire Line
	1750 6700 1750 7000
Wire Wire Line
	2050 6500 2350 6500
Wire Wire Line
	2200 6500 2200 6650
Connection ~ 2200 6500
Wire Wire Line
	1750 7000 11100 7000
Wire Wire Line
	2200 7000 2200 6950
Connection ~ 2200 7000
Wire Wire Line
	4500 6950 4500 7000
Connection ~ 4500 7000
Wire Wire Line
	6000 7000 6000 6950
Wire Wire Line
	9550 6950 9550 7000
Connection ~ 9550 7000
Wire Wire Line
	10500 6950 10500 7000
Connection ~ 10500 7000
Wire Wire Line
	4500 6100 4500 6650
Wire Wire Line
	3650 3750 3650 5700
Connection ~ 3650 4600
Wire Wire Line
	3950 4800 4500 4800
Wire Wire Line
	4500 4800 4500 5700
Wire Wire Line
	1750 1450 1750 800 
Wire Wire Line
	1750 800  1850 800 
Wire Wire Line
	3650 800  10500 800 
Wire Wire Line
	10500 1950 10500 5700
Wire Wire Line
	10500 5700 10450 5700
Wire Wire Line
	9850 5900 10150 5900
Wire Wire Line
	10500 5550 10000 5550
Wire Wire Line
	10000 5550 10000 5900
Connection ~ 10000 5900
Connection ~ 10500 5550
Wire Wire Line
	10450 6100 10450 6650
Wire Wire Line
	10450 6650 10500 6650
Wire Wire Line
	9550 6100 9550 6650
Wire Wire Line
	9550 1600 9550 5700
Wire Wire Line
	8500 1600 9550 1600
Wire Wire Line
	9050 800  9050 1300
Connection ~ 9050 800 
Connection ~ 9050 1600
Wire Wire Line
	8500 1300 8500 800 
Connection ~ 8500 800 
Wire Wire Line
	9550 2650 8850 2650
Connection ~ 9550 2650
Wire Wire Line
	7200 2450 8550 2450
Wire Wire Line
	7900 2450 7900 2550
Wire Wire Line
	7200 1550 7200 2550
Connection ~ 7900 2450
Wire Wire Line
	7200 800  7200 1250
Connection ~ 7200 800 
Connection ~ 7200 2450
Wire Wire Line
	3650 3350 3650 800 
Connection ~ 3650 800 
Wire Wire Line
	3950 4400 3950 800 
Connection ~ 3950 800 
Wire Wire Line
	4950 1150 4950 800 
Connection ~ 4950 800 
Wire Wire Line
	5950 1150 5950 800 
Connection ~ 5950 800 
Wire Wire Line
	6200 1850 5950 1850
Wire Wire Line
	5950 1450 5950 3100
Wire Wire Line
	4950 1450 4950 3750
Wire Wire Line
	4950 2350 5000 2350
Wire Wire Line
	5950 2350 5300 2350
Connection ~ 5950 1850
Wire Wire Line
	3650 3950 4150 3950
Connection ~ 3650 3950
Wire Wire Line
	4150 2950 3850 2950
Wire Wire Line
	3850 2950 3850 3950
Connection ~ 3850 3950
Wire Wire Line
	4950 2950 4450 2950
Connection ~ 4950 2350
Connection ~ 4950 2950
Wire Wire Line
	4650 3950 4450 3950
Wire Wire Line
	3650 6950 3650 7000
Connection ~ 3650 7000
Wire Wire Line
	3650 6650 3650 6100
Wire Wire Line
	10000 5900 3950 5900
Connection ~ 4800 5900
Wire Wire Line
	8550 6500 8550 4400
Connection ~ 2750 6500
Wire Wire Line
	8550 2850 8550 4100
Wire Wire Line
	8200 2750 8350 2750
Wire Wire Line
	8350 2750 8350 3000
Wire Wire Line
	8350 3000 8550 3000
Connection ~ 8550 3000
Wire Wire Line
	7900 2950 7900 6500
Connection ~ 7900 6500
Wire Wire Line
	7200 2950 7200 7000
Wire Wire Line
	6500 1650 6500 800 
Connection ~ 6500 800 
Connection ~ 7200 7000
Connection ~ 6000 7000
Wire Wire Line
	6500 6950 6500 7000
Connection ~ 6500 7000
Wire Wire Line
	5350 3300 5650 3300
Wire Wire Line
	5500 3300 5500 3450
Connection ~ 5500 3300
Wire Wire Line
	4950 4150 6000 4150
Wire Wire Line
	5950 4150 5950 3500
Wire Wire Line
	5500 3750 5500 4150
Connection ~ 5500 4150
Wire Wire Line
	6000 4150 6000 6650
Connection ~ 5950 4150
Connection ~ 5950 2350
Wire Wire Line
	3150 3550 3150 3700
Connection ~ 3150 3550
Wire Wire Line
	4700 5150 4500 5150
Connection ~ 4500 5150
Wire Notes Line
	2200 800  2900 800 
Wire Notes Line
	3150 4050 3150 7000
Wire Wire Line
	1300 1700 1300 1650
Connection ~ 1300 1650
Wire Wire Line
	5050 3300 4950 3300
Connection ~ 4950 3300
$Comp
L eSim_PNP Q20
U 1 1 5CA087B6
P 2650 1800
F 0 "Q20" H 2550 1850 50  0000 R CNN
F 1 "eSim_PNP" H 2600 1950 50  0000 R CNN
F 2 "" H 2850 1900 29  0000 C CNN
F 3 "" H 2650 1800 60  0000 C CNN
	1    2650 1800
	1    0    0    1   
$EndComp
Wire Wire Line
	2750 1450 2750 1600
Wire Notes Line
	2925 800  3600 800 
Wire Wire Line
	10500 800  10500 1650
Wire Wire Line
	6500 2050 6500 6650
Wire Wire Line
	6500 5100 6550 5100
Connection ~ 6500 5100
Wire Wire Line
	6900 2750 6500 2750
Connection ~ 6500 2750
$EndSCHEMATC
