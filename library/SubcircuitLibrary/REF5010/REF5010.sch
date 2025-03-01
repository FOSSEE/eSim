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
LIBS:REF5010-cache
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
U 1 1 675328EA
P 6450 3450
F 0 "X1" H 6250 3450 60  0000 C CNN
F 1 "lm_741" H 6350 3200 60  0000 C CNN
F 2 "" H 6450 3450 60  0000 C CNN
F 3 "" H 6450 3450 60  0000 C CNN
	1    6450 3450
	1    0    0    -1  
$EndComp
$Comp
L resistor R1
U 1 1 6753291B
P 4700 2500
F 0 "R1" H 4750 2630 50  0000 C CNN
F 1 "10k" H 4750 2450 50  0000 C CNN
F 2 "" H 4750 2480 30  0000 C CNN
F 3 "" V 4750 2550 30  0000 C CNN
	1    4700 2500
	1    0    0    -1  
$EndComp
$Comp
L resistor R2
U 1 1 67532938
P 6700 2500
F 0 "R2" H 6750 2630 50  0000 C CNN
F 1 "1k" H 6750 2450 50  0000 C CNN
F 2 "" H 6750 2480 30  0000 C CNN
F 3 "" V 6750 2550 30  0000 C CNN
	1    6700 2500
	1    0    0    -1  
$EndComp
$Comp
L resistor R4
U 1 1 675329A7
P 3500 3750
F 0 "R4" H 3550 3880 50  0000 C CNN
F 1 "60k" H 3550 3700 50  0000 C CNN
F 2 "" H 3550 3730 30  0000 C CNN
F 3 "" V 3550 3800 30  0000 C CNN
	1    3500 3750
	0    1    1    0   
$EndComp
$Comp
L dc I1
U 1 1 67532A3D
P 3550 2700
F 0 "I1" H 3350 2800 60  0000 C CNN
F 1 "10ua" H 3350 2650 60  0000 C CNN
F 2 "R1" H 3250 2700 60  0000 C CNN
F 3 "" H 3550 2700 60  0000 C CNN
	1    3550 2700
	-1   0    0    1   
$EndComp
$Comp
L DC v1
U 1 1 67532A78
P 4650 4600
F 0 "v1" H 4450 4700 60  0000 C CNN
F 1 "1.2v" H 4450 4550 60  0000 C CNN
F 2 "R1" H 4350 4600 60  0000 C CNN
F 3 "" H 4650 4600 60  0000 C CNN
	1    4650 4600
	1    0    0    -1  
$EndComp
$Comp
L resistor R3
U 1 1 67532AF1
P 4950 3600
F 0 "R3" H 5000 3730 50  0000 C CNN
F 1 "10k" H 5000 3550 50  0000 C CNN
F 2 "" H 5000 3580 30  0000 C CNN
F 3 "" V 5000 3650 30  0000 C CNN
	1    4950 3600
	1    0    0    -1  
$EndComp
$Comp
L resistor R5
U 1 1 67532BAE
P 6350 4650
F 0 "R5" H 6400 4780 50  0000 C CNN
F 1 "1k" H 6400 4600 50  0000 C CNN
F 2 "" H 6400 4630 30  0000 C CNN
F 3 "" V 6400 4700 30  0000 C CNN
	1    6350 4650
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 2 1 67532C44
P 4750 1400
F 0 "U1" H 4800 1500 30  0000 C CNN
F 1 "PORT" H 4750 1400 30  0000 C CNN
F 2 "" H 4750 1400 60  0000 C CNN
F 3 "" H 4750 1400 60  0000 C CNN
	2    4750 1400
	0    1    1    0   
$EndComp
$Comp
L PORT U1
U 7 1 67532C8A
P 8100 3450
F 0 "U1" H 8150 3550 30  0000 C CNN
F 1 "PORT" H 8100 3450 30  0000 C CNN
F 2 "" H 8100 3450 60  0000 C CNN
F 3 "" H 8100 3450 60  0000 C CNN
	7    8100 3450
	-1   0    0    1   
