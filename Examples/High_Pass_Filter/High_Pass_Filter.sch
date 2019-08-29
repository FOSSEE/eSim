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
LIBS:High_Pass_Filter-cache
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
U 1 1 56B86791
P 6300 3200
F 0 "R1" H 6350 3330 50  0000 C CNN
F 1 "1k" H 6350 3250 50  0000 C CNN
F 2 "" H 6350 3180 30  0000 C CNN
F 3 "" V 6350 3250 30  0000 C CNN
	1    6300 3200
	0    1    1    0   
$EndComp
$Comp
L C C1
U 1 1 56B8686C
P 5800 3000
F 0 "C1" H 5825 3100 50  0000 L CNN
F 1 "10u" H 5825 2900 50  0000 L CNN
F 2 "" H 5838 2850 30  0000 C CNN
F 3 "" H 5800 3000 60  0000 C CNN
	1    5800 3000
	0    1    1    0   
$EndComp
Wire Wire Line
	5250 3000 5650 3000
Wire Wire Line
	5950 3000 6350 3000
Wire Wire Line
	6350 2800 6350 3100
Wire Wire Line
	5250 3900 6350 3900
Wire Wire Line
	6350 3900 6350 3400
$Comp
L GND #PWR01
U 1 1 56B8692D
P 5800 4000
F 0 "#PWR01" H 5800 3750 50  0001 C CNN
F 1 "GND" H 5800 3850 50  0000 C CNN
F 2 "" H 5800 4000 50  0000 C CNN
F 3 "" H 5800 4000 50  0000 C CNN
	1    5800 4000
	1    0    0    -1  
$EndComp
Wire Wire Line
	5800 4000 5800 3900
Connection ~ 5800 3900
Text GLabel 5200 2800 0    60   Input ~ 0
in
Text GLabel 6400 2850 2    60   Input ~ 0
out
Wire Wire Line
	5350 2800 5350 3000
Connection ~ 5350 3000
Wire Wire Line
	6150 2850 6400 2850
Connection ~ 6350 3000
Wire Wire Line
	5200 2800 5350 2800
$Comp
L AC v1
U 1 1 56C17BEF
P 5250 3450
F 0 "v1" H 5050 3550 60  0000 C CNN
F 1 "AC" H 5050 3400 60  0000 C CNN
F 2 "R1" H 4950 3450 60  0000 C CNN
F 3 "" H 5250 3450 60  0000 C CNN
	1    5250 3450
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U1
U 1 1 56D46EBD
P 5300 2950
F 0 "U1" H 5300 3450 60  0000 C CNN
F 1 "plot_v1" H 5500 3300 60  0000 C CNN
F 2 "" H 5300 2950 60  0000 C CNN
F 3 "" H 5300 2950 60  0000 C CNN
	1    5300 2950
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U3
U 1 1 56D46F4C
P 6350 3000
F 0 "U3" H 6350 3500 60  0000 C CNN
F 1 "plot_v1" H 6550 3350 60  0000 C CNN
F 2 "" H 6350 3000 60  0000 C CNN
F 3 "" H 6350 3000 60  0000 C CNN
	1    6350 3000
	1    0    0    -1  
$EndComp
$Comp
L plot_log U2
U 1 1 56D46FA6
P 6150 3000
F 0 "U2" H 6150 3500 60  0000 C CNN
F 1 "plot_log" H 6350 3350 60  0000 C CNN
F 2 "" H 6150 3000 60  0000 C CNN
F 3 "" H 6150 3000 60  0000 C CNN
	1    6150 3000
	-1   0    0    -1  
$EndComp
Wire Wire Line
	5300 2750 5300 2800
Connection ~ 5300 2800
Wire Wire Line
	6150 2800 6150 2850
Connection ~ 6350 2850
$EndSCHEMATC
