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
P 3200 4350
F 0 "v1" H 3000 4450 60  0000 C CNN
F 1 "DC" H 3000 4300 60  0000 C CNN
F 2 "R1" H 2900 4350 60  0000 C CNN
F 3 "" H 3200 4350 60  0000 C CNN
	1    3200 4350
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR01
U 1 1 665448C6
P 5500 5050
F 0 "#PWR01" H 5500 4800 50  0001 C CNN
F 1 "GND" H 5500 4900 50  0000 C CNN
F 2 "" H 5500 5050 50  0001 C CNN
F 3 "" H 5500 5050 50  0001 C CNN
	1    5500 5050
	1    0    0    -1  
$EndComp
Text GLabel 3850 4900 3    60   Input ~ 0
Vout
Text GLabel 3600 5250 1    60   Input ~ 0
V1
Text GLabel 5800 3450 0    60   Input ~ 0
V2
$Comp
L GND #PWR02
U 1 1 6654BBA7
P 5800 4550
F 0 "#PWR02" H 5800 4300 50  0001 C CNN
F 1 "GND" H 5800 4400 50  0000 C CNN
F 2 "" H 5800 4550 50  0001 C CNN
F 3 "" H 5800 4550 50  0001 C CNN
	1    5800 4550
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR03
U 1 1 6654BC35
P 4950 6200
F 0 "#PWR03" H 4950 5950 50  0001 C CNN
F 1 "GND" H 4950 6050 50  0000 C CNN
F 2 "" H 4950 6200 50  0001 C CNN
F 3 "" H 4950 6200 50  0001 C CNN
	1    4950 6200
	1    0    0    -1  
$EndComp
Wire Wire Line
	3200 3900 4500 3900
Wire Wire Line
	4500 3900 4500 4300
Wire Wire Line
	5000 5050 5000 4950
Wire Wire Line
	5800 3350 5800 3550
Wire Wire Line
	3350 5250 3950 5250
Wire Wire Line
	5550 4850 5000 4850
Wire Wire Line
	3200 4800 3200 5200
Wire Wire Line
	3950 4600 3950 4650
Wire Wire Line
	3950 4900 3950 4850
Wire Wire Line
	3600 4900 3950 4900
Wire Wire Line
	5550 5050 5550 4650
Wire Wire Line
	5250 5050 5550 5050
Wire Wire Line
	5000 5250 5000 5400
Wire Wire Line
	3600 4600 3950 4600
Connection ~ 5500 5050
Wire Wire Line
	5800 4550 5800 4450
Wire Wire Line
	5000 5400 5250 5400
Wire Wire Line
	5250 5400 5250 5050
Connection ~ 5550 4850
Wire Wire Line
	3350 5300 3350 5250
Wire Wire Line
	5800 3350 5350 3350
Wire Wire Line
	3350 6200 4950 6200
$Comp
L GND #PWR04
U 1 1 6658DC6D
P 3800 4250
F 0 "#PWR04" H 3800 4000 50  0001 C CNN
F 1 "GND" H 3800 4100 50  0000 C CNN
F 2 "" H 3800 4250 50  0001 C CNN
F 3 "" H 3800 4250 50  0001 C CNN
	1    3800 4250
	1    0    0    -1  
$EndComp
Wire Wire Line
	3800 4250 3600 4250
$Comp
L DC v4
U 1 1 6658E251
P 2750 5150
F 0 "v4" H 2550 5250 60  0000 C CNN
F 1 "DC" H 2550 5100 60  0000 C CNN
F 2 "R1" H 2450 5150 60  0000 C CNN
F 3 "" H 2750 5150 60  0000 C CNN
	1    2750 5150
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR05
U 1 1 6658E2E3
P 2750 5650
F 0 "#PWR05" H 2750 5400 50  0001 C CNN
F 1 "GND" H 2750 5500 50  0000 C CNN
F 2 "" H 2750 5650 50  0001 C CNN
F 3 "" H 2750 5650 50  0001 C CNN
	1    2750 5650
	1    0    0    -1  
$EndComp
Wire Wire Line
	2750 5650 2750 5600
Wire Wire Line
	2750 4700 3100 4700
Wire Wire Line
	3100 4700 3100 5050
Wire Wire Line
	3100 5050 3950 5050
$Comp
L GND #PWR06
U 1 1 6658E44E
P 3200 5200
F 0 "#PWR06" H 3200 4950 50  0001 C CNN
F 1 "GND" H 3200 5050 50  0000 C CNN
F 2 "" H 3200 5200 50  0001 C CNN
F 3 "" H 3200 5200 50  0001 C CNN
	1    3200 5200
	1    0    0    -1  
$EndComp
Connection ~ 3600 4600
Wire Wire Line
	5350 3350 5350 5550
Wire Wire Line
	5350 5550 4500 5550
Wire Wire Line
	5500 4700 5500 4650
Wire Wire Line
	5500 4650 5550 4650
$Comp
L resistor R2
U 1 1 6666D283
P 3550 4700
F 0 "R2" H 3600 4830 50  0000 C CNN
F 1 "70k" H 3600 4650 50  0000 C CNN
F 2 "" H 3600 4680 30  0000 C CNN
F 3 "" V 3600 4750 30  0000 C CNN
	1    3550 4700
	0    1    1    0   
