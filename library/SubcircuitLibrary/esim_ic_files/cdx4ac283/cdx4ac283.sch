EESchema Schematic File Version 2
LIBS:4_bit_FA-rescue
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
LIBS:4_bit_FA-cache
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
Wire Wire Line
	3500 2050 5100 2050
Wire Wire Line
	5100 2050 5100 2800
Wire Wire Line
	3500 2350 5000 2350
Wire Wire Line
	5000 2350 5000 2900
Wire Wire Line
	5000 2900 5100 2900
Wire Wire Line
	3500 2650 4900 2650
Wire Wire Line
	4900 2650 4900 3000
Wire Wire Line
	4900 3000 5100 3000
Wire Wire Line
	3500 2950 4800 2950
Wire Wire Line
	4800 2950 4800 3100
Wire Wire Line
	4800 3100 5100 3100
Wire Wire Line
	3500 3250 5100 3250
Wire Wire Line
	5100 3250 5100 3200
Wire Wire Line
	3500 3550 3850 3550
Wire Wire Line
	3850 3550 3850 3350
Wire Wire Line
	3850 3350 5100 3350
Wire Wire Line
	3500 3850 3900 3850
Wire Wire Line
	3900 3850 3900 3450
Wire Wire Line
	3900 3450 5100 3450
Wire Wire Line
	3500 4150 3950 4150
Wire Wire Line
	3950 4150 3950 3550
Wire Wire Line
	3950 3550 5100 3550
Wire Wire Line
	3500 4450 4000 4450
Wire Wire Line
	4000 4450 4000 3650
Wire Wire Line
	4000 3650 5100 3650
$Comp
L GND #PWR01
U 1 1 67F3FF9A
P 1600 3450
F 0 "#PWR01" H 1600 3200 50  0001 C CNN
F 1 "GND" H 1600 3300 50  0000 C CNN
F 2 "" H 1600 3450 50  0001 C CNN
F 3 "" H 1600 3450 50  0001 C CNN
	1    1600 3450
	1    0    0    -1  
$EndComp
Wire Wire Line
	2600 2050 1600 2050
Wire Wire Line
	1600 2050 1600 3450
Wire Wire Line
	2600 2350 1600 2350
Connection ~ 1600 2350
Wire Wire Line
	2600 2650 1600 2650
Connection ~ 1600 2650
Wire Wire Line
	2600 2950 1600 2950
Connection ~ 1600 2950
Wire Wire Line
	2600 3250 1600 3250
Connection ~ 1600 3250
Wire Wire Line
	2600 3550 1800 3550
Wire Wire Line
	1800 3250 1800 4450
Connection ~ 1800 3250
Wire Wire Line
	1800 3850 2600 3850
Connection ~ 1800 3550
Wire Wire Line
	1800 4150 2600 4150
Connection ~ 1800 3850
Wire Wire Line
	1800 4450 2600 4450
Connection ~ 1800 4150
$Comp
L plot_v1 U2
U 1 1 67F401B5
P 3650 2100
F 0 "U2" H 3650 2600 60  0000 C CNN
F 1 "plot_v1" H 3850 2450 60  0000 C CNN
F 2 "" H 3650 2100 60  0000 C CNN
F 3 "" H 3650 2100 60  0000 C CNN
	1    3650 2100
	1    0    0    -1  
$EndComp
Wire Wire Line
	3650 1900 3650 2050
