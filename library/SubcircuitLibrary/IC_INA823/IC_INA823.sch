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
LIBS:IC_INA823-cache
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
L lm_741 X2
U 1 1 63E9DF0B
P 3150 1850
F 0 "X2" H 2950 1850 60  0000 C CNN
F 1 "lm_741" H 3050 1600 60  0000 C CNN
F 2 "" H 3150 1850 60  0000 C CNN
F 3 "" H 3150 1850 60  0000 C CNN
	1    3150 1850
	1    0    0    1   
$EndComp
$Comp
L lm_741 X1
U 1 1 63E9DF38
P 3100 3750
F 0 "X1" H 2900 3750 60  0000 C CNN
F 1 "lm_741" H 3000 3500 60  0000 C CNN
F 2 "" H 3100 3750 60  0000 C CNN
F 3 "" H 3100 3750 60  0000 C CNN
	1    3100 3750
	1    0    0    -1  
$EndComp
$Comp
L lm_741 X3
U 1 1 63E9F328
P 4850 2800
F 0 "X3" H 4650 2800 60  0000 C CNN
F 1 "lm_741" H 4750 2550 60  0000 C CNN
F 2 "" H 4850 2800 60  0000 C CNN
F 3 "" H 4850 2800 60  0000 C CNN
	1    4850 2800
	1    0    0    -1  
$EndComp
$Comp
L resistor R2
U 1 1 63E9F389
P 3000 3050
F 0 "R2" H 3050 3180 50  0000 C CNN
F 1 "50k" H 3050 3000 50  0000 C CNN
F 2 "" H 3050 3030 30  0000 C CNN
F 3 "" V 3050 3100 30  0000 C CNN
	1    3000 3050
	1    0    0    -1  
$EndComp
$Comp
L resistor R1
U 1 1 63E9F3B0
P 3000 2650
F 0 "R1" H 3050 2780 50  0000 C CNN
F 1 "50k" H 3050 2600 50  0000 C CNN
F 2 "" H 3050 2630 30  0000 C CNN
F 3 "" V 3050 2700 30  0000 C CNN
	1    3000 2650
	1    0    0    -1  
$EndComp
Wire Wire Line
	2050 2000 2600 2000
Wire Wire Line
	2550 2000 2550 2600
Wire Wire Line
	2550 2600 2900 2600
Wire Wire Line
	3200 2600 3750 2600
Wire Wire Line
	3750 2600 3750 1850
Wire Wire Line
	3700 1850 3950 1850
Wire Wire Line
	2900 3000 2500 3000
Wire Wire Line
	2500 3000 2500 3600
Wire Wire Line
	2050 3600 2550 3600
Wire Wire Line
	3200 3000 3650 3000
Wire Wire Line
	3650 3000 3650 3750
$Comp
L resistor R4
U 1 1 63E9F453
P 4050 1900
F 0 "R4" H 4100 2030 50  0000 C CNN
F 1 "50k" H 4100 1850 50  0000 C CNN
F 2 "" H 4100 1880 30  0000 C CNN
F 3 "" V 4100 1950 30  0000 C CNN
	1    4050 1900
	1    0    0    -1  
$EndComp
$Comp
L resistor R3
U 1 1 63E9F476
P 3950 3800
F 0 "R3" H 4000 3930 50  0000 C CNN
F 1 "50k" H 4000 3750 50  0000 C CNN
F 2 "" H 4000 3780 30  0000 C CNN
F 3 "" V 4000 3850 30  0000 C CNN
	1    3950 3800
	1    0    0    -1  
$EndComp
$Comp
L resistor R6
U 1 1 63E9F4AD
P 4750 1900
F 0 "R6" H 4800 2030 50  0000 C CNN
F 1 "50k" H 4800 1850 50  0000 C CNN
F 2 "" H 4800 1880 30  0000 C CNN
F 3 "" V 4800 1950 30  0000 C CNN
	1    4750 1900
	1    0    0    -1  
$EndComp
$Comp
L resistor R5
U 1 1 63E9F4D4
P 4650 3800
F 0 "R5" H 4700 3930 50  0000 C CNN
F 1 "50k" H 4700 3750 50  0000 C CNN
F 2 "" H 4700 3780 30  0000 C CNN
F 3 "" V 4700 3850 30  0000 C CNN
	1    4650 3800
	1    0    0    -1  
$EndComp
Wire Wire Line
	4300 2650 4300 1850
Wire Wire Line
	4250 1850 4650 1850
Wire Wire Line
	3650 3750 3850 3750
Connection ~ 3750 1850
Connection ~ 4300 1850
Wire Wire Line
	4550 3750 4150 3750
Wire Wire Line
	4300 2900 4300 3750
Connection ~ 4300 3750
Wire Wire Line
	4950 1850 5400 1850
Wire Wire Line
	5400 1850 5400 2800
