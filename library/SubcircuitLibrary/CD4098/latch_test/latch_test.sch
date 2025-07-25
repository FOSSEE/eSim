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
L cd4098_latch U1
U 1 1 685A6E23
P 2350 4550
F 0 "U1" H 5200 6350 60  0000 C CNN
F 1 "cd4098_latch" H 5200 6550 60  0000 C CNN
F 2 "" H 5200 6500 60  0000 C CNN
F 3 "" H 5200 6500 60  0000 C CNN
	1    2350 4550
	1    0    0    -1  
$EndComp
$Comp
L DC v4
U 1 1 685A6ED2
P 3350 1800
F 0 "v4" H 3150 1900 60  0000 C CNN
F 1 "DC" H 3150 1750 60  0000 C CNN
F 2 "R1" H 3050 1800 60  0000 C CNN
F 3 "" H 3350 1800 60  0000 C CNN
	1    3350 1800
	1    0    0    1   
$EndComp
Wire Wire Line
	4500 2400 4500 2650
$Comp
L adc_bridge_3 U2
U 1 1 685A6F16
P 3750 2800
F 0 "U2" H 3750 2800 60  0000 C CNN
F 1 "adc_bridge_3" H 3750 2950 60  0000 C CNN
F 2 "" H 3750 2800 60  0000 C CNN
F 3 "" H 3750 2800 60  0000 C CNN
	1    3750 2800
	1    0    0    -1  
$EndComp
Wire Wire Line
	4300 2750 4500 2750
Wire Wire Line
	4300 2850 4500 2850
Wire Wire Line
	4300 2950 4500 2950
$Comp
L pulse v1
U 1 1 685A6F6C
P 2300 3200
F 0 "v1" H 2100 3300 60  0000 C CNN
F 1 "pulse" H 2100 3150 60  0000 C CNN
F 2 "R1" H 2000 3200 60  0000 C CNN
F 3 "" H 2300 3200 60  0000 C CNN
	1    2300 3200
	1    0    0    -1  
$EndComp
$Comp
L pulse v2
U 1 1 685A6FAD
P 2650 3300
F 0 "v2" H 2450 3400 60  0000 C CNN
F 1 "pulse" H 2450 3250 60  0000 C CNN
F 2 "R1" H 2350 3300 60  0000 C CNN
F 3 "" H 2650 3300 60  0000 C CNN
	1    2650 3300
	1    0    0    -1  
$EndComp
$Comp
L pulse v3
U 1 1 685A6FDC
P 3000 3400
F 0 "v3" H 2800 3500 60  0000 C CNN
F 1 "pulse" H 2800 3350 60  0000 C CNN
F 2 "R1" H 2700 3400 60  0000 C CNN
F 3 "" H 3000 3400 60  0000 C CNN
	1    3000 3400
	1    0    0    -1  
$EndComp
Wire Wire Line
	3000 2950 3150 2950
Wire Wire Line
	2650 2850 3150 2850
Wire Wire Line
	2300 2750 3150 2750
$Comp
L eSim_GND #PWR01
U 1 1 685A7293
P 2300 3750
F 0 "#PWR01" H 2300 3500 50  0001 C CNN
F 1 "eSim_GND" H 2300 3600 50  0000 C CNN
F 2 "" H 2300 3750 50  0001 C CNN
F 3 "" H 2300 3750 50  0001 C CNN
	1    2300 3750
	1    0    0    -1  
$EndComp
$Comp
L eSim_GND #PWR02
U 1 1 685A72B7
P 2650 3850
F 0 "#PWR02" H 2650 3600 50  0001 C CNN
F 1 "eSim_GND" H 2650 3700 50  0000 C CNN
F 2 "" H 2650 3850 50  0001 C CNN
F 3 "" H 2650 3850 50  0001 C CNN
	1    2650 3850
	1    0    0    -1  
$EndComp
$Comp
L eSim_GND #PWR03
U 1 1 685A72D4
P 3000 3950
F 0 "#PWR03" H 3000 3700 50  0001 C CNN
F 1 "eSim_GND" H 3000 3800 50  0000 C CNN
F 2 "" H 3000 3950 50  0001 C CNN
F 3 "" H 3000 3950 50  0001 C CNN
	1    3000 3950
	1    0    0    -1  
$EndComp
Wire Wire Line
	2300 3650 2300 3750
Wire Wire Line
	2650 3750 2650 3850
Wire Wire Line
	3000 3850 3000 3950
$Comp
L eSim_GND #PWR04
U 1 1 685A73E1
P 3500 1350
F 0 "#PWR04" H 3500 1100 50  0001 C CNN
F 1 "eSim_GND" H 3500 1200 50  0000 C CNN
F 2 "" H 3500 1350 50  0001 C CNN
F 3 "" H 3500 1350 50  0001 C CNN
	1    3500 1350
	1    0    0    -1  
$EndComp
Wire Wire Line
	3350 1350 3500 1350
$Comp
L dac_bridge_1 U3
U 1 1 685A7670
P 6650 2700
F 0 "U3" H 6650 2700 60  0000 C CNN
F 1 "dac_bridge_1" H 6650 2850 60  0000 C CNN
F 2 "" H 6650 2700 60  0000 C CNN
F 3 "" H 6650 2700 60  0000 C CNN
	1    6650 2700
	1    0    0    -1  
$EndComp
Wire Wire Line
	6050 2650 5900 2650
$Comp
L plot_v1 U4
U 1 1 685A76B7
P 7250 2750
F 0 "U4" H 7250 3250 60  0000 C CNN
F 1 "plot_v1" H 7450 3100 60  0000 C CNN
F 2 "" H 7250 2750 60  0000 C CNN
F 3 "" H 7250 2750 60  0000 C CNN
	1    7250 2750
	1    0    0    -1  
$EndComp
Wire Wire Line
	7200 2650 7250 2650
Wire Wire Line
	7250 2550 7250 2850
Text GLabel 7250 2850 0    60   Input ~ 0
Q
Connection ~ 7250 2650
Text GLabel 2500 2650 0    60   Input ~ 0
C
Wire Wire Line
	2500 2650 2550 2650
Wire Wire Line
	2550 2650 2550 2750
Connection ~ 2550 2750
Text GLabel 2800 3000 0    60   Input ~ 0
R
Wire Wire Line
	2800 3000 2850 3000
Wire Wire Line
	2850 3000 2850 2850
Connection ~ 2850 2850
Text GLabel 3200 3100 2    60   Input ~ 0
RST
Wire Wire Line
	3100 2950 3100 3100
Wire Wire Line
	3100 3100 3200 3100
Connection ~ 3100 2950
$Comp
L adc_bridge_1 U5
U 1 1 685A7BCF
P 3950 2450
F 0 "U5" H 3950 2450 60  0000 C CNN
F 1 "adc_bridge_1" H 3950 2600 60  0000 C CNN
F 2 "" H 3950 2450 60  0000 C CNN
F 3 "" H 3950 2450 60  0000 C CNN
	1    3950 2450
	1    0    0    -1  
$EndComp
Wire Wire Line
	3350 2250 3350 2400
$EndSCHEMATC
