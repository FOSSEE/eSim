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
L d_and U5
U 1 1 6900CE92
P 7550 2350
F 0 "U5" H 7550 2350 60  0000 C CNN
F 1 "d_and" H 7600 2450 60  0000 C CNN
F 2 "" H 7550 2350 60  0000 C CNN
F 3 "" H 7550 2350 60  0000 C CNN
	1    7550 2350
	1    0    0    -1  
$EndComp
$Comp
L d_and U3
U 1 1 6900CF2B
P 4950 2250
F 0 "U3" H 4950 2250 60  0000 C CNN
F 1 "d_and" H 5000 2350 60  0000 C CNN
F 2 "" H 4950 2250 60  0000 C CNN
F 3 "" H 4950 2250 60  0000 C CNN
	1    4950 2250
	-1   0    0    1   
$EndComp
$Comp
L d_inverter U4
U 1 1 6900CFE3
P 6050 2250
F 0 "U4" H 6050 2150 60  0000 C CNN
F 1 "d_inverter" H 6050 2400 60  0000 C CNN
F 2 "" H 6100 2200 60  0000 C CNN
F 3 "" H 6100 2200 60  0000 C CNN
	1    6050 2250
	-1   0    0    1   
$EndComp
Wire Wire Line
	6350 2250 7100 2250
Wire Wire Line
	6550 2250 6550 3550
Connection ~ 6550 2250
Wire Wire Line
	5400 2250 5750 2250
Wire Wire Line
	5400 2350 5550 2350
Wire Wire Line
	5550 2350 5550 3550
$Comp
L d_nor U2
U 1 1 6900D0D3
P 4000 2550
F 0 "U2" H 4000 2550 60  0000 C CNN
F 1 "d_nor" H 4050 2650 60  0000 C CNN
F 2 "" H 4000 2550 60  0000 C CNN
F 3 "" H 4000 2550 60  0000 C CNN
	1    4000 2550
	-1   0    0    1   
$EndComp
$Comp
L d_nor U6
U 1 1 6900D124
P 8500 2650
F 0 "U6" H 8500 2650 60  0000 C CNN
F 1 "d_nor" H 8550 2750 60  0000 C CNN
F 2 "" H 8500 2650 60  0000 C CNN
F 3 "" H 8500 2650 60  0000 C CNN
	1    8500 2650
	1    0    0    -1  
$EndComp
Wire Wire Line
	4500 2300 4450 2300
Wire Wire Line
	4450 2300 4450 2550
Wire Wire Line
	8000 2300 8050 2300
Wire Wire Line
	8050 2300 8050 2550
Wire Wire Line
	4450 2650 4450 3350
Wire Wire Line
	4450 3350 9150 3350
Wire Wire Line
	9150 3350 9150 2600
Wire Wire Line
	8950 2600 9450 2600
Connection ~ 9150 2600
Wire Wire Line
	8050 2650 8050 3200
Wire Wire Line
	8050 3200 3300 3200
Wire Wire Line
	3300 3200 3300 2600
Wire Wire Line
	2950 2600 3550 2600
Connection ~ 3300 2600
Wire Wire Line
	5550 2500 7100 2500
Wire Wire Line
	7100 2500 7100 2350
Connection ~ 5550 2500
$Comp
L PORT U1
U 1 1 6900D3AC
P 2700 2600
F 0 "U1" H 2750 2700 30  0000 C CNN
F 1 "PORT" H 2700 2600 30  0000 C CNN
F 2 "" H 2700 2600 60  0000 C CNN
F 3 "" H 2700 2600 60  0000 C CNN
	1    2700 2600
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 2 1 6900D423
P 5550 3800
F 0 "U1" H 5600 3900 30  0000 C CNN
F 1 "PORT" H 5550 3800 30  0000 C CNN
F 2 "" H 5550 3800 60  0000 C CNN
F 3 "" H 5550 3800 60  0000 C CNN
	2    5550 3800
	0    -1   -1   0   
$EndComp
$Comp
L PORT U1
U 3 1 6900D47D
P 6550 3800
F 0 "U1" H 6600 3900 30  0000 C CNN
F 1 "PORT" H 6550 3800 30  0000 C CNN
F 2 "" H 6550 3800 60  0000 C CNN
F 3 "" H 6550 3800 60  0000 C CNN
	3    6550 3800
	0    -1   -1   0   
$EndComp
$Comp
L PORT U1
U 4 1 6900D4DA
P 9700 2600
F 0 "U1" H 9750 2700 30  0000 C CNN
F 1 "PORT" H 9700 2600 30  0000 C CNN
F 2 "" H 9700 2600 60  0000 C CNN
F 3 "" H 9700 2600 60  0000 C CNN
	4    9700 2600
	-1   0    0    1   
$EndComp
$EndSCHEMATC
