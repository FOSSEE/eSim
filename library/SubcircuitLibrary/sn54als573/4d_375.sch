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
L d_inverter U2
U 1 1 681ED689
P 3400 3450
F 0 "U2" H 3400 3350 60  0000 C CNN
F 1 "d_inverter" H 3400 3600 60  0000 C CNN
F 2 "" H 3450 3400 60  0000 C CNN
F 3 "" H 3450 3400 60  0000 C CNN
	1    3400 3450
	1    0    0    -1  
$EndComp
$Comp
L d_and U3
U 1 1 681ED6AE
P 4550 2500
F 0 "U3" H 4550 2500 60  0000 C CNN
F 1 "d_and" H 4600 2600 60  0000 C CNN
F 2 "" H 4550 2500 60  0000 C CNN
F 3 "" H 4550 2500 60  0000 C CNN
	1    4550 2500
	1    0    0    -1  
$EndComp
$Comp
L d_and U4
U 1 1 681ED6F1
P 4550 3500
F 0 "U4" H 4550 3500 60  0000 C CNN
F 1 "d_and" H 4600 3600 60  0000 C CNN
F 2 "" H 4550 3500 60  0000 C CNN
F 3 "" H 4550 3500 60  0000 C CNN
	1    4550 3500
	1    0    0    -1  
$EndComp
$Comp
L d_nor U5
U 1 1 681ED73E
P 5750 3000
F 0 "U5" H 5750 3000 60  0000 C CNN
F 1 "d_nor" H 5800 3100 60  0000 C CNN
F 2 "" H 5750 3000 60  0000 C CNN
F 3 "" H 5750 3000 60  0000 C CNN
	1    5750 3000
	1    0    0    -1  
$EndComp
$Comp
L d_inverter U6
U 1 1 681ED77D
P 7000 2950
F 0 "U6" H 7000 2850 60  0000 C CNN
F 1 "d_inverter" H 7000 3100 60  0000 C CNN
F 2 "" H 7050 2900 60  0000 C CNN
F 3 "" H 7050 2900 60  0000 C CNN
	1    7000 2950
	1    0    0    -1  
$EndComp
Wire Wire Line
	3100 3450 2300 3450
Wire Wire Line
	4100 2500 2800 2500
Wire Wire Line
	2800 2500 2800 3450
Connection ~ 2800 3450
Wire Wire Line
	4100 2400 2200 2400
Wire Wire Line
	3700 3450 4100 3450
Wire Wire Line
	4100 3450 4100 3400
Wire Wire Line
	7300 2950 7900 2950
Wire Wire Line
	4100 3500 4100 4150
Wire Wire Line
	4100 4150 7500 4150
Wire Wire Line
	7500 4150 7500 2950
Connection ~ 7500 2950
Wire Wire Line
	6200 2950 6700 2950
Wire Wire Line
	5000 2450 5300 2450
Wire Wire Line
	5300 2450 5300 2900
Wire Wire Line
	5000 3450 5300 3450
Wire Wire Line
	5300 3450 5300 3000
Wire Wire Line
	6450 2950 6450 2350
Wire Wire Line
	6450 2350 7900 2350
Connection ~ 6450 2950
$Comp
L PORT U1
U 1 1 681ED8C7
P 1950 2400
F 0 "U1" H 2000 2500 30  0000 C CNN
F 1 "PORT" H 1950 2400 30  0000 C CNN
F 2 "" H 1950 2400 60  0000 C CNN
F 3 "" H 1950 2400 60  0000 C CNN
	1    1950 2400
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 2 1 681ED912
P 2050 3450
F 0 "U1" H 2100 3550 30  0000 C CNN
F 1 "PORT" H 2050 3450 30  0000 C CNN
F 2 "" H 2050 3450 60  0000 C CNN
F 3 "" H 2050 3450 60  0000 C CNN
	2    2050 3450
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 3 1 681ED949
P 8150 2350
F 0 "U1" H 8200 2450 30  0000 C CNN
F 1 "PORT" H 8150 2350 30  0000 C CNN
F 2 "" H 8150 2350 60  0000 C CNN
F 3 "" H 8150 2350 60  0000 C CNN
	3    8150 2350
	-1   0    0    1   
$EndComp
$Comp
L PORT U1
U 4 1 681ED9BE
P 8150 2950
F 0 "U1" H 8200 3050 30  0000 C CNN
F 1 "PORT" H 8150 2950 30  0000 C CNN
F 2 "" H 8150 2950 60  0000 C CNN
F 3 "" H 8150 2950 60  0000 C CNN
	4    8150 2950
	-1   0    0    1   
$EndComp
$EndSCHEMATC
