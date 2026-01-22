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
LIBS:MPY100-cache
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
L DC v1
U 1 1 665446FD
P 4400 2700
F 0 "v1" H 4200 2800 60  0000 C CNN
F 1 "DC" H 4200 2650 60  0000 C CNN
F 2 "R1" H 4100 2700 60  0000 C CNN
F 3 "" H 4400 2700 60  0000 C CNN
	1    4400 2700
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR01
U 1 1 665448C6
P 6700 3400
F 0 "#PWR01" H 6700 3150 50  0001 C CNN
F 1 "GND" H 6700 3250 50  0000 C CNN
F 2 "" H 6700 3400 50  0001 C CNN
F 3 "" H 6700 3400 50  0001 C CNN
	1    6700 3400
	1    0    0    -1  
$EndComp
Text GLabel 5050 3250 3    60   Input ~ 0
Vout
Text GLabel 4800 3600 1    60   Input ~ 0
V1
Text GLabel 7000 1800 0    60   Input ~ 0
V2
$Comp
L GND #PWR02
U 1 1 6654BBA7
P 7000 2900
F 0 "#PWR02" H 7000 2650 50  0001 C CNN
F 1 "GND" H 7000 2750 50  0000 C CNN
F 2 "" H 7000 2900 50  0001 C CNN
F 3 "" H 7000 2900 50  0001 C CNN
	1    7000 2900
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR03
U 1 1 6654BC35
P 6150 4550
F 0 "#PWR03" H 6150 4300 50  0001 C CNN
F 1 "GND" H 6150 4400 50  0000 C CNN
F 2 "" H 6150 4550 50  0001 C CNN
F 3 "" H 6150 4550 50  0001 C CNN
	1    6150 4550
	1    0    0    -1  
$EndComp
Wire Wire Line
	4400 2250 5700 2250
Wire Wire Line
	5700 2250 5700 2650
Wire Wire Line
	6200 3400 6200 3300
Wire Wire Line
	7000 1700 7000 1900
Wire Wire Line
	4550 3600 5150 3600
Wire Wire Line
	6750 3200 6200 3200
Wire Wire Line
	4400 3150 4400 3550
Wire Wire Line
	5150 2950 5150 3000
Wire Wire Line
	5150 3250 5150 3200
Wire Wire Line
	4800 3250 5150 3250
Wire Wire Line
	6750 3400 6750 3000
Wire Wire Line
	6450 3400 6750 3400
Wire Wire Line
	6200 3600 6200 3750
Wire Wire Line
	4800 2950 5150 2950
Connection ~ 6700 3400
Wire Wire Line
	7000 2900 7000 2800
Wire Wire Line
	6200 3750 6450 3750
Wire Wire Line
	6450 3750 6450 3400
Connection ~ 6750 3200
Wire Wire Line
	4550 3650 4550 3600
Wire Wire Line
	7000 1700 6550 1700
Wire Wire Line
	4550 4550 6150 4550
$Comp
L GND #PWR04
U 1 1 6658DC6D
P 5000 2600
F 0 "#PWR04" H 5000 2350 50  0001 C CNN
F 1 "GND" H 5000 2450 50  0000 C CNN
F 2 "" H 5000 2600 50  0001 C CNN
F 3 "" H 5000 2600 50  0001 C CNN
	1    5000 2600
	1    0    0    -1  
$EndComp
Wire Wire Line
	5000 2600 4800 2600
$Comp
L DC v4
U 1 1 6658E251
P 3950 3500
F 0 "v4" H 3750 3600 60  0000 C CNN
F 1 "DC" H 3750 3450 60  0000 C CNN
F 2 "R1" H 3650 3500 60  0000 C CNN
F 3 "" H 3950 3500 60  0000 C CNN
	1    3950 3500
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR05
U 1 1 6658E2E3
P 3950 4000
F 0 "#PWR05" H 3950 3750 50  0001 C CNN
F 1 "GND" H 3950 3850 50  0000 C CNN
F 2 "" H 3950 4000 50  0001 C CNN
F 3 "" H 3950 4000 50  0001 C CNN
	1    3950 4000
	1    0    0    -1  
$EndComp
Wire Wire Line
	3950 4000 3950 3950
Wire Wire Line
	3950 3050 4300 3050
Wire Wire Line
	4300 3050 4300 3400
Wire Wire Line
	4300 3400 5150 3400
$Comp
L GND #PWR06
U 1 1 6658E44E
P 4400 3550
F 0 "#PWR06" H 4400 3300 50  0001 C CNN
F 1 "GND" H 4400 3400 50  0000 C CNN
F 2 "" H 4400 3550 50  0001 C CNN
F 3 "" H 4400 3550 50  0001 C CNN
	1    4400 3550
	1    0    0    -1  
$EndComp
Connection ~ 4800 2950
Wire Wire Line
	6550 1700 6550 3900
Wire Wire Line
	6550 3900 5700 3900
Wire Wire Line
	6700 3050 6700 3000
Wire Wire Line
	6700 3000 6750 3000
