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
LIBS:e_origin-cache
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
L PORT U1
U 1 1 67F6CA9D
P 3600 2450
F 0 "U1" H 3650 2550 30  0000 C CNN
F 1 "PORT" H 3600 2450 30  0000 C CNN
F 2 "" H 3600 2450 60  0000 C CNN
F 3 "" H 3600 2450 60  0000 C CNN
	1    3600 2450
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 2 1 67F6CAC2
P 3600 2850
F 0 "U1" H 3650 2950 30  0000 C CNN
F 1 "PORT" H 3600 2850 30  0000 C CNN
F 2 "" H 3600 2850 60  0000 C CNN
F 3 "" H 3600 2850 60  0000 C CNN
	2    3600 2850
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 3 1 67F6CAED
P 3600 3250
F 0 "U1" H 3650 3350 30  0000 C CNN
F 1 "PORT" H 3600 3250 30  0000 C CNN
F 2 "" H 3600 3250 60  0000 C CNN
F 3 "" H 3600 3250 60  0000 C CNN
	3    3600 3250
	1    0    0    -1  
$EndComp
Wire Wire Line
	3850 2450 4250 2450
$Comp
L d_inverter U2
U 1 1 67F6CB20
P 4550 2450
F 0 "U2" H 4550 2350 60  0000 C CNN
F 1 "d_inverter" H 4550 2600 60  0000 C CNN
F 2 "" H 4600 2400 60  0000 C CNN
F 3 "" H 4600 2400 60  0000 C CNN
	1    4550 2450
	1    0    0    -1  
$EndComp
$Comp
L d_inverter U3
U 1 1 67F6CB80
P 4600 3250
F 0 "U3" H 4600 3150 60  0000 C CNN
F 1 "d_inverter" H 4600 3400 60  0000 C CNN
F 2 "" H 4650 3200 60  0000 C CNN
F 3 "" H 4650 3200 60  0000 C CNN
	1    4600 3250
	1    0    0    -1  
$EndComp
Wire Wire Line
	3850 3250 4300 3250
Wire Wire Line
	4850 2450 5600 2450
Wire Wire Line
	4900 3250 5250 3250
Wire Wire Line
	5050 3250 5050 2550
Wire Wire Line
	5050 2550 5600 2550
Wire Wire Line
	3850 2850 5600 2850
Wire Wire Line
	5250 3250 5250 2950
Wire Wire Line
	5250 2950 5600 2950
Connection ~ 5050 3250
$Comp
L d_and U4
U 1 1 67F6CBCC
P 6050 2550
F 0 "U4" H 6050 2550 60  0000 C CNN
F 1 "d_and" H 6100 2650 60  0000 C CNN
F 2 "" H 6050 2550 60  0000 C CNN
F 3 "" H 6050 2550 60  0000 C CNN
	1    6050 2550
	1    0    0    -1  
$EndComp
$Comp
L d_and U5
U 1 1 67F6CC03
P 6050 2950
F 0 "U5" H 6050 2950 60  0000 C CNN
F 1 "d_and" H 6100 3050 60  0000 C CNN
F 2 "" H 6050 2950 60  0000 C CNN
F 3 "" H 6050 2950 60  0000 C CNN
	1    6050 2950
	1    0    0    -1  
$EndComp
$Comp
L d_or U6
U 1 1 67F6CC38
P 7200 2600
F 0 "U6" H 7200 2600 60  0000 C CNN
F 1 "d_or" H 7200 2700 60  0000 C CNN
F 2 "" H 7200 2600 60  0000 C CNN
F 3 "" H 7200 2600 60  0000 C CNN
	1    7200 2600
	1    0    0    -1  
$EndComp
Wire Wire Line
	6500 2500 6750 2500
Wire Wire Line
	6500 2900 6750 2900
Wire Wire Line
	6750 2900 6750 2600
Wire Wire Line
	7650 2550 7900 2550
$Comp
L PORT U1
U 4 1 67F6CCD0
P 8150 2550
F 0 "U1" H 8200 2650 30  0000 C CNN
F 1 "PORT" H 8150 2550 30  0000 C CNN
F 2 "" H 8150 2550 60  0000 C CNN
F 3 "" H 8150 2550 60  0000 C CNN
	4    8150 2550
	-1   0    0    1   
$EndComp
Text Label 3950 2450 0    60   ~ 0
x
Text Label 4000 2850 0    60   ~ 0
y
Text Label 3950 3250 0    60   ~ 0
z
$EndSCHEMATC
