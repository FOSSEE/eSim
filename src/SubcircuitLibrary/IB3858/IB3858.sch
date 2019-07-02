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
LIBS:speaker-cache
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
U 1 1 5D10AD49
P 6050 3150
F 0 "R1" H 6100 3280 50  0000 C CNN
F 1 "5.2" H 6100 3200 50  0000 C CNN
F 2 "" H 6100 3130 30  0000 C CNN
F 3 "" V 6100 3200 30  0000 C CNN
	1    6050 3150
	1    0    0    -1  
$EndComp
$Comp
L eSim_L L1
U 1 1 5D10AD4A
P 4800 3650
F 0 "L1" H 6750 4150 50  0000 C CNN
F 1 "3.08m" H 6750 4300 50  0000 C CNN
F 2 "" V 6750 4200 60  0000 C CNN
F 3 "" V 6750 4200 60  0000 C CNN
	1    4800 3650
	1    0    0    -1  
$EndComp
$Comp
L eSim_L L2
U 1 1 5D10AD4B
P 7300 1750
F 0 "L2" H 9250 2250 50  0000 C CNN
F 1 "61.100458m" H 9250 2400 50  0000 C CNN
F 2 "" V 9250 2300 60  0000 C CNN
F 3 "" V 9250 2300 60  0000 C CNN
	1    7300 1750
	0    1    1    0   
$EndComp
$Comp
L eSim_C C1
U 1 1 5D10AD4C
P 7350 3700
F 0 "C1" H 7375 3800 50  0000 L CNN
F 1 "896.8481u" H 7375 3600 50  0000 L CNN
F 2 "" H 7388 3550 30  0000 C CNN
F 3 "" H 7350 3700 60  0000 C CNN
	1    7350 3700
	1    0    0    -1  
$EndComp
$Comp
L eSim_R R2
U 1 1 5D10AD4D
P 8450 3700
F 0 "R2" H 8500 3830 50  0000 C CNN
F 1 "73.6254" H 8500 3750 50  0000 C CNN
F 2 "" H 8500 3680 30  0000 C CNN
F 3 "" V 8500 3750 30  0000 C CNN
	1    8450 3700
	0    1    1    0   
$EndComp
Wire Wire Line
	7350 3850 7350 4350
Connection ~ 7850 4350
Wire Wire Line
	7850 4000 7850 4350
Wire Wire Line
	8500 4350 8500 3900
Connection ~ 7850 3100
Wire Wire Line
	8500 3100 8500 3600
Connection ~ 7350 3100
Wire Wire Line
	7850 3100 7850 3400
Wire Wire Line
	7350 3100 7350 3550
Wire Wire Line
	7050 3100 8500 3100
Wire Wire Line
	6250 3100 6450 3100
Wire Wire Line
	7050 4350 8500 4350
$Comp
L PORT U1
U 1 1 5D10B0D2
P 5250 3100
F 0 "U1" H 5300 3200 30  0000 C CNN
F 1 "PORT" H 5250 3100 30  0000 C CNN
F 2 "" H 5250 3100 60  0000 C CNN
F 3 "" H 5250 3100 60  0000 C CNN
	1    5250 3100
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 2 1 5D10B10F
P 6800 4350
F 0 "U1" H 6850 4450 30  0000 C CNN
F 1 "PORT" H 6800 4350 30  0000 C CNN
F 2 "" H 6800 4350 60  0000 C CNN
F 3 "" H 6800 4350 60  0000 C CNN
	2    6800 4350
	1    0    0    -1  
$EndComp
Wire Wire Line
	5950 3100 5500 3100
Connection ~ 7350 4350
$EndSCHEMATC
