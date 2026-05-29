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
LIBS:7805VoltageRegulator-cache
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
L eSim_Diode D1
U 1 1 5CFF3A6D
P 4300 2350
F 0 "D1" H 4300 2450 50  0000 C CNN
F 1 "eSim_Diode" H 4300 2250 50  0000 C CNN
F 2 "" H 4300 2350 60  0000 C CNN
F 3 "" H 4300 2350 60  0000 C CNN
	1    4300 2350
	0    -1   -1   0   
$EndComp
$Comp
L eSim_Diode D2
U 1 1 5CFF3A6E
P 4300 3200
F 0 "D2" H 4300 3300 50  0000 C CNN
F 1 "eSim_Diode" H 4300 3100 50  0000 C CNN
F 2 "" H 4300 3200 60  0000 C CNN
F 3 "" H 4300 3200 60  0000 C CNN
	1    4300 3200
	0    -1   -1   0   
$EndComp
$Comp
L eSim_Diode D4
U 1 1 5CFF3A6F
P 5200 3200
F 0 "D4" H 5200 3300 50  0000 C CNN
F 1 "eSim_Diode" H 5200 3100 50  0000 C CNN
F 2 "" H 5200 3200 60  0000 C CNN
F 3 "" H 5200 3200 60  0000 C CNN
	1    5200 3200
	0    -1   -1   0   
$EndComp
$Comp
L eSim_Diode D3
U 1 1 5CFF3A70
P 5200 2350
F 0 "D3" H 5200 2450 50  0000 C CNN
F 1 "eSim_Diode" H 5200 2250 50  0000 C CNN
F 2 "" H 5200 2350 60  0000 C CNN
F 3 "" H 5200 2350 60  0000 C CNN
	1    5200 2350
	0    -1   -1   0   
$EndComp
$Comp
L eSim_Diode D5
U 1 1 5CFF3A71
P 8900 2850
F 0 "D5" H 8900 2950 50  0000 C CNN
F 1 "eSim_Diode" H 8900 2750 50  0000 C CNN
F 2 "" H 8900 2850 60  0000 C CNN
F 3 "" H 8900 2850 60  0000 C CNN
	1    8900 2850
	0    -1   -1   0   
$EndComp
$Comp
L C C1
U 1 1 5CFF3A73
P 6100 2850
F 0 "C1" H 6125 2950 50  0000 L CNN
F 1 "1000u" H 6125 2750 50  0000 L CNN
F 2 "" H 6138 2700 50  0001 C CNN
F 3 "" H 6100 2850 50  0001 C CNN
	1    6100 2850
	1    0    0    -1  
$EndComp
$Comp
L C C2
U 1 1 5CFF3A74
P 8200 2850
F 0 "C2" H 8225 2950 50  0000 L CNN
F 1 "3.3u" H 8225 2750 50  0000 L CNN
F 2 "" H 8238 2700 50  0001 C CNN
F 3 "" H 8200 2850 50  0001 C CNN
	1    8200 2850
	1    0    0    -1  
$EndComp
$Comp
L R R1
U 1 1 5CFF3A75
P 9400 2850
F 0 "R1" V 9480 2850 50  0000 C CNN
F 1 "1k" V 9400 2850 50  0000 C CNN
F 2 "" V 9330 2850 50  0001 C CNN
F 3 "" H 9400 2850 50  0001 C CNN
	1    9400 2850
	1    0    0    -1  
$EndComp
$Comp
L sine v1
U 1 1 5CFF3A76
P 3200 2850
F 0 "v1" H 3000 2950 60  0000 C CNN
F 1 "sine" H 3000 2800 60  0000 C CNN
F 2 "R1" H 2900 2850 60  0000 C CNN
F 3 "" H 3200 2850 60  0000 C CNN
	1    3200 2850
	1    0    0    -1  
