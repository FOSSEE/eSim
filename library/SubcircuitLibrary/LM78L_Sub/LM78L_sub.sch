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
LIBS:LM78L-cache
EELAYER 25 0
EELAYER END
$Descr User 17748 11236
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
U 1 1 6671981A
P 2850 1550
F 0 "R1" H 2900 1680 50  0000 C CNN
F 1 "418" H 2900 1500 50  0000 C CNN
F 2 "" H 2900 1530 30  0000 C CNN
F 3 "" V 2900 1600 30  0000 C CNN
	1    2850 1550
	0    1    1    0   
$EndComp
$Comp
L jfet_n J1
U 1 1 6671981B
P 1700 2100
F 0 "J1" H 1600 2150 50  0000 R CNN
F 1 "jfet_n" H 1650 2250 50  0000 R CNN
F 2 "" H 1900 2200 29  0000 C CNN
F 3 "" H 1700 2100 60  0000 C CNN
	1    1700 2100
	1    0    0    -1  
$EndComp
$Comp
L eSim_PNP Q2
U 1 1 6671981C
P 3000 2200
F 0 "Q2" H 2900 2250 50  0000 R CNN
F 1 "eSim_PNP" H 2950 2350 50  0000 R CNN
F 2 "" H 3200 2300 29  0000 C CNN
F 3 "" H 3000 2200 60  0000 C CNN
	1    3000 2200
	-1   0    0    1   
$EndComp
$Comp
L eSim_PNP Q3
U 1 1 6671981D
P 3750 2200
F 0 "Q3" H 3650 2250 50  0000 R CNN
F 1 "eSim_PNP" H 3700 2350 50  0000 R CNN
F 2 "" H 3950 2300 29  0000 C CNN
F 3 "" H 3750 2200 60  0000 C CNN
	1    3750 2200
	1    0    0    1   
$EndComp
$Comp
L eSim_PNP Q8
U 1 1 6671981E
P 4350 2200
F 0 "Q8" H 4250 2250 50  0000 R CNN
F 1 "eSim_PNP" H 4300 2350 50  0000 R CNN
F 2 "" H 4550 2300 29  0000 C CNN
F 3 "" H 4350 2200 60  0000 C CNN
	1    4350 2200
	1    0    0    1   
$EndComp
$Comp
L eSim_NPN Q1
U 1 1 6671981F
P 2100 2750
F 0 "Q1" H 2000 2800 50  0000 R CNN
F 1 "eSim_NPN" H 2050 2900 50  0000 R CNN
F 2 "" H 2300 2850 29  0000 C CNN
F 3 "" H 2100 2750 60  0000 C CNN
	1    2100 2750
	1    0    0    -1  
$EndComp
$Comp
L eSim_NPN Q4
U 1 1 66719820
P 3800 3200
F 0 "Q4" H 3700 3250 50  0000 R CNN
F 1 "eSim_NPN" H 3750 3350 50  0000 R CNN
F 2 "" H 4000 3300 29  0000 C CNN
F 3 "" H 3800 3200 60  0000 C CNN
	1    3800 3200
	1    0    0    -1  
$EndComp
$Comp
L resistor R2
U 1 1 66719821
P 3850 3700
F 0 "R2" H 3900 3830 50  0000 C CNN
F 1 "576" H 3900 3650 50  0000 C CNN
F 2 "" H 3900 3680 30  0000 C CNN
F 3 "" V 3900 3750 30  0000 C CNN
	1    3850 3700
	0    1    1    0   
$EndComp
$Comp
L eSim_PNP Q7
U 1 1 66719822
P 4300 4150
F 0 "Q7" H 4200 4200 50  0000 R CNN
F 1 "eSim_PNP" H 4250 4300 50  0000 R CNN
F 2 "" H 4500 4250 29  0000 C CNN
F 3 "" H 4300 4150 60  0000 C CNN
	1    4300 4150
	1    0    0    1   
$EndComp
$Comp
L resistor R3
U 1 1 66719823
P 3850 4650
F 0 "R3" H 3900 4780 50  0000 C CNN
F 1 "3.41k" H 3900 4600 50  0000 C CNN
F 2 "" H 3900 4630 30  0000 C CNN
F 3 "" V 3900 4700 30  0000 C CNN
	1    3850 4650
	0    1    1    0   
$EndComp
$Comp
L zener U1
U 1 1 66719824
P 1800 5300
F 0 "U1" H 1750 5200 60  0000 C CNN
F 1 "zener" H 1800 5400 60  0000 C CNN
F 2 "" H 1850 5300 60  0000 C CNN
F 3 "" H 1850 5300 60  0000 C CNN
	1    1800 5300
	0    1    -1   0   
