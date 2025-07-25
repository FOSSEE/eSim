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
LIBS:TA7642_test-cache
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
L capacitor C1
U 1 1 683D76B8
P 4400 3900
F 0 "C1" H 4425 4000 50  0000 L CNN
F 1 "0.01u" H 4425 3800 50  0000 L CNN
F 2 "" H 4438 3750 30  0000 C CNN
F 3 "" H 4400 3900 60  0000 C CNN
	1    4400 3900
	0    1    1    0   
$EndComp
$Comp
L resistor R1
U 1 1 683D76F0
P 4100 4400
F 0 "R1" H 4150 4530 50  0000 C CNN
F 1 "75" H 4150 4350 50  0000 C CNN
F 2 "" H 4150 4380 30  0000 C CNN
F 3 "" V 4150 4450 30  0000 C CNN
	1    4100 4400
	0    1    1    0   
$EndComp
$Comp
L capacitor C2
U 1 1 683D775A
P 5800 4200
F 0 "C2" H 5825 4300 50  0000 L CNN
F 1 "1u" H 5825 4100 50  0000 L CNN
F 2 "" H 5838 4050 30  0000 C CNN
F 3 "" H 5800 4200 60  0000 C CNN
	1    5800 4200
	-1   0    0    1   
$EndComp
$Comp
L resistor R2
U 1 1 683D77BE
P 5350 3400
F 0 "R2" H 5400 3530 50  0000 C CNN
F 1 "100k" H 5400 3350 50  0000 C CNN
F 2 "" H 5400 3380 30  0000 C CNN
F 3 "" V 5400 3450 30  0000 C CNN
	1    5350 3400
	1    0    0    -1  
$EndComp
$Comp
L resistor R3
U 1 1 683D7822
P 6100 3400
F 0 "R3" H 6150 3530 50  0000 C CNN
F 1 "1.5k" H 6150 3350 50  0000 C CNN
F 2 "" H 6150 3380 30  0000 C CNN
F 3 "" V 6150 3450 30  0000 C CNN
	1    6100 3400
	1    0    0    -1  
$EndComp
$Comp
L eSim_GND #PWR01
U 1 1 683D78A0
P 6000 4800
F 0 "#PWR01" H 6000 4550 50  0001 C CNN
F 1 "eSim_GND" H 6000 4650 50  0000 C CNN
F 2 "" H 6000 4800 50  0001 C CNN
F 3 "" H 6000 4800 50  0001 C CNN
	1    6000 4800
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U1
U 1 1 683D78F9
P 6100 4100
F 0 "U1" H 6100 4600 60  0000 C CNN
F 1 "plot_v1" H 6300 4450 60  0000 C CNN
F 2 "" H 6100 4100 60  0000 C CNN
F 3 "" H 6100 4100 60  0000 C CNN
	1    6100 4100
	1    0    0    -1  
$EndComp
Text GLabel 6500 4050 2    60   Input ~ 0
Vout
$Comp
L sine v1
U 1 1 683D79C7
P 3750 4350
F 0 "v1" H 3550 4450 60  0000 C CNN
F 1 "sine" H 3550 4300 60  0000 C CNN
F 2 "R1" H 3450 4350 60  0000 C CNN
F 3 "" H 3750 4350 60  0000 C CNN
	1    3750 4350
	1    0    0    -1  
$EndComp
Wire Wire Line
	4550 3900 4800 3900
Wire Wire Line
	4150 3900 4150 4300
Wire Wire Line
	3750 3900 4250 3900
Wire Wire Line
	5600 3900 6100 3900
Wire Wire Line
	5800 3350 5800 4050
Wire Wire Line
	4700 3900 4700 3350
Wire Wire Line
	4700 3350 5250 3350
Connection ~ 4700 3900
Wire Wire Line
	5550 3350 6000 3350
Connection ~ 5800 3900
Connection ~ 5800 3350
Wire Wire Line
	5950 3900 5950 4050
Wire Wire Line
	5950 4050 6500 4050
Connection ~ 5950 3900
Connection ~ 4150 3900
Wire Wire Line
	3750 4800 6000 4800
Wire Wire Line
	4150 4800 4150 4600
Wire Wire Line
	5200 4800 5200 4200
Connection ~ 4150 4800
Wire Wire Line
	5800 4800 5800 4350
Connection ~ 5200 4800
Connection ~ 5800 4800
Text GLabel 3800 3800 0    60   Input ~ 0
in
$Comp
L plot_v1 U2
U 1 1 683DD3EC
P 3950 3900
F 0 "U2" H 3950 4400 60  0000 C CNN
F 1 "plot_v1" H 4150 4250 60  0000 C CNN
F 2 "" H 3950 3900 60  0000 C CNN
F 3 "" H 3950 3900 60  0000 C CNN
	1    3950 3900
	1    0    0    -1  
$EndComp
Wire Wire Line
	3950 3700 3950 3900
Connection ~ 3950 3900
Wire Wire Line
	3800 3800 3950 3800
Connection ~ 3950 3800
$Comp
L eSim_VCC #PWR02
U 1 1 683E8921
P 6350 3250
F 0 "#PWR02" H 6350 3100 50  0001 C CNN
F 1 "eSim_VCC" H 6350 3400 50  0000 C CNN
F 2 "" H 6350 3250 50  0001 C CNN
F 3 "" H 6350 3250 50  0001 C CNN
	1    6350 3250
	1    0    0    -1  
$EndComp
Wire Wire Line
	6350 3250 6350 3350
Wire Wire Line
	6350 3350 6300 3350
$Comp
L TA7642 X1
U 1 1 683E9609
P 5200 3900
F 0 "X1" H 5200 3500 60  0000 C CNN
F 1 "TA7642" H 5200 4200 60  0000 C CNN
F 2 "" H 5200 3900 60  0001 C CNN
F 3 "" H 5200 3900 60  0001 C CNN
	1    5200 3900
	1    0    0    -1  
$EndComp
$Comp
L resistor R4
U 1 1 683EA678
P 6000 4350
F 0 "R4" V 6050 4480 50  0000 C CNN
F 1 "100k" H 6050 4300 50  0000 C CNN
F 2 "" H 6050 4330 30  0000 C CNN
F 3 "" V 6050 4400 30  0000 C CNN
	1    6000 4350
	0    1    1    0   
$EndComp
Wire Wire Line
	6050 4550 6050 4650
Wire Wire Line
	6050 4650 5900 4650
Wire Wire Line
	5900 4650 5900 4800
Connection ~ 5900 4800
Wire Wire Line
	6050 4250 6050 4100
Wire Wire Line
	6050 4100 5900 4100
Wire Wire Line
	5900 4100 5900 3900
Connection ~ 5900 3900
$EndSCHEMATC
