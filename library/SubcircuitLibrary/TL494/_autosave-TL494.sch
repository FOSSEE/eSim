EESchema Schematic File Version 5
EELAYER 36 0
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
Comment5 ""
Comment6 ""
Comment7 ""
Comment8 ""
Comment9 ""
$EndDescr
Connection ~ 2700 4050
Connection ~ 3250 2850
Connection ~ 5500 3200
Connection ~ 6650 3100
NoConn ~ 4400 3200
NoConn ~ 4450 1650
NoConn ~ 4500 3250
NoConn ~ 4500 4750
NoConn ~ 4550 1700
NoConn ~ 4600 4800
NoConn ~ 4950 2650
Wire Wire Line
	2700 2500 2700 4050
Wire Wire Line
	2700 4050 2700 5600
Wire Wire Line
	2700 4050 4300 4050
Wire Wire Line
	2700 5600 4400 5600
Wire Wire Line
	3250 1600 3250 2850
Wire Wire Line
	3250 2850 3250 4700
Wire Wire Line
	3250 4700 4400 4700
Wire Wire Line
	3550 3050 5400 3050
Wire Wire Line
	3550 3700 3550 3050
Wire Wire Line
	3700 3450 3900 3450
Wire Wire Line
	3750 1900 3950 1900
Wire Wire Line
	3750 2150 3950 2150
Wire Wire Line
	3800 5250 4000 5250
Wire Wire Line
	3850 5000 4000 5000
Wire Wire Line
	3900 3700 3550 3700
Wire Wire Line
	4300 2850 3250 2850
Wire Wire Line
	4300 3150 4300 2850
Wire Wire Line
	4350 1600 3250 1600
Wire Wire Line
	4350 2500 2700 2500
Wire Wire Line
	5000 3600 6450 3600
Wire Wire Line
	5050 2050 5500 2050
Wire Wire Line
	5400 3050 5400 3200
Wire Wire Line
	5400 3200 5500 3200
Wire Wire Line
	5500 2050 5500 3200
Wire Wire Line
	5500 3200 5500 5150
Wire Wire Line
	5500 5150 5100 5150
Wire Wire Line
	6450 3100 6650 3100
Wire Wire Line
	6450 3600 6450 3100
Wire Wire Line
	6650 2500 6650 3100
Wire Wire Line
	6650 3100 6650 3700
Wire Wire Line
	6650 3700 6700 3700
Wire Wire Line
	6950 2800 6950 2700
Wire Wire Line
	7000 4000 7000 3900
Text Label 1600 5700 0    50   ~ 0
DTC
Text Label 1600 6000 0    50   ~ 0
OUTPUT_CTRL
Text Label 1650 6350 0    50   ~ 0
VREF
Text Label 2700 4050 0    50   ~ 0
GND
Text Label 3250 2850 0    50   ~ 0
VCC
Text Label 3700 3450 0    50   ~ 0
RAMP
Text Label 3750 1900 0    50   ~ 0
1IN-
Text Label 3750 2150 0    50   ~ 0
1IN+
Text Label 3800 5250 0    50   ~ 0
2IN+
Text Label 3850 5000 0    50   ~ 0
2IN-
Text Label 5500 3250 0    50   ~ 0
FEEDBACK
Text Label 6950 2300 0    50   ~ 0
C1
Text Label 6950 2800 0    50   ~ 0
E1
Text Label 7000 3500 0    50   ~ 0
C2
Text Label 7000 4000 0    50   ~ 0
E2
$Comp
L eSim_Devices:eSim_NPN Q1
U 1 1 00000000
P 6850 2500
F 0 "Q1" H 7050 2550 50  0000 L CNN
F 1 "eSim_NPN" H 7050 2450 50  0000 L CNN
F 2 "" H 7050 2600 29  0000 C CNN
F 3 "" H 6850 2500 60  0000 C CNN
	1    6850 2500
	1    0    0    -1  
$EndComp
$Comp
L eSim_Devices:eSim_NPN Q2
U 1 1 00000000
P 6900 3700
F 0 "Q2" H 7100 3750 50  0000 L CNN
F 1 "eSim_NPN" H 7100 3650 50  0000 L CNN
F 2 "" H 7100 3800 29  0000 C CNN
F 3 "" H 6900 3700 60  0000 C CNN
	1    6900 3700
	1    0    0    -1  
$EndComp
$Comp
L eSim_Subckt:lm_741 X1
U 1 1 00000000
P 4450 3600
F 0 "X1" H 5000 3802 60  0000 C CNN
F 1 "lm_741" H 5000 3652 60  0000 C CNN
F 2 "" H 4450 3600 60  0000 C CNN
F 3 "" H 4450 3600 60  0000 C CNN
	1    4450 3600
	1    0    0    -1  
$EndComp
$Comp
L eSim_Subckt:lm_741 X2
U 1 1 00000000
P 4500 2050
F 0 "X2" H 5050 2252 60  0000 C CNN
F 1 "lm_741" H 5050 2102 60  0000 C CNN
F 2 "" H 4500 2050 60  0000 C CNN
F 3 "" H 4500 2050 60  0000 C CNN
	1    4500 2050
	1    0    0    -1  
$EndComp
$Comp
L eSim_Subckt:lm_741 X3
U 1 1 00000000
P 4550 5150
F 0 "X3" H 5100 5352 60  0000 C CNN
F 1 "lm_741" H 5100 5202 60  0000 C CNN
F 2 "" H 4550 5150 60  0000 C CNN
F 3 "" H 4550 5150 60  0000 C CNN
	1    4550 5150
	1    0    0    -1  
$EndComp
$EndSCHEMATC