$EndComp
$Comp
L resistor R4
U 1 1 66719825
P 3850 5550
F 0 "R4" H 3900 5680 50  0000 C CNN
F 1 "3.89k" H 3900 5500 50  0000 C CNN
F 2 "" H 3900 5530 30  0000 C CNN
F 3 "" V 3900 5600 30  0000 C CNN
	1    3850 5550
	0    1    1    0   
$EndComp
Wire Wire Line
	1800 2300 1800 5000
Wire Wire Line
	1900 2750 1800 2750
Connection ~ 1800 2750
Wire Wire Line
	1800 1900 1800 1250
Wire Wire Line
	1800 1250 11450 1250
Wire Wire Line
	2900 1450 2900 1250
Connection ~ 2900 1250
Wire Wire Line
	2900 1750 2900 2000
Wire Wire Line
	2200 2550 3850 2550
Wire Wire Line
	2200 2950 2200 3200
Wire Wire Line
	3900 3400 3900 3600
Wire Wire Line
	3900 3900 3900 4550
Wire Wire Line
	4100 4150 3900 4150
Connection ~ 3900 4150
Wire Wire Line
	3900 3500 4400 3500
Wire Wire Line
	4400 3500 4400 3950
Connection ~ 3900 3500
Wire Wire Line
	3900 4850 3900 5450
Wire Wire Line
	3900 5050 5300 5050
Connection ~ 3900 5050
$Comp
L eSim_NPN Q5
U 1 1 66719826
P 3800 6300
F 0 "Q5" H 3700 6350 50  0000 R CNN
F 1 "eSim_NPN" H 3750 6450 50  0000 R CNN
F 2 "" H 4000 6400 29  0000 C CNN
F 3 "" H 3800 6300 60  0000 C CNN
	1    3800 6300
	1    0    0    -1  
$EndComp
$Comp
L eSim_NPN Q6
U 1 1 66719827
P 3800 7050
F 0 "Q6" H 3700 7100 50  0000 R CNN
F 1 "eSim_NPN" H 3750 7200 50  0000 R CNN
F 2 "" H 4000 7150 29  0000 C CNN
F 3 "" H 3800 7050 60  0000 C CNN
	1    3800 7050
	1    0    0    -1  
$EndComp
Wire Wire Line
	3900 5750 3900 6100
Wire Wire Line
	3900 6500 3900 6850
$Comp
L zener U2
U 1 1 66719828
P 2900 5150
F 0 "U2" H 2850 5050 60  0000 C CNN
F 1 "zener" H 2900 5250 60  0000 C CNN
F 2 "" H 2950 5150 60  0000 C CNN
F 3 "" H 2950 5150 60  0000 C CNN
	1    2900 5150
	0    1    -1   0   
$EndComp
Wire Wire Line
	2900 4850 2900 2400
Wire Wire Line
	3850 2400 3850 3000
Wire Wire Line
	3850 3000 3900 3000
Wire Wire Line
	2200 3200 3600 3200
Connection ~ 3850 2550
Wire Wire Line
	3400 2200 3400 2450
Wire Wire Line
	3400 2450 3850 2450
Connection ~ 3850 2450
Connection ~ 3400 2200
Connection ~ 2900 3200
Wire Wire Line
	3850 2000 3850 1900
Wire Wire Line
	3850 1900 4450 1900
Wire Wire Line
	4450 1900 4450 2000
Wire Wire Line
	4150 1900 4150 1250
Connection ~ 4150 1250
Connection ~ 4150 1900
Wire Wire Line
	4450 2400 4450 2500
Wire Wire Line
	4450 2500 9350 2500
Wire Wire Line
	3200 2200 4150 2200
Wire Wire Line
	2900 5350 2900 7500
Wire Wire Line
	1200 7500 11700 7500
Wire Wire Line
	3900 7500 3900 7250
Wire Wire Line
	1800 5450 1800 7500
Connection ~ 2900 7500
Wire Wire Line
	3600 7050 3300 7050
Wire Wire Line
	3300 7050 3300 6650
Wire Wire Line
	3300 6650 3900 6650
Connection ~ 3900 6650
Wire Wire Line
	3250 6300 3250 5900
Wire Wire Line
	3250 5900 3900 5900
Connection ~ 3900 5900
Wire Wire Line
	1500 2100 1200 2100
Wire Wire Line
	1200 2100 1200 7500
Connection ~ 1800 7500
Wire Wire Line
	4400 4350 4400 5450
