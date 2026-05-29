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
L d_inverter U7
U 1 1 685AC144
P 4800 3050
F 0 "U7" H 4800 2950 60  0000 C CNN
F 1 "d_inverter" H 4800 3200 60  0000 C CNN
F 2 "" H 4850 3000 60  0000 C CNN
F 3 "" H 4850 3000 60  0000 C CNN
	1    4800 3050
	1    0    0    -1  
$EndComp
$Comp
L d_inverter U2
U 1 1 685AC16D
P 4800 3700
F 0 "U2" H 4800 3600 60  0000 C CNN
F 1 "d_inverter" H 4800 3850 60  0000 C CNN
F 2 "" H 4850 3650 60  0000 C CNN
F 3 "" H 4850 3650 60  0000 C CNN
	1    4800 3700
	1    0    0    -1  
$EndComp
$Comp
L d_inverter U3
U 1 1 685AC19E
P 4800 4400
F 0 "U3" H 4800 4300 60  0000 C CNN
F 1 "d_inverter" H 4800 4550 60  0000 C CNN
F 2 "" H 4850 4350 60  0000 C CNN
F 3 "" H 4850 4350 60  0000 C CNN
	1    4800 4400
	1    0    0    -1  
$EndComp
$Comp
L d_and U4
U 1 1 685AC1E0
P 6900 3350
F 0 "U4" H 6900 3350 60  0000 C CNN
F 1 "d_and" H 6950 3450 60  0000 C CNN
F 2 "" H 6900 3350 60  0000 C CNN
F 3 "" H 6900 3350 60  0000 C CNN
	1    6900 3350
	1    0    0    -1  
$EndComp
$Comp
L d_nor U5
U 1 1 685AC23D
P 6900 4000
F 0 "U5" H 6900 4000 60  0000 C CNN
F 1 "d_nor" H 6950 4100 60  0000 C CNN
F 2 "" H 6900 4000 60  0000 C CNN
F 3 "" H 6900 4000 60  0000 C CNN
	1    6900 4000
	1    0    0    -1  
$EndComp
$Comp
L d_nor U6
U 1 1 685AC29F
P 8450 3650
F 0 "U6" H 8450 3650 60  0000 C CNN
F 1 "d_nor" H 8500 3750 60  0000 C CNN
F 2 "" H 8450 3650 60  0000 C CNN
F 3 "" H 8450 3650 60  0000 C CNN
	1    8450 3650
	1    0    0    -1  
$EndComp
Wire Wire Line
	5100 3050 6450 3050
Wire Wire Line
	6450 3050 6450 3250
Wire Wire Line
	5100 4400 6000 4400
Wire Wire Line
	6000 4400 6000 3350
Wire Wire Line
	6000 3350 6450 3350
Wire Wire Line
	5100 3700 6450 3700
Wire Wire Line
	6450 3700 6450 3900
Wire Wire Line
	6000 4000 6450 4000
Connection ~ 6000 4000
Wire Wire Line
	7350 3300 7350 3550
Wire Wire Line
	7350 3550 8000 3550
Wire Wire Line
	7350 3950 7350 3650
Wire Wire Line
	7350 3650 8000 3650
$Comp
L PORT U1
U 1 1 685AC4F6
P 4000 3700
F 0 "U1" H 4050 3800 30  0000 C CNN
F 1 "PORT" H 4000 3700 30  0000 C CNN
F 2 "" H 4000 3700 60  0000 C CNN
F 3 "" H 4000 3700 60  0000 C CNN
	1    4000 3700
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 3 1 685AC57C
P 4000 3050
F 0 "U1" H 4050 3150 30  0000 C CNN
F 1 "PORT" H 4000 3050 30  0000 C CNN
F 2 "" H 4000 3050 60  0000 C CNN
F 3 "" H 4000 3050 60  0000 C CNN
	3    4000 3050
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 4 1 685AC5C3
P 9500 3600
F 0 "U1" H 9550 3700 30  0000 C CNN
F 1 "PORT" H 9500 3600 30  0000 C CNN
F 2 "" H 9500 3600 60  0000 C CNN
F 3 "" H 9500 3600 60  0000 C CNN
	4    9500 3600
	-1   0    0    1   
$EndComp
$Comp
L PORT U1
U 6 1 685AC803
P 4100 4400
F 0 "U1" H 4150 4500 30  0000 C CNN
F 1 "PORT" H 4100 4400 30  0000 C CNN
F 2 "" H 4100 4400 60  0000 C CNN
F 3 "" H 4100 4400 60  0000 C CNN
	6    4100 4400
	1    0    0    -1  
$EndComp
Wire Wire Line
	4250 3050 4500 3050
Wire Wire Line
	4250 3700 4500 3700
Wire Wire Line
	4350 4400 4500 4400
Wire Wire Line
	8900 3600 9250 3600
$EndSCHEMATC