$EndComp
Text GLabel 3200 2150 0    60   Input ~ 0
in1
Text GLabel 3200 3600 0    60   Input ~ 0
in2
$Comp
L plot_v1 U1
U 1 1 5CFF3A77
P 3450 2250
F 0 "U1" H 3450 2750 60  0000 C CNN
F 1 "plot_v1" H 3650 2600 60  0000 C CNN
F 2 "" H 3450 2250 60  0000 C CNN
F 3 "" H 3450 2250 60  0000 C CNN
	1    3450 2250
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U2
U 1 1 5CFF3A78
P 3450 3700
F 0 "U2" H 3450 4200 60  0000 C CNN
F 1 "plot_v1" H 3650 4050 60  0000 C CNN
F 2 "" H 3450 3700 60  0000 C CNN
F 3 "" H 3450 3700 60  0000 C CNN
	1    3450 3700
	-1   0    0    1   
$EndComp
Text GLabel 9750 1800 2    60   Input ~ 0
out
$Comp
L plot_v1 U3
U 1 1 5CFF3A79
P 9400 1900
F 0 "U3" H 9400 2400 60  0000 C CNN
F 1 "plot_v1" H 9600 2250 60  0000 C CNN
F 2 "" H 9400 1900 60  0000 C CNN
F 3 "" H 9400 1900 60  0000 C CNN
	1    9400 1900
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR01
U 1 1 5CFF3A7A
P 7350 3800
F 0 "#PWR01" H 7350 3550 50  0001 C CNN
F 1 "GND" H 7350 3650 50  0000 C CNN
F 2 "" H 7350 3800 50  0001 C CNN
F 3 "" H 7350 3800 50  0001 C CNN
	1    7350 3800
	1    0    0    -1  
$EndComp
Connection ~ 7350 3600
Wire Wire Line
	7350 2400 7350 3800
Connection ~ 3450 3600
Wire Wire Line
	3200 3600 3450 3600
Connection ~ 3450 3300
Wire Wire Line
	3450 3900 3450 3300
Connection ~ 3450 2150
Wire Wire Line
	3200 2150 3450 2150
Connection ~ 3450 2400
Wire Wire Line
	3450 2050 3450 2400
Connection ~ 9400 1800
Wire Wire Line
	9750 1800 9400 1800
Connection ~ 9400 2000
Connection ~ 8900 3600
Wire Wire Line
	9400 3600 9400 3000
Connection ~ 8900 2000
Wire Wire Line
	9400 1700 9400 2700
Connection ~ 8200 2000
Wire Wire Line
	8900 2000 8900 2700
Connection ~ 8200 3600
Wire Wire Line
	8900 3600 8900 3000
Connection ~ 6100 3600
Wire Wire Line
	8200 3600 8200 3000
Wire Wire Line
	7900 2000 9400 2000
Wire Wire Line
	8200 2700 8200 2000
Connection ~ 6100 2000
Wire Wire Line
	6100 2700 6100 2000
Connection ~ 5200 3600
Wire Wire Line
	6100 3600 6100 3000
Connection ~ 4300 2950
Wire Wire Line
	3800 2950 4300 2950
Wire Wire Line
	3800 3300 3800 2950
Wire Wire Line
	3200 3300 3800 3300
Connection ~ 5200 2600
Wire Wire Line
	3800 2600 5200 2600
Wire Wire Line
	3800 2400 3800 2600
Wire Wire Line
	3200 2400 3800 2400
Wire Wire Line
	5200 3600 5200 3350
Wire Wire Line
	4300 3600 9400 3600
Wire Wire Line
	4300 3350 4300 3600
Wire Wire Line
	4300 3050 4300 2500
Wire Wire Line
	5200 2500 5200 3050
Connection ~ 5200 2000
Wire Wire Line
	5200 2000 5200 2200
Wire Wire Line
	4300 2000 6800 2000
Wire Wire Line
	4300 2200 4300 2000
$Comp
L LM_7812 X1
U 1 1 5CFF3AF7
P 7350 2000
F 0 "X1" H 7350 2050 60  0000 C CNN
F 1 "LM_7812" H 7350 2150 60  0000 C CNN
F 2 "" H 7350 2000 60  0001 C CNN
F 3 "" H 7350 2000 60  0001 C CNN
	1    7350 2000
	1    0    0    -1  
$EndComp
$EndSCHEMATC
