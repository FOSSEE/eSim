EESchema Schematic File Version 2
LIBS:Clippercircuit-rescue
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
LIBS:device
LIBS:transistors
LIBS:conn
LIBS:linear
LIBS:regul
LIBS:74xx
LIBS:cmos4000
LIBS:Clippercircuit-cache
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
U 1 1 56A86127
P 4100 3500
F 0 "v1" H 3900 3600 60  0000 C CNN
F 1 "sine" H 3900 3450 60  0000 C CNN
F 2 "R1" H 3800 3500 60  0000 C CNN
F 3 "" H 4100 3500 60  0000 C CNN
	1    4100 3500
	1    0    0    -1  
$EndComp
$Comp
L D-RESCUE-Clippercircuit D1
U 1 1 56A86229
P 5550 3450
F 0 "D1" H 5550 3550 50  0000 C CNN
F 1 "D" H 5550 3350 50  0000 C CNN
F 2 "" H 5550 3450 60  0000 C CNN
F 3 "" H 5550 3450 60  0000 C CNN
	1    5550 3450
	0    -1   -1   0   
$EndComp
$Comp
L D-RESCUE-Clippercircuit D2
U 1 1 56A863C8
P 6250 3450
F 0 "D2" H 6250 3550 50  0000 C CNN
F 1 "D" H 6250 3350 50  0000 C CNN
F 2 "" H 6250 3450 60  0000 C CNN
F 3 "" H 6250 3450 60  0000 C CNN
	1    6250 3450
	0    1    1    0   
$EndComp
$Comp
L R-RESCUE-Clippercircuit R1
U 1 1 56A86416
P 4700 3050
F 0 "R1" H 4750 3180 50  0000 C CNN
F 1 "1k" H 4750 3100 50  0000 C CNN
F 2 "" H 4750 3030 30  0000 C CNN
F 3 "" V 4750 3100 30  0000 C CNN
	1    4700 3050
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR01
U 1 1 56A8645F
P 5350 4100
F 0 "#PWR01" H 5350 3850 50  0001 C CNN
F 1 "GND" H 5350 3950 50  0000 C CNN
F 2 "" H 5350 4100 50  0000 C CNN
F 3 "" H 5350 4100 50  0000 C CNN
	1    5350 4100
	1    0    0    -1  
$EndComp
Wire Wire Line
	4100 3050 4100 3000
Wire Wire Line
	4100 3000 4600 3000
Wire Wire Line
	4900 3000 6250 3000
Wire Wire Line
	6250 3000 6250 3300
Wire Wire Line
	4100 3950 4100 4050
Wire Wire Line
	4100 4050 6250 4050
Wire Wire Line
	6250 4050 6250 3600
Wire Wire Line
	5550 3300 5550 3000
Connection ~ 5550 3000
Wire Wire Line
	5550 3600 5550 4050
Connection ~ 5550 4050
Wire Wire Line
	5350 4100 5350 4050
Connection ~ 5350 4050
Text GLabel 6350 2900 2    60   Input ~ 0
out
Text GLabel 4100 2850 0    60   Input ~ 0
in
Wire Wire Line
	4100 2850 4200 2850
Wire Wire Line
	4200 2650 4200 3000
Connection ~ 4200 3000
Wire Wire Line
	6350 2900 6200 2900
Wire Wire Line
	6200 2650 6200 3000
Connection ~ 6200 3000
$Comp
L plot_v1 U1
U 1 1 56D43E99
P 4200 2850
F 0 "U1" H 4200 3350 60  0000 C CNN
F 1 "plot_v1" H 4400 3200 60  0000 C CNN
F 2 "" H 4200 2850 60  0000 C CNN
F 3 "" H 4200 2850 60  0000 C CNN
	1    4200 2850
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U2
U 1 1 56D43EEE
P 6200 2850
F 0 "U2" H 6200 3350 60  0000 C CNN
F 1 "plot_v1" H 6400 3200 60  0000 C CNN
F 2 "" H 6200 2850 60  0000 C CNN
F 3 "" H 6200 2850 60  0000 C CNN
	1    6200 2850
	1    0    0    -1  
$EndComp
Connection ~ 4200 2850
Connection ~ 6200 2900
$EndSCHEMATC
