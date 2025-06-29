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
LIBS:Tri_state_buffer-cache
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
L mosfet_p M2
U 1 1 6836AEEF
P 4350 3250
F 0 "M2" H 4300 3300 50  0000 R CNN
F 1 "mosfet_p" H 4400 3400 50  0000 R CNN
F 2 "" H 4600 3350 29  0000 C CNN
F 3 "" H 4400 3250 60  0000 C CNN
	1    4350 3250
	1    0    0    1   
$EndComp
Wire Wire Line
	4500 3450 4500 3850
Wire Wire Line
	4200 3250 4200 4050
Wire Wire Line
	4600 4200 4600 4800
Wire Wire Line
	4600 3100 4600 3050
Wire Wire Line
	4600 3050 4500 3050
Connection ~ 4200 3600
Connection ~ 4500 3550
Wire Wire Line
	4550 2600 4550 3050
Connection ~ 4550 3050
$Comp
L mosfet_n M5
U 1 1 683749D7
P 5150 3800
F 0 "M5" H 5150 3650 50  0000 R CNN
F 1 "mosfet_n" H 5250 3750 50  0000 R CNN
F 2 "" H 5450 3500 29  0000 C CNN
F 3 "" H 5250 3600 60  0000 C CNN
	1    5150 3800
	1    0    0    -1  
$EndComp
$Comp
L mosfet_n M6
U 1 1 68374A1E
P 5150 4350
F 0 "M6" H 5150 4200 50  0000 R CNN
F 1 "mosfet_n" H 5250 4300 50  0000 R CNN
F 2 "" H 5450 4050 29  0000 C CNN
F 3 "" H 5250 4150 60  0000 C CNN
	1    5150 4350
	1    0    0    -1  
$EndComp
$Comp
L mosfet_p M8
U 1 1 68374A51
P 5200 3400
F 0 "M8" H 5150 3450 50  0000 R CNN
F 1 "mosfet_p" H 5250 3550 50  0000 R CNN
F 2 "" H 5450 3500 29  0000 C CNN
F 3 "" H 5250 3400 60  0000 C CNN
	1    5200 3400
	1    0    0    1   
$EndComp
$Comp
L mosfet_p M7
U 1 1 68374A9C
P 5200 2850
F 0 "M7" H 5150 2900 50  0000 R CNN
F 1 "mosfet_p" H 5250 3000 50  0000 R CNN
F 2 "" H 5450 2950 29  0000 C CNN
F 3 "" H 5250 2850 60  0000 C CNN
	1    5200 2850
	1    0    0    1   
$EndComp
Wire Wire Line
	5350 3600 5350 3800
Wire Wire Line
	5350 3200 5350 3050
Wire Wire Line
	5600 3250 5450 3250
Wire Wire Line
	5600 2650 5600 3250
Wire Wire Line
	5600 2700 5450 2700
Wire Wire Line
	5350 2650 5600 2650
Connection ~ 5600 2700
Wire Wire Line
	5350 4200 5350 4350
Wire Wire Line
	5450 4150 5600 4150
Wire Wire Line
	5600 4150 5600 4750
Wire Wire Line
	5600 4700 5450 4700
Wire Wire Line
	5600 4750 5350 4750
Connection ~ 5600 4700
$Comp
L mosfet_n M1
U 1 1 6836AF30
P 4300 3850
F 0 "M1" H 4300 3700 50  0000 R CNN
F 1 "mosfet_n" H 4400 3800 50  0000 R CNN
F 2 "" H 4600 3550 29  0000 C CNN
F 3 "" H 4400 3650 60  0000 C CNN
	1    4300 3850
	1    0    0    -1  
$EndComp
Wire Wire Line
	3250 4800 5450 4800
Wire Wire Line
	5450 4800 5450 4750
Connection ~ 5450 4750
Connection ~ 4950 4800
Wire Wire Line
	4500 4250 4500 4350
Wire Wire Line
	4500 4350 4600 4350
Connection ~ 4600 4350
Wire Wire Line
	5050 2850 4800 2850
Wire Wire Line
	4800 2850 4800 4550
Wire Wire Line
	4800 4550 5050 4550
Wire Wire Line
	4550 2600 5450 2600
Wire Wire Line
	5450 2600 5450 2650
Connection ~ 5450 2650
Wire Wire Line
	4500 3550 4800 3550
