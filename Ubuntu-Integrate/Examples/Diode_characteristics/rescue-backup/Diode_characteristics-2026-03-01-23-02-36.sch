EESchema Schematic File Version 2
LIBS:Diode_characteristics-rescue
LIBS:eSim_Analog
LIBS:eSim_Devices
LIBS:eSim_Digital
LIBS:eSim_Hybrid
LIBS:eSim_Miscellaneous
LIBS:eSim_Plot
LIBS:eSim_Power
LIBS:eSim_Sources
LIBS:eSim_Subckt
LIBS:eSim_User
LIBS:power
LIBS:device
LIBS:transistors
LIBS:conn
LIBS:linear
LIBS:regul
LIBS:74xx
LIBS:cmos4000
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
LIBS:valves
LIBS:Diode_characteristics-cache
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
L DC-RESCUE-Diode_characteristics v1
U 1 1 562485DC
P 4350 3150
F 0 "v1" H 4150 3250 60  0000 C CNN
F 1 "DC" H 4150 3100 60  0000 C CNN
F 2 "R1" H 4050 3150 60  0000 C CNN
F 3 "" H 4350 3150 60  0000 C CNN
	1    4350 3150
	1    0    0    -1  
$EndComp
$Comp
L D-RESCUE-Diode_characteristics D1
U 1 1 5624867D
P 5150 2500
F 0 "D1" H 5150 2600 50  0000 C CNN
F 1 "D" H 5150 2400 50  0000 C CNN
F 2 "" H 5150 2500 60  0000 C CNN
F 3 "" H 5150 2500 60  0000 C CNN
	1    5150 2500
	1    0    0    -1  
$EndComp
$Comp
L R-RESCUE-Diode_characteristics R1
U 1 1 562486CA
P 6900 2950
F 0 "R1" H 6950 3080 50  0000 C CNN
F 1 "1k" H 6950 3000 50  0000 C CNN
F 2 "" H 6950 2930 30  0000 C CNN
F 3 "" V 6950 3000 30  0000 C CNN
	1    6900 2950
	0    1    1    0   
$EndComp
$Comp
L GND #PWR01
U 1 1 562486FF
P 5300 3700
F 0 "#PWR01" H 5300 3450 50  0001 C CNN
F 1 "GND" H 5300 3550 50  0000 C CNN
F 2 "" H 5300 3700 60  0000 C CNN
F 3 "" H 5300 3700 60  0000 C CNN
	1    5300 3700
	1    0    0    -1  
$EndComp
Wire Wire Line
	4350 2700 4350 2500
Wire Wire Line
	4350 2500 5000 2500
Wire Wire Line
	5300 2500 6250 2500
Wire Wire Line
	4350 3600 4350 3650
Wire Wire Line
	4350 3650 6950 3650
Wire Wire Line
	5300 3700 5300 3650
Connection ~ 5300 3650
Text GLabel 5850 2400 2    60   Input ~ 0
out
Text GLabel 4400 2350 0    60   Input ~ 0
in
Wire Wire Line
	4400 2350 4550 2350
Wire Wire Line
	4550 2350 4550 2500
Connection ~ 4550 2500
Wire Wire Line
	5850 2400 5700 2400
Wire Wire Line
	5700 2400 5700 2500
Connection ~ 5700 2500
Wire Wire Line
	6850 2500 6950 2500
Wire Wire Line
	6950 2500 6950 2850
Wire Wire Line
	6950 3650 6950 3150
$Comp
L plot_i2 U1
U 1 1 56CC373C
P 6550 2750
F 0 "U1" H 6550 3150 60  0000 C CNN
F 1 "plot_i2" H 6550 2850 60  0000 C CNN
F 2 "" H 6550 2750 60  0000 C CNN
F 3 "" H 6550 2750 60  0000 C CNN
	1    6550 2750
	1    0    0    -1  
$EndComp
$EndSCHEMATC
