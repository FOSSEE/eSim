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
LIBS:TINA_TI_Rectifier-cache
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
L lm_741 X1
U 1 1 630DEBC8
P 4000 3500
F 0 "X1" H 3800 3500 60  0000 C CNN
F 1 "lm_741" H 3900 3250 60  0000 C CNN
F 2 "" H 4000 3500 60  0000 C CNN
F 3 "" H 4000 3500 60  0000 C CNN
	1    4000 3500
	1    0    0    -1  
$EndComp
$Comp
L lm_741 X2
U 1 1 630DEC2E
P 6700 3400
F 0 "X2" H 6500 3400 60  0000 C CNN
F 1 "lm_741" H 6600 3150 60  0000 C CNN
F 2 "" H 6700 3400 60  0000 C CNN
F 3 "" H 6700 3400 60  0000 C CNN
	1    6700 3400
	1    0    0    -1  
$EndComp
$Comp
L resistor R1
U 1 1 630DED64
P 3250 4100
F 0 "R1" H 3300 4230 50  0000 C CNN
F 1 "49.9" H 3300 4050 50  0000 C CNN
F 2 "" H 3300 4080 30  0000 C CNN
F 3 "" V 3300 4150 30  0000 C CNN
	1    3250 4100
	0    1    1    0   
$EndComp
$Comp
L resistor R3
U 1 1 630DEE0E
P 5900 4100
F 0 "R3" H 5950 4230 50  0000 C CNN
F 1 "1k" H 5950 4050 50  0000 C CNN
F 2 "" H 5950 4080 30  0000 C CNN
F 3 "" V 5950 4150 30  0000 C CNN
	1    5900 4100
	0    1    1    0   
$EndComp
$Comp
L eSim_Diode D2
U 1 1 630DEEA8
P 5400 3500
F 0 "D2" H 5400 3600 50  0000 C CNN
F 1 "eSim_Diode" H 5400 3400 50  0000 C CNN
F 2 "" H 5400 3500 60  0000 C CNN
F 3 "" H 5400 3500 60  0000 C CNN
	1    5400 3500
	1    0    0    -1  
$EndComp
$Comp
L eSim_Diode D1
U 1 1 630DEF23
P 5000 2600
F 0 "D1" H 5000 2700 50  0000 C CNN
F 1 "eSim_Diode" H 5000 2500 50  0000 C CNN
F 2 "" H 5000 2600 60  0000 C CNN
F 3 "" H 5000 2600 60  0000 C CNN
	1    5000 2600
	0    1    1    0   
$EndComp
$Comp
L capacitor C1
U 1 1 630DEF6B
P 4600 2600
F 0 "C1" H 4625 2700 50  0000 L CNN
F 1 "47p" H 4625 2500 50  0000 L CNN
F 2 "" H 4638 2450 30  0000 C CNN
F 3 "" H 4600 2600 60  0000 C CNN
	1    4600 2600
	1    0    0    -1  
$EndComp
$Comp
L resistor R2
U 1 1 630DF05D
P 5550 2050
F 0 "R2" H 5600 2180 50  0000 C CNN
F 1 "1k" H 5600 2000 50  0000 C CNN
F 2 "" H 5600 2030 30  0000 C CNN
F 3 "" V 5600 2100 30  0000 C CNN
	1    5550 2050
	-1   0    0    1   
$EndComp
$Comp
L resistor R4
U 1 1 630DF101
P 6500 2050
F 0 "R4" H 6550 2180 50  0000 C CNN
F 1 "1k" H 6550 2000 50  0000 C CNN
F 2 "" H 6550 2030 30  0000 C CNN
F 3 "" V 6550 2100 30  0000 C CNN
	1    6500 2050
	-1   0    0    1   
$EndComp
$Comp
L capacitor C3
U 1 1 630DF148
P 7100 2700
F 0 "C3" H 7125 2800 50  0000 L CNN
F 1 "100p" H 7125 2600 50  0000 L CNN
F 2 "" H 7138 2550 30  0000 C CNN
F 3 "" H 7100 2700 60  0000 C CNN
	1    7100 2700
	1    0    0    -1  
