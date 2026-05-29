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
LIBS:SN74LS74_TEST-cache
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
L SN74LS74 X1
U 1 1 68FB8F0C
P 3800 5750
F 0 "X1" H 5750 7350 60  0000 C CNN
F 1 "SN74LS74" H 5750 7450 60  0000 C CNN
F 2 "" H 5750 7350 60  0001 C CNN
F 3 "" H 5750 7350 60  0001 C CNN
	1    3800 5750
	1    0    0    -1  
$EndComp
$Comp
L adc_bridge_4 U5
U 1 1 68FB8F85
P 4150 4100
F 0 "U5" H 4150 4100 60  0000 C CNN
F 1 "adc_bridge_4" H 4150 4400 60  0000 C CNN
F 2 "" H 4150 4100 60  0000 C CNN
F 3 "" H 4150 4100 60  0000 C CNN
	1    4150 4100
	1    0    0    -1  
$EndComp
$Comp
L pulse v1
U 1 1 68FB9067
P 2200 3050
F 0 "v1" H 2000 3150 60  0000 C CNN
F 1 "pulse" H 2000 3000 60  0000 C CNN
F 2 "R1" H 1900 3050 60  0000 C CNN
F 3 "" H 2200 3050 60  0000 C CNN
	1    2200 3050
	0    1    1    0   
$EndComp
$Comp
L pulse v2
U 1 1 68FB90C0
P 2200 4000
F 0 "v2" H 2000 4100 60  0000 C CNN
F 1 "pulse" H 2000 3950 60  0000 C CNN
F 2 "R1" H 1900 4000 60  0000 C CNN
F 3 "" H 2200 4000 60  0000 C CNN
	1    2200 4000
	0    1    1    0   
$EndComp
$Comp
L pulse v3
U 1 1 68FB9101
P 2200 4600
F 0 "v3" H 2000 4700 60  0000 C CNN
F 1 "pulse" H 2000 4550 60  0000 C CNN
F 2 "R1" H 1900 4600 60  0000 C CNN
F 3 "" H 2200 4600 60  0000 C CNN
	1    2200 4600
	0    1    1    0   
$EndComp
$Comp
L pulse v4
U 1 1 68FB912C
P 2200 5150
F 0 "v4" H 2000 5250 60  0000 C CNN
F 1 "pulse" H 2000 5100 60  0000 C CNN
F 2 "R1" H 1900 5150 60  0000 C CNN
F 3 "" H 2200 5150 60  0000 C CNN
	1    2200 5150
	0    1    1    0   
$EndComp
$Comp
L GND #PWR01
U 1 1 68FB924A
P 1200 3850
F 0 "#PWR01" H 1200 3600 50  0001 C CNN
F 1 "GND" H 1200 3700 50  0000 C CNN
F 2 "" H 1200 3850 50  0001 C CNN
F 3 "" H 1200 3850 50  0001 C CNN
	1    1200 3850
	0    1    1    0   
$EndComp
$Comp
L dac_bridge_2 U6
U 1 1 68FB9294
P 6850 4050
F 0 "U6" H 6850 4050 60  0000 C CNN
F 1 "dac_bridge_2" H 6900 4200 60  0000 C CNN
F 2 "" H 6850 4050 60  0000 C CNN
F 3 "" H 6850 4050 60  0000 C CNN
	1    6850 4050
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U7
U 1 1 68FB939E
P 7750 3800
F 0 "U7" H 7750 4300 60  0000 C CNN
F 1 "plot_v1" H 7950 4150 60  0000 C CNN
F 2 "" H 7750 3800 60  0000 C CNN
F 3 "" H 7750 3800 60  0000 C CNN
	1    7750 3800
	0    1    1    0   
$EndComp
$Comp
L plot_v1 U8
U 1 1 68FB93D7
P 7750 4350
F 0 "U8" H 7750 4850 60  0000 C CNN
F 1 "plot_v1" H 7950 4700 60  0000 C CNN
F 2 "" H 7750 4350 60  0000 C CNN
F 3 "" H 7750 4350 60  0000 C CNN
	1    7750 4350
	0    1    1    0   
