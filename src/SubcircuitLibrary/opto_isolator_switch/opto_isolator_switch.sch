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
LIBS:opto_isolator_switch-cache
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
L eSim_R R1
U 1 1 5D0B5974
P 4350 3450
F 0 "R1" H 4400 3580 50  0000 C CNN
F 1 "1000" H 4400 3500 50  0000 C CNN
F 2 "" H 4400 3430 30  0000 C CNN
F 3 "" V 4400 3500 30  0000 C CNN
	1    4350 3450
	1    0    0    -1  
$EndComp
$Comp
L CCCS F1
U 1 1 5D0B59A2
P 5200 3450
F 0 "F1" H 5200 3600 50  0000 C CNN
F 1 "3" H 5000 3400 50  0000 C CNN
F 2 "" H 5200 3450 60  0000 C CNN
F 3 "" H 5200 3450 60  0000 C CNN
	1    5200 3450
	0    1    1    0   
$EndComp
$Comp
L eSim_R R2
U 1 1 5D0B59D5
P 5200 4050
F 0 "R2" H 5250 4180 50  0000 C CNN
F 1 "1000" H 5250 4100 50  0000 C CNN
F 2 "" H 5250 4030 30  0000 C CNN
F 3 "" V 5250 4100 30  0000 C CNN
	1    5200 4050
	0    1    1    0   
$EndComp
Wire Wire Line
	4550 3400 5000 3400
Wire Wire Line
	5000 3500 4750 3500
Wire Wire Line
	4750 3500 4750 3700
Wire Wire Line
	5250 3950 5250 3750
Wire Wire Line
	5250 3150 5250 3000
Wire Wire Line
	5250 3000 5650 3000
Wire Wire Line
	5650 3000 5650 3350
Wire Wire Line
	5650 3350 5700 3350
Wire Wire Line
	5250 4250 5250 4350
Wire Wire Line
	4250 3400 4000 3400
$Comp
L PORT U1
U 1 1 5D0B5AC7
P 3750 3400
F 0 "U1" H 3800 3500 30  0000 C CNN
F 1 "PORT" H 3750 3400 30  0000 C CNN
F 2 "" H 3750 3400 60  0000 C CNN
F 3 "" H 3750 3400 60  0000 C CNN
	1    3750 3400
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 2 1 5D0B5B16
P 4750 3950
F 0 "U1" H 4800 4050 30  0000 C CNN
F 1 "PORT" H 4750 3950 30  0000 C CNN
F 2 "" H 4750 3950 60  0000 C CNN
F 3 "" H 4750 3950 60  0000 C CNN
	2    4750 3950
	0    -1   -1   0   
$EndComp
$Comp
L PORT U1
U 4 1 5D0B5B84
P 6050 3800
F 0 "U1" H 6100 3900 30  0000 C CNN
F 1 "PORT" H 6050 3800 30  0000 C CNN
F 2 "" H 6050 3800 60  0000 C CNN
F 3 "" H 6050 3800 60  0000 C CNN
	4    6050 3800
	-1   0    0    1   
$EndComp
$Comp
L PORT U1
U 3 1 5D0B5BF0
P 5950 3350
F 0 "U1" H 6000 3450 30  0000 C CNN
F 1 "PORT" H 5950 3350 30  0000 C CNN
F 2 "" H 5950 3350 60  0000 C CNN
F 3 "" H 5950 3350 60  0000 C CNN
	3    5950 3350
	-1   0    0    1   
$EndComp
$Comp
L eSim_C C1
U 1 1 5D0B5EB6
P 5500 3350
F 0 "C1" H 5525 3450 50  0000 L CNN
F 1 "14n" H 5525 3250 50  0000 L CNN
F 2 "" H 5538 3200 30  0000 C CNN
F 3 "" H 5500 3350 60  0000 C CNN
	1    5500 3350
	1    0    0    -1  
$EndComp
Wire Wire Line
	5500 3200 5500 3000
Connection ~ 5500 3000
Wire Wire Line
	5500 3500 5500 3800
Wire Wire Line
	5250 3800 5800 3800
Connection ~ 5250 3800
Connection ~ 5500 3800
Wire Wire Line
	5250 4350 4900 4350
Wire Wire Line
	4900 4350 4900 3500
Connection ~ 4900 3500
$EndSCHEMATC
