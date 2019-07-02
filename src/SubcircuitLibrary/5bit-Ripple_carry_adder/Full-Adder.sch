EESchema Schematic File Version 2
LIBS:eSim_Analog
LIBS:eSim_Devices
LIBS:eSim_Digital
LIBS:eSim_Hybrid
LIBS:eSim_Miscellaneous
LIBS:eSim_Plot
LIBS:eSim_Power
LIBS:eSim_PSpice
LIBS:eSim_Sources
LIBS:eSim_Subckt
LIBS:eSim_User
LIBS:half-adder
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
LIBS:Full-Adder-cache
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
L PORT U1
U 1 1 5C93775D
P 4100 2800
F 0 "U1" H 4150 2900 30  0000 C CNN
F 1 "PORT" H 4100 2800 30  0000 C CNN
F 2 "" H 4100 2800 60  0000 C CNN
F 3 "" H 4100 2800 60  0000 C CNN
	1    4100 2800
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 2 1 5C9377A8
P 4100 3100
F 0 "U1" H 4150 3200 30  0000 C CNN
F 1 "PORT" H 4100 3100 30  0000 C CNN
F 2 "" H 4100 3100 60  0000 C CNN
F 3 "" H 4100 3100 60  0000 C CNN
	2    4100 3100
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 3 1 5C9377CD
P 4100 3400
F 0 "U1" H 4150 3500 30  0000 C CNN
F 1 "PORT" H 4100 3400 30  0000 C CNN
F 2 "" H 4100 3400 60  0000 C CNN
F 3 "" H 4100 3400 60  0000 C CNN
	3    4100 3400
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 4 1 5C9377F2
P 8450 2900
F 0 "U1" H 8500 3000 30  0000 C CNN
F 1 "PORT" H 8450 2900 30  0000 C CNN
F 2 "" H 8450 2900 60  0000 C CNN
F 3 "" H 8450 2900 60  0000 C CNN
	4    8450 2900
	-1   0    0    1   
$EndComp
$Comp
L PORT U1
U 5 1 5C937851
P 8450 3200
F 0 "U1" H 8500 3300 30  0000 C CNN
F 1 "PORT" H 8450 3200 30  0000 C CNN
F 2 "" H 8450 3200 60  0000 C CNN
F 3 "" H 8450 3200 60  0000 C CNN
	5    8450 3200
	-1   0    0    1   
$EndComp
$Comp
L d_xor U2
U 1 1 5C93788C
P 5150 2900
F 0 "U2" H 5150 2900 60  0000 C CNN
F 1 "d_xor" H 5200 3000 47  0000 C CNN
F 2 "" H 5150 2900 60  0000 C CNN
F 3 "" H 5150 2900 60  0000 C CNN
	1    5150 2900
	1    0    0    -1  
$EndComp
$Comp
L d_xor U5
U 1 1 5C9378DF
P 6400 2950
F 0 "U5" H 6400 2950 60  0000 C CNN
F 1 "d_xor" H 6450 3050 47  0000 C CNN
F 2 "" H 6400 2950 60  0000 C CNN
F 3 "" H 6400 2950 60  0000 C CNN
	1    6400 2950
	1    0    0    -1  
$EndComp
$Comp
L d_and U4
U 1 1 5C937928
P 6150 3300
F 0 "U4" H 6150 3300 60  0000 C CNN
F 1 "d_and" H 6200 3400 60  0000 C CNN
F 2 "" H 6150 3300 60  0000 C CNN
F 3 "" H 6150 3300 60  0000 C CNN
	1    6150 3300
	1    0    0    -1  
$EndComp
$Comp
L d_and U3
U 1 1 5C9379CF
P 5200 3500
F 0 "U3" H 5200 3500 60  0000 C CNN
F 1 "d_and" H 5250 3600 60  0000 C CNN
F 2 "" H 5200 3500 60  0000 C CNN
F 3 "" H 5200 3500 60  0000 C CNN
	1    5200 3500
	1    0    0    -1  
$EndComp
$Comp
L d_or U6
U 1 1 5C937A14
P 7250 3550
F 0 "U6" H 7250 3550 60  0000 C CNN
F 1 "d_or" H 7250 3650 60  0000 C CNN
F 2 "" H 7250 3550 60  0000 C CNN
F 3 "" H 7250 3550 60  0000 C CNN
	1    7250 3550
	1    0    0    -1  
$EndComp
Wire Wire Line
	4350 2800 4700 2800
Wire Wire Line
	4350 3100 4700 3100
Wire Wire Line
	4700 3100 4700 2900
Wire Wire Line
	5600 2850 5950 2850
Wire Wire Line
	4350 3400 4400 3400
Wire Wire Line
	4400 3400 4400 3150
Wire Wire Line
	4400 3150 5450 3150
Wire Wire Line
	5450 3150 5450 2950
Wire Wire Line
	5450 2950 5950 2950
Wire Wire Line
	6850 2900 8200 2900
Wire Wire Line
	4450 2800 4450 3400
Wire Wire Line
	4450 3400 4750 3400
Connection ~ 4450 2800
Wire Wire Line
	4600 3100 4600 3500
Wire Wire Line
	4600 3500 4750 3500
Connection ~ 4600 3100
Wire Wire Line
	5650 3450 6800 3450
Wire Wire Line
	4400 3300 5700 3300
Connection ~ 4400 3300
Wire Wire Line
	5700 3200 5700 2850
Connection ~ 5700 2850
Wire Wire Line
	6600 3250 6650 3250
Wire Wire Line
	6650 3250 6650 3550
Wire Wire Line
	6650 3550 6800 3550
Wire Wire Line
	7700 3500 7700 3200
Wire Wire Line
	7700 3200 8200 3200
Text Notes 4400 2750 0    60   ~ 0
A
Text Notes 4400 3050 0    60   ~ 0
B
Text Notes 4350 3500 0    60   ~ 0
Cin
Text Notes 7950 2850 0    60   ~ 0
Sum
Text Notes 7950 3150 0    60   ~ 0
Cout
$EndSCHEMATC
