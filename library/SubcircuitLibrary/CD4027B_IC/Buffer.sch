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
LIBS:Buffer-cache
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
L NOT_Gate X1
U 1 1 66559010
P 3600 3650
F 0 "X1" H 4200 3450 60  0000 C CNN
F 1 "NOT_Gate" H 4250 3850 60  0000 C CNN
F 2 "" H 3600 3650 60  0001 C CNN
F 3 "" H 3600 3650 60  0001 C CNN
	1    3600 3650
	1    0    0    -1  
$EndComp
$Comp
L NOT_Gate X2
U 1 1 66559039
P 4650 3650
F 0 "X2" H 5250 3450 60  0000 C CNN
F 1 "NOT_Gate" H 5300 3850 60  0000 C CNN
F 2 "" H 4650 3650 60  0001 C CNN
F 3 "" H 4650 3650 60  0001 C CNN
	1    4650 3650
	1    0    0    -1  
$EndComp
Wire Wire Line
	5000 3650 4650 3650
Wire Wire Line
	5700 3650 6100 3650
Wire Wire Line
	3950 3650 3650 3650
$Comp
L PORT U1
U 1 1 6655907A
P 3400 3650
F 0 "U1" H 3450 3750 30  0000 C CNN
F 1 "PORT" H 3400 3650 30  0000 C CNN
F 2 "" H 3400 3650 60  0000 C CNN
F 3 "" H 3400 3650 60  0000 C CNN
	1    3400 3650
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 2 1 665590B5
P 6350 3650
F 0 "U1" H 6400 3750 30  0000 C CNN
F 1 "PORT" H 6350 3650 30  0000 C CNN
F 2 "" H 6350 3650 60  0000 C CNN
F 3 "" H 6350 3650 60  0000 C CNN
	2    6350 3650
	-1   0    0    -1  
$EndComp
$Comp
L PORT U1
U 3 1 665614BF
P 4500 3000
F 0 "U1" H 4550 3100 30  0000 C CNN
F 1 "PORT" H 4500 3000 30  0000 C CNN
F 2 "" H 4500 3000 60  0000 C CNN
F 3 "" H 4500 3000 60  0000 C CNN
	3    4500 3000
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 4 1 665614F8
P 4550 4250
F 0 "U1" H 4600 4350 30  0000 C CNN
F 1 "PORT" H 4550 4250 30  0000 C CNN
F 2 "" H 4550 4250 60  0000 C CNN
F 3 "" H 4550 4250 60  0000 C CNN
	4    4550 4250
	1    0    0    -1  
$EndComp
Wire Wire Line
	4200 3950 4200 4100
Wire Wire Line
	4200 4100 5250 4100
Wire Wire Line
	5250 4100 5250 3950
Wire Wire Line
	4800 4250 4800 4100
Connection ~ 4800 4100
Wire Wire Line
	4200 3350 4200 3200
Wire Wire Line
	4200 3200 5250 3200
Wire Wire Line
	5250 3200 5250 3350
Wire Wire Line
	4750 3000 4750 3200
Connection ~ 4750 3200
$EndSCHEMATC