Connection ~ 3650 2050
$Comp
L plot_v1 U3
U 1 1 67F403E7
P 3850 2400
F 0 "U3" H 3850 2900 60  0000 C CNN
F 1 "plot_v1" H 4050 2750 60  0000 C CNN
F 2 "" H 3850 2400 60  0000 C CNN
F 3 "" H 3850 2400 60  0000 C CNN
	1    3850 2400
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U4
U 1 1 67F40422
P 4100 2650
F 0 "U4" H 4100 3150 60  0000 C CNN
F 1 "plot_v1" H 4300 3000 60  0000 C CNN
F 2 "" H 4100 2650 60  0000 C CNN
F 3 "" H 4100 2650 60  0000 C CNN
	1    4100 2650
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U5
U 1 1 67F4046B
P 4300 3000
F 0 "U5" H 4300 3500 60  0000 C CNN
F 1 "plot_v1" H 4500 3350 60  0000 C CNN
F 2 "" H 4300 3000 60  0000 C CNN
F 3 "" H 4300 3000 60  0000 C CNN
	1    4300 3000
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U7
U 1 1 67F404AA
P 4550 3350
F 0 "U7" H 4550 3850 60  0000 C CNN
F 1 "plot_v1" H 4750 3700 60  0000 C CNN
F 2 "" H 4550 3350 60  0000 C CNN
F 3 "" H 4550 3350 60  0000 C CNN
	1    4550 3350
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U1
U 1 1 67F404E7
P 3600 3550
F 0 "U1" H 3600 4050 60  0000 C CNN
F 1 "plot_v1" H 3800 3900 60  0000 C CNN
F 2 "" H 3600 3550 60  0000 C CNN
F 3 "" H 3600 3550 60  0000 C CNN
	1    3600 3550
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U6
U 1 1 67F405AC
P 4400 4600
F 0 "U6" H 4400 5100 60  0000 C CNN
F 1 "plot_v1" H 4600 4950 60  0000 C CNN
F 2 "" H 4400 4600 60  0000 C CNN
F 3 "" H 4400 4600 60  0000 C CNN
	1    4400 4600
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U8
U 1 1 67F405F7
P 4850 4700
F 0 "U8" H 4850 5200 60  0000 C CNN
F 1 "plot_v1" H 5050 5050 60  0000 C CNN
F 2 "" H 4850 4700 60  0000 C CNN
F 3 "" H 4850 4700 60  0000 C CNN
	1    4850 4700
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U9
U 1 1 67F4064A
P 5400 4750
F 0 "U9" H 5400 5250 60  0000 C CNN
F 1 "plot_v1" H 5600 5100 60  0000 C CNN
F 2 "" H 5400 4750 60  0000 C CNN
F 3 "" H 5400 4750 60  0000 C CNN
	1    5400 4750
	1    0    0    -1  
$EndComp
Wire Wire Line
	3850 2200 3850 2350
Connection ~ 3850 2350
Wire Wire Line
	4100 2450 4100 2650
Connection ~ 4100 2650
Wire Wire Line
	4300 2800 4300 2950
Connection ~ 4300 2950
Wire Wire Line
	4550 3150 4550 3250
Connection ~ 4550 3250
Wire Wire Line
	3600 3350 3600 3550
Connection ~ 3600 3550
Wire Wire Line
	4400 4400 4000 4400
Connection ~ 4000 4400
Wire Wire Line
	4850 4500 3850 4500
Wire Wire Line
	3850 4500 3850 4150
Connection ~ 3850 4150
Wire Wire Line
	5400 4550 5400 4650
Wire Wire Line
	5400 4650 3700 4650
Wire Wire Line
	3700 4650 3700 3850
Connection ~ 3700 3850
Text GLabel 3450 1800 0    60   Input ~ 0
C0
Wire Wire Line
	3450 1800 3550 1800
Wire Wire Line
	3550 1800 3550 2000
Wire Wire Line
	3550 2000 3650 2000
Connection ~ 3650 2000
Text GLabel 3650 2200 0    60   Input ~ 0
A1
Wire Wire Line
	3650 2200 3800 2200
Wire Wire Line
	3800 2200 3800 2300
Wire Wire Line
	3800 2300 3850 2300
Connection ~ 3850 2300
Text GLabel 3850 2500 0    60   Input ~ 0
A2
Wire Wire Line
	3850 2500 3950 2500
Wire Wire Line
	3950 2500 3950 2600
Wire Wire Line
	3950 2600 4100 2600
Connection ~ 4100 2600
Text GLabel 3900 2800 0    60   Input ~ 0
A3
Wire Wire Line
	3900 2800 4100 2800
Wire Wire Line
	4100 2800 4100 2900
Wire Wire Line
	4100 2900 4300 2900
Connection ~ 4300 2900
Text GLabel 4150 3100 0    60   Input ~ 0
A4
Wire Wire Line
	4150 3100 4350 3100
Wire Wire Line
	4350 3100 4350 3200
