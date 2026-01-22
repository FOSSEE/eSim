EESchema Schematic File Version 2
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
LIBS:RL-cache
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
L R R1
U 1 1 56B869D4
P 5950 2850
F 0 "R1" H 6000 2980 50  0000 C CNN
F 1 "10" H 6000 2900 50  0000 C CNN
F 2 "" H 6000 2830 30  0000 C CNN
F 3 "" V 6000 2900 30  0000 C CNN
	1    5950 2850
	1    0    0    -1  
$EndComp
$Comp
L L L1
U 1 1 56B86AA0
P 6300 1300
F 0 "L1" H 8250 1800 50  0000 C CNN
F 1 "100m" H 8250 1950 50  0000 C CNN
F 2 "" V 8250 1850 60  0000 C CNN
F 3 "" V 8250 1850 60  0000 C CNN
	1    6300 1300
	0    1    1    0   
$EndComp
$Comp
L pwl v1
U 1 1 56B86CEB
P 5150 3300
F 0 "v1" H 4950 3400 60  0000 C CNN
F 1 "pwl" H 4900 3250 60  0000 C CNN
F 2 "R1" H 4850 3300 60  0000 C CNN
F 3 "" H 5150 3300 60  0000 C CNN
	1    5150 3300
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR01
U 1 1 56B86D45
P 5900 3900
F 0 "#PWR01" H 5900 3650 50  0001 C CNN
F 1 "GND" H 5900 3750 50  0000 C CNN
F 2 "" H 5900 3900 50  0000 C CNN
F 3 "" H 5900 3900 50  0000 C CNN
	1    5900 3900
	1    0    0    -1  
$EndComp
Text GLabel 5400 2650 0    60   Input ~ 0
in
Text GLabel 6650 2650 2    60   Input ~ 0
out
Wire Wire Line
	5900 3900 5900 3850
Connection ~ 5900 3850
Wire Wire Line
	5400 2650 5450 2650
Wire Wire Line
	5450 2600 5450 2800
Connection ~ 5450 2800
Wire Wire Line
	6650 2650 6500 2650
Wire Wire Line
	6500 2600 6500 2800
Connection ~ 6500 2800
Wire Wire Line
	5150 2850 5150 2800
Wire Wire Line
	5150 2800 5850 2800
Wire Wire Line
	6150 2800 6850 2800
Wire Wire Line
	6850 2800 6850 2950
Wire Wire Line
	5150 3750 5150 3850
Wire Wire Line
	5150 3850 6850 3850
Wire Wire Line
	6850 3850 6850 3550
$Comp
L plot_v1 U1
U 1 1 56D46CBE
P 5450 2800
F 0 "U1" H 5450 3300 60  0000 C CNN
F 1 "plot_v1" H 5650 3150 60  0000 C CNN
F 2 "" H 5450 2800 60  0000 C CNN
F 3 "" H 5450 2800 60  0000 C CNN
	1    5450 2800
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U2
U 1 1 56D46CF1
P 6500 2800
F 0 "U2" H 6500 3300 60  0000 C CNN
F 1 "plot_v1" H 6700 3150 60  0000 C CNN
F 2 "" H 6500 2800 60  0000 C CNN
F 3 "" H 6500 2800 60  0000 C CNN
	1    6500 2800
	1    0    0    -1  
$EndComp
Connection ~ 5450 2650
Connection ~ 6500 2650
$EndSCHEMATC