$Comp
L resistor R5
U 1 1 66719829
P 4350 5550
F 0 "R5" H 4400 5680 50  0000 C CNN
F 1 "7.8k" H 4400 5500 50  0000 C CNN
F 2 "" H 4400 5530 30  0000 C CNN
F 3 "" V 4400 5600 30  0000 C CNN
	1    4350 5550
	0    1    1    0   
$EndComp
Wire Wire Line
	4400 7500 4400 5750
Connection ~ 3900 7500
$Comp
L eSim_NPN Q9
U 1 1 6671982A
P 5000 5300
F 0 "Q9" H 4900 5350 50  0000 R CNN
F 1 "eSim_NPN" H 4950 5450 50  0000 R CNN
F 2 "" H 5200 5400 29  0000 C CNN
F 3 "" H 5000 5300 60  0000 C CNN
	1    5000 5300
	1    0    0    -1  
$EndComp
Wire Wire Line
	4800 5300 4400 5300
Connection ~ 4400 5300
Wire Wire Line
	5100 5100 5100 2500
Connection ~ 5100 2500
$Comp
L eSim_PNP Q12
U 1 1 6671982B
P 6750 3600
F 0 "Q12" H 6650 3650 50  0000 R CNN
F 1 "eSim_PNP" H 6700 3750 50  0000 R CNN
F 2 "" H 6950 3700 29  0000 C CNN
F 3 "" H 6750 3600 60  0000 C CNN
	1    6750 3600
	-1   0    0    1   
$EndComp
$Comp
L resistor R8
U 1 1 6671982C
P 7450 3000
F 0 "R8" H 7500 3130 50  0000 C CNN
F 1 "5.76k" H 7500 2950 50  0000 C CNN
F 2 "" H 7500 2980 30  0000 C CNN
F 3 "" V 7500 3050 30  0000 C CNN
	1    7450 3000
	0    1    1    0   
$EndComp
$Comp
L eSim_NPN Q10
U 1 1 6671982D
P 6100 5050
F 0 "Q10" H 6000 5100 50  0000 R CNN
F 1 "eSim_NPN" H 6050 5200 50  0000 R CNN
F 2 "" H 6300 5150 29  0000 C CNN
F 3 "" H 6100 5050 60  0000 C CNN
	1    6100 5050
	1    0    0    -1  
$EndComp
$Comp
L eSim_NPN Q13
U 1 1 6671982E
P 7600 5000
F 0 "Q13" H 7500 5050 50  0000 R CNN
F 1 "eSim_NPN" H 7550 5150 50  0000 R CNN
F 2 "" H 7800 5100 29  0000 C CNN
F 3 "" H 7600 5000 60  0000 C CNN
	1    7600 5000
	-1   0    0    -1  
$EndComp
$Comp
L resistor R6
U 1 1 6671982F
P 5500 5000
F 0 "R6" H 5550 5130 50  0000 C CNN
F 1 "13k" H 5550 4950 50  0000 C CNN
F 2 "" H 5550 4980 30  0000 C CNN
F 3 "" V 5550 5050 30  0000 C CNN
	1    5500 5000
	-1   0    0    1   
$EndComp
Wire Wire Line
	5900 5050 5600 5050
Wire Wire Line
	6650 3400 6650 2500
Connection ~ 6650 2500
Wire Wire Line
	6650 3800 6650 7500
Wire Wire Line
	6950 3600 7500 3600
Wire Wire Line
	7500 3200 7500 4800
Wire Wire Line
	7500 2500 7500 2900
Connection ~ 7500 3600
Wire Wire Line
	6200 4850 6200 3950
Wire Wire Line
	6200 3950 10050 3950
$Comp
L eSim_NPN Q14
U 1 1 66719830
P 8200 3100
F 0 "Q14" H 8100 3150 50  0000 R CNN
F 1 "eSim_NPN" H 8150 3250 50  0000 R CNN
F 2 "" H 8400 3200 29  0000 C CNN
F 3 "" H 8200 3100 60  0000 C CNN
	1    8200 3100
	-1   0    0    -1  
$EndComp
$Comp
L resistor R9
U 1 1 66719831
P 8050 3500
F 0 "R9" H 8100 3630 50  0000 C CNN
F 1 "100" H 8100 3450 50  0000 C CNN
F 2 "" H 8100 3480 30  0000 C CNN
F 3 "" V 8100 3550 30  0000 C CNN
	1    8050 3500
	0    1    1    0   
$EndComp
Wire Wire Line
	8100 2500 8100 2900
Connection ~ 7500 2500
$Comp
L zener U4
U 1 1 66719832
P 8700 2850
F 0 "U4" H 8650 2750 60  0000 C CNN
F 1 "zener" H 8700 2950 60  0000 C CNN
F 2 "" H 8750 2850 60  0000 C CNN
F 3 "" H 8750 2850 60  0000 C CNN
	1    8700 2850
	0    1    -1   0   
