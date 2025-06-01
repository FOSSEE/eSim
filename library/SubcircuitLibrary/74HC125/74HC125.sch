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
L d_tristate U4
U 1 1 682765A8
P 3650 2800
F 0 "U4" H 3400 3050 60  0000 C CNN
F 1 "d_tristate" H 3450 3250 60  0000 C CNN
F 2 "" H 3550 3150 60  0000 C CNN
F 3 "" H 3550 3150 60  0000 C CNN
	1    3650 2800
	1    0    0    -1  
$EndComp
$Comp
L d_tristate U5
U 1 1 682765FE
P 3650 4450
F 0 "U5" H 3400 4700 60  0000 C CNN
F 1 "d_tristate" H 3450 4900 60  0000 C CNN
F 2 "" H 3550 4800 60  0000 C CNN
F 3 "" H 3550 4800 60  0000 C CNN
	1    3650 4450
	1    0    0    -1  
$EndComp
$Comp
L d_tristate U8
U 1 1 68276621
P 7050 1950
F 0 "U8" H 6800 2200 60  0000 C CNN
F 1 "d_tristate" H 6850 2400 60  0000 C CNN
F 2 "" H 6950 2300 60  0000 C CNN
F 3 "" H 6950 2300 60  0000 C CNN
	1    7050 1950
	-1   0    0    1   
$EndComp
$Comp
L d_tristate U9
U 1 1 682766AC
P 7100 3700
F 0 "U9" H 6850 3950 60  0000 C CNN
F 1 "d_tristate" H 6900 4150 60  0000 C CNN
F 2 "" H 7000 4050 60  0000 C CNN
F 3 "" H 7000 4050 60  0000 C CNN
	1    7100 3700
	-1   0    0    1   
$EndComp
$Comp
L d_inverter U2
U 1 1 68276705
P 2700 2750
F 0 "U2" H 2700 2650 60  0000 C CNN
F 1 "d_inverter" H 2700 2900 60  0000 C CNN
F 2 "" H 2750 2700 60  0000 C CNN
F 3 "" H 2750 2700 60  0000 C CNN
	1    2700 2750
	1    0    0    -1  
$EndComp
Wire Wire Line
	3000 2750 3600 2750
$Comp
L PORT U1
U 1 1 682767CD
P 2150 2750
F 0 "U1" H 2200 2850 30  0000 C CNN
F 1 "PORT" H 2150 2750 30  0000 C CNN
F 2 "" H 2150 2750 60  0000 C CNN
F 3 "" H 2150 2750 60  0000 C CNN
	1    2150 2750
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 3 1 68276846
P 2800 2450
F 0 "U1" H 2850 2550 30  0000 C CNN
F 1 "PORT" H 2800 2450 30  0000 C CNN
F 2 "" H 2800 2450 60  0000 C CNN
F 3 "" H 2800 2450 60  0000 C CNN
	3    2800 2450
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 5 1 682768BB
P 4450 2450
F 0 "U1" H 4500 2550 30  0000 C CNN
F 1 "PORT" H 4450 2450 30  0000 C CNN
F 2 "" H 4450 2450 60  0000 C CNN
F 3 "" H 4450 2450 60  0000 C CNN
	5    4450 2450
	-1   0    0    1   
$EndComp
$Comp
L d_inverter U3
U 1 1 6827692E
P 2750 4400
F 0 "U3" H 2750 4300 60  0000 C CNN
F 1 "d_inverter" H 2750 4550 60  0000 C CNN
F 2 "" H 2800 4350 60  0000 C CNN
F 3 "" H 2800 4350 60  0000 C CNN
	1    2750 4400
	1    0    0    -1  
$EndComp
Wire Wire Line
	3050 4400 3600 4400
