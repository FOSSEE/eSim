EESchema Schematic File Version 2
LIBS:RC-rescue
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
LIBS:RC-cache
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
L R-RESCUE-RC R1
U 1 1 56B86791
P 5750 3050
F 0 "R1" H 5800 3180 50  0000 C CNN
F 1 "1k" H 5800 3100 50  0000 C CNN
F 2 "" H 5800 3030 30  0000 C CNN
F 3 "" V 5800 3100 30  0000 C CNN
	1    5750 3050
	1    0    0    -1  
$EndComp
$Comp
L C C1
U 1 1 56B8686C
P 6350 3250
F 0 "C1" H 6375 3350 50  0000 L CNN
F 1 "10u" H 6375 3150 50  0000 L CNN
F 2 "" H 6388 3100 30  0000 C CNN
F 3 "" H 6350 3250 60  0000 C CNN
	1    6350 3250
	1    0    0    -1  
$EndComp
$Comp
L pwl v1
U 1 1 56B868AD
P 5250 3450
F 0 "v1" H 5050 3550 60  0000 C CNN
F 1 "pwl" H 5000 3400 60  0000 C CNN
F 2 "R1" H 4950 3450 60  0000 C CNN
F 3 "" H 5250 3450 60  0000 C CNN
	1    5250 3450
	1    0    0    -1  
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
	5350 2750 5350 3000
Connection ~ 5350 3000
Wire Wire Line
	6400 2850 6350 2850
Connection ~ 6350 3000
Wire Wire Line
	5200 2800 5350 2800
$Comp
L plot_v1 U1
U 1 1 56D46C33
P 5350 2950
F 0 "U1" H 5350 3450 60  0000 C CNN
F 1 "plot_v1" H 5550 3300 60  0000 C CNN
F 2 "" H 5350 2950 60  0000 C CNN
F 3 "" H 5350 2950 60  0000 C CNN
	1    5350 2950
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U2
U 1 1 56D46CCE
P 6350 3000
F 0 "U2" H 6350 3500 60  0000 C CNN
F 1 "plot_v1" H 6550 3350 60  0000 C CNN
F 2 "" H 6350 3000 60  0000 C CNN
F 3 "" H 6350 3000 60  0000 C CNN
	1    6350 3000
	1    0    0    -1  
$EndComp
Connection ~ 5350 2800
Connection ~ 6350 2850
$EndSCHEMATC
