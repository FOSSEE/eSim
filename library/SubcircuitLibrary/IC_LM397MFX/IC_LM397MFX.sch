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
LIBS:IC_LM397MFX-cache
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
L jfet_n J1
U 1 1 6414AD39
P 3400 3450
F 0 "J1" H 3300 3500 50  0000 R CNN
F 1 "jfet_n" H 3350 3600 50  0000 R CNN
F 2 "" H 3600 3550 29  0000 C CNN
F 3 "" H 3400 3450 60  0000 C CNN
	1    3400 3450
	1    0    0    -1  
$EndComp
$Comp
L eSim_PNP Q1
U 1 1 6414AD5B
P 3900 3100
F 0 "Q1" H 3800 3150 50  0000 R CNN
F 1 "eSim_PNP" H 3850 3250 50  0000 R CNN
F 2 "" H 4100 3200 29  0000 C CNN
F 3 "" H 3900 3100 60  0000 C CNN
	1    3900 3100
	-1   0    0    1   
$EndComp
$Comp
L eSim_PNP Q4
U 1 1 6414AD78
P 5050 3100
F 0 "Q4" H 4950 3150 50  0000 R CNN
F 1 "eSim_PNP" H 5000 3250 50  0000 R CNN
F 2 "" H 5250 3200 29  0000 C CNN
F 3 "" H 5050 3100 60  0000 C CNN
	1    5050 3100
	-1   0    0    1   
$EndComp
$Comp
L eSim_PNP Q5
U 1 1 6414AD97
P 5300 3500
F 0 "Q5" H 5200 3550 50  0000 R CNN
F 1 "eSim_PNP" H 5250 3650 50  0000 R CNN
F 2 "" H 5500 3600 29  0000 C CNN
F 3 "" H 5300 3500 60  0000 C CNN
	1    5300 3500
	-1   0    0    1   
$EndComp
$Comp
L eSim_PNP Q8
U 1 1 6414ADCC
P 6550 3100
F 0 "Q8" H 6450 3150 50  0000 R CNN
F 1 "eSim_PNP" H 6500 3250 50  0000 R CNN
F 2 "" H 6750 3200 29  0000 C CNN
F 3 "" H 6550 3100 60  0000 C CNN
	1    6550 3100
	1    0    0    1   
$EndComp
$Comp
L eSim_PNP Q7
U 1 1 6414ADFD
P 6200 3500
F 0 "Q7" H 6100 3550 50  0000 R CNN
F 1 "eSim_PNP" H 6150 3650 50  0000 R CNN
F 2 "" H 6400 3600 29  0000 C CNN
F 3 "" H 6200 3500 60  0000 C CNN
	1    6200 3500
	1    0    0    1   
$EndComp
$Comp
L eSim_PNP Q10
U 1 1 64188296
P 7350 3100
F 0 "Q10" H 7250 3150 50  0000 R CNN
F 1 "eSim_PNP" H 7300 3250 50  0000 R CNN
F 2 "" H 7550 3200 29  0000 C CNN
F 3 "" H 7350 3100 60  0000 C CNN
	1    7350 3100
	1    0    0    1   
$EndComp
$Comp
L resistor R2
U 1 1 641882BF
P 4450 3050
F 0 "R2" H 4500 3180 50  0000 C CNN
F 1 "2k" H 4500 3000 50  0000 C CNN
F 2 "" H 4500 3030 30  0000 C CNN
F 3 "" V 4500 3100 30  0000 C CNN
	1    4450 3050
	-1   0    0    1   
$EndComp
$Comp
L resistor R3
U 1 1 641882F4
P 6600 2450
F 0 "R3" H 6650 2580 50  0000 C CNN
F 1 "2.1k" H 6650 2400 50  0000 C CNN
F 2 "" H 6650 2430 30  0000 C CNN
F 3 "" V 6650 2500 30  0000 C CNN
	1    6600 2450
	0    1    1    0   
$EndComp
$Comp
L eSim_NPN Q2
U 1 1 6418832D
P 3900 4600
F 0 "Q2" H 3800 4650 50  0000 R CNN
F 1 "eSim_NPN" H 3850 4750 50  0000 R CNN
F 2 "" H 4100 4700 29  0000 C CNN
F 3 "" H 3900 4600 60  0000 C CNN
	1    3900 4600
	-1   0    0    -1  