Wire Wire Line
	4350 3200 4550 3200
Connection ~ 4550 3200
Text GLabel 3450 3400 0    60   Input ~ 0
B1
Wire Wire Line
	3450 3400 3450 3500
Wire Wire Line
	3450 3500 3600 3500
Connection ~ 3600 3500
Text GLabel 4300 4850 0    60   Input ~ 0
B2
Wire Wire Line
	4300 4850 4400 4850
Wire Wire Line
	4400 4850 4400 4650
Connection ~ 4400 4650
Text GLabel 3900 4800 0    60   Input ~ 0
B3
Wire Wire Line
	3900 4800 4050 4800
Wire Wire Line
	4050 4800 4050 4500
Connection ~ 4050 4500
Text GLabel 4100 4150 0    60   Input ~ 0
B4
Wire Wire Line
	4100 4150 4150 4150
Wire Wire Line
	4150 4150 4150 4400
Connection ~ 4150 4400
$Comp
L plot_v1 U10
U 1 1 67F40F19
P 6800 3250
F 0 "U10" H 6800 3750 60  0000 C CNN
F 1 "plot_v1" H 7000 3600 60  0000 C CNN
F 2 "" H 6800 3250 60  0000 C CNN
F 3 "" H 6800 3250 60  0000 C CNN
	1    6800 3250
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U11
U 1 1 67F40F66
P 7250 3250
F 0 "U11" H 7250 3750 60  0000 C CNN
F 1 "plot_v1" H 7450 3600 60  0000 C CNN
F 2 "" H 7250 3250 60  0000 C CNN
F 3 "" H 7250 3250 60  0000 C CNN
	1    7250 3250
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U12
U 1 1 67F40FB3
P 7700 3250
F 0 "U12" H 7700 3750 60  0000 C CNN
F 1 "plot_v1" H 7900 3600 60  0000 C CNN
F 2 "" H 7700 3250 60  0000 C CNN
F 3 "" H 7700 3250 60  0000 C CNN
	1    7700 3250
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U13
U 1 1 67F41000
P 8100 3250
F 0 "U13" H 8100 3750 60  0000 C CNN
F 1 "plot_v1" H 8300 3600 60  0000 C CNN
F 2 "" H 8100 3250 60  0000 C CNN
F 3 "" H 8100 3250 60  0000 C CNN
	1    8100 3250
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U14
U 1 1 67F4104F
P 8500 3250
F 0 "U14" H 8500 3750 60  0000 C CNN
F 1 "plot_v1" H 8700 3600 60  0000 C CNN
F 2 "" H 8500 3250 60  0000 C CNN
F 3 "" H 8500 3250 60  0000 C CNN
	1    8500 3250
	1    0    0    -1  
$EndComp
Wire Wire Line
	6800 3050 6300 3050
Wire Wire Line
	7250 3050 7250 3150
Wire Wire Line
	7250 3150 6300 3150
Wire Wire Line
	7700 3050 7700 3250
Wire Wire Line
	7700 3250 6300 3250
Wire Wire Line
	8100 3050 8100 3350
Wire Wire Line
	8100 3350 6300 3350
Wire Wire Line
	8500 3050 8500 3500
Wire Wire Line
	8500 3500 6300 3500
Text GLabel 6500 2950 0    60   Input ~ 0
S1
Wire Wire Line
	6500 2950 6550 2950
Wire Wire Line
	6550 2950 6550 3050
Connection ~ 6550 3050
Text GLabel 6400 2600 0    60   Input ~ 0
S2
Wire Wire Line
	6400 2600 6600 2600
Wire Wire Line
	6600 2600 6600 3150
Connection ~ 6600 3150
Text GLabel 6400 2350 0    60   Input ~ 0
S3
Wire Wire Line
	6400 2350 6650 2350
Wire Wire Line
	6650 2350 6650 3250
Connection ~ 6650 3250
Text GLabel 6400 2100 0    60   Input ~ 0
S4
Wire Wire Line
	6400 2100 6700 2100
Wire Wire Line
	6700 2100 6700 3350
Connection ~ 6700 3350
Text GLabel 6850 3600 0    60   Input ~ 0
C_out
Wire Wire Line
	6850 3600 7000 3600
