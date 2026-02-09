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
U 1 1 69180703
P 4300 3100
F 0 "U2" H 4300 3000 60  0000 C CNN
F 1 "d_inverter" H 4300 3250 60  0000 C CNN
F 2 "" H 4350 3050 60  0000 C CNN
F 3 "" H 4350 3050 60  0000 C CNN
	1    4300 3100
	1    0    0    -1  
$EndComp
$Comp
L d_inverter U3
U 1 1 69180752
P 4300 3600
F 0 "U3" H 4300 3500 60  0000 C CNN
F 1 "d_inverter" H 4300 3750 60  0000 C CNN
F 2 "" H 4350 3550 60  0000 C CNN
F 3 "" H 4350 3550 60  0000 C CNN
	1    4300 3600
	1    0    0    -1  
$EndComp
$Comp
L d_inverter U4
U 1 1 6918079B
P 4300 4000
F 0 "U4" H 4300 3900 60  0000 C CNN
F 1 "d_inverter" H 4300 4150 60  0000 C CNN
F 2 "" H 4350 3950 60  0000 C CNN
F 3 "" H 4350 3950 60  0000 C CNN
	1    4300 4000
	1    0    0    -1  
$EndComp
$Comp
L d_and U7
U 1 1 691807D6
P 6750 3250
F 0 "U7" H 6750 3250 60  0000 C CNN
F 1 "d_and" H 6800 3350 60  0000 C CNN
F 2 "" H 6750 3250 60  0000 C CNN
F 3 "" H 6750 3250 60  0000 C CNN
	1    6750 3250
	1    0    0    -1  
$EndComp
$Comp
L d_and U8
U 1 1 6918082B
P 6750 3750
F 0 "U8" H 6750 3750 60  0000 C CNN
F 1 "d_and" H 6800 3850 60  0000 C CNN
F 2 "" H 6750 3750 60  0000 C CNN
F 3 "" H 6750 3750 60  0000 C CNN
	1    6750 3750
	1    0    0    -1  
$EndComp
$Comp
L d_inverter U5
U 1 1 691808C0
P 5900 3650
F 0 "U5" H 5900 3550 60  0000 C CNN
F 1 "d_inverter" H 5900 3800 60  0000 C CNN
F 2 "" H 5950 3600 60  0000 C CNN
F 3 "" H 5950 3600 60  0000 C CNN
	1    5900 3650
	1    0    0    -1  
$EndComp
$Comp
L d_inverter U6
U 1 1 69180939
P 5900 3900
F 0 "U6" H 5900 3800 60  0000 C CNN
F 1 "d_inverter" H 5900 4050 60  0000 C CNN
F 2 "" H 5950 3850 60  0000 C CNN
F 3 "" H 5950 3850 60  0000 C CNN
	1    5900 3900
	1    0    0    -1  
$EndComp
Wire Wire Line
	4600 3100 6300 3100
Wire Wire Line
	6300 3100 6300 3150
Wire Wire Line
	4600 3600 5600 3600
Wire Wire Line
	5600 3600 5600 3650
Wire Wire Line
	6200 3650 6300 3650
Wire Wire Line
	4600 4000 5400 4000
Wire Wire Line
	5400 4000 5400 3250
Wire Wire Line
	5400 3250 6300 3250
Wire Wire Line
	5400 3900 5600 3900
Connection ~ 5400 3900
Wire Wire Line
	6200 3900 6300 3900
Wire Wire Line
	6300 3900 6300 3750
Wire Wire Line
	4000 3100 3500 3100
Wire Wire Line
	4000 3600 3500 3600
Wire Wire Line
	4000 4000 3500 4000
$Comp
L PORT U1
U 1 1 69180B16
P 3250 3100
F 0 "U1" H 3300 3200 30  0000 C CNN
F 1 "PORT" H 3250 3100 30  0000 C CNN
F 2 "" H 3250 3100 60  0000 C CNN
F 3 "" H 3250 3100 60  0000 C CNN
	1    3250 3100
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 2 1 69180B71
P 3250 3600
F 0 "U1" H 3300 3700 30  0000 C CNN
F 1 "PORT" H 3250 3600 30  0000 C CNN
F 2 "" H 3250 3600 60  0000 C CNN
F 3 "" H 3250 3600 60  0000 C CNN
	2    3250 3600
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 3 1 69180BC9
P 3250 4000
F 0 "U1" H 3300 4100 30  0000 C CNN
F 1 "PORT" H 3250 4000 30  0000 C CNN
F 2 "" H 3250 4000 60  0000 C CNN
F 3 "" H 3250 4000 60  0000 C CNN
	3    3250 4000
	1    0    0    -1  
$EndComp
$Comp
L d_nor U9
U 1 1 6918100A
P 7750 3500
F 0 "U9" H 7750 3500 60  0000 C CNN
F 1 "d_nor" H 7800 3600 60  0000 C CNN
F 2 "" H 7750 3500 60  0000 C CNN
F 3 "" H 7750 3500 60  0000 C CNN
	1    7750 3500
	1    0    0    -1  
$EndComp
Wire Wire Line
	7200 3200 7300 3200
Wire Wire Line
	7300 3200 7300 3400
Wire Wire Line
	7200 3700 7300 3700
Wire Wire Line
	7300 3700 7300 3500
Wire Wire Line
	8200 3450 8400 3450
$Comp
L PORT U1
U 4 1 691810C0
P 8650 3450
F 0 "U1" H 8700 3550 30  0000 C CNN
F 1 "PORT" H 8650 3450 30  0000 C CNN
F 2 "" H 8650 3450 60  0000 C CNN
F 3 "" H 8650 3450 60  0000 C CNN
	4    8650 3450
	-1   0    0    1   
$EndComp
$EndSCHEMATC