$EndComp
$Comp
L resistor R1
U 1 1 6666D2CC
P 3550 4400
F 0 "R1" H 3600 4530 50  0000 C CNN
F 1 "10k" H 3600 4350 50  0000 C CNN
F 2 "" H 3600 4380 30  0000 C CNN
F 3 "" V 3600 4450 30  0000 C CNN
	1    3550 4400
	0    1    1    0   
$EndComp
Wire Wire Line
	3600 4250 3600 4300
Wire Wire Line
	5500 4700 5450 4700
Wire Wire Line
	5450 4700 5450 4650
Wire Wire Line
	5450 4650 5000 4650
$Comp
L sine v2
U 1 1 6667F51E
P 3350 5750
F 0 "v2" H 3150 5850 60  0000 C CNN
F 1 "sine" H 3150 5700 60  0000 C CNN
F 2 "R1" H 3050 5750 60  0000 C CNN
F 3 "" H 3350 5750 60  0000 C CNN
	1    3350 5750
	1    0    0    -1  
$EndComp
$Comp
L sine v3
U 1 1 6667F581
P 5800 4000
F 0 "v3" H 5600 4100 60  0000 C CNN
F 1 "sine" H 5600 3950 60  0000 C CNN
F 2 "R1" H 5500 4000 60  0000 C CNN
F 3 "" H 5800 4000 60  0000 C CNN
	1    5800 4000
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U1
U 1 1 6667F6A9
P 3350 5200
F 0 "U1" H 3350 5700 60  0000 C CNN
F 1 "plot_v1" H 3550 5550 60  0000 C CNN
F 2 "" H 3350 5200 60  0000 C CNN
F 3 "" H 3350 5200 60  0000 C CNN
	1    3350 5200
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U2
U 1 1 6667F75A
P 3700 5900
F 0 "U2" H 3700 6400 60  0000 C CNN
F 1 "plot_v1" H 3900 6250 60  0000 C CNN
F 2 "" H 3700 5900 60  0000 C CNN
F 3 "" H 3700 5900 60  0000 C CNN
	1    3700 5900
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U3
U 1 1 6667F7C2
P 5200 4150
F 0 "U3" H 5200 4650 60  0000 C CNN
F 1 "plot_v1" H 5400 4500 60  0000 C CNN
F 2 "" H 5200 4150 60  0000 C CNN
F 3 "" H 5200 4150 60  0000 C CNN
	1    5200 4150
	1    0    0    -1  
$EndComp
Wire Wire Line
	5200 3950 5200 4000
Wire Wire Line
	5200 4000 5350 4000
Connection ~ 5350 4000
Wire Wire Line
	3350 5000 3700 5000
Wire Wire Line
	3700 5000 3700 4900
Connection ~ 3700 4900
Wire Wire Line
	3500 5700 3700 5700
Wire Wire Line
	3500 5700 3500 5250
Connection ~ 3500 5250
$Comp
L sine v5
U 1 1 6667FA92
P 5750 5750
F 0 "v5" H 5550 5850 60  0000 C CNN
F 1 "sine" H 5550 5700 60  0000 C CNN
F 2 "R1" H 5450 5750 60  0000 C CNN
F 3 "" H 5750 5750 60  0000 C CNN
	1    5750 5750
	1    0    0    -1  
$EndComp
Wire Wire Line
	5000 4950 5750 4950
Wire Wire Line
	5750 4950 5750 5300
$Comp
L GND #PWR07
U 1 1 6667FC05
P 5750 6250
F 0 "#PWR07" H 5750 6000 50  0001 C CNN
F 1 "GND" H 5750 6100 50  0000 C CNN
F 2 "" H 5750 6250 50  0001 C CNN
F 3 "" H 5750 6250 50  0001 C CNN
	1    5750 6250
	1    0    0    -1  
$EndComp
Wire Wire Line
	5750 6250 5750 6200
$Comp
L plot_v1 U4
U 1 1 6667FD96
P 5950 5300
F 0 "U4" H 5950 5800 60  0000 C CNN
F 1 "plot_v1" H 6150 5650 60  0000 C CNN
F 2 "" H 5950 5300 60  0000 C CNN
F 3 "" H 5950 5300 60  0000 C CNN
	1    5950 5300
	1    0    0    -1  
$EndComp
Wire Wire Line
	5750 5150 5950 5150
Wire Wire Line
	5950 5150 5950 5100
Connection ~ 5750 5150
Text GLabel 5700 4950 1    60   Input ~ 0
Z2
$Comp
L MPY100 X1
U 1 1 66680ABD
P 3600 5350
F 0 "X1" H 4500 5850 60  0000 C CNN
F 1 "MPY100" H 4500 5750 60  0000 C CNN
F 2 "" H 3600 5350 60  0001 C CNN
F 3 "" H 3600 5350 60  0001 C CNN
	1    3600 5350
	1    0    0    -1  
$EndComp
$EndSCHEMATC
