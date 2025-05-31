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
LIBS:d_origin-cache
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
U 1 1 67F4E50B
P 3100 1300
F 0 "U1" H 3150 1400 30  0000 C CNN
F 1 "PORT" H 3100 1300 30  0000 C CNN
F 2 "" H 3100 1300 60  0000 C CNN
F 3 "" H 3100 1300 60  0000 C CNN
	1    3100 1300
	0    -1   1    0   
$EndComp
$Comp
L PORT U1
U 2 1 67F4E50C
P 3850 1300
F 0 "U1" H 3900 1400 30  0000 C CNN
F 1 "PORT" H 3850 1300 30  0000 C CNN
F 2 "" H 3850 1300 60  0000 C CNN
F 3 "" H 3850 1300 60  0000 C CNN
	2    3850 1300
	0    -1   1    0   
$EndComp
$Comp
L PORT U1
U 3 1 67F4E50D
P 4450 1300
F 0 "U1" H 4500 1400 30  0000 C CNN
F 1 "PORT" H 4450 1300 30  0000 C CNN
F 2 "" H 4450 1300 60  0000 C CNN
F 3 "" H 4450 1300 60  0000 C CNN
	3    4450 1300
	0    -1   1    0   
$EndComp
Text Label 3100 1700 3    60   ~ 0
x
Text Label 3850 1700 3    60   ~ 0
y
Text Label 4450 1700 3    60   ~ 0
z
$Comp
L d_inverter U2
U 1 1 67F4E50F
P 3450 2450
F 0 "U2" H 3450 2350 60  0000 C CNN
F 1 "d_inverter" H 3450 2600 60  0000 C CNN
F 2 "" H 3500 2400 60  0000 C CNN
F 3 "" H 3500 2400 60  0000 C CNN
	1    3450 2450
	0    1    1    0   
$EndComp
$Comp
L d_inverter U3
U 1 1 67F4E510
P 4100 2400
F 0 "U3" H 4100 2300 60  0000 C CNN
F 1 "d_inverter" H 4100 2550 60  0000 C CNN
F 2 "" H 4150 2350 60  0000 C CNN
F 3 "" H 4150 2350 60  0000 C CNN
	1    4100 2400
	0    1    1    0   
$EndComp
$Comp
L d_inverter U4
U 1 1 67F4E511
P 4800 2300
F 0 "U4" H 4800 2200 60  0000 C CNN
F 1 "d_inverter" H 4800 2450 60  0000 C CNN
F 2 "" H 4850 2250 60  0000 C CNN
F 3 "" H 4850 2250 60  0000 C CNN
	1    4800 2300
	0    1    1    0   
$EndComp
$Comp
L 4_OR X2
U 1 1 67F4E512
P 7050 3400
F 0 "X2" H 7200 3300 60  0000 C CNN
F 1 "4_OR" H 7200 3500 60  0000 C CNN
F 2 "" H 7050 3400 60  0000 C CNN
F 3 "" H 7050 3400 60  0000 C CNN
	1    7050 3400
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 4 1 67F4E513
P 8250 3400
F 0 "U1" H 8300 3500 30  0000 C CNN
F 1 "PORT" H 8250 3400 30  0000 C CNN
F 2 "" H 8250 3400 60  0000 C CNN
F 3 "" H 8250 3400 60  0000 C CNN
	4    8250 3400
	-1   0    0    1   
$EndComp
$Comp
L d_and U5
U 1 1 67F4E754
P 5650 3000
F 0 "U5" H 5650 3000 60  0000 C CNN
F 1 "d_and" H 5700 3100 60  0000 C CNN
F 2 "" H 5650 3000 60  0000 C CNN
F 3 "" H 5650 3000 60  0000 C CNN
	1    5650 3000
	1    0    0    -1  
$EndComp
$Comp
L d_and U6
U 1 1 67F4E7A8
P 5650 3300
F 0 "U6" H 5650 3300 60  0000 C CNN
F 1 "d_and" H 5700 3400 60  0000 C CNN
F 2 "" H 5650 3300 60  0000 C CNN
F 3 "" H 5650 3300 60  0000 C CNN
	1    5650 3300
	1    0    0    -1  
$EndComp
$Comp
L d_and U7
U 1 1 67F4E7E1
P 5700 3600
F 0 "U7" H 5700 3600 60  0000 C CNN
F 1 "d_and" H 5750 3700 60  0000 C CNN
F 2 "" H 5700 3600 60  0000 C CNN
F 3 "" H 5700 3600 60  0000 C CNN
	1    5700 3600
	1    0    0    -1  
$EndComp
$Comp
L 3_and X1
U 1 1 67F4E85E
P 5550 4050
F 0 "X1" H 5650 4000 60  0000 C CNN
F 1 "3_and" H 5700 4200 60  0000 C CNN
F 2 "" H 5550 4050 60  0000 C CNN
F 3 "" H 5550 4050 60  0000 C CNN
	1    5550 4050
	1    0    0    -1  
$EndComp
Wire Wire Line
	3100 2100 3450 2100
Wire Wire Line
	3450 2100 3450 2150
Connection ~ 3100 2100
Wire Wire Line
	4100 2050 3850 2050
Wire Wire Line
	3850 2050 3850 2100
Connection ~ 3850 2100
Wire Wire Line
	4100 2050 4100 2100
Wire Wire Line
	4800 1950 4450 1950
Connection ~ 4450 1950
Wire Wire Line
	4800 1950 4800 2000
Wire Wire Line
	7600 3400 8000 3400
Wire Wire Line
	3100 1550 3100 3900
Wire Wire Line
	3450 2900 5200 2900
Connection ~ 3450 2900
Wire Wire Line
	4800 3000 5200 3000
Connection ~ 4800 3000
Wire Wire Line
	3450 3200 5200 3200
Connection ~ 3450 3200
Wire Wire Line
	3850 3300 5200 3300
Connection ~ 3850 3300
Wire Wire Line
	3850 3500 5250 3500
Connection ~ 3850 3500
Wire Wire Line
	4800 3600 5250 3600
Connection ~ 4800 3600
Wire Wire Line
	3100 3900 5200 3900
Wire Wire Line
	4100 4000 5200 4000
Connection ~ 4100 4000
Wire Wire Line
	4450 4100 5200 4100
Connection ~ 4450 4100
Wire Wire Line
	4450 4100 4450 1550
Wire Wire Line
	4100 4000 4100 2700
Wire Wire Line
	4800 3600 4800 2600
Wire Wire Line
	3850 1550 3850 3500
Wire Wire Line
	3450 2750 3450 3200
Wire Wire Line
	6100 2950 6700 2950
Wire Wire Line
	6700 2950 6700 3250
Wire Wire Line
	6100 3250 6550 3250
Wire Wire Line
	6550 3250 6550 3350
Wire Wire Line
	6550 3350 6700 3350
Wire Wire Line
	6150 3550 6150 3450
Wire Wire Line
	6150 3450 6700 3450
Wire Wire Line
	6050 4000 6700 4000
Wire Wire Line
	6700 4000 6700 3550
$EndSCHEMATC
