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
LIBS:UAF42-cache
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
U 1 1 63E6548C
P 3900 3750
F 0 "X1" H 3700 3750 60  0000 C CNN
F 1 "lm_741" H 3800 3500 60  0000 C CNN
F 2 "" H 3900 3750 60  0000 C CNN
F 3 "" H 3900 3750 60  0000 C CNN
	1    3900 3750
	1    0    0    -1  
$EndComp
$Comp
L lm_741 X2
U 1 1 63E654A3
P 5300 3750
F 0 "X2" H 5100 3750 60  0000 C CNN
F 1 "lm_741" H 5200 3500 60  0000 C CNN
F 2 "" H 5300 3750 60  0000 C CNN
F 3 "" H 5300 3750 60  0000 C CNN
	1    5300 3750
	1    0    0    -1  
$EndComp
$Comp
L lm_741 X3
U 1 1 63E654BC
P 6800 3750
F 0 "X3" H 6600 3750 60  0000 C CNN
F 1 "lm_741" H 6700 3500 60  0000 C CNN
F 2 "" H 6800 3750 60  0000 C CNN
F 3 "" H 6800 3750 60  0000 C CNN
	1    6800 3750
	1    0    0    -1  
$EndComp
$Comp
L resistor R2
U 1 1 63E654EA
P 3100 4450
F 0 "R2" H 3150 4580 50  0000 C CNN
F 1 "50k" H 3150 4400 50  0000 C CNN
F 2 "" H 3150 4430 30  0000 C CNN
F 3 "" V 3150 4500 30  0000 C CNN
	1    3100 4450
	1    0    0    -1  
$EndComp
$Comp
L resistor R4
U 1 1 63E65511
P 4200 4450
F 0 "R4" H 4250 4580 50  0000 C CNN
F 1 "50k" H 4250 4400 50  0000 C CNN
F 2 "" H 4250 4430 30  0000 C CNN
F 3 "" V 4250 4500 30  0000 C CNN
	1    4200 4450
	1    0    0    -1  
$EndComp
Wire Wire Line
	3350 3850 3350 4400
Wire Wire Line
	3300 4400 4100 4400
Connection ~ 3350 4400
Wire Wire Line
	5850 1600 5850 4400
Wire Wire Line
	5850 4400 4400 4400
$Comp
L resistor R3
U 1 1 63E65551
P 3800 3000
F 0 "R3" H 3850 3130 50  0000 C CNN
F 1 "50k" H 3850 2950 50  0000 C CNN
F 2 "" H 3850 2980 30  0000 C CNN
F 3 "" V 3850 3050 30  0000 C CNN
	1    3800 3000
	1    0    0    -1  
$EndComp
$Comp
L resistor R6
U 1 1 63E655E2
P 5300 2650
F 0 "R6" H 5350 2780 50  0000 C CNN
F 1 "50k" H 5350 2600 50  0000 C CNN
F 2 "" H 5350 2630 30  0000 C CNN
F 3 "" V 5350 2700 30  0000 C CNN
	1    5300 2650
	1    0    0    -1  
$EndComp
$Comp
L capacitor C1
U 1 1 63E6560F
P 5150 2950
F 0 "C1" H 5175 3050 50  0000 L CNN
F 1 "1n" H 5175 2850 50  0000 L CNN
F 2 "" H 5188 2800 30  0000 C CNN
F 3 "" H 5150 2950 60  0000 C CNN
	1    5150 2950
	0    1    1    0   
$EndComp
$Comp
L capacitor C2
U 1 1 63E6563E
P 6700 2950
F 0 "C2" H 6725 3050 50  0000 L CNN
F 1 "1n" H 6725 2850 50  0000 L CNN
F 2 "" H 6738 2800 30  0000 C CNN
F 3 "" H 6700 2950 60  0000 C CNN
	1    6700 2950
	0    1    1    0   
$EndComp
Wire Wire Line
	3700 2950 3350 2950
Wire Wire Line
	3350 2600 3350 3600
Wire Wire Line
	3150 2600 5200 2600
Connection ~ 3350 2950
Wire Wire Line
	4000 2950 4450 2950
Connection ~ 4450 2950
Wire Wire Line
	5000 2950 4750 2950
Wire Wire Line
	4750 2300 4750 3600
Wire Wire Line
	4450 1900 4450 3750
Wire Wire Line
	6850 2950 7350 2950
Wire Wire Line
	7350 2200 7350 3750
Connection ~ 7350 2950
Wire Wire Line
	6550 2950 6250 2950
Wire Wire Line
	6250 2300 6250 3600
Wire Wire Line
	5300 2950 5850 2950
Connection ~ 5850 3750
Wire Wire Line
	4750 3850 4650 3850
