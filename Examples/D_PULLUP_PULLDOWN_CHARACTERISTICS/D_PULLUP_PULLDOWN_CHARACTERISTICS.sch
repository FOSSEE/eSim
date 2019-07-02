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
LIBS:device
LIBS:transistors
LIBS:conn
LIBS:linear
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
LIBS:eSim_User
LIBS:eSim_Plot
LIBS:eSim_PSpice
LIBS:digital_2-cache
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
Wire Wire Line
	4550 3900 4550 4050
Wire Wire Line
	4550 4050 4750 4050
$Comp
L d_pulldown U2
U 1 1 5D1B07FC
P 4800 3400
F 0 "U2" H 4800 3600 60  0000 C CNN
F 1 "d_pulldown" H 4750 3700 55  0000 C CNN
F 2 "" H 4800 3600 60  0000 C CNN
F 3 "" H 4800 3600 60  0000 C CNN
	1    4800 3400
	0    -1   -1   0   
$EndComp
Text Label 4550 4000 0    60   ~ 0
1
$Comp
L d_and U3
U 1 1 5D1B07FD
P 5200 4150
F 0 "U3" H 5200 4150 60  0000 C CNN
F 1 "d_and" H 5250 4250 60  0000 C CNN
F 2 "" H 5200 4150 60  0000 C CNN
F 3 "" H 5200 4150 60  0000 C CNN
	1    5200 4150
	1    0    0    -1  
$EndComp
Wire Wire Line
	4600 4150 4750 4150
$Comp
L dac_bridge_1 U4
U 1 1 5D1B07FE
P 6500 4150
F 0 "U4" H 6500 4150 60  0000 C CNN
F 1 "dac_bridge_1" H 6500 4300 60  0000 C CNN
F 2 "" H 6500 4150 60  0000 C CNN
F 3 "" H 6500 4150 60  0000 C CNN
	1    6500 4150
	1    0    0    -1  
$EndComp
Wire Wire Line
	5900 4100 5650 4100
$Comp
L plot_v1 U5
U 1 1 5D1B07FF
P 7250 4100
F 0 "U5" H 7250 4600 60  0000 C CNN
F 1 "plot_v1" H 7450 4450 60  0000 C CNN
F 2 "" H 7250 4100 60  0000 C CNN
F 3 "" H 7250 4100 60  0000 C CNN
	1    7250 4100
	1    0    0    -1  
$EndComp
Wire Wire Line
	7250 3900 7250 4100
Wire Wire Line
	7250 4100 7050 4100
Text GLabel 7400 4000 2    60   Input ~ 0
o
Wire Wire Line
	7400 4000 7250 4000
Connection ~ 7250 4000
$Comp
L d_pullup U1
U 1 1 5D1B0801
P 4100 4100
F 0 "U1" H 4100 4100 60  0000 C CNN
F 1 "d_pullup" H 4100 4200 60  0000 C CNN
F 2 "" H 4100 4100 60  0000 C CNN
F 3 "" H 4100 4100 60  0000 C CNN
	1    4100 4100
	-1   0    0    1   
$EndComp
$EndSCHEMATC