$EndComp
$Comp
L PORT U1
U 8 1 67532E38
P 8200 4600
F 0 "U1" H 8250 4700 30  0000 C CNN
F 1 "PORT" H 8200 4600 30  0000 C CNN
F 2 "" H 8200 4600 60  0000 C CNN
F 3 "" H 8200 4600 60  0000 C CNN
	8    8200 4600
	-1   0    0    1   
$EndComp
$Comp
L PORT U1
U 3 1 67532F0B
P 2600 3450
F 0 "U1" H 2650 3550 30  0000 C CNN
F 1 "PORT" H 2600 3450 30  0000 C CNN
F 2 "" H 2600 3450 60  0000 C CNN
F 3 "" H 2600 3450 60  0000 C CNN
	3    2600 3450
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 1 1 67533ECE
P 8350 2300
F 0 "U1" H 8400 2400 30  0000 C CNN
F 1 "PORT" H 8350 2300 30  0000 C CNN
F 2 "" H 8350 2300 60  0000 C CNN
F 3 "" H 8350 2300 60  0000 C CNN
	1    8350 2300
	-1   0    0    1   
$EndComp
$Comp
L PORT U1
U 4 1 67533F39
P 8800 4200
F 0 "U1" H 8850 4300 30  0000 C CNN
F 1 "PORT" H 8800 4200 30  0000 C CNN
F 2 "" H 8800 4200 60  0000 C CNN
F 3 "" H 8800 4200 60  0000 C CNN
	4    8800 4200
	-1   0    0    1   
$EndComp
$Comp
L PORT U1
U 5 1 67534049
P 9100 3250
F 0 "U1" H 9150 3350 30  0000 C CNN
F 1 "PORT" H 9100 3250 30  0000 C CNN
F 2 "" H 9100 3250 60  0000 C CNN
F 3 "" H 9100 3250 60  0000 C CNN
	5    9100 3250
	-1   0    0    1   
$EndComp
$Comp
L PORT U1
U 6 1 675340BF
P 5550 6100
F 0 "U1" H 5600 6200 30  0000 C CNN
F 1 "PORT" H 5550 6100 30  0000 C CNN
F 2 "" H 5550 6100 60  0000 C CNN
F 3 "" H 5550 6100 60  0000 C CNN
	6    5550 6100
	-1   0    0    1   
$EndComp
NoConn ~ 8100 2300
NoConn ~ 8850 3250
NoConn ~ 8550 4200
NoConn ~ 9050 4950
Wire Wire Line
	3550 2250 3550 1800
Wire Wire Line
	3550 1800 4750 1800
Wire Wire Line
	4750 1800 4750 1650
Wire Wire Line
	3550 3150 3550 3650
Wire Wire Line
	3550 3950 3550 5400
Wire Wire Line
	3550 5400 5250 5400
Wire Wire Line
	5250 5400 5250 6100
Wire Wire Line
	2850 3450 3550 3450
Connection ~ 3550 3450
Wire Wire Line
	4900 2450 6600 2450
Wire Wire Line
	7000 3450 7850 3450
Wire Wire Line
	6900 2450 7550 2450
Wire Wire Line
	7550 2450 7550 3450
Connection ~ 7550 3450
Wire Wire Line
	5150 3550 5900 3550
Wire Wire Line
	5900 3300 5550 3300
Wire Wire Line
	5550 3300 5550 2450
Connection ~ 5550 2450
Wire Wire Line
	5450 3550 5450 4600
Wire Wire Line
	5450 4600 6250 4600
Connection ~ 5450 3550
Wire Wire Line
	6550 4600 7950 4600
Wire Wire Line
	4650 4150 4650 3550
Wire Wire Line
	4650 3550 4850 3550
Wire Wire Line
	4600 2450 4250 2450
Wire Wire Line
	4250 2450 4250 5400
Connection ~ 4250 5400
Wire Wire Line
	4650 5050 4650 5400
Connection ~ 4650 5400
Wire Wire Line
	5250 6100 5300 6100
$EndSCHEMATC
