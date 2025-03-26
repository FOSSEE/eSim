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
LIBS:device
LIBS:transistors
LIBS:conn
LIBS:linear
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
LIBS:eSim_User
LIBS:eSim_Plot
LIBS:eSim_PSpice
LIBS:UJT_RO-cache
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
L eSim_R R1
U 1 1 5D664780
P 4650 3000
F 0 "R1" H 4700 3130 50  0000 C CNN
F 1 "95.3k" H 4700 3050 50  0000 C CNN
F 2 "" H 4700 2980 30  0000 C CNN
F 3 "" V 4700 3050 30  0000 C CNN
	1    4650 3000
	0    -1   -1   0   
$EndComp
$Comp
L eSim_R R2
U 1 1 5D664781
P 5800 2850
F 0 "R2" H 5850 2980 50  0000 C CNN
F 1 "4.7K" H 5850 2900 50  0000 C CNN
F 2 "" H 5850 2830 30  0000 C CNN
F 3 "" V 5850 2900 30  0000 C CNN
	1    5800 2850
	0    -1   -1   0   
$EndComp
$Comp
L eSim_R R3
U 1 1 5D664782
P 5800 4550
F 0 "R3" H 5850 4680 50  0000 C CNN
F 1 "4.7k" H 5850 4600 50  0000 C CNN
F 2 "" H 5850 4530 30  0000 C CNN
F 3 "" V 5850 4600 30  0000 C CNN
	1    5800 4550
	0    -1   -1   0   
$EndComp
$Comp
L eSim_C C1
U 1 1 5D664783
P 4550 4300
F 0 "C1" H 4575 4400 50  0000 L CNN
F 1 "100n" H 4575 4200 50  0000 L CNN
F 2 "" H 4588 4150 30  0000 C CNN
F 3 "" H 4550 4300 60  0000 C CNN
	1    4550 4300
	1    0    0    -1  
$EndComp
Connection ~ 4550 3600
Wire Wire Line
	4600 2450 4600 2800
Wire Wire Line
	5750 2450 5750 2650
Wire Wire Line
	5750 2950 5750 3250
Wire Wire Line
	4600 3100 4550 3100
Wire Wire Line
	4550 3100 4550 4150
Wire Wire Line
	4550 4450 4550 5050
Wire Wire Line
	5750 2450 4600 2450
Wire Wire Line
	5750 4050 5750 4350
Wire Wire Line
	5750 4650 5750 5050
Wire Wire Line
	5750 5050 4550 5050
$Comp
L DC v1
U 1 1 5D664784
P 6800 3500
F 0 "v1" H 6600 3600 60  0000 C CNN
F 1 "DC" H 6600 3450 60  0000 C CNN
F 2 "R1" H 6500 3500 60  0000 C CNN
F 3 "" H 6800 3500 60  0000 C CNN
	1    6800 3500
	1    0    0    -1  
$EndComp
Wire Wire Line
	6800 3050 6800 2150
Wire Wire Line
	6800 2150 5300 2150
Wire Wire Line
	5300 2150 5300 2450
Connection ~ 5300 2450
Wire Wire Line
	6800 3950 6800 5650
Wire Wire Line
	6800 5650 5250 5650
Wire Wire Line
	5250 5650 5250 5050
Connection ~ 5250 5050
$Comp
L GND #PWR01
U 1 1 5D664785
P 4900 5050
F 0 "#PWR01" H 4900 4800 50  0001 C CNN
F 1 "GND" H 4900 4900 50  0000 C CNN
F 2 "" H 4900 5050 50  0001 C CNN
F 3 "" H 4900 5050 50  0001 C CNN
	1    4900 5050
	1    0    0    -1  
$EndComp
Connection ~ 4900 5050
$Comp
L UJT X1
U 1 1 5D664787
P 5750 3600
F 0 "X1" H 5700 3550 60  0000 C CNN
F 1 "UJT" H 5800 3550 60  0000 C CNN
F 2 "" H 5700 3550 60  0001 C CNN
F 3 "" H 5700 3550 60  0001 C CNN
	1    5750 3600
	1    0    0    -1  
$EndComp
Wire Wire Line
	4550 3600 5300 3600
$Comp
L plot_v1 U1
U 1 1 5D664788
P 6150 3200
F 0 "U1" H 6150 3700 60  0000 C CNN
F 1 "plot_v1" H 6350 3550 60  0000 C CNN
F 2 "" H 6150 3200 60  0000 C CNN
F 3 "" H 6150 3200 60  0000 C CNN
	1    6150 3200
	1    0    0    -1  
$EndComp
Wire Wire Line
	6150 3000 6150 3150
Wire Wire Line
	6150 3150 5750 3150
Connection ~ 5750 3150
$Comp
L plot_v1 U2
U 1 1 5D664789
P 6150 4400
F 0 "U2" H 6150 4900 60  0000 C CNN
F 1 "plot_v1" H 6350 4750 60  0000 C CNN
F 2 "" H 6150 4400 60  0000 C CNN
F 3 "" H 6150 4400 60  0000 C CNN
	1    6150 4400
	1    0    0    -1  
$EndComp
Wire Wire Line
	6150 4200 6150 4250
Wire Wire Line
	6150 4250 5750 4250
Connection ~ 5750 4250
Text GLabel 6150 3150 2    60   Input ~ 0
Vb2
Text GLabel 6150 4250 2    60   Input ~ 0
Vb1
$EndSCHEMATC
