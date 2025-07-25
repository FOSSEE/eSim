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
L MC3340 X1
U 1 1 684032A2
P 5400 3300
F 0 "X1" H 5400 2800 60  0000 C CNN
F 1 "MC3340" H 5750 3550 60  0000 C CNN
F 2 "" H 5400 3900 60  0001 C CNN
F 3 "" H 5400 3900 60  0001 C CNN
	1    5400 3300
	1    0    0    -1  
$EndComp
$Comp
L capacitor_polarised C1
U 1 1 68403397
P 4400 3300
F 0 "C1" H 4425 3400 50  0000 L CNN
F 1 "1u" H 4425 3200 50  0000 L CNN
F 2 "" H 4400 3300 50  0001 C CNN
F 3 "" H 4400 3300 50  0001 C CNN
	1    4400 3300
	0    1    1    0   
$EndComp
$Comp
L sine v1
U 1 1 68403533
P 4250 4100
F 0 "v1" H 4050 4200 60  0000 C CNN
F 1 "sine" H 4050 4050 60  0000 C CNN
F 2 "R1" H 3950 4100 60  0000 C CNN
F 3 "" H 4250 4100 60  0000 C CNN
	1    4250 4100
	1    0    0    -1  
$EndComp
$Comp
L capacitor_polarised C2
U 1 1 68403666
P 5050 4250
F 0 "C2" H 5075 4350 50  0000 L CNN
F 1 "50u" H 5075 4150 50  0000 L CNN
F 2 "" H 5050 4250 50  0001 C CNN
F 3 "" H 5050 4250 50  0001 C CNN
	1    5050 4250
	1    0    0    -1  
$EndComp
$Comp
L eSim_GND #PWR01
U 1 1 6840394D
P 5400 4800
F 0 "#PWR01" H 5400 4550 50  0001 C CNN
F 1 "eSim_GND" H 5400 4650 50  0000 C CNN
F 2 "" H 5400 4800 50  0001 C CNN
F 3 "" H 5400 4800 50  0001 C CNN
	1    5400 4800
	1    0    0    -1  
$EndComp
$Comp
L resistor R1
U 1 1 68403F36
P 5200 5000
F 0 "R1" H 5250 5130 50  0000 C CNN
F 1 "50k" H 5250 4950 50  0000 C CNN
F 2 "" H 5250 4980 30  0000 C CNN
F 3 "" V 5250 5050 30  0000 C CNN
	1    5200 5000
	0    1    1    0   
$EndComp
$Comp
L eSim_GND #PWR02
U 1 1 68403FF4
P 5250 5300
F 0 "#PWR02" H 5250 5050 50  0001 C CNN
F 1 "eSim_GND" H 5250 5150 50  0000 C CNN
F 2 "" H 5250 5300 50  0001 C CNN
F 3 "" H 5250 5300 50  0001 C CNN
	1    5250 5300
	1    0    0    -1  
$EndComp
$Comp
L capacitor_polarised C3
U 1 1 6840431E
P 5800 4150
F 0 "C3" H 5825 4250 50  0000 L CNN
F 1 "620p" H 5825 4050 50  0000 L CNN
F 2 "" H 5800 4150 50  0001 C CNN
F 3 "" H 5800 4150 50  0001 C CNN
	1    5800 4150
	1    0    0    1   
$EndComp
$Comp
L plot_v1 U1
U 1 1 68404541
P 6250 3350
F 0 "U1" H 6250 3850 60  0000 C CNN
F 1 "plot_v1" H 6450 3700 60  0000 C CNN
F 2 "" H 6250 3350 60  0000 C CNN
F 3 "" H 6250 3350 60  0000 C CNN
	1    6250 3350
	1    0    0    -1  
$EndComp
Text GLabel 6450 3250 2    60   Input ~ 0
out
$Comp
L plot_v1 U2
U 1 1 68404A11
P 3600 3800
F 0 "U2" H 3600 4300 60  0000 C CNN
F 1 "plot_v1" H 3800 4150 60  0000 C CNN
F 2 "" H 3600 3800 60  0000 C CNN
F 3 "" H 3600 3800 60  0000 C CNN
	1    3600 3800
	1    0    0    -1  
$EndComp
Text GLabel 3700 3800 0    60   Input ~ 0
in
Wire Wire Line
	5450 2850 5450 2950
Wire Wire Line
	4550 3300 4950 3300
Wire Wire Line
	4250 3300 4250 3650
Wire Wire Line
	5050 4100 5250 4100
Wire Wire Line
	5250 3800 5250 4900
Wire Wire Line
	5050 4400 5050 4650
Wire Wire Line
	4250 4650 5800 4650
Wire Wire Line
	5400 3750 5400 4800
Connection ~ 5400 4650
Connection ~ 5250 4100
Wire Wire Line
	5250 5200 5250 5300
Wire Wire Line
	5800 4000 5800 3550
Wire Wire Line
	5800 4650 5800 4300
Wire Wire Line
	6250 3300 6100 3300
Wire Wire Line
	6250 3150 6250 3300
Wire Wire Line
	6250 3250 6450 3250
Connection ~ 6250 3250
Wire Wire Line
	4250 4550 4250 4650
Connection ~ 5050 4650
Wire Wire Line
	3600 3600 4250 3600
Wire Wire Line
	4250 3600 4250 3550
Connection ~ 4250 3550
Wire Wire Line
	3700 3800 3850 3800
Wire Wire Line
	3850 3800 3850 3600
Connection ~ 3850 3600
$Comp
L resistor R2
U 1 1 68413101
P 4650 4000
F 0 "R2" H 4700 4130 50  0000 C CNN
F 1 "100k" H 4700 3950 50  0000 C CNN
F 2 "" H 4700 3980 30  0000 C CNN
F 3 "" V 4700 4050 30  0000 C CNN
	1    4650 4000
	0    1    1    0   
$EndComp
Wire Wire Line
	4700 3900 4700 3300
Wire Wire Line
	4700 3300 4750 3300
Connection ~ 4750 3300
Wire Wire Line
	4700 4200 4700 4650
Connection ~ 4700 4650
$Comp
L DC v2
U 1 1 6841325C
P 5450 2400
F 0 "v2" H 5250 2500 60  0000 C CNN
F 1 "DC" H 5250 2350 60  0000 C CNN
F 2 "R1" H 5150 2400 60  0000 C CNN
F 3 "" H 5450 2400 60  0000 C CNN
	1    5450 2400
	1    0    0    1   
$EndComp
$Comp
L eSim_GND #PWR03
U 1 1 6841330C
P 5700 1950
F 0 "#PWR03" H 5700 1700 50  0001 C CNN
F 1 "eSim_GND" H 5700 1800 50  0000 C CNN
F 2 "" H 5700 1950 50  0001 C CNN
F 3 "" H 5700 1950 50  0001 C CNN
	1    5700 1950
	1    0    0    -1  
$EndComp
Wire Wire Line
	5450 1950 5700 1950
$EndSCHEMATC