$EndComp
$Comp
L eSim_NPN Q3
U 1 1 6418846C
P 4550 4950
F 0 "Q3" H 4450 5000 50  0000 R CNN
F 1 "eSim_NPN" H 4500 5100 50  0000 R CNN
F 2 "" H 4750 5050 29  0000 C CNN
F 3 "" H 4550 4950 60  0000 C CNN
	1    4550 4950
	1    0    0    -1  
$EndComp
$Comp
L eSim_Diode D2
U 1 1 64188527
P 6300 4050
F 0 "D2" H 6300 4150 50  0000 C CNN
F 1 "eSim_Diode" H 6300 3950 50  0000 C CNN
F 2 "" H 6300 4050 60  0000 C CNN
F 3 "" H 6300 4050 60  0000 C CNN
	1    6300 4050
	0    1    1    0   
$EndComp
$Comp
L eSim_Diode D1
U 1 1 6418855E
P 5900 4300
F 0 "D1" H 5900 4400 50  0000 C CNN
F 1 "eSim_Diode" H 5900 4200 50  0000 C CNN
F 2 "" H 5900 4300 60  0000 C CNN
F 3 "" H 5900 4300 60  0000 C CNN
	1    5900 4300
	1    0    0    -1  
$EndComp
$Comp
L eSim_PNP Q6
U 1 1 64188654
P 5950 4750
F 0 "Q6" H 5850 4800 50  0000 R CNN
F 1 "eSim_PNP" H 5900 4900 50  0000 R CNN
F 2 "" H 6150 4850 29  0000 C CNN
F 3 "" H 5950 4750 60  0000 C CNN
	1    5950 4750
	1    0    0    1   
$EndComp
$Comp
L eSim_PNP Q9
U 1 1 64188693
P 6900 4400
F 0 "Q9" H 6800 4450 50  0000 R CNN
F 1 "eSim_PNP" H 6850 4550 50  0000 R CNN
F 2 "" H 7100 4500 29  0000 C CNN
F 3 "" H 6900 4400 60  0000 C CNN
	1    6900 4400
	1    0    0    1   
$EndComp
$Comp
L eSim_PNP Q12
U 1 1 641886CE
P 7550 4400
F 0 "Q12" H 7450 4450 50  0000 R CNN
F 1 "eSim_PNP" H 7500 4550 50  0000 R CNN
F 2 "" H 7750 4500 29  0000 C CNN
F 3 "" H 7550 4400 60  0000 C CNN
	1    7550 4400
	-1   0    0    1   
$EndComp
$Comp
L eSim_PNP Q13
U 1 1 64188747
P 8100 4750
F 0 "Q13" H 8000 4800 50  0000 R CNN
F 1 "eSim_PNP" H 8050 4900 50  0000 R CNN
F 2 "" H 8300 4850 29  0000 C CNN
F 3 "" H 8100 4750 60  0000 C CNN
	1    8100 4750
	-1   0    0    1   
$EndComp
$Comp
L eSim_Diode D4
U 1 1 64188788
P 7950 4050
F 0 "D4" H 7950 4150 50  0000 C CNN
F 1 "eSim_Diode" H 7950 3950 50  0000 C CNN
F 2 "" H 7950 4050 60  0000 C CNN
F 3 "" H 7950 4050 60  0000 C CNN
	1    7950 4050
	0    1    1    0   
$EndComp
$Comp
L eSim_Diode D5
U 1 1 641887CB
P 8200 4300
F 0 "D5" H 8200 4400 50  0000 C CNN
F 1 "eSim_Diode" H 8200 4200 50  0000 C CNN
F 2 "" H 8200 4300 60  0000 C CNN
F 3 "" H 8200 4300 60  0000 C CNN
	1    8200 4300
	-1   0    0    1   
$EndComp
$Comp
L resistor R1
U 1 1 641891A9
P 3750 5300
F 0 "R1" H 3800 5430 50  0000 C CNN
F 1 "4.8k" H 3800 5250 50  0000 C CNN
F 2 "" H 3800 5280 30  0000 C CNN
F 3 "" V 3800 5350 30  0000 C CNN
	1    3750 5300
	0    1    1    0   
$EndComp
$Comp
L eSim_NPN Q11
U 1 1 6418974E
P 7350 5300
F 0 "Q11" H 7250 5350 50  0000 R CNN
F 1 "eSim_NPN" H 7300 5450 50  0000 R CNN
F 2 "" H 7550 5400 29  0000 C CNN
F 3 "" H 7350 5300 60  0000 C CNN
	1    7350 5300
	1    0    0    -1  
