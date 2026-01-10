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
LIBS:SN74LVC1G0832_fellow-cache
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
L d_and U2
U 1 1 682F224D
P 5100 3450
F 0 "U2" H 5100 3450 60  0000 C CNN
F 1 "d_and" H 5150 3550 60  0000 C CNN
F 2 "" H 5100 3450 60  0000 C CNN
F 3 "" H 5100 3450 60  0000 C CNN
	1    5100 3450
	1    0    0    -1  
$EndComp
$Comp
L d_or U3
U 1 1 682F2275
P 6100 3750
F 0 "U3" H 6100 3750 60  0000 C CNN
F 1 "d_or" H 6100 3850 60  0000 C CNN
F 2 "" H 6100 3750 60  0000 C CNN
F 3 "" H 6100 3750 60  0000 C CNN
	1    6100 3750
	1    0    0    -1  
$EndComp
Wire Wire Line
	6550 3700 6950 3700
Wire Wire Line
	5550 3400 5650 3400
Wire Wire Line
	5650 3400 5650 3650
Wire Wire Line
	4450 3700 5650 3700
Wire Wire Line
	5650 3700 5650 3750
Wire Wire Line
	4350 3350 4650 3350
Wire Wire Line
	4300 3500 4650 3500
Wire Wire Line
	4650 3500 4650 3450
$Comp
L eSim_GND #PWR01
U 1 1 6873B7AD
P 6000 4750
F 0 "#PWR01" H 6000 4500 50  0001 C CNN
F 1 "eSim_GND" H 6000 4600 50  0000 C CNN
F 2 "" H 6000 4750 50  0001 C CNN
F 3 "" H 6000 4750 50  0001 C CNN
	1    6000 4750
	1    0    0    -1  
$EndComp
$Comp
L eSim_GND #PWR02
U 1 1 6873B7E5
P 6800 4750
F 0 "#PWR02" H 6800 4500 50  0001 C CNN
F 1 "eSim_GND" H 6800 4600 50  0000 C CNN
F 2 "" H 6800 4750 50  0001 C CNN
F 3 "" H 6800 4750 50  0001 C CNN
	1    6800 4750
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 2 1 6873B881
P 5650 4650
F 0 "U1" H 5700 4750 30  0000 C CNN
F 1 "PORT" H 5650 4650 30  0000 C CNN
F 2 "" H 5650 4650 60  0000 C CNN
F 3 "" H 5650 4650 60  0000 C CNN
	2    5650 4650
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 5 1 6873B8AF
P 6450 4600
F 0 "U1" H 6500 4700 30  0000 C CNN
F 1 "PORT" H 6450 4600 30  0000 C CNN
F 2 "" H 6450 4600 60  0000 C CNN
F 3 "" H 6450 4600 60  0000 C CNN
	5    6450 4600
	1    0    0    -1  
$EndComp
Wire Wire Line
	5900 4650 6000 4650
Wire Wire Line
	6000 4650 6000 4750
Wire Wire Line
	6700 4600 6800 4600
Wire Wire Line
	6800 4600 6800 4750
$Comp
L PORT U1
U 1 1 6873B961
P 4100 3350
F 0 "U1" H 4150 3450 30  0000 C CNN
F 1 "PORT" H 4100 3350 30  0000 C CNN
F 2 "" H 4100 3350 60  0000 C CNN
F 3 "" H 4100 3350 60  0000 C CNN
	1    4100 3350
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 3 1 6873B9B2
P 4050 3500
F 0 "U1" H 4100 3600 30  0000 C CNN
F 1 "PORT" H 4050 3500 30  0000 C CNN
F 2 "" H 4050 3500 60  0000 C CNN
F 3 "" H 4050 3500 60  0000 C CNN
	3    4050 3500
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 6 1 6873B9D8
P 4200 3700
F 0 "U1" H 4250 3800 30  0000 C CNN
F 1 "PORT" H 4200 3700 30  0000 C CNN
F 2 "" H 4200 3700 60  0000 C CNN
F 3 "" H 4200 3700 60  0000 C CNN
	6    4200 3700
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 4 1 6873BA07
P 6650 3550
F 0 "U1" H 6700 3650 30  0000 C CNN
F 1 "PORT" H 6650 3550 30  0000 C CNN
F 2 "" H 6650 3550 60  0000 C CNN
F 3 "" H 6650 3550 60  0000 C CNN
	4    6650 3550
	1    0    0    -1  
$EndComp
Wire Wire Line
	6900 3550 6950 3550
Wire Wire Line
	6950 3550 6950 3700
$EndSCHEMATC
