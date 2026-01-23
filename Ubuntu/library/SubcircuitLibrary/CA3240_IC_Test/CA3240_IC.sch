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
L CA3240-OP X1
U 1 1 6648AE92
P 4250 3400
F 0 "X1" H 4700 3250 60  0000 C CNN
F 1 "CA3240-OP" H 4850 4050 60  0000 C CNN
F 2 "" H 4700 3250 60  0001 C CNN
F 3 "" H 4700 3250 60  0001 C CNN
	1    4250 3400
	1    0    0    -1  
$EndComp
$Comp
L CA3240-OP X2
U 1 1 6648AEFB
P 4300 4550
F 0 "X2" H 4750 4400 60  0000 C CNN
F 1 "CA3240-OP" H 4900 5200 60  0000 C CNN
F 2 "" H 4750 4400 60  0001 C CNN
F 3 "" H 4750 4400 60  0001 C CNN
	1    4300 4550
	1    0    0    -1  
$EndComp
Wire Wire Line
	5400 4050 5000 4050
Wire Wire Line
	5400 2550 5400 4050
Wire Wire Line
	5400 2900 4950 2900
Wire Wire Line
	4900 3400 4900 3750
Wire Wire Line
	4900 3750 4200 3750
Wire Wire Line
	4200 3750 4200 4800
Wire Wire Line
	4200 4800 5500 4800
Wire Wire Line
	4950 4800 4950 4550
Wire Wire Line
	5400 2550 5750 2550
Connection ~ 5400 2900
Wire Wire Line
	5500 4800 5500 5250
Wire Wire Line
	5500 5250 6300 5250
Connection ~ 4950 4800
Wire Wire Line
	5250 4300 6350 4300
Wire Wire Line
	5200 3150 5800 3150
Wire Wire Line
	4450 2950 4150 2950
Wire Wire Line
	4450 3350 4150 3350
Wire Wire Line
	4500 4100 4150 4100
Wire Wire Line
	4500 4500 4150 4500
$Comp
L PORT U1
U 1 1 6648B0B5
P 6050 3150
F 0 "U1" H 6100 3250 30  0000 C CNN
F 1 "PORT" H 6050 3150 30  0000 C CNN
F 2 "" H 6050 3150 60  0000 C CNN
F 3 "" H 6050 3150 60  0000 C CNN
	1    6050 3150
	-1   0    0    -1  
$EndComp
$Comp
L PORT U1
U 2 1 6648B0DC
P 3900 2950
F 0 "U1" H 3950 3050 30  0000 C CNN
F 1 "PORT" H 3900 2950 30  0000 C CNN
F 2 "" H 3900 2950 60  0000 C CNN
F 3 "" H 3900 2950 60  0000 C CNN
	2    3900 2950
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 3 1 6648B0F9
P 3900 3350
F 0 "U1" H 3950 3450 30  0000 C CNN
F 1 "PORT" H 3900 3350 30  0000 C CNN
F 2 "" H 3900 3350 60  0000 C CNN
F 3 "" H 3900 3350 60  0000 C CNN
	3    3900 3350
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 4 1 6648B126
P 6000 2550
F 0 "U1" H 6050 2650 30  0000 C CNN
F 1 "PORT" H 6000 2550 30  0000 C CNN
F 2 "" H 6000 2550 60  0000 C CNN
F 3 "" H 6000 2550 60  0000 C CNN
	4    6000 2550
	-1   0    0    -1  
$EndComp
$Comp
L PORT U1
U 5 1 6648B163
P 6550 5250
F 0 "U1" H 6600 5350 30  0000 C CNN
F 1 "PORT" H 6550 5250 30  0000 C CNN
F 2 "" H 6550 5250 60  0000 C CNN
F 3 "" H 6550 5250 60  0000 C CNN
	5    6550 5250
	-1   0    0    -1  
$EndComp
$Comp
L PORT U1
U 6 1 6648B186
P 6600 4300
F 0 "U1" H 6650 4400 30  0000 C CNN
F 1 "PORT" H 6600 4300 30  0000 C CNN
F 2 "" H 6600 4300 60  0000 C CNN
F 3 "" H 6600 4300 60  0000 C CNN
	6    6600 4300
	-1   0    0    -1  
$EndComp
$Comp
L PORT U1
U 7 1 6648B1CF
P 3900 4100
F 0 "U1" H 3950 4200 30  0000 C CNN
F 1 "PORT" H 3900 4100 30  0000 C CNN
F 2 "" H 3900 4100 60  0000 C CNN
F 3 "" H 3900 4100 60  0000 C CNN
	7    3900 4100
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 8 1 6648B21A
P 3900 4500
F 0 "U1" H 3950 4600 30  0000 C CNN
F 1 "PORT" H 3900 4500 30  0000 C CNN
F 2 "" H 3900 4500 60  0000 C CNN
F 3 "" H 3900 4500 60  0000 C CNN
	8    3900 4500
	1    0    0    -1  
$EndComp
$EndSCHEMATC