Connection ~ 4800 3550
$Comp
L mosfet_p M4
U 1 1 683753B5
P 3100 2050
F 0 "M4" H 3050 2100 50  0000 R CNN
F 1 "mosfet_p" H 3150 2200 50  0000 R CNN
F 2 "" H 3350 2150 29  0000 C CNN
F 3 "" H 3150 2050 60  0000 C CNN
	1    3100 2050
	1    0    0    1   
$EndComp
$Comp
L mosfet_n M3
U 1 1 68375452
P 3050 2450
F 0 "M3" H 3050 2300 50  0000 R CNN
F 1 "mosfet_n" H 3150 2400 50  0000 R CNN
F 2 "" H 3350 2150 29  0000 C CNN
F 3 "" H 3150 2250 60  0000 C CNN
	1    3050 2450
	1    0    0    -1  
$EndComp
Wire Wire Line
	3250 1800 3250 1850
Wire Wire Line
	3250 1800 4700 1800
Wire Wire Line
	4700 1800 4700 2600
Connection ~ 4700 2600
Wire Wire Line
	3350 1900 3350 1800
Connection ~ 3350 1800
Wire Wire Line
	3250 2250 3250 2450
Wire Wire Line
	3250 2850 3250 4800
Wire Wire Line
	3350 2800 3350 3050
Wire Wire Line
	3350 3050 3250 3050
Connection ~ 3250 3050
Wire Wire Line
	2950 2050 2950 2650
Connection ~ 2950 2350
Wire Wire Line
	2650 2350 2650 3500
Wire Wire Line
	2650 3500 3750 3500
Wire Wire Line
	3750 3500 3750 3700
Wire Wire Line
	3750 3700 5050 3700
Wire Wire Line
	5050 3700 5050 4000
Connection ~ 2650 2350
Wire Wire Line
	3250 2350 4850 2350
Wire Wire Line
	4850 2350 4850 3400
Wire Wire Line
	4850 3400 5050 3400
Connection ~ 3250 2350
Connection ~ 5350 3700
Wire Wire Line
	2450 2350 2950 2350
Wire Wire Line
	4200 3600 2350 3600
Connection ~ 4600 4800
Wire Wire Line
	4950 4800 4950 5050
Wire Wire Line
	4950 5050 2850 5050
Wire Wire Line
	2850 5050 2850 3800
Wire Wire Line
	2850 3800 2350 3800
Wire Wire Line
	3750 1800 3750 1700
Wire Wire Line
	3750 1700 2500 1700
Connection ~ 3750 1800
Wire Wire Line
	5350 3700 6000 3700
$Comp
L PORT U1
U 3 1 6837F170
P 2250 1700
F 0 "U1" H 2300 1800 30  0000 C CNN
F 1 "PORT" H 2250 1700 30  0000 C CNN
F 2 "" H 2250 1700 60  0000 C CNN
F 3 "" H 2250 1700 60  0000 C CNN
	3    2250 1700
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 1 1 6837F1DD
P 2100 3600
F 0 "U1" H 2150 3700 30  0000 C CNN
F 1 "PORT" H 2100 3600 30  0000 C CNN
F 2 "" H 2100 3600 60  0000 C CNN
F 3 "" H 2100 3600 60  0000 C CNN
	1    2100 3600
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 4 1 6837F228
P 2100 3800
F 0 "U1" H 2150 3900 30  0000 C CNN
F 1 "PORT" H 2100 3800 30  0000 C CNN
F 2 "" H 2100 3800 60  0000 C CNN
F 3 "" H 2100 3800 60  0000 C CNN
	4    2100 3800
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 2 1 6837F257
P 2200 2350
F 0 "U1" H 2250 2450 30  0000 C CNN
F 1 "PORT" H 2200 2350 30  0000 C CNN
F 2 "" H 2200 2350 60  0000 C CNN
F 3 "" H 2200 2350 60  0000 C CNN
	2    2200 2350
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 5 1 6837F284
P 6250 3700
F 0 "U1" H 6300 3800 30  0000 C CNN
F 1 "PORT" H 6250 3700 30  0000 C CNN
F 2 "" H 6250 3700 60  0000 C CNN
F 3 "" H 6250 3700 60  0000 C CNN
	5    6250 3700
	-1   0    0    1   
$EndComp
$EndSCHEMATC