$EndComp
$Comp
L eSim_Diode D3
U 1 1 6418979F
P 7000 5600
F 0 "D3" H 7000 5700 50  0000 C CNN
F 1 "eSim_Diode" H 7000 5500 50  0000 C CNN
F 2 "" H 7000 5600 60  0000 C CNN
F 3 "" H 7000 5600 60  0000 C CNN
	1    7000 5600
	0    1    1    0   
$EndComp
$Comp
L eSim_PNP Q14
U 1 1 6418A83F
P 8850 3100
F 0 "Q14" H 8750 3150 50  0000 R CNN
F 1 "eSim_PNP" H 8800 3250 50  0000 R CNN
F 2 "" H 9050 3200 29  0000 C CNN
F 3 "" H 8850 3100 60  0000 C CNN
	1    8850 3100
	1    0    0    1   
$EndComp
$Comp
L eSim_NPN Q15
U 1 1 6418A890
P 8900 5150
F 0 "Q15" H 8800 5200 50  0000 R CNN
F 1 "eSim_NPN" H 8850 5300 50  0000 R CNN
F 2 "" H 9100 5250 29  0000 C CNN
F 3 "" H 8900 5150 60  0000 C CNN
	1    8900 5150
	1    0    0    -1  
$EndComp
$Comp
L eSim_NPN Q16
U 1 1 6418A8D7
P 9350 4600
F 0 "Q16" H 9250 4650 50  0000 R CNN
F 1 "eSim_NPN" H 9300 4750 50  0000 R CNN
F 2 "" H 9550 4700 29  0000 C CNN
F 3 "" H 9350 4600 60  0000 C CNN
	1    9350 4600
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 3 1 6418FD2B
P 8450 1900
F 0 "U1" H 8500 2000 30  0000 C CNN
F 1 "PORT" H 8450 1900 30  0000 C CNN
F 2 "" H 8450 1900 60  0000 C CNN
F 3 "" H 8450 1900 60  0000 C CNN
	3    8450 1900
	0    1    1    0   
$EndComp
$Comp
L PORT U1
U 4 1 6418FD82
P 9450 1900
F 0 "U1" H 9500 2000 30  0000 C CNN
F 1 "PORT" H 9450 1900 30  0000 C CNN
F 2 "" H 9450 1900 60  0000 C CNN
F 3 "" H 9450 1900 60  0000 C CNN
	4    9450 1900
	0    1    1    0   
$EndComp
$Comp
L PORT U1
U 2 1 6418FEFE
P 5650 1850
F 0 "U1" H 5700 1950 30  0000 C CNN
F 1 "PORT" H 5650 1850 30  0000 C CNN
F 2 "" H 5650 1850 60  0000 C CNN
F 3 "" H 5650 1850 60  0000 C CNN
	2    5650 1850
	0    1    1    0   
$EndComp
Wire Wire Line
	5250 3100 6350 3100
Wire Wire Line
	5500 3100 5500 3500
Wire Wire Line
	6000 3100 6000 3500
Wire Wire Line
	4950 2900 5200 2900
Wire Wire Line
	5200 2900 5200 3300
Wire Wire Line
	6650 2900 6300 2900
Wire Wire Line
	6300 2900 6300 3300
Wire Wire Line
	3800 4400 3800 3300
Wire Wire Line
	7750 4400 8000 4400
Wire Wire Line
	8000 4400 8000 4550
Wire Wire Line
	7950 4200 7950 4400
Connection ~ 7950 4400
Wire Wire Line
	8050 4300 7950 4300
Connection ~ 7950 4300
Wire Wire Line
	7000 4200 7450 4200
Wire Wire Line
	6300 3700 6300 3900
Wire Wire Line
	6050 4300 6300 4300
Wire Wire Line
	6300 4200 6300 4550
Wire Wire Line
	5750 4300 5650 4300
Wire Wire Line
	5650 2100 5650 4750
Wire Wire Line
	5650 4750 5750 4750
Wire Wire Line
	3800 5200 3800 4800
Wire Wire Line
	5200 3700 5200 5050
Wire Wire Line
	5200 5050 3800 5050
Connection ~ 3800 5050
Wire Wire Line
	4950 3300 4950 4650
Wire Wire Line
	4950 4650 4650 4650
Wire Wire Line
	4650 4600 4650 4750
Wire Wire Line
	4350 4950 4250 4950
Wire Wire Line
	4250 4950 4250 5050