$Comp
L resistor R2
U 1 1 6666D283
P 4750 3050
F 0 "R2" H 4800 3180 50  0000 C CNN
F 1 "70k" H 4800 3000 50  0000 C CNN
F 2 "" H 4800 3030 30  0000 C CNN
F 3 "" V 4800 3100 30  0000 C CNN
	1    4750 3050
	0    1    1    0   
$EndComp
$Comp
L resistor R1
U 1 1 6666D2CC
P 4750 2750
F 0 "R1" H 4800 2880 50  0000 C CNN
F 1 "10k" H 4800 2700 50  0000 C CNN
F 2 "" H 4800 2730 30  0000 C CNN
F 3 "" V 4800 2800 30  0000 C CNN
	1    4750 2750
	0    1    1    0   
$EndComp
Wire Wire Line
	4800 2600 4800 2650
Wire Wire Line
	6700 3050 6650 3050
Wire Wire Line
	6650 3050 6650 3000
Wire Wire Line
	6650 3000 6200 3000
$Comp
L sine v2
U 1 1 6667F51E
P 4550 4100
F 0 "v2" H 4350 4200 60  0000 C CNN
F 1 "sine" H 4350 4050 60  0000 C CNN
F 2 "R1" H 4250 4100 60  0000 C CNN
F 3 "" H 4550 4100 60  0000 C CNN
	1    4550 4100
	1    0    0    -1  
$EndComp
$Comp
L sine v3
U 1 1 6667F581
P 7000 2350
F 0 "v3" H 6800 2450 60  0000 C CNN
F 1 "sine" H 6800 2300 60  0000 C CNN
F 2 "R1" H 6700 2350 60  0000 C CNN
F 3 "" H 7000 2350 60  0000 C CNN
	1    7000 2350
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U1
U 1 1 6667F6A9
P 4550 3550
F 0 "U1" H 4550 4050 60  0000 C CNN
F 1 "plot_v1" H 4750 3900 60  0000 C CNN
F 2 "" H 4550 3550 60  0000 C CNN
F 3 "" H 4550 3550 60  0000 C CNN
	1    4550 3550
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U2
U 1 1 6667F75A
P 4900 4250
F 0 "U2" H 4900 4750 60  0000 C CNN
F 1 "plot_v1" H 5100 4600 60  0000 C CNN
F 2 "" H 4900 4250 60  0000 C CNN
F 3 "" H 4900 4250 60  0000 C CNN
	1    4900 4250
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U3
U 1 1 6667F7C2
P 6400 2500
F 0 "U3" H 6400 3000 60  0000 C CNN
F 1 "plot_v1" H 6600 2850 60  0000 C CNN
F 2 "" H 6400 2500 60  0000 C CNN
F 3 "" H 6400 2500 60  0000 C CNN
	1    6400 2500
	1    0    0    -1  
$EndComp
Wire Wire Line
	6400 2300 6400 2350
Wire Wire Line
	6400 2350 6550 2350
Connection ~ 6550 2350
Wire Wire Line
	4550 3350 4900 3350
Wire Wire Line
	4900 3350 4900 3250
Connection ~ 4900 3250
Wire Wire Line
	4700 4050 4900 4050
Wire Wire Line
	4700 4050 4700 3600
Connection ~ 4700 3600
$Comp
L sine v5
U 1 1 6667FA92
P 6950 4100
F 0 "v5" H 6750 4200 60  0000 C CNN
F 1 "sine" H 6750 4050 60  0000 C CNN
F 2 "R1" H 6650 4100 60  0000 C CNN
F 3 "" H 6950 4100 60  0000 C CNN
	1    6950 4100
	1    0    0    -1  
$EndComp
Wire Wire Line
	6200 3300 6950 3300
Wire Wire Line
	6950 3300 6950 3650
$Comp
L GND #PWR07
U 1 1 6667FC05
P 6950 4600
F 0 "#PWR07" H 6950 4350 50  0001 C CNN
F 1 "GND" H 6950 4450 50  0000 C CNN
F 2 "" H 6950 4600 50  0001 C CNN
F 3 "" H 6950 4600 50  0001 C CNN
	1    6950 4600
	1    0    0    -1  
$EndComp
Wire Wire Line
	6950 4600 6950 4550
$Comp
L plot_v1 U4
U 1 1 6667FD96
P 7150 3650
F 0 "U4" H 7150 4150 60  0000 C CNN
F 1 "plot_v1" H 7350 4000 60  0000 C CNN
F 2 "" H 7150 3650 60  0000 C CNN
F 3 "" H 7150 3650 60  0000 C CNN
	1    7150 3650
	1    0    0    -1  
$EndComp
Wire Wire Line
	6950 3500 7150 3500
Wire Wire Line
	7150 3500 7150 3450
Connection ~ 6950 3500
Text GLabel 6900 3300 1    60   Input ~ 0
Z2
$Comp
L MPY100 X1
U 1 1 66680ABD
P 4800 3700
F 0 "X1" H 5700 4200 60  0000 C CNN
F 1 "MPY100" H 5700 4100 60  0000 C CNN
F 2 "" H 4800 3700 60  0001 C CNN
F 3 "" H 4800 3700 60  0001 C CNN
	1    4800 3700
	1    0    0    -1  
$EndComp
$EndSCHEMATC
