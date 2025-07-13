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
L d_nand U2
U 1 1 686919A7
P 4350 2800
F 0 "U2" H 4350 2800 60  0000 C CNN
F 1 "d_nand" H 4400 2900 60  0000 C CNN
F 2 "" H 4350 2800 60  0000 C CNN
F 3 "" H 4350 2800 60  0000 C CNN
	1    4350 2800
	1    0    0    -1  
$EndComp
$Comp
L d_nand U4
U 1 1 686919EC
P 5850 2800
F 0 "U4" H 5850 2800 60  0000 C CNN
F 1 "d_nand" H 5900 2900 60  0000 C CNN
F 2 "" H 5850 2800 60  0000 C CNN
F 3 "" H 5850 2800 60  0000 C CNN
	1    5850 2800
	1    0    0    -1  
$EndComp
$Comp
L d_nand U5
U 1 1 68691A1F
P 5900 4000
F 0 "U5" H 5900 4000 60  0000 C CNN
F 1 "d_nand" H 5950 4100 60  0000 C CNN
F 2 "" H 5900 4000 60  0000 C CNN
F 3 "" H 5900 4000 60  0000 C CNN
	1    5900 4000
	1    0    0    -1  
$EndComp
Wire Wire Line
	6300 2750 6800 2750
Wire Wire Line
	6350 3950 7000 3950
Wire Wire Line
	6700 2750 6700 3300
Wire Wire Line
	6700 3300 5200 3300
Wire Wire Line
	5200 3300 5200 3900
Wire Wire Line
	5200 3900 5450 3900
Connection ~ 6700 2750
Wire Wire Line
	6550 3950 6550 3050
Wire Wire Line
	6550 3050 5250 3050
Wire Wire Line
	5250 3050 5250 2800
Wire Wire Line
	5250 2800 5400 2800
Connection ~ 6550 3950
$Comp
L d_nand U3
U 1 1 68691A8B
P 4350 4050
F 0 "U3" H 4350 4050 60  0000 C CNN
F 1 "d_nand" H 4400 4150 60  0000 C CNN
F 2 "" H 4350 4050 60  0000 C CNN
F 3 "" H 4350 4050 60  0000 C CNN
	1    4350 4050
	1    0    0    -1  
$EndComp
Wire Wire Line
	4800 2750 4900 2750
Wire Wire Line
	4900 2750 4900 2700
Wire Wire Line
	4900 2700 5400 2700
Wire Wire Line
	4800 4000 5450 4000
Wire Wire Line
	3900 2800 3600 2800
Wire Wire Line
	3600 2800 3600 3950
Wire Wire Line
	3600 3950 3900 3950
Wire Wire Line
	3900 2700 3150 2700
Wire Wire Line
	3900 4050 3150 4050
Wire Wire Line
	3600 3350 2400 3350
Connection ~ 3600 3350
$Comp
L PORT U1
U 4 1 68691B28
P 7250 3950
F 0 "U1" H 7300 4050 30  0000 C CNN
F 1 "PORT" H 7250 3950 30  0000 C CNN
F 2 "" H 7250 3950 60  0000 C CNN
F 3 "" H 7250 3950 60  0000 C CNN
	4    7250 3950
	-1   0    0    1   
$EndComp
$Comp
L PORT U1
U 5 1 68691BB8
P 7050 2750
F 0 "U1" H 7100 2850 30  0000 C CNN
F 1 "PORT" H 7050 2750 30  0000 C CNN
F 2 "" H 7050 2750 60  0000 C CNN
F 3 "" H 7050 2750 60  0000 C CNN
	5    7050 2750
	-1   0    0    1   
$EndComp
$Comp
L PORT U1
U 3 1 68691BFB
P 2900 4050
F 0 "U1" H 2950 4150 30  0000 C CNN
F 1 "PORT" H 2900 4050 30  0000 C CNN
F 2 "" H 2900 4050 60  0000 C CNN
F 3 "" H 2900 4050 60  0000 C CNN
	3    2900 4050
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 2 1 68691C28
P 2150 3350
F 0 "U1" H 2200 3450 30  0000 C CNN
F 1 "PORT" H 2150 3350 30  0000 C CNN
F 2 "" H 2150 3350 60  0000 C CNN
F 3 "" H 2150 3350 60  0000 C CNN
	2    2150 3350
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 1 1 68691C55
P 2900 2700
F 0 "U1" H 2950 2800 30  0000 C CNN
F 1 "PORT" H 2900 2700 30  0000 C CNN
F 2 "" H 2900 2700 60  0000 C CNN
F 3 "" H 2900 2700 60  0000 C CNN
	1    2900 2700
	1    0    0    -1  
$EndComp
$EndSCHEMATC
