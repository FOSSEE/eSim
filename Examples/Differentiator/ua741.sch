EESchema Schematic File Version 2  date Wednesday 19 December 2012 10:15:16 AM IST
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
LIBS:special
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
LIBS:analogSpice
LIBS:converterSpice
LIBS:digitalSpice
LIBS:linearSpice
LIBS:measurementSpice
LIBS:portSpice
LIBS:sourcesSpice
LIBS:analogXSpice
LIBS:ua741-cache
EELAYER 25  0
EELAYER END
$Descr A4 11700 8267
encoding utf-8
Sheet 1 1
Title ""
Date "19 dec 2012"
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
Text Notes 3800 2400 0    60   ~ 0
Op-Amp
Text Notes 3750 2850 0    60   ~ 0
VCCS
Text Notes 5800 2500 0    60   ~ 0
out
Text Notes 2750 3100 0    60   ~ 0
-
Text Notes 2700 2600 0    60   ~ 0
+
$Comp
L PORT U1
U 6 1 5082C027
P 6250 2500
F 0 "U1" H 6250 2450 30  0000 C CNN
F 1 "PORT" H 6250 2500 30  0000 C CNN
	6    6250 2500
	-1   0    0    1   
$EndComp
$Comp
L PORT U1
U 2 1 5082C011
P 2300 3100
F 0 "U1" H 2300 3050 30  0000 C CNN
F 1 "PORT" H 2300 3100 30  0000 C CNN
	2    2300 3100
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 3 1 5082C00B
P 2250 2600
F 0 "U1" H 2250 2550 30  0000 C CNN
F 1 "PORT" H 2250 2600 30  0000 C CNN
	3    2250 2600
	1    0    0    -1  
$EndComp
Connection ~ 3700 3200
Wire Wire Line
	3450 3200 3700 3200
Connection ~ 5000 3300
Wire Wire Line
	3700 3300 5250 3300
Wire Wire Line
	5250 3300 5250 3200
Connection ~ 4550 3300
Wire Wire Line
	5000 3300 5000 2950
Connection ~ 3700 3300
Wire Wire Line
	4550 3300 4550 3100
Wire Wire Line
	3900 2500 3700 2500
Wire Wire Line
	3700 2500 3700 2550
Wire Wire Line
	3450 2900 3300 2900
Wire Wire Line
	3300 2900 3300 3200
Wire Wire Line
	3300 3200 2950 3200
Connection ~ 2950 3100
Wire Wire Line
	2950 3200 2950 3100
Wire Wire Line
	3000 2600 2500 2600
Wire Wire Line
	2550 3100 3000 3100
Wire Wire Line
	2950 2600 2950 2500
Connection ~ 2950 2600
Wire Wire Line
	2950 2500 3300 2500
Wire Wire Line
	3300 2500 3300 2800
Wire Wire Line
	3300 2800 3450 2800
Wire Wire Line
	3700 3150 3700 3400
Wire Wire Line
	4550 2500 4550 2700
Wire Wire Line
	4400 2500 5000 2500
Wire Wire Line
	5000 2500 5000 2850
Connection ~ 4550 2500
Wire Wire Line
	5250 2600 5250 2500
Wire Wire Line
	5250 2500 5350 2500
Wire Wire Line
	5850 2500 6000 2500
$Comp
L PWR_FLAG #FLG01
U 1 1 508152A0
P 3450 3200
F 0 "#FLG01" H 3450 3470 30  0001 C CNN
F 1 "PWR_FLAG" H 3450 3430 30  0000 C CNN
	1    3450 3200
	1    0    0    -1  
$EndComp
$Comp
L R Rout1
U 1 1 50813F5B
P 5600 2500
F 0 "Rout1" V 5680 2500 50  0000 C CNN
F 1 "75" V 5600 2500 50  0000 C CNN
	1    5600 2500
	0    1    1    0   
$EndComp
$Comp
L VCVS Eout1
U 1 1 50813F0F
P 5200 2900
F 0 "Eout1" H 5000 3000 50  0000 C CNN
F 1 "1" H 5000 2850 50  0000 C CNN
	1    5200 2900
	0    1    1    0   
$EndComp
$Comp
L C Cbw1
U 1 1 50813EE0
P 4550 2900
F 0 "Cbw1" H 4600 3000 50  0000 L CNN
F 1 "31.85e-9" H 4600 2800 50  0000 L CNN
	1    4550 2900
	1    0    0    -1  
$EndComp
$Comp
L R Rbw1
U 1 1 50813EAB
P 4150 2500
F 0 "Rbw1" V 4230 2500 50  0000 C CNN
F 1 "0.5e6" V 4150 2500 50  0000 C CNN
	1    4150 2500
	0    1    1    0   
$EndComp
$Comp
L GND #PWR02
U 1 1 50813E0D
P 3700 3400
F 0 "#PWR02" H 3700 3400 30  0001 C CNN
F 1 "GND" H 3700 3330 30  0001 C CNN
	1    3700 3400
	1    0    0    -1  
$EndComp
$Comp
L VCVS Ein1
U 1 1 50813D7C
P 3650 2850
F 0 "Ein1" H 3450 2950 50  0000 C CNN
F 1 "100e3" H 3450 2800 50  0000 C CNN
	1    3650 2850
	0    1    1    0   
$EndComp
$Comp
L R Rin1
U 1 1 50813C57
P 3000 2850
F 0 "Rin1" V 3080 2850 50  0000 C CNN
F 1 "2e6" V 3000 2850 50  0000 C CNN
	1    3000 2850
	1    0    0    -1  
$EndComp
$EndSCHEMATC