$EndComp
Wire Wire Line
	8700 2350 8700 2550
Connection ~ 8100 2500
Wire Wire Line
	8400 3100 9050 3100
Wire Wire Line
	8700 3100 8700 3050
Wire Wire Line
	8100 3300 8100 3400
Wire Wire Line
	8100 3700 8100 3800
Wire Wire Line
	8100 3800 11150 3800
$Comp
L resistor R11
U 1 1 66719833
P 9250 3050
F 0 "R11" H 9300 3180 50  0000 C CNN
F 1 "100" H 9300 3000 50  0000 C CNN
F 2 "" H 9300 3030 30  0000 C CNN
F 3 "" V 9300 3100 30  0000 C CNN
	1    9250 3050
	-1   0    0    1   
$EndComp
Connection ~ 8700 3100
$Comp
L eSim_NPN Q15
U 1 1 66719834
P 9550 2500
F 0 "Q15" H 9450 2550 50  0000 R CNN
F 1 "eSim_NPN" H 9500 2650 50  0000 R CNN
F 2 "" H 9750 2600 29  0000 C CNN
F 3 "" H 9550 2500 60  0000 C CNN
	1    9550 2500
	1    0    0    -1  
$EndComp
Wire Wire Line
	9650 2700 9650 2750
Wire Wire Line
	9650 2750 10450 2750
Wire Wire Line
	10050 3950 10050 2750
Connection ~ 10050 2750
$Comp
L resistor R13
U 1 1 66719835
P 10400 3550
F 0 "R13" H 10450 3680 50  0000 C CNN
F 1 "2.5k" H 10450 3500 50  0000 C CNN
F 2 "" H 10450 3530 30  0000 C CNN
F 3 "" V 10450 3600 30  0000 C CNN
	1    10400 3550
	0    -1   -1   0   
$EndComp
Wire Wire Line
	10350 3350 10350 2750
Connection ~ 10350 2750
Wire Wire Line
	10350 3650 10350 3800
Connection ~ 10350 3800
$Comp
L eSim_NPN Q16
U 1 1 66719836
P 10650 2750
F 0 "Q16" H 10550 2800 50  0000 R CNN
F 1 "eSim_NPN" H 10600 2900 50  0000 R CNN
F 2 "" H 10850 2850 29  0000 C CNN
F 3 "" H 10650 2750 60  0000 C CNN
	1    10650 2750
	1    0    0    -1  
$EndComp
$Comp
L resistor R14
U 1 1 66719837
P 10800 3550
F 0 "R14" H 10850 3680 50  0000 C CNN
F 1 "1.9" H 10850 3500 50  0000 C CNN
F 2 "" H 10850 3530 30  0000 C CNN
F 3 "" V 10850 3600 30  0000 C CNN
	1    10800 3550
	0    -1   -1   0   
$EndComp
Wire Wire Line
	9350 3100 10750 3100
Wire Wire Line
	10750 2950 10750 3350
Connection ~ 10750 3100
Wire Wire Line
	10750 3650 10750 4350
Connection ~ 10750 3800
$Comp
L resistor R10
U 1 1 66719838
P 8750 2250
F 0 "R10" H 8800 2380 50  0000 C CNN
F 1 "5k" H 8800 2200 50  0000 C CNN
F 2 "" H 8800 2230 30  0000 C CNN
F 3 "" V 8800 2300 30  0000 C CNN
	1    8750 2250
	0    -1   -1   0   
$EndComp
$Comp
L zener U3
U 1 1 66719839
P 8700 1750
F 0 "U3" H 8650 1650 60  0000 C CNN
F 1 "zener" H 8700 1850 60  0000 C CNN
F 2 "" H 8750 1750 60  0000 C CNN
F 3 "" H 8750 1750 60  0000 C CNN
	1    8700 1750
	0    1    -1   0   
$EndComp
Wire Wire Line
	8700 1950 8700 2050
Wire Wire Line
	8700 1250 8700 1450
Wire Wire Line
	9650 1250 9650 2300
Connection ~ 8700 1250
Wire Wire Line
	10750 1250 10750 2550
Connection ~ 9650 1250
Connection ~ 10750 1250
$Comp
L eSim_NPN Q11
U 1 1 6671983A
P 6400 6300
F 0 "Q11" H 6300 6350 50  0000 R CNN
F 1 "eSim_NPN" H 6350 6450 50  0000 R CNN
F 2 "" H 6600 6400 29  0000 C CNN
F 3 "" H 6400 6300 60  0000 C CNN
	1    6400 6300
	1    0    0    -1  