Wire Wire Line
	4650 3850 4650 4350
Wire Wire Line
	4650 4350 6250 4350
Wire Wire Line
	6250 3850 6250 4550
Wire Wire Line
	5500 2600 7350 2600
$Comp
L resistor R5
U 1 1 63E659CB
P 4550 2350
F 0 "R5" H 4600 2480 50  0000 C CNN
F 1 "316k" H 4600 2300 50  0000 C CNN
F 2 "" H 4600 2330 30  0000 C CNN
F 3 "" V 4600 2400 30  0000 C CNN
	1    4550 2350
	1    0    0    -1  
$EndComp
$Comp
L resistor R7
U 1 1 63E659FC
P 5950 2350
F 0 "R7" H 6000 2480 50  0000 C CNN
F 1 "316k" H 6000 2300 50  0000 C CNN
F 2 "" H 6000 2330 30  0000 C CNN
F 3 "" V 6000 2400 30  0000 C CNN
	1    5950 2350
	1    0    0    -1  
$EndComp
$Comp
L lm_741 X4
U 1 1 63E65C46
P 8150 3750
F 0 "X4" H 7950 3750 60  0000 C CNN
F 1 "lm_741" H 8050 3500 60  0000 C CNN
F 2 "" H 8150 3750 60  0000 C CNN
F 3 "" H 8150 3750 60  0000 C CNN
	1    8150 3750
	1    0    0    -1  
$EndComp
$Comp
L resistor R8
U 1 1 63E65C73
P 6650 2000
F 0 "R8" H 6700 2130 50  0000 C CNN
F 1 "10k" H 6700 1950 50  0000 C CNN
F 2 "" H 6700 1980 30  0000 C CNN
F 3 "" V 6700 2050 30  0000 C CNN
	1    6650 2000
	1    0    0    -1  
$EndComp
$Comp
L resistor R9
U 1 1 63E65CAA
P 7900 2000
F 0 "R9" H 7950 2130 50  0000 C CNN
F 1 "100k" H 7950 1950 50  0000 C CNN
F 2 "" H 7950 1980 30  0000 C CNN
F 3 "" V 7950 2050 30  0000 C CNN
	1    7900 2000
	1    0    0    -1  
$EndComp
Connection ~ 4750 2950
Connection ~ 5850 2950
Wire Wire Line
	6150 2300 6250 2300
Connection ~ 6250 2950
Wire Wire Line
	6550 1950 5850 1950
Connection ~ 5850 2300
$Comp
L resistor R1
U 1 1 63E663C7
P 2950 2650
F 0 "R1" H 3000 2780 50  0000 C CNN
F 1 "50k" H 3000 2600 50  0000 C CNN
F 2 "" H 3000 2630 30  0000 C CNN
F 3 "" V 3000 2700 30  0000 C CNN
	1    2950 2650
	1    0    0    -1  
$EndComp
Wire Wire Line
	6850 1950 7800 1950
Wire Wire Line
	7600 3600 7600 1950
Connection ~ 7600 1950
Wire Wire Line
	8100 1950 8700 1950
Wire Wire Line
	8700 1950 8700 3750
Connection ~ 3350 2600
$Comp
L eSim_GND #PWR01
U 1 1 63E66A2A
P 6250 4550
F 0 "#PWR01" H 6250 4300 50  0001 C CNN
F 1 "eSim_GND" H 6250 4400 50  0000 C CNN
F 2 "" H 6250 4550 50  0001 C CNN
F 3 "" H 6250 4550 50  0001 C CNN
	1    6250 4550
	1    0    0    -1  
$EndComp
$Comp
L eSim_GND #PWR02
U 1 1 63E66A5C
P 7600 4200
F 0 "#PWR02" H 7600 3950 50  0001 C CNN
F 1 "eSim_GND" H 7600 4050 50  0000 C CNN
F 2 "" H 7600 4200 50  0001 C CNN
F 3 "" H 7600 4200 50  0001 C CNN
	1    7600 4200
	1    0    0    -1  
$EndComp
Connection ~ 6250 4350
Wire Wire Line
	7600 4200 7600 3850
$Comp
L eSim_GND #PWR03
U 1 1 63E66C93
P 2650 4450
F 0 "#PWR03" H 2650 4200 50  0001 C CNN
F 1 "eSim_GND" H 2650 4300 50  0000 C CNN
F 2 "" H 2650 4450 50  0001 C CNN
F 3 "" H 2650 4450 50  0001 C CNN
	1    2650 4450
	1    0    0    -1  
$EndComp
Wire Wire Line
	2650 4450 2650 4400
Wire Wire Line
	2650 4400 3000 4400