$EndComp
$Comp
L capacitor C5
U 1 1 630DF1F2
P 7500 2700
F 0 "C5" H 7525 2800 50  0000 L CNN
F 1 "100n" H 7525 2600 50  0000 L CNN
F 2 "" H 7538 2550 30  0000 C CNN
F 3 "" H 7500 2700 60  0000 C CNN
	1    7500 2700
	1    0    0    -1  
$EndComp
$Comp
L capacitor C2
U 1 1 630DF244
P 6800 4550
F 0 "C2" H 6825 4650 50  0000 L CNN
F 1 "100p" H 6825 4450 50  0000 L CNN
F 2 "" H 6838 4400 30  0000 C CNN
F 3 "" H 6800 4550 60  0000 C CNN
	1    6800 4550
	1    0    0    -1  
$EndComp
$Comp
L capacitor C4
U 1 1 630DF2AA
P 7250 4550
F 0 "C4" H 7275 4650 50  0000 L CNN
F 1 "100n" H 7275 4450 50  0000 L CNN
F 2 "" H 7288 4400 30  0000 C CNN
F 3 "" H 7250 4550 60  0000 C CNN
	1    7250 4550
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR01
U 1 1 630DF502
P 3350 5050
F 0 "#PWR01" H 3350 4800 50  0001 C CNN
F 1 "GND" H 3350 4900 50  0000 C CNN
F 2 "" H 3350 5050 50  0001 C CNN
F 3 "" H 3350 5050 50  0001 C CNN
	1    3350 5050
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR02
U 1 1 630DFA95
P 5950 4800
F 0 "#PWR02" H 5950 4550 50  0001 C CNN
F 1 "GND" H 5950 4650 50  0000 C CNN
F 2 "" H 5950 4800 50  0001 C CNN
F 3 "" H 5950 4800 50  0001 C CNN
	1    5950 4800
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR03
U 1 1 630DFAD1
P 6800 4900
F 0 "#PWR03" H 6800 4650 50  0001 C CNN
F 1 "GND" H 6800 4750 50  0000 C CNN
F 2 "" H 6800 4900 50  0001 C CNN
F 3 "" H 6800 4900 50  0001 C CNN
	1    6800 4900
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR04
U 1 1 630DFB06
P 7250 4900
F 0 "#PWR04" H 7250 4650 50  0001 C CNN
F 1 "GND" H 7250 4750 50  0000 C CNN
F 2 "" H 7250 4900 50  0001 C CNN
F 3 "" H 7250 4900 50  0001 C CNN
	1    7250 4900
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR05
U 1 1 630DFB3B
P 7100 3050
F 0 "#PWR05" H 7100 2800 50  0001 C CNN
F 1 "GND" H 7100 2900 50  0000 C CNN
F 2 "" H 7100 3050 50  0001 C CNN
F 3 "" H 7100 3050 50  0001 C CNN
	1    7100 3050
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR06
U 1 1 630DFB70
P 7500 3050
F 0 "#PWR06" H 7500 2800 50  0001 C CNN
F 1 "GND" H 7500 2900 50  0000 C CNN
F 2 "" H 7500 3050 50  0001 C CNN
F 3 "" H 7500 3050 50  0001 C CNN
	1    7500 3050
	1    0    0    -1  
$EndComp
Text Label 8350 2350 0    60   Italic 12
Vpos
Text Label 7950 4150 0    60   Italic 12
Vneg
$Comp
L PORT U1
U 1 1 631276E6
P 2550 4000
F 0 "U1" H 2600 4100 30  0000 C CNN
F 1 "PORT" H 2550 4000 30  0000 C CNN
F 2 "" H 2550 4000 60  0000 C CNN
F 3 "" H 2550 4000 60  0000 C CNN
	1    2550 4000
	1    0    0    -1  
$EndComp
Wire Wire Line
	4550 3500 5250 3500