$EndComp
$Comp
L plot_v1 U4
U 1 1 68FB9472
P 3050 3050
F 0 "U4" H 3050 3550 60  0000 C CNN
F 1 "plot_v1" H 3250 3400 60  0000 C CNN
F 2 "" H 3050 3050 60  0000 C CNN
F 3 "" H 3050 3050 60  0000 C CNN
	1    3050 3050
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U1
U 1 1 68FB94ED
P 2750 4150
F 0 "U1" H 2750 4650 60  0000 C CNN
F 1 "plot_v1" H 2950 4500 60  0000 C CNN
F 2 "" H 2750 4150 60  0000 C CNN
F 3 "" H 2750 4150 60  0000 C CNN
	1    2750 4150
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U2
U 1 1 68FB952E
P 2800 4750
F 0 "U2" H 2800 5250 60  0000 C CNN
F 1 "plot_v1" H 3000 5100 60  0000 C CNN
F 2 "" H 2800 4750 60  0000 C CNN
F 3 "" H 2800 4750 60  0000 C CNN
	1    2800 4750
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U3
U 1 1 68FB95A9
P 2850 5300
F 0 "U3" H 2850 5800 60  0000 C CNN
F 1 "plot_v1" H 3050 5650 60  0000 C CNN
F 2 "" H 2850 5300 60  0000 C CNN
F 3 "" H 2850 5300 60  0000 C CNN
	1    2850 5300
	1    0    0    -1  
$EndComp
Text GLabel 3500 3150 0    60   Input ~ 0
SDbar
Text GLabel 3250 3900 1    60   Input ~ 0
D
Text GLabel 3300 4550 1    60   Input ~ 0
Clock
Text GLabel 7750 3700 0    60   Input ~ 0
Q
Text GLabel 7800 4200 0    60   Input ~ 0
Qbar
Wire Wire Line
	4700 3900 4700 3250
Wire Wire Line
	4700 3250 5750 3250
Wire Wire Line
	5750 3250 5750 3500
Wire Wire Line
	4700 4000 5200 4000
Wire Wire Line
	5200 4000 5200 3850
Wire Wire Line
	4700 4100 5200 4100
Wire Wire Line
	5200 4100 5200 4300
Wire Wire Line
	4700 4200 4700 4850
Wire Wire Line
	4700 4850 5750 4850
Wire Wire Line
	5750 4850 5750 4650
Wire Wire Line
	3600 3900 3600 3050
Wire Wire Line
	3600 3050 2650 3050
Wire Wire Line
	2650 4000 3600 4000
Wire Wire Line
	3600 4100 3450 4100
Wire Wire Line
	3450 4100 3450 4600
Wire Wire Line
	3450 4600 2650 4600
Wire Wire Line
	3600 4200 3600 5150
Wire Wire Line
	3600 5150 2650 5150
Wire Wire Line
	1750 3050 1400 3050
Wire Wire Line
	1400 3050 1400 5150
Wire Wire Line
	1400 5150 1750 5150
Wire Wire Line
	1750 4600 1400 4600
Connection ~ 1400 4600
Wire Wire Line
	1750 4000 1400 4000
Connection ~ 1400 4000
Wire Wire Line
	1400 3850 1200 3850
Connection ~ 1400 3850
Wire Wire Line
	6300 3850 6400 3850
Wire Wire Line
	6400 3850 6400 4000
Wire Wire Line
	6300 4250 6400 4250
Wire Wire Line
	6400 4250 6400 4100
Wire Wire Line
	7400 4000 7400 3800
Wire Wire Line
	7400 3800 7950 3800
Wire Wire Line
	7400 4100 7400 4350
Wire Wire Line
	7400 4350 7950 4350
Wire Wire Line
	3050 2850 3050 3050
Connection ~ 3050 3050
Wire Wire Line
	3500 3150 3600 3150
Connection ~ 3600 3150
Wire Wire Line
	2750 3950 2750 4000
Connection ~ 2750 4000
Wire Wire Line
	3250 3900 3250 4000
Connection ~ 3250 4000
Wire Wire Line
	2800 4550 2800 4600
Connection ~ 2800 4600
Wire Wire Line
	3300 4550 3300 4600
Connection ~ 3300 4600
Wire Wire Line
	2850 5100 2850 5150
Connection ~ 2850 5150
Wire Wire Line
	3400 5050 3400 5150
Connection ~ 3400 5150
Wire Wire Line
	7750 3700 7800 3700
Wire Wire Line
	7800 3700 7800 3800
Connection ~ 7800 3800
Wire Wire Line
	7800 4200 7850 4200
Wire Wire Line
	7850 4200 7850 4350
Connection ~ 7850 4350
Text GLabel 3400 5050 1    60   Input ~ 0
CDbar
$EndSCHEMATC
