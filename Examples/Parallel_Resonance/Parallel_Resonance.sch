EESchema Schematic File Version 2
LIBS:Parallel_Resonance-rescue
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
LIBS:Parallel_Resonance-cache
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
L R-RESCUE-Parallel_Resonance R1
U 1 1 56C172A1
P 5100 3150
F 0 "R1" H 5150 3280 50  0000 C CNN
F 1 "100" H 5150 3200 50  0000 C CNN
F 2 "" H 5150 3130 30  0000 C CNN
F 3 "" V 5150 3200 30  0000 C CNN
	1    5100 3150
	0    1    1    0   
$EndComp
$Comp
L L-RESCUE-Parallel_Resonance L1
U 1 1 56C172D6
P 5850 1250
F 0 "L1" H 7800 1750 50  0000 C CNN
F 1 "100m" H 7800 1900 50  0000 C CNN
F 2 "" V 7800 1800 60  0000 C CNN
F 3 "" V 7800 1800 60  0000 C CNN
	1    5850 1250
	0    1    1    0   
$EndComp
$Comp
L C C1
U 1 1 56C17369
P 5900 3150
F 0 "C1" H 5925 3250 50  0000 L CNN
F 1 "10u" H 5925 3050 50  0000 L CNN
F 2 "" H 5938 3000 30  0000 C CNN
F 3 "" H 5900 3150 60  0000 C CNN
	1    5900 3150
	-1   0    0    1   
$EndComp
$Comp
L GND #PWR01
U 1 1 56C173A6
P 5400 3900
F 0 "#PWR01" H 5400 3650 50  0001 C CNN
F 1 "GND" H 5400 3750 50  0000 C CNN
F 2 "" H 5400 3900 50  0000 C CNN
F 3 "" H 5400 3900 50  0000 C CNN
	1    5400 3900
	1    0    0    -1  
$EndComp
Wire Wire Line
	4200 2850 4200 2650
Wire Wire Line
	4200 3750 4200 3850
Wire Wire Line
	4200 3850 6400 3850
Wire Wire Line
	6400 3850 6400 3500
Wire Wire Line
	5400 3900 5400 3850
Connection ~ 5400 3850
Text GLabel 4200 2500 0    60   Input ~ 0
in
Text GLabel 6400 2500 2    60   Input ~ 0
out
Wire Wire Line
	4200 2500 4250 2500
Wire Wire Line
	4250 2450 4250 2650
Connection ~ 4250 2650
Wire Wire Line
	6350 2500 6350 2650
Connection ~ 6350 2650
$Comp
L AC v1
U 1 1 56C199FB
P 4200 3300
F 0 "v1" H 4000 3400 60  0000 C CNN
F 1 "AC" H 4000 3250 60  0000 C CNN
F 2 "R1" H 3900 3300 60  0000 C CNN
F 3 "" H 4200 3300 60  0000 C CNN
	1    4200 3300
	1    0    0    -1  
$EndComp
Wire Wire Line
	6400 2650 6400 2900
Wire Wire Line
	5150 3050 5150 2650
Connection ~ 5150 2650
Wire Wire Line
	5900 2650 5900 3000
Connection ~ 5900 2650
Wire Wire Line
	5150 3350 5150 3850
Connection ~ 5150 3850
Wire Wire Line
	5900 3300 5900 3850
Connection ~ 5900 3850
$Comp
L R-RESCUE-Parallel_Resonance R2
U 1 1 56C1A863
P 4600 2600
F 0 "R2" H 4650 2730 50  0000 C CNN
F 1 "1000" H 4650 2650 50  0000 C CNN
F 2 "" H 4650 2580 30  0000 C CNN
F 3 "" V 4650 2650 30  0000 C CNN
	1    4600 2600
	-1   0    0    1   
$EndComp
Wire Wire Line
	4200 2650 4400 2650
Wire Wire Line
	4700 2650 6400 2650
$Comp
L plot_v1 U1
U 1 1 56D8706D
P 4250 2650
F 0 "U1" H 4250 3150 60  0000 C CNN
F 1 "plot_v1" H 4450 3000 60  0000 C CNN
F 2 "" H 4250 2650 60  0000 C CNN
F 3 "" H 4250 2650 60  0000 C CNN
	1    4250 2650
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U3
U 1 1 56D870C6
P 6300 2650
F 0 "U3" H 6300 3150 60  0000 C CNN
F 1 "plot_v1" H 6500 3000 60  0000 C CNN
F 2 "" H 6300 2650 60  0000 C CNN
F 3 "" H 6300 2650 60  0000 C CNN
	1    6300 2650
	1    0    0    -1  
$EndComp
Wire Wire Line
	6300 2450 6300 2500
Connection ~ 4250 2500
Wire Wire Line
	6300 2500 6400 2500
Connection ~ 6350 2500
$EndSCHEMATC
