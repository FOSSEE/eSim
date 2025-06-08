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
U 1 1 681D7759
P 5250 3300
F 0 "U2" H 5250 3300 60  0000 C CNN
F 1 "d_nand" H 5300 3400 60  0000 C CNN
F 2 "" H 5250 3300 60  0000 C CNN
F 3 "" H 5250 3300 60  0000 C CNN
	1    5250 3300
	1    0    0    -1  
$EndComp
$Comp
L d_nand U3
U 1 1 681D778E
P 5250 4200
F 0 "U3" H 5250 4200 60  0000 C CNN
F 1 "d_nand" H 5300 4300 60  0000 C CNN
F 2 "" H 5250 4200 60  0000 C CNN
F 3 "" H 5250 4200 60  0000 C CNN
	1    5250 4200
	1    0    0    -1  
$EndComp
Wire Wire Line
	5700 3250 6000 3250
Wire Wire Line
	6000 3250 6000 3500
Wire Wire Line
	6000 3500 4500 3500
Wire Wire Line
	4500 3500 4500 4100
Wire Wire Line
	4500 4100 4800 4100
Wire Wire Line
	4800 3300 4650 3300
Wire Wire Line
	4650 3300 4650 4000
Wire Wire Line
	4650 4000 5800 4000
Wire Wire Line
	5800 4000 5800 4150
Wire Wire Line
	5700 4150 6400 4150
Connection ~ 5800 4150
Wire Wire Line
	4800 3200 4250 3200
Wire Wire Line
	4800 4200 4300 4200
$Comp
L PORT U1
U 1 1 681D781F
P 4000 3200
F 0 "U1" H 4050 3300 30  0000 C CNN
F 1 "PORT" H 4000 3200 30  0000 C CNN
F 2 "" H 4000 3200 60  0000 C CNN
F 3 "" H 4000 3200 60  0000 C CNN
	1    4000 3200
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 2 1 681D7855
P 4050 4200
F 0 "U1" H 4100 4300 30  0000 C CNN
F 1 "PORT" H 4050 4200 30  0000 C CNN
F 2 "" H 4050 4200 60  0000 C CNN
F 3 "" H 4050 4200 60  0000 C CNN
	2    4050 4200
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 3 1 681D788A
P 6650 4150
F 0 "U1" H 6700 4250 30  0000 C CNN
F 1 "PORT" H 6650 4150 30  0000 C CNN
F 2 "" H 6650 4150 60  0000 C CNN
F 3 "" H 6650 4150 60  0000 C CNN
	3    6650 4150
	-1   0    0    1   
$EndComp
$EndSCHEMATC
