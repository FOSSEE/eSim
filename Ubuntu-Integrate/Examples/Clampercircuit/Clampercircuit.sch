EESchema Schematic File Version 2
LIBS:Clampercircuit-rescue
LIBS:eSim_Analog
LIBS:eSim_Devices
LIBS:eSim_Digital
LIBS:eSim_Hybrid
LIBS:eSim_Miscellaneous
LIBS:eSim_Plot
LIBS:eSim_Power
LIBS:eSim_Sources
LIBS:eSim_Subckt
LIBS:eSim_User
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
LIBS:device
LIBS:transistors
LIBS:conn
LIBS:linear
LIBS:regul
LIBS:74xx
LIBS:cmos4000
LIBS:Clampercircuit-cache
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
L sine v1
U 1 1 56A864A1
P 3750 3550
F 0 "v1" H 3550 3650 60  0000 C CNN
F 1 "sine" H 3550 3500 60  0000 C CNN
F 2 "R1" H 3450 3550 60  0000 C CNN
F 3 "" H 3750 3550 60  0000 C CNN
	1    3750 3550
	1    0    0    -1  
$EndComp
$Comp
L C C1
U 1 1 56A86522
P 4300 2900
F 0 "C1" H 4325 3000 50  0000 L CNN
F 1 "1n" H 4325 2800 50  0000 L CNN
F 2 "" H 4338 2750 30  0000 C CNN
F 3 "" H 4300 2900 60  0000 C CNN
	1    4300 2900
	0    1    1    0   
$EndComp
$Comp
L D-RESCUE-Clampercircuit D1
U 1 1 56A86555
P 5100 3400
F 0 "D1" H 5100 3500 50  0000 C CNN
F 1 "D" H 5100 3300 50  0000 C CNN
F 2 "" H 5100 3400 60  0000 C CNN
F 3 "" H 5100 3400 60  0000 C CNN
	1    5100 3400
	0    1    1    0   
$EndComp
$Comp
L GND #PWR01
U 1 1 56A86578
P 4550 4150
F 0 "#PWR01" H 4550 3900 50  0001 C CNN
F 1 "GND" H 4550 4000 50  0000 C CNN
F 2 "" H 4550 4150 50  0000 C CNN
F 3 "" H 4550 4150 50  0000 C CNN
	1    4550 4150
	1    0    0    -1  
$EndComp
Wire Wire Line
	4150 2900 3750 2900
Wire Wire Line
	3750 2900 3750 3100
Wire Wire Line
	4450 2900 5100 2900
Wire Wire Line
	5100 2900 5100 3250
Wire Wire Line
	3750 4000 3750 4100
Wire Wire Line
	3750 4100 5100 4100
Wire Wire Line
	5100 4100 5100 3550
Text GLabel 3700 2800 0    60   Input ~ 0
in_neg
Text GLabel 5000 2750 2    60   Input ~ 0
out_neg
Wire Wire Line
	3700 2800 3800 2800
Wire Wire Line
	3800 2750 3800 2900
Connection ~ 3800 2900
Wire Wire Line
	5000 2750 4950 2750
Wire Wire Line
	4950 2750 4950 2900
Connection ~ 4950 2900
Wire Wire Line
	4550 4150 4550 4100
Connection ~ 4550 4100
$Comp
L sine v2
U 1 1 56A86723
P 6950 3550
F 0 "v2" H 6750 3650 60  0000 C CNN
F 1 "sine" H 6750 3500 60  0000 C CNN
F 2 "R1" H 6650 3550 60  0000 C CNN
F 3 "" H 6950 3550 60  0000 C CNN
	1    6950 3550
	1    0    0    -1  
$EndComp
$Comp
L C C2
U 1 1 56A86783
P 7600 2900
F 0 "C2" H 7625 3000 50  0000 L CNN
F 1 "1n" H 7625 2800 50  0000 L CNN
F 2 "" H 7638 2750 30  0000 C CNN
F 3 "" H 7600 2900 60  0000 C CNN
	1    7600 2900
	0    1    1    0   
$EndComp
$Comp
L D-RESCUE-Clampercircuit D2
U 1 1 56A867F1
P 8500 3400
F 0 "D2" H 8500 3500 50  0000 C CNN
F 1 "D" H 8500 3300 50  0000 C CNN
F 2 "" H 8500 3400 60  0000 C CNN
F 3 "" H 8500 3400 60  0000 C CNN
	1    8500 3400
	0    -1   -1   0   
$EndComp
$Comp
L GND #PWR02
U 1 1 56A868AB
P 7850 4150
F 0 "#PWR02" H 7850 3900 50  0001 C CNN
F 1 "GND" H 7850 4000 50  0000 C CNN
F 2 "" H 7850 4150 50  0000 C CNN
F 3 "" H 7850 4150 50  0000 C CNN
	1    7850 4150
	1    0    0    -1  
$EndComp
Wire Wire Line
	6950 3100 6950 2900
Wire Wire Line
	6950 2900 7450 2900
Wire Wire Line
	7750 2900 8500 2900
Wire Wire Line
	8500 2900 8500 3250
Wire Wire Line
	6950 4000 6950 4050
Wire Wire Line
	6950 4050 8500 4050
Wire Wire Line
	8500 4050 8500 3550
Wire Wire Line
	7850 4150 7850 4050
Connection ~ 7850 4050
Text GLabel 7000 2800 0    60   Input ~ 0
in_pos
Text GLabel 8450 2750 2    60   Input ~ 0
out_pos
Wire Wire Line
	7000 2800 7050 2800
Wire Wire Line
	7050 2650 7050 2900
Connection ~ 7050 2900
Wire Wire Line
	8450 2750 8400 2750
Wire Wire Line
	8400 2750 8400 2900
Connection ~ 8400 2900
Text Notes 4150 4750 0    60   ~ 0
Negative Clamper\n\n
Text Notes 7600 4650 0    60   ~ 0
Positive Clamper\n
$Comp
L plot_v1 U1
U 1 1 56D43FBF
P 3800 2950
F 0 "U1" H 3800 3450 60  0000 C CNN
F 1 "plot_v1" H 4000 3300 60  0000 C CNN
F 2 "" H 3800 2950 60  0000 C CNN
F 3 "" H 3800 2950 60  0000 C CNN
	1    3800 2950
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U2
U 1 1 56D44022
P 4950 2900
F 0 "U2" H 4950 3400 60  0000 C CNN
F 1 "plot_v1" H 5150 3250 60  0000 C CNN
F 2 "" H 4950 2900 60  0000 C CNN
F 3 "" H 4950 2900 60  0000 C CNN
	1    4950 2900
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U3
U 1 1 56D44072
P 7050 2850
F 0 "U3" H 7050 3350 60  0000 C CNN
F 1 "plot_v1" H 7250 3200 60  0000 C CNN
F 2 "" H 7050 2850 60  0000 C CNN
F 3 "" H 7050 2850 60  0000 C CNN
	1    7050 2850
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U4
U 1 1 56D440D3
P 8400 2850
F 0 "U4" H 8400 3350 60  0000 C CNN
F 1 "plot_v1" H 8600 3200 60  0000 C CNN
F 2 "" H 8400 2850 60  0000 C CNN
F 3 "" H 8400 2850 60  0000 C CNN
	1    8400 2850
	1    0    0    -1  
$EndComp
Connection ~ 3800 2800
Wire Wire Line
	4950 2700 4950 2800
Connection ~ 4950 2800
Connection ~ 7050 2800
Wire Wire Line
	8400 2650 8400 2800
Connection ~ 8400 2800
$EndSCHEMATC