$Comp
L PORT U1
U 3 1 63E9F7D3
P 1800 3600
F 0 "U1" H 1850 3700 30  0000 C CNN
F 1 "PORT" H 1800 3600 30  0000 C CNN
F 2 "" H 1800 3600 60  0000 C CNN
F 3 "" H 1800 3600 60  0000 C CNN
	3    1800 3600
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 4 1 63E9F7FE
P 1800 3900
F 0 "U1" H 1850 4000 30  0000 C CNN
F 1 "PORT" H 1800 3900 30  0000 C CNN
F 2 "" H 1800 3900 60  0000 C CNN
F 3 "" H 1800 3900 60  0000 C CNN
	4    1800 3900
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 2 1 63E9FB83
P 1800 2000
F 0 "U1" H 1850 2100 30  0000 C CNN
F 1 "PORT" H 1800 2000 30  0000 C CNN
F 2 "" H 1800 2000 60  0000 C CNN
F 3 "" H 1800 2000 60  0000 C CNN
	2    1800 2000
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 1 1 63E9FBC2
P 1800 1750
F 0 "U1" H 1850 1850 30  0000 C CNN
F 1 "PORT" H 1800 1750 30  0000 C CNN
F 2 "" H 1800 1750 60  0000 C CNN
F 3 "" H 1800 1750 60  0000 C CNN
	1    1800 1750
	1    0    0    -1  
$EndComp
Wire Wire Line
	2050 1750 2600 1750
Connection ~ 2550 2000
Connection ~ 2500 3600
Wire Wire Line
	2050 3900 2550 3900
Wire Wire Line
	2550 3900 2550 3850
$Comp
L PORT U1
U 5 1 63E9FD93
P 3950 1450
F 0 "U1" H 4000 1550 30  0000 C CNN
F 1 "PORT" H 3950 1450 30  0000 C CNN
F 2 "" H 3950 1450 60  0000 C CNN
F 3 "" H 3950 1450 60  0000 C CNN
	5    3950 1450
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 7 1 63E9FDEE
P 5250 1450
F 0 "U1" H 5300 1550 30  0000 C CNN
F 1 "PORT" H 5250 1450 30  0000 C CNN
F 2 "" H 5250 1450 60  0000 C CNN
F 3 "" H 5250 1450 60  0000 C CNN
	7    5250 1450
	-1   0    0    1   
$EndComp
$Comp
L PORT U1
U 6 1 63E9FF0C
P 5500 3750
F 0 "U1" H 5550 3850 30  0000 C CNN
F 1 "PORT" H 5500 3750 30  0000 C CNN
F 2 "" H 5500 3750 60  0000 C CNN
F 3 "" H 5500 3750 60  0000 C CNN
	6    5500 3750
	-1   0    0    1   
$EndComp
$Comp
L PORT U1
U 8 1 63E9FF8B
P 5950 2800
F 0 "U1" H 6000 2900 30  0000 C CNN
F 1 "PORT" H 5950 2800 30  0000 C CNN
F 2 "" H 5950 2800 60  0000 C CNN
F 3 "" H 5950 2800 60  0000 C CNN
	8    5950 2800
	-1   0    0    1   
$EndComp
Wire Wire Line
	4850 3750 5250 3750
Wire Wire Line
	5400 2800 5700 2800
Text GLabel 4200 1200 0    60   Input ~ 0
V+
Text GLabel 4950 1200 2    60   Input ~ 0
V-
Wire Wire Line
	4200 1200 4350 1200
Wire Wire Line
	4350 1200 4350 1450
Connection ~ 4350 1450
Wire Wire Line
	4950 1200 4850 1200
Wire Wire Line
	4850 1200 4850 1450
Connection ~ 4850 1450
Text GLabel 3300 3250 2    60   Input ~ 0
V+
Text GLabel 3300 2450 2    60   Input ~ 0
V+
Text GLabel 4950 2200 2    60   Input ~ 0
V+
Text GLabel 3300 4350 2    60   Input ~ 0
V-
Text GLabel 3200 1150 2    60   Input ~ 0
V-
Text GLabel 4950 3400 2    60   Input ~ 0
V-
Wire Wire Line
	3200 1150 3000 1150
Wire Wire Line
	3000 1150 3000 1400
Wire Wire Line
	3300 2450 3000 2450
Wire Wire Line
	3000 2450 3000 2300
Wire Wire Line
	3300 3250 2950 3250
Wire Wire Line
	2950 3250 2950 3300
Wire Wire Line
	4950 2200 4700 2200
Wire Wire Line
	4700 2200 4700 2350
Wire Wire Line
	4950 3400 4700 3400
Wire Wire Line
	4700 3400 4700 3250
Wire Wire Line
	3300 4350 2950 4350
Wire Wire Line
	2950 4350 2950 4200
Wire Wire Line
	4350 1450 4200 1450
Wire Wire Line
	4850 1450 5000 1450
$EndSCHEMATC
