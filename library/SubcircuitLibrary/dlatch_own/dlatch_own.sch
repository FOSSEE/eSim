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
U 1 1 6856B545
P 4350 3350
F 0 "U3" H 4350 3350 60  0000 C CNN
F 1 "d_and" H 4400 3450 60  0000 C CNN
F 2 "" H 4350 3350 60  0000 C CNN
F 3 "" H 4350 3350 60  0000 C CNN
	1    4350 3350
	1    0    0    -1  
$EndComp
$Comp
L d_and U4
U 1 1 6856B5D2
P 4400 4750
F 0 "U4" H 4400 4750 60  0000 C CNN
F 1 "d_and" H 4450 4850 60  0000 C CNN
F 2 "" H 4400 4750 60  0000 C CNN
F 3 "" H 4400 4750 60  0000 C CNN
	1    4400 4750
	1    0    0    -1  
$EndComp
$Comp
L d_nor U5
U 1 1 6856B5DC
P 7300 3350
F 0 "U5" H 7300 3350 60  0000 C CNN
F 1 "d_nor" H 7350 3450 60  0000 C CNN
F 2 "" H 7300 3350 60  0000 C CNN
F 3 "" H 7300 3350 60  0000 C CNN
	1    7300 3350
	1    0    0    -1  
$EndComp
$Comp
L d_nor U6
U 1 1 6856B689
P 7300 4750
F 0 "U6" H 7300 4750 60  0000 C CNN
F 1 "d_nor" H 7350 4850 60  0000 C CNN
F 2 "" H 7300 4750 60  0000 C CNN
F 3 "" H 7300 4750 60  0000 C CNN
	1    7300 4750
	1    0    0    -1  
$EndComp
$Comp
L d_inverter U1
U 1 1 6856B986
P 2800 3250
F 0 "U1" H 2800 3150 60  0000 C CNN
F 1 "d_inverter" H 2800 3400 60  0000 C CNN
F 2 "" H 2850 3200 60  0000 C CNN
F 3 "" H 2850 3200 60  0000 C CNN
	1    2800 3250
	1    0    0    -1  
$EndComp
Wire Wire Line
	7750 3300 8750 3300
Wire Wire Line
	7750 4700 9050 4700
Wire Wire Line
	6850 4650 6500 4650
Wire Wire Line
	6500 4650 6500 4300
Wire Wire Line
	6500 4300 8400 4300
Wire Wire Line
	8400 4300 8400 3300
Connection ~ 8400 3300
Wire Wire Line
	8250 4700 8250 3800
Wire Wire Line
	8250 3800 6600 3800
Wire Wire Line
	6600 3800 6600 3350
Wire Wire Line
	6600 3350 6850 3350
Connection ~ 8250 4700
Wire Wire Line
	5150 4700 5150 4750
Wire Wire Line
	5150 4750 6850 4750
Wire Wire Line
	4850 4700 5150 4700
Wire Wire Line
	4800 3300 6400 3300
Wire Wire Line
	6400 3300 6400 3250
Wire Wire Line
	6400 3250 6850 3250
Wire Wire Line
	3900 3350 3450 3350
Wire Wire Line
	3450 3350 3450 4650
Wire Wire Line
	3450 4650 3950 4650
Wire Wire Line
	3950 4750 2500 4750
Wire Wire Line
	3100 3250 3900 3250
Wire Wire Line
	2500 3250 2500 4150
Wire Wire Line
	2500 4150 2800 4150
Wire Wire Line
	2800 4150 2800 4750
Connection ~ 2800 4750
Wire Wire Line
	3450 3950 3200 3950
Connection ~ 3450 3950
$Comp
L PORT U2
U 1 1 6856BAF3
P 2250 4750
F 0 "U2" H 2300 4850 30  0000 C CNN
F 1 "PORT" H 2250 4750 30  0000 C CNN
F 2 "" H 2250 4750 60  0000 C CNN
F 3 "" H 2250 4750 60  0000 C CNN
	1    2250 4750
	1    0    0    -1  
$EndComp
$Comp
L PORT U2
U 3 1 6856BB14
P 9300 4700
F 0 "U2" H 9350 4800 30  0000 C CNN
F 1 "PORT" H 9300 4700 30  0000 C CNN
F 2 "" H 9300 4700 60  0000 C CNN
F 3 "" H 9300 4700 60  0000 C CNN
	3    9300 4700
	-1   0    0    1   
$EndComp
$Comp
L PORT U2
U 2 1 6856BB59
P 2950 3950
F 0 "U2" H 3000 4050 30  0000 C CNN
F 1 "PORT" H 2950 3950 30  0000 C CNN
F 2 "" H 2950 3950 60  0000 C CNN
F 3 "" H 2950 3950 60  0000 C CNN
	2    2950 3950
	1    0    0    -1  
$EndComp
$Comp
L PORT U2
U 4 1 6856BB9A
P 9000 3300
F 0 "U2" H 9050 3400 30  0000 C CNN
F 1 "PORT" H 9000 3300 30  0000 C CNN
F 2 "" H 9000 3300 60  0000 C CNN
F 3 "" H 9000 3300 60  0000 C CNN
	4    9000 3300
	-1   0    0    1   
$EndComp
$EndSCHEMATC
