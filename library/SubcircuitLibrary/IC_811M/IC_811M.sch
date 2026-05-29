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
LIBS:IC_811M-cache
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
L TL811M X1
U 1 1 6845BEBA
P 6400 2750
F 0 "X1" H 6450 2200 60  0000 C CNN
F 1 "TL811M" H 6450 3300 60  0000 C CNN
F 2 "" H 6400 2750 60  0001 C CNN
F 3 "" H 6400 2750 60  0001 C CNN
	1    6400 2750
	1    0    0    -1  
$EndComp
$Comp
L resistor R1
U 1 1 6845BF00
P 4950 2250
F 0 "R1" H 5000 2380 50  0000 C CNN
F 1 "50k" H 5000 2200 50  0000 C CNN
F 2 "" H 5000 2230 30  0000 C CNN
F 3 "" V 5000 2300 30  0000 C CNN
	1    4950 2250
	1    0    0    -1  
$EndComp
$Comp
L resistor R2
U 1 1 6845BF41
P 4950 2500
F 0 "R2" H 5000 2630 50  0000 C CNN
F 1 "50k" H 5000 2450 50  0000 C CNN
F 2 "" H 5000 2480 30  0000 C CNN
F 3 "" V 5000 2550 30  0000 C CNN
	1    4950 2500
	1    0    0    -1  
$EndComp
$Comp
L DC v2
U 1 1 6845C1D6
P 5700 4400
F 0 "v2" H 5500 4500 60  0000 C CNN
F 1 "DC" H 5500 4350 60  0000 C CNN
F 2 "R1" H 5400 4400 60  0000 C CNN
F 3 "" H 5700 4400 60  0000 C CNN
	1    5700 4400
	1    0    0    -1  
$EndComp
$Comp
L DC v3
U 1 1 6845C210
P 6250 4400
F 0 "v3" H 6050 4500 60  0000 C CNN
F 1 "DC" H 6050 4350 60  0000 C CNN
F 2 "R1" H 5950 4400 60  0000 C CNN
F 3 "" H 6250 4400 60  0000 C CNN
	1    6250 4400
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR01
U 1 1 6845C27E
P 5550 4050
F 0 "#PWR01" H 5550 3800 50  0001 C CNN
F 1 "GND" H 5550 3900 50  0000 C CNN
F 2 "" H 5550 4050 50  0001 C CNN
F 3 "" H 5550 4050 50  0001 C CNN
	1    5550 4050
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR02
U 1 1 6845C2C0
P 5900 3450
F 0 "#PWR02" H 5900 3200 50  0001 C CNN
F 1 "GND" H 5900 3300 50  0000 C CNN
F 2 "" H 5900 3450 50  0001 C CNN
F 3 "" H 5900 3450 50  0001 C CNN
	1    5900 3450
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR03
U 1 1 6845C2DD
P 5700 4950
F 0 "#PWR03" H 5700 4700 50  0001 C CNN
F 1 "GND" H 5700 4800 50  0000 C CNN
F 2 "" H 5700 4950 50  0001 C CNN
F 3 "" H 5700 4950 50  0001 C CNN
	1    5700 4950
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR04
U 1 1 6845C2FA
P 6250 4950
F 0 "#PWR04" H 6250 4700 50  0001 C CNN
F 1 "GND" H 6250 4800 50  0000 C CNN
F 2 "" H 6250 4950 50  0001 C CNN
F 3 "" H 6250 4950 50  0001 C CNN
	1    6250 4950
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U1
U 1 1 6845C3CC
P 7000 2700
F 0 "U1" H 7000 3200 60  0000 C CNN
F 1 "plot_v1" H 7200 3050 60  0000 C CNN
F 2 "" H 7000 2700 60  0000 C CNN
F 3 "" H 7000 2700 60  0000 C CNN
	1    7000 2700
	0    1    1    0   
$EndComp
Text GLabel 7100 2400 1    60   Input ~ 0
OUT
$Comp
L plot_v1 U2
U 1 1 6845DA75
P 4150 2550
F 0 "U2" H 4150 3050 60  0000 C CNN
F 1 "plot_v1" H 4350 2900 60  0000 C CNN
F 2 "" H 4150 2550 60  0000 C CNN
F 3 "" H 4150 2550 60  0000 C CNN
	1    4150 2550
	0    -1   -1   0   
$EndComp
Text GLabel 4200 2400 1    60   Input ~ 0
IN
$Comp
L pulse v1
U 1 1 6845C0E1
P 4400 3050
F 0 "v1" H 4200 3150 60  0000 C CNN
F 1 "pulse" H 4200 3000 60  0000 C CNN
F 2 "R1" H 4100 3050 60  0000 C CNN
F 3 "" H 4400 3050 60  0000 C CNN
	1    4400 3050
	1    0    0    -1  
$EndComp
Wire Wire Line
	5900 2200 5900 2350
Wire Wire Line
	5150 2450 5900 2450
Wire Wire Line
	4850 2200 4400 2200
Wire Wire Line
	4400 2200 4400 2600
Wire Wire Line
	4400 2450 4850 2450
Wire Wire Line
	5900 2550 5550 2550
Wire Wire Line
	5550 2550 5550 4050
Wire Wire Line
	5900 2650 5550 2650
Connection ~ 5550 2650
Wire Wire Line
	5900 2800 5700 2800
Wire Wire Line
	5700 2800 5700 3950
Wire Wire Line
	5900 2900 5800 2900
Wire Wire Line
	5800 2900 5800 3950
Wire Wire Line
	5900 3250 5900 3450
Wire Wire Line
	5550 3100 5900 3100
Connection ~ 5550 3100
Connection ~ 4400 2450
Wire Wire Line
	4400 3500 4400 3800
Wire Wire Line
	4400 3800 5550 3800
Connection ~ 5550 3800
Wire Wire Line
	5800 3950 6250 3950
Wire Wire Line
	5700 4850 5700 4950
Wire Wire Line
	6250 4850 6250 4950
Wire Wire Line
	6900 2700 7200 2700
Wire Wire Line
	7100 2400 7100 2700
Connection ~ 7100 2700
Wire Wire Line
	3950 2550 4400 2550
Connection ~ 4400 2550
Wire Wire Line
	4200 2400 4200 2550
Connection ~ 4200 2550
Wire Wire Line
	5150 2200 5900 2200
$EndSCHEMATC
