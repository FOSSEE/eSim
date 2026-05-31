EESchema Schematic File Version 2
LIBS:Fullwavebridgerectifier-rescue
LIBS:eSim_Analog
LIBS:eSim_Devices
LIBS:eSim_Digital
LIBS:eSim_Hybrid
LIBS:eSim_Miscellaneous
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
LIBS:eSim_Plot
LIBS:Fullwavebridgerectifier-cache
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
U 1 1 56A85DC5
P 3400 3600
F 0 "v1" H 3200 3700 60  0000 C CNN
F 1 "sine" H 3200 3550 60  0000 C CNN
F 2 "R1" H 3100 3600 60  0000 C CNN
F 3 "" H 3400 3600 60  0000 C CNN
	1    3400 3600
	1    0    0    -1  
$EndComp
$Comp
L D-RESCUE-Fullwavebridgerectifier D1
U 1 1 56A85EED
P 4200 2900
F 0 "D1" H 4200 3000 50  0000 C CNN
F 1 "D" H 4200 2800 50  0000 C CNN
F 2 "" H 4200 2900 60  0000 C CNN
F 3 "" H 4200 2900 60  0000 C CNN
	1    4200 2900
	0    -1   -1   0   
$EndComp
$Comp
L D-RESCUE-Fullwavebridgerectifier D3
U 1 1 56A85F6E
P 5000 2900
F 0 "D3" H 5000 3000 50  0000 C CNN
F 1 "D" H 5000 2800 50  0000 C CNN
F 2 "" H 5000 2900 60  0000 C CNN
F 3 "" H 5000 2900 60  0000 C CNN
	1    5000 2900
	0    -1   -1   0   
$EndComp
$Comp
L D-RESCUE-Fullwavebridgerectifier D2
U 1 1 56A85FBD
P 4200 4250
F 0 "D2" H 4200 4350 50  0000 C CNN
F 1 "D" H 4200 4150 50  0000 C CNN
F 2 "" H 4200 4250 60  0000 C CNN
F 3 "" H 4200 4250 60  0000 C CNN
	1    4200 4250
	0    -1   -1   0   
$EndComp
$Comp
L D-RESCUE-Fullwavebridgerectifier D4
U 1 1 56A8602F
P 5000 4250
F 0 "D4" H 5000 4350 50  0000 C CNN
F 1 "D" H 5000 4150 50  0000 C CNN
F 2 "" H 5000 4250 60  0000 C CNN
F 3 "" H 5000 4250 60  0000 C CNN
	1    5000 4250
	0    -1   -1   0   
$EndComp
$Comp
L R-RESCUE-Fullwavebridgerectifier R1
U 1 1 56A860D7
P 6050 3400
F 0 "R1" H 6100 3530 50  0000 C CNN
F 1 "1k" H 6100 3450 50  0000 C CNN
F 2 "" H 6100 3380 30  0000 C CNN
F 3 "" V 6100 3450 30  0000 C CNN
	1    6050 3400
	0    1    1    0   
$EndComp
Wire Wire Line
	4200 2750 4200 2650
Wire Wire Line
	4200 2650 6100 2650
Wire Wire Line
	5000 2650 5000 2750
Wire Wire Line
	4200 4100 4200 3050
Wire Wire Line
	5000 4100 5000 3050
Wire Wire Line
	4200 4400 4200 4500
Wire Wire Line
	4200 4500 6100 4500
Wire Wire Line
	5000 4500 5000 4400
Wire Wire Line
	6100 2650 6100 3300
Connection ~ 5000 2650
Wire Wire Line
	6100 4500 6100 3600
Connection ~ 5000 4500
Wire Wire Line
	3400 3150 3700 3150
Wire Wire Line
	3700 3150 3700 3400
Connection ~ 4200 3400
Wire Wire Line
	3400 4050 3700 4050
Wire Wire Line
	3700 4050 3700 3600
Connection ~ 5000 3600
$Comp
L GND #PWR1
U 1 1 56A862E5
P 5300 4650
F 0 "#PWR1" H 5300 4400 50  0001 C CNN
F 1 "GND" H 5300 4500 50  0000 C CNN
F 2 "" H 5300 4650 50  0000 C CNN
F 3 "" H 5300 4650 50  0000 C CNN
	1    5300 4650
	1    0    0    -1  
$EndComp
Wire Wire Line
	5300 4650 5300 4500
Connection ~ 5300 4500
Text GLabel 3550 3050 1    60   Input ~ 0
in1
Text GLabel 3550 4150 3    60   Input ~ 0
in2
Text GLabel 5800 2500 2    60   Input ~ 0
out
Wire Wire Line
	3550 3050 3550 3150
Connection ~ 3550 3150
Wire Wire Line
	3550 4150 3550 4050
Connection ~ 3550 4050
Wire Wire Line
	5800 2500 5750 2500
Wire Wire Line
	5750 2400 5750 2650
Connection ~ 5750 2650
Connection ~ 5750 2500
Wire Wire Line
	2850 3250 2850 3100
Wire Wire Line
	2850 3100 3550 3100
Connection ~ 3550 3100
Wire Wire Line
	2850 3850 2850 4100
Wire Wire Line
	2850 4100 3550 4100
Connection ~ 3550 4100
$Comp
L plot_v1 U2
U 1 1 56D43D75
P 5750 2600
F 0 "U2" H 5750 3100 60  0000 C CNN
F 1 "plot_v1" H 5950 2950 60  0000 C CNN
F 2 "" H 5750 2600 60  0000 C CNN
F 3 "" H 5750 2600 60  0000 C CNN
	1    5750 2600
	1    0    0    -1  
$EndComp
$Comp
L plot_v2 U1
U 1 1 56D43E45
P 2600 3550
F 0 "U1" H 2600 3950 60  0000 C CNN
F 1 "plot_v2" H 2600 3650 60  0000 C CNN
F 2 "" H 2600 3550 60  0000 C CNN
F 3 "" H 2600 3550 60  0000 C CNN
	1    2600 3550
	0    1    1    0   
$EndComp
Wire Wire Line
	3700 3400 4200 3400
Wire Wire Line
	3700 3600 5000 3600
$EndSCHEMATC
