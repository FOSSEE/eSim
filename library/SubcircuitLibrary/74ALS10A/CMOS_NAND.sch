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
LIBS:CMOS_NAND-cache
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
L eSim_MOS_P M1
U 1 1 5EA19849
P 5150 2100
F 0 "M1" H 5100 2150 50  0000 R CNN
F 1 "eSim_MOS_P" H 5200 2250 50  0000 R CNN
F 2 "" H 5400 2200 29  0000 C CNN
F 3 "" H 5200 2100 60  0000 C CNN
	1    5150 2100
	1    0    0    -1  
$EndComp
$Comp
L eSim_MOS_P M4
U 1 1 5EA1984A
P 5950 2050
F 0 "M4" H 5900 2100 50  0000 R CNN
F 1 "eSim_MOS_P" H 6000 2200 50  0000 R CNN
F 2 "" H 6200 2150 29  0000 C CNN
F 3 "" H 6000 2050 60  0000 C CNN
	1    5950 2050
	-1   0    0    -1  
$EndComp
$Comp
L eSim_MOS_N M2
U 1 1 5EA1984B
P 5350 2800
F 0 "M2" H 5350 2650 50  0000 R CNN
F 1 "eSim_MOS_N" H 5450 2750 50  0000 R CNN
F 2 "" H 5650 2500 29  0000 C CNN
F 3 "" H 5450 2600 60  0000 C CNN
	1    5350 2800
	1    0    0    -1  
$EndComp
$Comp
L eSim_MOS_N M3
U 1 1 5EA1984C
P 5350 3450
F 0 "M3" H 5350 3300 50  0000 R CNN
F 1 "eSim_MOS_N" H 5450 3400 50  0000 R CNN
F 2 "" H 5650 3150 29  0000 C CNN
F 3 "" H 5450 3250 60  0000 C CNN
	1    5350 3450
	1    0    0    -1  
$EndComp
Wire Wire Line
	5300 2300 5300 2550
Wire Wire Line
	5300 2550 5800 2550
Wire Wire Line
	5800 2550 5800 2250
Wire Wire Line
	5400 2250 5450 2250
Wire Wire Line
	5450 2250 5450 1800
Wire Wire Line
	5300 1800 5800 1800
Wire Wire Line
	5300 1800 5300 1900
Wire Wire Line
	5600 2200 5700 2200
Wire Wire Line
	5600 1650 5600 2200
Wire Wire Line
	5800 1800 5800 1850
Wire Wire Line
	5550 3200 5550 3450
Wire Wire Line
	5550 2550 5550 2800
Connection ~ 5550 2550
Wire Wire Line
	5650 3150 5800 3150
Wire Wire Line
	5800 3150 5800 4100
Wire Wire Line
	5550 3850 5550 4100
Wire Wire Line
	5650 3800 5650 4200
Connection ~ 5650 4000
Connection ~ 5450 1800
Connection ~ 5600 1800
Wire Wire Line
	7400 2250 7400 1650
Wire Wire Line
	7400 1650 5600 1650
Wire Wire Line
	7400 4200 7400 3150
Wire Wire Line
	5650 4200 7400 4200
Wire Wire Line
	4650 3650 5250 3650
Connection ~ 5650 4200
Wire Wire Line
	3950 2400 4650 2400
Wire Wire Line
	4650 2400 4650 3000
Wire Wire Line
	4650 3000 5250 3000
Wire Wire Line
	4950 2100 5000 2100
Connection ~ 4950 3650
Wire Wire Line
	6400 2050 6400 4850
Wire Wire Line
	6400 2050 6100 2050
Connection ~ 6050 4200
Connection ~ 5550 2750
Wire Wire Line
	4950 3000 4950 2100
Connection ~ 4950 3000
Wire Wire Line
	4950 3650 4950 4850
Wire Wire Line
	4950 4850 6400 4850
Wire Wire Line
	6000 2750 5550 2750
Connection ~ 4200 2400
Wire Wire Line
	4650 3350 4650 3650
Wire Wire Line
	6000 2750 6000 3000
$Comp
L PORT U1
U 1 1 5EA19AC9
P 3600 2150
F 0 "U1" H 3650 2250 30  0000 C CNN
F 1 "PORT" H 3600 2150 30  0000 C CNN
F 2 "" H 3600 2150 60  0000 C CNN
F 3 "" H 3600 2150 60  0000 C CNN
	1    3600 2150
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 2 1 5EA19B16
P 4150 3350
F 0 "U1" H 4200 3450 30  0000 C CNN
F 1 "PORT" H 4150 3350 30  0000 C CNN
F 2 "" H 4150 3350 60  0000 C CNN
F 3 "" H 4150 3350 60  0000 C CNN
	2    4150 3350
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 3 1 5EA19B5B
P 6250 3000
F 0 "U1" H 6300 3100 30  0000 C CNN
F 1 "PORT" H 6250 3000 30  0000 C CNN
F 2 "" H 6250 3000 60  0000 C CNN
F 3 "" H 6250 3000 60  0000 C CNN
	3    6250 3000
	-1   0    0    1   
$EndComp
Wire Wire Line
	4400 3350 4650 3350
Wire Wire Line
	3850 2150 3950 2150
Wire Wire Line
	3950 2150 3950 2400
Text Notes 7800 2100 0    60   ~ 0
vcc
Text Notes 7850 3300 0    60   ~ 0
gnd
Text Notes 3250 2150 0    60   ~ 0
in1\n
Text Notes 3800 3400 0    60   ~ 0
in2
Text Notes 6150 2850 0    60   ~ 0
out\n
Wire Wire Line
	5550 4100 5800 4100
Connection ~ 5650 4100
$Comp
L DC v1
U 1 1 5EA1AB6C
P 7550 2700
F 0 "v1" H 7350 2800 60  0000 C CNN
F 1 "DC" H 7350 2650 60  0000 C CNN
F 2 "R1" H 7250 2700 60  0000 C CNN
F 3 "" H 7550 2700 60  0000 C CNN
	1    7550 2700
	1    0    0    -1  
$EndComp
Wire Wire Line
	7550 2250 7400 2250
Wire Wire Line
	7400 3150 7550 3150
$Comp
L GND #PWR1
U 1 1 5EA1AC79
P 6750 4300
F 0 "#PWR1" H 6750 4050 50  0001 C CNN
F 1 "GND" H 6750 4150 50  0000 C CNN
F 2 "" H 6750 4300 50  0001 C CNN
F 3 "" H 6750 4300 50  0001 C CNN
	1    6750 4300
	1    0    0    -1  
$EndComp
Wire Wire Line
	6750 4300 6750 4200
Connection ~ 6750 4200
$EndSCHEMATC
