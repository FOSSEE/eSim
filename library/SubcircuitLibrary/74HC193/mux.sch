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
L d_and U3
U 1 1 67CB20E3
P 5000 3050
F 0 "U3" H 5000 3050 60  0000 C CNN
F 1 "d_and" H 5050 3150 60  0000 C CNN
F 2 "" H 5000 3050 60  0000 C CNN
F 3 "" H 5000 3050 60  0000 C CNN
	1    5000 3050
	1    0    0    -1  
$EndComp
$Comp
L d_and U4
U 1 1 67CB217D
P 5000 3800
F 0 "U4" H 5000 3800 60  0000 C CNN
F 1 "d_and" H 5050 3900 60  0000 C CNN
F 2 "" H 5000 3800 60  0000 C CNN
F 3 "" H 5000 3800 60  0000 C CNN
	1    5000 3800
	1    0    0    -1  
$EndComp
$Comp
L d_or U5
U 1 1 67CB21A2
P 6600 3400
F 0 "U5" H 6600 3400 60  0000 C CNN
F 1 "d_or" H 6600 3500 60  0000 C CNN
F 2 "" H 6600 3400 60  0000 C CNN
F 3 "" H 6600 3400 60  0000 C CNN
	1    6600 3400
	1    0    0    -1  
$EndComp
Wire Wire Line
	5450 3000 6150 3000
Wire Wire Line
	6150 3000 6150 3300
Wire Wire Line
	5450 3750 6150 3750
Wire Wire Line
	6150 3750 6150 3400
$Comp
L d_inverter U2
U 1 1 67CB21FF
P 3050 3800
F 0 "U2" H 3050 3700 60  0000 C CNN
F 1 "d_inverter" H 3050 3950 60  0000 C CNN
F 2 "" H 3100 3750 60  0000 C CNN
F 3 "" H 3100 3750 60  0000 C CNN
	1    3050 3800
	1    0    0    -1  
$EndComp
Wire Wire Line
	3350 3800 4550 3800
$Comp
L PORT U1
U 1 1 67CB22E7
P 1700 2750
F 0 "U1" H 1750 2850 30  0000 C CNN
F 1 "PORT" H 1700 2750 30  0000 C CNN
F 2 "" H 1700 2750 60  0000 C CNN
F 3 "" H 1700 2750 60  0000 C CNN
	1    1700 2750
	1    0    0    -1  
$EndComp
Wire Wire Line
	1950 2750 4550 2750
Wire Wire Line
	4550 2750 4550 2950
Wire Wire Line
	2750 3800 2750 2750
Connection ~ 2750 2750
$Comp
L PORT U1
U 3 1 67CB23D9
P 4100 3050
F 0 "U1" H 4150 3150 30  0000 C CNN
F 1 "PORT" H 4100 3050 30  0000 C CNN
F 2 "" H 4100 3050 60  0000 C CNN
F 3 "" H 4100 3050 60  0000 C CNN
	3    4100 3050
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 2 1 67CB2470
P 4000 3700
F 0 "U1" H 4050 3800 30  0000 C CNN
F 1 "PORT" H 4000 3700 30  0000 C CNN
F 2 "" H 4000 3700 60  0000 C CNN
F 3 "" H 4000 3700 60  0000 C CNN
	2    4000 3700
	1    0    0    -1  
$EndComp
Wire Wire Line
	4350 3050 4550 3050
Wire Wire Line
	4250 3700 4550 3700
$Comp
L PORT U1
U 4 1 67CB24FC
P 7400 3350
F 0 "U1" H 7450 3450 30  0000 C CNN
F 1 "PORT" H 7400 3350 30  0000 C CNN
F 2 "" H 7400 3350 60  0000 C CNN
F 3 "" H 7400 3350 60  0000 C CNN
	4    7400 3350
	-1   0    0    1   
$EndComp
Wire Wire Line
	7150 3350 7050 3350
$EndSCHEMATC
