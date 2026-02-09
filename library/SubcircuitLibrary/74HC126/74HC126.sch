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
U 1 1 694F6974
P 4900 3550
F 0 "U2" H 4900 3450 60  0000 C CNN
F 1 "d_inverter" H 4900 3700 60  0000 C CNN
F 2 "" H 4950 3500 60  0000 C CNN
F 3 "" H 4950 3500 60  0000 C CNN
	1    4900 3550
	1    0    0    -1  
$EndComp
$Comp
L d_inverter U4
U 1 1 694F69B3
P 5950 3550
F 0 "U4" H 5950 3450 60  0000 C CNN
F 1 "d_inverter" H 5950 3700 60  0000 C CNN
F 2 "" H 6000 3500 60  0000 C CNN
F 3 "" H 6000 3500 60  0000 C CNN
	1    5950 3550
	1    0    0    -1  
$EndComp
$Comp
L d_inverter U6
U 1 1 694F69DE
P 6850 3550
F 0 "U6" H 6850 3450 60  0000 C CNN
F 1 "d_inverter" H 6850 3700 60  0000 C CNN
F 2 "" H 6900 3500 60  0000 C CNN
F 3 "" H 6900 3500 60  0000 C CNN
	1    6850 3550
	1    0    0    -1  
$EndComp
$Comp
L d_inverter U3
U 1 1 694F6A0F
P 4900 4450
F 0 "U3" H 4900 4350 60  0000 C CNN
F 1 "d_inverter" H 4900 4600 60  0000 C CNN
F 2 "" H 4950 4400 60  0000 C CNN
F 3 "" H 4950 4400 60  0000 C CNN
	1    4900 4450
	1    0    0    -1  
$EndComp
$Comp
L d_inverter U5
U 1 1 694F6A3C
P 5950 4450
F 0 "U5" H 5950 4350 60  0000 C CNN
F 1 "d_inverter" H 5950 4600 60  0000 C CNN
F 2 "" H 6000 4400 60  0000 C CNN
F 3 "" H 6000 4400 60  0000 C CNN
	1    5950 4450
	1    0    0    -1  
$EndComp
$Comp
L d_inverter U7
U 1 1 694F6A61
P 6850 4450
F 0 "U7" H 6850 4350 60  0000 C CNN
F 1 "d_inverter" H 6850 4600 60  0000 C CNN
F 2 "" H 6900 4400 60  0000 C CNN
F 3 "" H 6900 4400 60  0000 C CNN
	1    6850 4450
	1    0    0    -1  
$EndComp
$Comp
L d_tristate U8
U 1 1 694F6A92
P 8250 3900
F 0 "U8" H 8000 4150 60  0000 C CNN
F 1 "d_tristate" H 8050 4350 60  0000 C CNN
F 2 "" H 8150 4250 60  0000 C CNN
F 3 "" H 8150 4250 60  0000 C CNN
	1    8250 3900
	1    0    0    -1  
$EndComp
Wire Wire Line
	4600 3550 4150 3550
Wire Wire Line
	5200 3550 5650 3550
Wire Wire Line
	6250 3550 6550 3550
Wire Wire Line
	7150 3550 7650 3550
Wire Wire Line
	4600 4450 4200 4450
Wire Wire Line
	5200 4450 5650 4450
Wire Wire Line
	6250 4450 6550 4450
Wire Wire Line
	7150 4450 8200 4450
Wire Wire Line
	8200 4450 8200 3850
Wire Wire Line
	8800 3550 9150 3550
$Comp
L d_inverter U9
U 1 1 694F6CBA
P 9450 3550
F 0 "U9" H 9450 3450 60  0000 C CNN
F 1 "d_inverter" H 9450 3700 60  0000 C CNN
F 2 "" H 9500 3500 60  0000 C CNN
F 3 "" H 9500 3500 60  0000 C CNN
	1    9450 3550
	1    0    0    -1  
$EndComp
Wire Wire Line
	9750 3550 10050 3550
$Comp
L PORT U1
U 1 1 694F6DED
P 3900 3550
F 0 "U1" H 3950 3650 30  0000 C CNN
F 1 "PORT" H 3900 3550 30  0000 C CNN
F 2 "" H 3900 3550 60  0000 C CNN
F 3 "" H 3900 3550 60  0000 C CNN
	1    3900 3550
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 2 1 694F6E9D
P 3950 4450
F 0 "U1" H 4000 4550 30  0000 C CNN
F 1 "PORT" H 3950 4450 30  0000 C CNN
F 2 "" H 3950 4450 60  0000 C CNN
F 3 "" H 3950 4450 60  0000 C CNN
	2    3950 4450
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 3 1 694F6F18
P 10300 3550
F 0 "U1" H 10350 3650 30  0000 C CNN
F 1 "PORT" H 10300 3550 30  0000 C CNN
F 2 "" H 10300 3550 60  0000 C CNN
F 3 "" H 10300 3550 60  0000 C CNN
	3    10300 3550
	-1   0    0    1   
$EndComp
$EndSCHEMATC