$Comp
L PORT U1
U 4 1 682769ED
P 2800 4100
F 0 "U1" H 2850 4200 30  0000 C CNN
F 1 "PORT" H 2800 4100 30  0000 C CNN
F 2 "" H 2800 4100 60  0000 C CNN
F 3 "" H 2800 4100 60  0000 C CNN
	4    2800 4100
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 6 1 68276A5A
P 4450 4100
F 0 "U1" H 4500 4200 30  0000 C CNN
F 1 "PORT" H 4450 4100 30  0000 C CNN
F 2 "" H 4450 4100 60  0000 C CNN
F 3 "" H 4450 4100 60  0000 C CNN
	6    4450 4100
	-1   0    0    1   
$EndComp
$Comp
L PORT U1
U 2 1 68276AB3
P 2200 4400
F 0 "U1" H 2250 4500 30  0000 C CNN
F 1 "PORT" H 2200 4400 30  0000 C CNN
F 2 "" H 2200 4400 60  0000 C CNN
F 3 "" H 2200 4400 60  0000 C CNN
	2    2200 4400
	1    0    0    -1  
$EndComp
$Comp
L d_inverter U6
U 1 1 68276B0A
P 6800 2000
F 0 "U6" H 6800 1900 60  0000 C CNN
F 1 "d_inverter" H 6800 2150 60  0000 C CNN
F 2 "" H 6850 1950 60  0000 C CNN
F 3 "" H 6850 1950 60  0000 C CNN
	1    6800 2000
	1    0    0    -1  
$EndComp
$Comp
L d_inverter U7
U 1 1 68276B97
P 6850 3750
F 0 "U7" H 6850 3650 60  0000 C CNN
F 1 "d_inverter" H 6850 3900 60  0000 C CNN
F 2 "" H 6900 3700 60  0000 C CNN
F 3 "" H 6900 3700 60  0000 C CNN
	1    6850 3750
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 7 1 68276BD4
P 6250 2000
F 0 "U1" H 6300 2100 30  0000 C CNN
F 1 "PORT" H 6250 2000 30  0000 C CNN
F 2 "" H 6250 2000 60  0000 C CNN
F 3 "" H 6250 2000 60  0000 C CNN
	7    6250 2000
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 9 1 68276CC1
P 6300 3750
F 0 "U1" H 6350 3850 30  0000 C CNN
F 1 "PORT" H 6300 3750 30  0000 C CNN
F 2 "" H 6300 3750 60  0000 C CNN
F 3 "" H 6300 3750 60  0000 C CNN
	9    6300 3750
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 11 1 68276D3E
P 7900 2300
F 0 "U1" H 7950 2400 30  0000 C CNN
F 1 "PORT" H 7900 2300 30  0000 C CNN
F 2 "" H 7900 2300 60  0000 C CNN
F 3 "" H 7900 2300 60  0000 C CNN
	11   7900 2300
	-1   0    0    1   
$EndComp
$Comp
L PORT U1
U 8 1 68276DB4
P 6250 2300
F 0 "U1" H 6300 2400 30  0000 C CNN
F 1 "PORT" H 6250 2300 30  0000 C CNN
F 2 "" H 6250 2300 60  0000 C CNN
F 3 "" H 6250 2300 60  0000 C CNN
	8    6250 2300
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 12 1 68276E19
P 7950 4050
F 0 "U1" H 8000 4150 30  0000 C CNN
F 1 "PORT" H 7950 4050 30  0000 C CNN
F 2 "" H 7950 4050 60  0000 C CNN
F 3 "" H 7950 4050 60  0000 C CNN
	12   7950 4050
	-1   0    0    1   
$EndComp
$Comp
L PORT U1
U 10 1 68276E94
P 6300 4050
F 0 "U1" H 6350 4150 30  0000 C CNN
F 1 "PORT" H 6300 4050 30  0000 C CNN
F 2 "" H 6300 4050 60  0000 C CNN
F 3 "" H 6300 4050 60  0000 C CNN
	10   6300 4050
	1    0    0    -1  
$EndComp
$EndSCHEMATC
