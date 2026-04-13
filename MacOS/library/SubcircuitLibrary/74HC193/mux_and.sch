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
LIBS:eSim_SKY130
LIBS:eSim_SKY130_Subckts
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
L d_and U3
U 1 1 67CC00D5
P 4500 3000
F 0 "U3" H 4500 3000 60  0000 C CNN
F 1 "d_and" H 4550 3100 60  0000 C CNN
F 2 "" H 4500 3000 60  0000 C CNN
F 3 "" H 4500 3000 60  0000 C CNN
	1    4500 3000
	1    0    0    -1  
$EndComp
$Comp
L d_and U4
U 1 1 67CC0132
P 4500 4050
F 0 "U4" H 4500 4050 60  0000 C CNN
F 1 "d_and" H 4550 4150 60  0000 C CNN
F 2 "" H 4500 4050 60  0000 C CNN
F 3 "" H 4500 4050 60  0000 C CNN
	1    4500 4050
	1    0    0    -1  
$EndComp
$Comp
L d_or U5
U 1 1 67CC0167
P 6400 3450
F 0 "U5" H 6400 3450 60  0000 C CNN
F 1 "d_or" H 6400 3550 60  0000 C CNN
F 2 "" H 6400 3450 60  0000 C CNN
F 3 "" H 6400 3450 60  0000 C CNN
	1    6400 3450
	1    0    0    -1  
$EndComp
Wire Wire Line
	4950 2950 5950 2950
Wire Wire Line
	5950 2950 5950 3350
Wire Wire Line
	4950 4000 6650 4000
Wire Wire Line
	5950 4000 5950 3450
Wire Wire Line
	6850 3400 7200 3400
$Comp
L PORT U1
U 1 1 67CC01A6
P 2000 2900
F 0 "U1" H 2050 3000 30  0000 C CNN
F 1 "PORT" H 2000 2900 30  0000 C CNN
F 2 "" H 2000 2900 60  0000 C CNN
F 3 "" H 2000 2900 60  0000 C CNN
	1    2000 2900
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 2 1 67CC0221
P 3200 3000
F 0 "U1" H 3250 3100 30  0000 C CNN
F 1 "PORT" H 3200 3000 30  0000 C CNN
F 2 "" H 3200 3000 60  0000 C CNN
F 3 "" H 3200 3000 60  0000 C CNN
	2    3200 3000
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 3 1 67CC0296
P 3350 4050
F 0 "U1" H 3400 4150 30  0000 C CNN
F 1 "PORT" H 3350 4050 30  0000 C CNN
F 2 "" H 3350 4050 60  0000 C CNN
F 3 "" H 3350 4050 60  0000 C CNN
	3    3350 4050
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 6 1 67CC0355
P 7450 3400
F 0 "U1" H 7500 3500 30  0000 C CNN
F 1 "PORT" H 7450 3400 30  0000 C CNN
F 2 "" H 7450 3400 60  0000 C CNN
F 3 "" H 7450 3400 60  0000 C CNN
	6    7450 3400
	-1   0    0    1   
$EndComp
$Comp
L PORT U1
U 4 1 67CC03E0
P 6850 3000
F 0 "U1" H 6900 3100 30  0000 C CNN
F 1 "PORT" H 6850 3000 30  0000 C CNN
F 2 "" H 6850 3000 60  0000 C CNN
F 3 "" H 6850 3000 60  0000 C CNN
	4    6850 3000
	-1   0    0    1   
$EndComp
$Comp
L PORT U1
U 5 1 67CC044B
P 6900 4000
F 0 "U1" H 6950 4100 30  0000 C CNN
F 1 "PORT" H 6900 4000 30  0000 C CNN
F 2 "" H 6900 4000 60  0000 C CNN
F 3 "" H 6900 4000 60  0000 C CNN
	5    6900 4000
	-1   0    0    1   
$EndComp
$Comp
L d_inverter U2
U 1 1 67CC04A4
P 2800 3950
F 0 "U2" H 2800 3850 60  0000 C CNN
F 1 "d_inverter" H 2800 4100 60  0000 C CNN
F 2 "" H 2850 3900 60  0000 C CNN
F 3 "" H 2850 3900 60  0000 C CNN
	1    2800 3950
	1    0    0    -1  
$EndComp
Wire Wire Line
	2250 2900 2250 3950
Wire Wire Line
	2250 3950 2500 3950
Wire Wire Line
	3100 3950 4050 3950
Wire Wire Line
	3600 4050 4050 4050
Connection ~ 2250 2900
Wire Wire Line
	2250 2900 4050 2900
Wire Wire Line
	3450 3000 4050 3000
Wire Wire Line
	6600 3000 5950 3000
Connection ~ 5950 3000
Connection ~ 5950 4000
$EndSCHEMATC
