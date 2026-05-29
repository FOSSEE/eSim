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
L d_nand U3
U 1 1 685EBFD6
P 3900 2450
F 0 "U3" H 3900 2450 60  0000 C CNN
F 1 "d_nand" H 3950 2550 60  0000 C CNN
F 2 "" H 3900 2450 60  0000 C CNN
F 3 "" H 3900 2450 60  0000 C CNN
	1    3900 2450
	1    0    0    -1  
$EndComp
$Comp
L d_nand U4
U 1 1 685EC025
P 3900 3450
F 0 "U4" H 3900 3450 60  0000 C CNN
F 1 "d_nand" H 3950 3550 60  0000 C CNN
F 2 "" H 3900 3450 60  0000 C CNN
F 3 "" H 3900 3450 60  0000 C CNN
	1    3900 3450
	1    0    0    -1  
$EndComp
$Comp
L d_nand U5
U 1 1 685EC070
P 5950 2500
F 0 "U5" H 5950 2500 60  0000 C CNN
F 1 "d_nand" H 6000 2600 60  0000 C CNN
F 2 "" H 5950 2500 60  0000 C CNN
F 3 "" H 5950 2500 60  0000 C CNN
	1    5950 2500
	1    0    0    -1  
$EndComp
$Comp
L d_nand U6
U 1 1 685EC0ED
P 5950 3400
F 0 "U6" H 5950 3400 60  0000 C CNN
F 1 "d_nand" H 6000 3500 60  0000 C CNN
F 2 "" H 5950 3400 60  0000 C CNN
F 3 "" H 5950 3400 60  0000 C CNN
	1    5950 3400
	1    0    0    -1  
$EndComp
Wire Wire Line
	4350 2400 5500 2400
Wire Wire Line
	3450 2450 3250 2450
Wire Wire Line
	3250 2450 3250 3350
Wire Wire Line
	3250 3350 3450 3350
Wire Wire Line
	4350 3400 5500 3400
Wire Wire Line
	6400 2450 6400 2900
Wire Wire Line
	6400 2900 5500 2900
Wire Wire Line
	5500 2900 5500 3300
Wire Wire Line
	5500 2500 5500 2800
Wire Wire Line
	5500 2800 6500 2800
Wire Wire Line
	6500 2800 6500 3350
Wire Wire Line
	6400 3350 6650 3350
$Comp
L PORT U1
U 1 1 685EC1AC
P 3200 2350
F 0 "U1" H 3250 2450 30  0000 C CNN
F 1 "PORT" H 3200 2350 30  0000 C CNN
F 2 "" H 3200 2350 60  0000 C CNN
F 3 "" H 3200 2350 60  0000 C CNN
	1    3200 2350
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 2 1 685EC215
P 3200 3450
F 0 "U1" H 3250 3550 30  0000 C CNN
F 1 "PORT" H 3200 3450 30  0000 C CNN
F 2 "" H 3200 3450 60  0000 C CNN
F 3 "" H 3200 3450 60  0000 C CNN
	2    3200 3450
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 3 1 685EC266
P 2000 2850
F 0 "U1" H 2050 2950 30  0000 C CNN
F 1 "PORT" H 2000 2850 30  0000 C CNN
F 2 "" H 2000 2850 60  0000 C CNN
F 3 "" H 2000 2850 60  0000 C CNN
	3    2000 2850
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 4 1 685EC2D2
P 6900 2450
F 0 "U1" H 6950 2550 30  0000 C CNN
F 1 "PORT" H 6900 2450 30  0000 C CNN
F 2 "" H 6900 2450 60  0000 C CNN
F 3 "" H 6900 2450 60  0000 C CNN
	4    6900 2450
	-1   0    0    1   
$EndComp
$Comp
L PORT U1
U 5 1 685EC34B
P 6900 3350
F 0 "U1" H 6950 3450 30  0000 C CNN
F 1 "PORT" H 6900 3350 30  0000 C CNN
F 2 "" H 6900 3350 60  0000 C CNN
F 3 "" H 6900 3350 60  0000 C CNN
	5    6900 3350
	-1   0    0    1   
$EndComp
Wire Wire Line
	6400 2450 6650 2450
Connection ~ 6500 3350
Wire Wire Line
	3000 2850 3250 2850
Connection ~ 3250 2850
$Comp
L d_inverter U2
U 1 1 685EC8BB
P 2700 2850
F 0 "U2" H 2700 2750 60  0000 C CNN
F 1 "d_inverter" H 2700 3000 60  0000 C CNN
F 2 "" H 2750 2800 60  0000 C CNN
F 3 "" H 2750 2800 60  0000 C CNN
	1    2700 2850
	1    0    0    -1  
$EndComp
Wire Wire Line
	2250 2850 2400 2850
$EndSCHEMATC