Wire Wire Line
	5550 3500 6150 3500
Wire Wire Line
	5950 4000 5950 3500
Connection ~ 5950 3500
Wire Wire Line
	5950 4300 5950 4800
Wire Wire Line
	6550 3850 6550 4150
Wire Wire Line
	6450 4150 8150 4150
Wire Wire Line
	6800 4400 6800 4150
Connection ~ 6800 4150
Wire Wire Line
	7250 4400 7250 4150
Connection ~ 7250 4150
Wire Wire Line
	6800 4700 6800 4900
Wire Wire Line
	7250 4900 7250 4700
Wire Wire Line
	6550 2350 6550 2950
Wire Wire Line
	6550 2450 7950 2450
Wire Wire Line
	7950 2450 7950 2350
Wire Wire Line
	7100 2550 7100 2450
Connection ~ 7100 2450
Wire Wire Line
	7500 2550 7500 2450
Connection ~ 7500 2450
Wire Wire Line
	7100 2850 7100 3050
Wire Wire Line
	7500 2850 7500 3050
Wire Wire Line
	7250 3400 8450 3400
Wire Wire Line
	6600 2100 8250 2100
Wire Wire Line
	8250 2100 8250 3400
Connection ~ 8250 3400
Wire Wire Line
	6300 2100 5650 2100
Wire Wire Line
	5350 2100 3250 2100
Wire Wire Line
	3250 2100 3250 3350
Wire Wire Line
	3250 3350 3450 3350
Wire Wire Line
	5000 2450 5000 2100
Connection ~ 5000 2100
Wire Wire Line
	5000 2750 5000 3500
Connection ~ 5000 3500
Wire Wire Line
	4600 2750 4600 3500
Connection ~ 4600 3500
Wire Wire Line
	4600 2450 4600 2100
Connection ~ 4600 2100
Wire Wire Line
	3450 3600 2800 3600
Wire Wire Line
	2800 3600 2800 4000
Wire Wire Line
	3300 4300 3300 5050
Wire Wire Line
	3300 5050 3350 5050
Wire Wire Line
	3300 4000 3300 3600
Connection ~ 3300 3600
Wire Wire Line
	6150 3250 5850 3250
Wire Wire Line
	5850 3250 5850 2100
Wire Wire Line
	5850 2100 5900 2100
Connection ~ 5900 2100
Text Label 2800 3950 0    60   Italic 12
Vin
Text Label 8300 3400 0    60   Italic 12
Vout
$Comp
L PORT U1
U 2 1 63128122
P 8400 4150
F 0 "U1" H 8450 4250 30  0000 C CNN
F 1 "PORT" H 8400 4150 30  0000 C CNN
F 2 "" H 8400 4150 60  0000 C CNN
F 3 "" H 8400 4150 60  0000 C CNN
	2    8400 4150
	-1   0    0    1   
$EndComp
Wire Wire Line
	3850 3050 3850 2350
Wire Wire Line
	3850 2350 6550 2350
Connection ~ 6550 2450
Wire Wire Line
	3850 3950 6450 3950
Wire Wire Line
	6450 3950 6450 4150
Connection ~ 6550 4150
$Comp
L PORT U1
U 4 1 631984C4
P 8800 2350
F 0 "U1" H 8850 2450 30  0000 C CNN
F 1 "PORT" H 8800 2350 30  0000 C CNN
F 2 "" H 8800 2350 60  0000 C CNN
F 3 "" H 8800 2350 60  0000 C CNN
	4    8800 2350
	-1   0    0    1   
$EndComp
$Comp
L PORT U1
U 3 1 63198559
P 8700 3400
F 0 "U1" H 8750 3500 30  0000 C CNN
F 1 "PORT" H 8700 3400 30  0000 C CNN
F 2 "" H 8700 3400 60  0000 C CNN
F 3 "" H 8700 3400 60  0000 C CNN
	3    8700 3400
	-1   0    0    1   
$EndComp
Wire Wire Line
	7950 2350 8550 2350
$EndSCHEMATC
