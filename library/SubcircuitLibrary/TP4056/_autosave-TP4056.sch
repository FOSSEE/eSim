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
Connection ~ 4250 4000
Connection ~ 5950 3000
Connection ~ 5950 3300
Wire Wire Line
	3850 3000 4350 3000
Wire Wire Line
	3850 3900 3850 4000
Wire Wire Line
	3850 4000 4250 4000
Wire Wire Line
	4250 3150 4250 4000
Wire Wire Line
	4350 3000 4350 2950
Wire Wire Line
	4350 3150 4250 3150
Wire Wire Line
	5250 3150 5350 3150
Wire Wire Line
	5700 3000 5950 3000
Wire Wire Line
	5700 3300 5950 3300
Wire Wire Line
	5950 2950 5250 2950
Wire Wire Line
	5950 3000 5950 2950
Wire Wire Line
	5950 3000 6200 3000
Wire Wire Line
	5950 3300 5950 3400
Wire Wire Line
	5950 3300 6200 3300
Text Label 4050 3000 0    50   ~ 0
vin
Text Label 5350 3150 0    50   ~ 0
chg_st
Text Label 5450 2950 0    50   ~ 0
vbat
$Comp
L eSim_Power:eSim_GND #PWR01
U 1 1 00000000
P 4250 4000
F 0 "#PWR01" H 4250 3750 50  0001 C CNN
F 1 "eSim_GND" H 4250 3800 50  0000 C CNN
F 2 "" H 4250 4000 50  0001 C CNN
F 3 "" H 4250 4000 50  0001 C CNN
	1    4250 4000
	1    0    0    -1  
$EndComp
$Comp
L eSim_Power:eSim_GND #PWR02
U 1 1 00000000
P 5950 3400
F 0 "#PWR02" H 5950 3150 50  0001 C CNN
F 1 "eSim_GND" H 5950 3200 50  0000 C CNN
F 2 "" H 5950 3400 50  0001 C CNN
F 3 "" H 5950 3400 50  0001 C CNN
	1    5950 3400
	1    0    0    -1  
$EndComp
$Comp
L eSim_Devices:resistor R1
U 1 1 00000000
P 5750 3200
F 0 "R1" V 5850 3150 50  0000 R CNN
F 1 "1k" V 5750 3150 50  0000 R CNN
F 2 "" H 5800 3180 30  0000 C CNN
F 3 "" V 5800 3250 30  0000 C CNN
	1    5750 3200
	0    -1   -1   0   
$EndComp
$Comp
L eSim_Devices:capacitor C1
U 1 1 00000000
P 6200 3150
F 0 "C1" H 6350 3200 50  0000 L CNN
F 1 "4.7uf" H 6350 3100 50  0000 L CNN
F 2 "" H 6238 3000 30  0000 C CNN
F 3 "" H 6200 3150 60  0000 C CNN
	1    6200 3150
	1    0    0    -1  
$EndComp
$Comp
L eSim_Sources:DC v1
U 1 1 00000000
P 3850 3450
F 0 "v1" H 4050 3575 60  0000 L CNN
F 1 "5v" H 4050 3425 60  0000 L CNN
F 2 "" H 4050 3275 60  0000 L CNN
F 3 "" H 3850 3450 60  0000 C CNN
	1    3850 3450
	1    0    0    -1  
$EndComp
$Comp
L TP4056:TP4056 X1
U 1 1 00000000
P 4750 3000
F 0 "X1" H 4800 3400 50  0000 C CNN
F 1 "TP4056" H 4800 3300 50  0000 C CNN
F 2 "" H 4750 3000 50  0000 C CNN
F 3 "" H 4750 3000 50  0000 C CNN
	1    4750 3000
	1    0    0    -1  
$EndComp
$EndSCHEMATC
