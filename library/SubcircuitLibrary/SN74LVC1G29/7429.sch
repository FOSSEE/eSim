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
U 1 1 6821B961
P 2600 2100
F 0 "U2" H 2600 2000 60  0000 C CNN
F 1 "d_inverter" H 2600 2250 60  0000 C CNN
F 2 "" H 2650 2050 60  0000 C CNN
F 3 "" H 2650 2050 60  0000 C CNN
	1    2600 2100
	1    0    0    -1  
$EndComp
$Comp
L d_inverter U3
U 1 1 6821B9A6
P 3600 2600
F 0 "U3" H 3600 2500 60  0000 C CNN
F 1 "d_inverter" H 3600 2750 60  0000 C CNN
F 2 "" H 3650 2550 60  0000 C CNN
F 3 "" H 3650 2550 60  0000 C CNN
	1    3600 2600
	1    0    0    -1  
$EndComp
$Comp
L d_and U6
U 1 1 6821B9C3
P 5100 3050
F 0 "U6" H 5100 3050 60  0000 C CNN
F 1 "d_and" H 5150 3150 60  0000 C CNN
F 2 "" H 5100 3050 60  0000 C CNN
F 3 "" H 5100 3050 60  0000 C CNN
	1    5100 3050
	1    0    0    -1  
$EndComp
$Comp
L d_inverter U4
U 1 1 6821B9DE
P 3600 3550
F 0 "U4" H 3600 3450 60  0000 C CNN
F 1 "d_inverter" H 3600 3700 60  0000 C CNN
F 2 "" H 3650 3500 60  0000 C CNN
F 3 "" H 3650 3500 60  0000 C CNN
	1    3600 3550
	1    0    0    -1  
$EndComp
$Comp
L d_and U5
U 1 1 6821BA03
P 5050 4100
F 0 "U5" H 5050 4100 60  0000 C CNN
F 1 "d_and" H 5100 4200 60  0000 C CNN
F 2 "" H 5050 4100 60  0000 C CNN
F 3 "" H 5050 4100 60  0000 C CNN
	1    5050 4100
	1    0    0    -1  
$EndComp
$Comp
L d_nand U9
U 1 1 6821BA2A
P 7500 2100
F 0 "U9" H 7500 2100 60  0000 C CNN
F 1 "d_nand" H 7550 2200 60  0000 C CNN
F 2 "" H 7500 2100 60  0000 C CNN
F 3 "" H 7500 2100 60  0000 C CNN
	1    7500 2100
	1    0    0    -1  
$EndComp
$Comp
L d_nand U7
U 1 1 6821BA51
P 7450 3150
F 0 "U7" H 7450 3150 60  0000 C CNN
F 1 "d_nand" H 7500 3250 60  0000 C CNN
F 2 "" H 7450 3150 60  0000 C CNN
F 3 "" H 7450 3150 60  0000 C CNN
	1    7450 3150
	1    0    0    -1  
$EndComp
$Comp
L d_nand U8
U 1 1 6821BA7A
P 7450 4150
F 0 "U8" H 7450 4150 60  0000 C CNN
F 1 "d_nand" H 7500 4250 60  0000 C CNN
F 2 "" H 7450 4150 60  0000 C CNN
F 3 "" H 7450 4150 60  0000 C CNN
	1    7450 4150
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 1 1 6821BAA5
P 1750 2100
F 0 "U1" H 1800 2200 30  0000 C CNN
F 1 "PORT" H 1750 2100 30  0000 C CNN
F 2 "" H 1750 2100 60  0000 C CNN
F 3 "" H 1750 2100 60  0000 C CNN
	1    1750 2100
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 2 1 6821BB1D
P 1750 2550
F 0 "U1" H 1800 2650 30  0000 C CNN
F 1 "PORT" H 1750 2550 30  0000 C CNN
F 2 "" H 1750 2550 60  0000 C CNN
F 3 "" H 1750 2550 60  0000 C CNN
	2    1750 2550
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 3 1 6821BB4A
P 1750 3550
F 0 "U1" H 1800 3650 30  0000 C CNN
F 1 "PORT" H 1750 3550 30  0000 C CNN
F 2 "" H 1750 3550 60  0000 C CNN
F 3 "" H 1750 3550 60  0000 C CNN
	3    1750 3550
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 4 1 6821BBE9
P 8500 2050
F 0 "U1" H 8550 2150 30  0000 C CNN
F 1 "PORT" H 8500 2050 30  0000 C CNN
F 2 "" H 8500 2050 60  0000 C CNN
F 3 "" H 8500 2050 60  0000 C CNN
	4    8500 2050
	-1   0    0    1   
$EndComp
$Comp
L PORT U1
U 5 1 6821BC47
P 8500 3100
F 0 "U1" H 8550 3200 30  0000 C CNN
F 1 "PORT" H 8500 3100 30  0000 C CNN
F 2 "" H 8500 3100 60  0000 C CNN
F 3 "" H 8500 3100 60  0000 C CNN
	5    8500 3100
	-1   0    0    1   
$EndComp
$Comp
L PORT U1
U 6 1 6821BC84
P 8500 4100
F 0 "U1" H 8550 4200 30  0000 C CNN
F 1 "PORT" H 8500 4100 30  0000 C CNN
F 2 "" H 8500 4100 60  0000 C CNN
F 3 "" H 8500 4100 60  0000 C CNN
	6    8500 4100
	-1   0    0    1   
$EndComp
Wire Wire Line
	2000 2100 2300 2100
Wire Wire Line
	2000 2550 3300 2550
Wire Wire Line
	3300 2550 3300 2600
Wire Wire Line
	2000 3550 3300 3550
Wire Wire Line
	3000 2550 3000 4000
Wire Wire Line
	3000 2950 4650 2950
Connection ~ 3000 2550
Wire Wire Line
	3900 3550 4650 3550
Wire Wire Line
	4650 3550 4650 3050
Wire Wire Line
	3000 4000 4600 4000
Connection ~ 3000 2950
Wire Wire Line
	2500 3550 2500 4100
Wire Wire Line
	2500 4100 4600 4100
Connection ~ 2500 3550
Wire Wire Line
	2900 2100 6200 2100
Wire Wire Line
	6200 2100 6200 2000
Wire Wire Line
	6200 2000 7050 2000
Wire Wire Line
	3900 2600 6300 2600
Wire Wire Line
	6300 2600 6300 2100
Wire Wire Line
	6300 2100 7050 2100
Wire Wire Line
	5550 3000 6100 3000
Wire Wire Line
	6100 3000 6100 3150
Wire Wire Line
	6100 3150 7000 3150
Wire Wire Line
	6750 2000 6750 4050
Wire Wire Line
	6750 3050 7000 3050
Connection ~ 6750 2000
Wire Wire Line
	5500 4050 5900 4050
Wire Wire Line
	5900 4050 5900 4150
Wire Wire Line
	5900 4150 7000 4150
Wire Wire Line
	6750 4050 7000 4050
Connection ~ 6750 3050
Wire Wire Line
	7950 2050 8250 2050
Wire Wire Line
	7900 3100 8250 3100
Wire Wire Line
	7900 4100 8250 4100
$EndSCHEMATC