Connection ~ 4250 5050
Wire Wire Line
	3500 4600 4650 4600
Connection ~ 4650 4650
Wire Wire Line
	3500 3650 3500 4600
Connection ~ 4100 4600
Wire Wire Line
	4250 3100 4100 3100
Wire Wire Line
	4550 3100 5350 3100
Wire Wire Line
	4650 3100 4650 3400
Wire Wire Line
	4650 3400 3800 3400
Connection ~ 3800 3400
Wire Wire Line
	6650 3300 6650 3550
Wire Wire Line
	6650 3550 7950 3550
Wire Wire Line
	7950 3550 7950 3900
Wire Wire Line
	7450 3300 7450 4000
Wire Wire Line
	7450 4000 7200 4000
Wire Wire Line
	7200 4000 7200 4200
Connection ~ 7200 4200
Connection ~ 6000 3100
Connection ~ 5500 3100
Connection ~ 4650 3100
Connection ~ 5350 3100
Wire Wire Line
	6650 2650 6650 2900
Wire Wire Line
	7150 3100 6200 3100
Connection ~ 6200 3100
Wire Wire Line
	8650 3100 7100 3100
Connection ~ 7100 3100
Wire Wire Line
	3500 3250 3500 2250
Wire Wire Line
	3500 2250 8950 2250
Wire Wire Line
	8950 2250 8950 2900
Wire Wire Line
	6650 2350 6650 2250
Connection ~ 6650 2250
Wire Wire Line
	4950 2900 4950 2250
Connection ~ 4950 2250
Wire Wire Line
	7450 2900 7450 2250
Connection ~ 7450 2250
Wire Wire Line
	3800 2100 3800 2900
Connection ~ 3800 2250
Wire Wire Line
	8950 3300 8950 4950
Wire Wire Line
	8950 4950 9000 4950
Wire Wire Line
	9150 4600 8950 4600
Connection ~ 8950 4600
Wire Wire Line
	7450 4600 7450 5100
Wire Wire Line
	7000 4600 7000 5450
Wire Wire Line
	7150 5300 7000 5300
Connection ~ 7000 5300
Wire Wire Line
	6300 4550 6050 4550
Connection ~ 6300 4300
Wire Wire Line
	6700 4400 6300 4400
Connection ~ 6300 4400
Wire Wire Line
	3200 3450 3200 5900
Wire Wire Line
	3200 5900 9450 5900
Wire Wire Line
	9450 5900 9450 4800
Wire Wire Line
	3800 5500 3800 5900
Connection ~ 3800 5900
Wire Wire Line
	4650 5150 4650 5900
Connection ~ 4650 5900
Wire Wire Line
	7000 5750 7000 5900
Connection ~ 7000 5900
Wire Wire Line
	6050 4950 6050 5900
Connection ~ 6050 5900
Wire Wire Line
	7450 5500 7450 5900
Connection ~ 7450 5900
Wire Wire Line
	8000 4950 8000 5900
Connection ~ 8000 5900
Wire Wire Line
	8700 5150 7650 5150
Wire Wire Line
	7650 5150 7650 5000
Wire Wire Line
	7650 5000 7450 5000
Connection ~ 7450 5000
Wire Wire Line
	8350 4300 8450 4300
Wire Wire Line
	8450 2150 8450 4750
Wire Wire Line
	8450 4750 8300 4750
Wire Wire Line
	9000 5350 9000 5900
Connection ~ 9000 5900
Wire Wire Line
	9450 2150 9450 4400
Connection ~ 8450 4300
$Comp
L PORT U1
U 1 1 641906E5
P 3800 1850
F 0 "U1" H 3850 1950 30  0000 C CNN
F 1 "PORT" H 3800 1850 30  0000 C CNN
F 2 "" H 3800 1850 60  0000 C CNN
F 3 "" H 3800 1850 60  0000 C CNN
	1    3800 1850
	0    1    1    0   
$EndComp
$Comp
L eSim_GND #PWR01
U 1 1 64191056
P 6450 6100
F 0 "#PWR01" H 6450 5850 50  0001 C CNN
F 1 "eSim_GND" H 6450 5950 50  0000 C CNN
F 2 "" H 6450 6100 50  0001 C CNN
F 3 "" H 6450 6100 50  0001 C CNN
	1    6450 6100
	1    0    0    -1  
$EndComp
Wire Wire Line
	6450 6100 6450 5900
Connection ~ 6450 5900
Connection ~ 5650 4300
$EndSCHEMATC