Wire Wire Line
	7000 3600 7000 3500
Connection ~ 7000 3500
$Comp
L 283 X1
U 1 1 67F4018C
P 6100 4100
F 0 "X1" H 5700 4200 60  0000 C CNN
F 1 "283" H 5750 5600 60  0000 C CNN
F 2 "" H 5750 5600 60  0001 C CNN
F 3 "" H 5750 5600 60  0001 C CNN
	1    6100 4100
	1    0    0    -1  
$EndComp
$Comp
L pulse v1
U 1 1 67F4A87C
P 3050 2050
F 0 "v1" H 2850 2150 60  0000 C CNN
F 1 "pulse" H 2850 2000 60  0000 C CNN
F 2 "R1" H 2750 2050 60  0000 C CNN
F 3 "" H 3050 2050 60  0000 C CNN
	1    3050 2050
	0    1    1    0   
$EndComp
$Comp
L pulse v2
U 1 1 67F4A8DB
P 3050 2350
F 0 "v2" H 2850 2450 60  0000 C CNN
F 1 "pulse" H 2850 2300 60  0000 C CNN
F 2 "R1" H 2750 2350 60  0000 C CNN
F 3 "" H 3050 2350 60  0000 C CNN
	1    3050 2350
	0    1    1    0   
$EndComp
$Comp
L pulse v3
U 1 1 67F4A950
P 3050 2650
F 0 "v3" H 2850 2750 60  0000 C CNN
F 1 "pulse" H 2850 2600 60  0000 C CNN
F 2 "R1" H 2750 2650 60  0000 C CNN
F 3 "" H 3050 2650 60  0000 C CNN
	1    3050 2650
	0    1    1    0   
$EndComp
$Comp
L pulse v4
U 1 1 67F4A956
P 3050 2950
F 0 "v4" H 2850 3050 60  0000 C CNN
F 1 "pulse" H 2850 2900 60  0000 C CNN
F 2 "R1" H 2750 2950 60  0000 C CNN
F 3 "" H 3050 2950 60  0000 C CNN
	1    3050 2950
	0    1    1    0   
$EndComp
$Comp
L pulse v5
U 1 1 67F4A9E6
P 3050 3250
F 0 "v5" H 2850 3350 60  0000 C CNN
F 1 "pulse" H 2850 3200 60  0000 C CNN
F 2 "R1" H 2750 3250 60  0000 C CNN
F 3 "" H 3050 3250 60  0000 C CNN
	1    3050 3250
	0    1    1    0   
$EndComp
$Comp
L pulse v6
U 1 1 67F4A9EC
P 3050 3550
F 0 "v6" H 2850 3650 60  0000 C CNN
F 1 "pulse" H 2850 3500 60  0000 C CNN
F 2 "R1" H 2750 3550 60  0000 C CNN
F 3 "" H 3050 3550 60  0000 C CNN
	1    3050 3550
	0    1    1    0   
$EndComp
$Comp
L pulse v7
U 1 1 67F4A9F2
P 3050 3850
F 0 "v7" H 2850 3950 60  0000 C CNN
F 1 "pulse" H 2850 3800 60  0000 C CNN
F 2 "R1" H 2750 3850 60  0000 C CNN
F 3 "" H 3050 3850 60  0000 C CNN
	1    3050 3850
	0    1    1    0   
$EndComp
$Comp
L pulse v8
U 1 1 67F4A9F8
P 3050 4150
F 0 "v8" H 2850 4250 60  0000 C CNN
F 1 "pulse" H 2850 4100 60  0000 C CNN
F 2 "R1" H 2750 4150 60  0000 C CNN
F 3 "" H 3050 4150 60  0000 C CNN
	1    3050 4150
	0    1    1    0   
$EndComp
$Comp
L pulse v9
U 1 1 67F4AA2C
P 3050 4450
F 0 "v9" H 2850 4550 60  0000 C CNN
F 1 "pulse" H 2850 4400 60  0000 C CNN
F 2 "R1" H 2750 4450 60  0000 C CNN
F 3 "" H 3050 4450 60  0000 C CNN
	1    3050 4450
	0    1    1    0   
$EndComp
$EndSCHEMATC