$EndComp
Wire Wire Line
	6200 5250 6200 5350
Wire Wire Line
	6200 5350 7500 5350
Wire Wire Line
	7500 5350 7500 5200
Wire Wire Line
	6500 6100 6500 5350
Connection ~ 6500 5350
Wire Wire Line
	5100 7500 5100 5500
Connection ~ 4400 7500
$Comp
L resistor R7
U 1 1 6671983B
P 6450 6850
F 0 "R7" H 6500 6980 50  0000 C CNN
F 1 "2.84k" H 6500 6800 50  0000 C CNN
F 2 "" H 6500 6830 30  0000 C CNN
F 3 "" V 6500 6900 30  0000 C CNN
	1    6450 6850
	0    1    1    0   
$EndComp
Wire Wire Line
	6500 6750 6500 6500
Wire Wire Line
	6500 7500 6500 7050
Connection ~ 5100 7500
Connection ~ 6500 7500
$Comp
L capacitor_polarised C1
U 1 1 6671983C
P 8150 4550
F 0 "C1" H 8175 4650 50  0000 L CNN
F 1 "5pF" H 8175 4450 50  0000 L CNN
F 2 "" H 8150 4550 50  0001 C CNN
F 3 "" H 8150 4550 50  0001 C CNN
	1    8150 4550
	0    -1   -1   0   
$EndComp
Wire Wire Line
	8000 4550 7500 4550
Connection ~ 7500 4550
Wire Wire Line
	8300 4550 8500 4550
Wire Wire Line
	8500 4550 8500 5000
Wire Wire Line
	7800 5000 9300 5000
$Comp
L resistor R12
U 1 1 6671983D
P 9500 4950
F 0 "R12" H 9550 5080 50  0000 C CNN
F 1 "15k" H 9550 4900 50  0000 C CNN
F 2 "" H 9550 4930 30  0000 C CNN
F 3 "" V 9550 5000 30  0000 C CNN
	1    9500 4950
	-1   0    0    1   
$EndComp
$Comp
L resistor R15
U 1 1 6671983E
P 10800 4550
F 0 "R15" H 10850 4680 50  0000 C CNN
F 1 "1.5k" H 10850 4500 50  0000 C CNN
F 2 "" H 10850 4530 30  0000 C CNN
F 3 "" V 10850 4600 30  0000 C CNN
	1    10800 4550
	0    -1   -1   0   
$EndComp
Connection ~ 8500 5000
Wire Wire Line
	9600 5000 10750 5000
Wire Wire Line
	10750 4650 10750 5950
Connection ~ 6650 7500
$Comp
L resistor R16
U 1 1 6671983F
P 10800 6150
F 0 "R16" H 10850 6280 50  0000 C CNN
F 1 "2.23k" H 10850 6100 50  0000 C CNN
F 2 "" H 10850 6130 30  0000 C CNN
F 3 "" V 10850 6200 30  0000 C CNN
	1    10800 6150
	0    -1   -1   0   
$EndComp
Wire Wire Line
	10800 6250 10800 7500
Wire Wire Line
	10800 6250 10750 6250
Connection ~ 10750 5000
Connection ~ 10800 7500
Wire Wire Line
	3250 6300 6200 6300
Connection ~ 3550 2200
Connection ~ 3600 6300
$Comp
L PORT U5
U 2 1 66719C33
P 11400 3800
F 0 "U5" H 11450 3900 30  0000 C CNN
F 1 "PORT" H 11400 3800 30  0000 C CNN
F 2 "" H 11400 3800 60  0000 C CNN
F 3 "" H 11400 3800 60  0000 C CNN
	2    11400 3800
	-1   0    0    1   
$EndComp
$Comp
L PORT U5
U 1 1 66719F7B
P 11700 1250
F 0 "U5" H 11750 1350 30  0000 C CNN
F 1 "PORT" H 11700 1250 30  0000 C CNN
F 2 "" H 11700 1250 60  0000 C CNN
F 3 "" H 11700 1250 60  0000 C CNN
	1    11700 1250
	-1   0    0    1   
$EndComp
$Comp
L PORT U5
U 3 1 6671A2F2
P 11950 7500
F 0 "U5" H 12000 7600 30  0000 C CNN
F 1 "PORT" H 11950 7500 30  0000 C CNN
F 2 "" H 11950 7500 60  0000 C CNN
F 3 "" H 11950 7500 60  0000 C CNN
	3    11950 7500
	-1   0    0    1   
$EndComp
$EndSCHEMATC