$Comp
L PORT U1
U 1 1 63E670A1
P 2350 2600
F 0 "U1" H 2400 2700 30  0000 C CNN
F 1 "PORT" H 2350 2600 30  0000 C CNN
F 2 "" H 2350 2600 60  0000 C CNN
F 3 "" H 2350 2600 60  0000 C CNN
	1    2350 2600
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 2 1 63E67100
P 4800 1900
F 0 "U1" H 4850 2000 30  0000 C CNN
F 1 "PORT" H 4800 1900 30  0000 C CNN
F 2 "" H 4800 1900 60  0000 C CNN
F 3 "" H 4800 1900 60  0000 C CNN
	2    4800 1900
	-1   0    0    1   
$EndComp
$Comp
L PORT U1
U 3 1 63E673ED
P 6200 1600
F 0 "U1" H 6250 1700 30  0000 C CNN
F 1 "PORT" H 6200 1600 30  0000 C CNN
F 2 "" H 6200 1600 60  0000 C CNN
F 3 "" H 6200 1600 60  0000 C CNN
	3    6200 1600
	-1   0    0    1   
$EndComp
$Comp
L PORT U1
U 4 1 63E67488
P 7650 2200
F 0 "U1" H 7700 2300 30  0000 C CNN
F 1 "PORT" H 7650 2200 30  0000 C CNN
F 2 "" H 7650 2200 60  0000 C CNN
F 3 "" H 7650 2200 60  0000 C CNN
	4    7650 2200
	-1   0    0    1   
$EndComp
Wire Wire Line
	2600 2600 2850 2600
Wire Wire Line
	4550 1900 4450 1900
Connection ~ 4450 2300
Wire Wire Line
	5950 1600 5850 1600
Connection ~ 5850 1950
Wire Wire Line
	7400 2200 7350 2200
Connection ~ 7350 2600
Text GLabel 7750 4950 2    60   Input ~ 0
V+
Text GLabel 7750 5250 2    60   Input ~ 0
V-
Text GLabel 4100 3150 2    60   Input ~ 0
V+
Text GLabel 3950 4250 2    60   Input ~ 0
V-
$Comp
L PORT U1
U 5 1 63E694DD
P 9100 3750
F 0 "U1" H 9150 3850 30  0000 C CNN
F 1 "PORT" H 9100 3750 30  0000 C CNN
F 2 "" H 9100 3750 60  0000 C CNN
F 3 "" H 9100 3750 60  0000 C CNN
	5    9100 3750
	-1   0    0    1   
$EndComp
Wire Wire Line
	8700 3750 8850 3750
Text GLabel 5400 3100 2    60   Input ~ 0
V+
Text GLabel 5350 4250 2    60   Input ~ 0
V-
Text GLabel 6900 3150 2    60   Input ~ 0
V+
Text GLabel 6950 4300 2    60   Input ~ 0
V-
Text GLabel 8250 3050 2    60   Input ~ 0
V+
Text GLabel 8250 4300 2    60   Input ~ 0
V-
Wire Wire Line
	4100 3150 3750 3150
Wire Wire Line
	3750 3150 3750 3300
Wire Wire Line
	3950 4250 3750 4250
Wire Wire Line
	3750 4250 3750 4200
Wire Wire Line
	5400 3100 5150 3100
Wire Wire Line
	5150 3100 5150 3300
Wire Wire Line
	5350 4250 5150 4250
Wire Wire Line
	5150 4250 5150 4200
Wire Wire Line
	6900 3150 6650 3150
Wire Wire Line
	6650 3150 6650 3300
Wire Wire Line
	6950 4300 6650 4300
Wire Wire Line
	6650 4300 6650 4200
Wire Wire Line
	8250 3050 8000 3050
Wire Wire Line
	8000 3050 8000 3300
Wire Wire Line
	8250 4300 8000 4300
Wire Wire Line
	8000 4300 8000 4200
$Comp
L PORT U1
U 6 1 63E67DDE
P 7400 4950
F 0 "U1" H 7450 5050 30  0000 C CNN
F 1 "PORT" H 7400 4950 30  0000 C CNN
F 2 "" H 7400 4950 60  0000 C CNN
F 3 "" H 7400 4950 60  0000 C CNN
	6    7400 4950
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 7 1 63E67E29
P 7400 5250
F 0 "U1" H 7450 5350 30  0000 C CNN
F 1 "PORT" H 7400 5250 30  0000 C CNN
F 2 "" H 7400 5250 60  0000 C CNN
F 3 "" H 7400 5250 60  0000 C CNN
	7    7400 5250
	1    0    0    -1  
$EndComp
Wire Wire Line
	7750 4950 7650 4950
Wire Wire Line
	7750 5250 7650 5250
$EndSCHEMATC
