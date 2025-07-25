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
L sine v1
U 1 1 683EA82C
P 2400 3250
F 0 "v1" H 2200 3350 60  0000 C CNN
F 1 "sine" H 2200 3200 60  0000 C CNN
F 2 "R1" H 2100 3250 60  0000 C CNN
F 3 "" H 2400 3250 60  0000 C CNN
	1    2400 3250
	1    0    0    -1  
$EndComp
$Comp
L eSim_Diode D1
U 1 1 683EA84F
P 3100 2700
F 0 "D1" H 3100 2800 50  0000 C CNN
F 1 "eSim_Diode" H 3100 2600 50  0000 C CNN
F 2 "" H 3100 2700 60  0000 C CNN
F 3 "" H 3100 2700 60  0000 C CNN
	1    3100 2700
	1    0    0    -1  
$EndComp
Wire Wire Line
	2400 2800 2400 2700
Wire Wire Line
	2400 2700 2950 2700
$Comp
L capacitor C1
U 1 1 683EA87C
P 3600 3250
F 0 "C1" H 3625 3350 50  0000 L CNN
F 1 "0.047u" H 3625 3150 50  0000 L CNN
F 2 "" H 3638 3100 30  0000 C CNN
F 3 "" H 3600 3250 60  0000 C CNN
	1    3600 3250
	1    0    0    -1  
$EndComp
Wire Wire Line
	3250 2700 4100 2700
Wire Wire Line
	3600 2700 3600 3100
$Comp
L resistor R1
U 1 1 683EA8B0
P 4050 3250
F 0 "R1" H 4100 3380 50  0000 C CNN
F 1 "10k" H 4100 3200 50  0000 C CNN
F 2 "" H 4100 3230 30  0000 C CNN
F 3 "" V 4100 3300 30  0000 C CNN
	1    4050 3250
	0    1    1    0   
$EndComp
Wire Wire Line
	4100 2700 4100 3150
Connection ~ 3600 2700
Wire Wire Line
	3600 3400 3600 4050
Wire Wire Line
	2400 3850 4100 3850
Wire Wire Line
	4100 3850 4100 3450
Wire Wire Line
	2400 3700 2400 3850
Connection ~ 3600 3850
$Comp
L eSim_GND #PWR01
U 1 1 683EA934
P 3600 4050
F 0 "#PWR01" H 3600 3800 50  0001 C CNN
F 1 "eSim_GND" H 3600 3900 50  0000 C CNN
F 2 "" H 3600 4050 50  0001 C CNN
F 3 "" H 3600 4050 50  0001 C CNN
	1    3600 4050
	1    0    0    -1  
$EndComp
$EndSCHEMATC
