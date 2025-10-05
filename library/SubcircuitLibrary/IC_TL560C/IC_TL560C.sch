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
LIBS:IC_TL560C-cache
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
L TL560 X1
U 1 1 684BA5C1
P 5650 4000
F 0 "X1" H 5650 3750 60  0000 C CNN
F 1 "TL560" H 5650 4100 60  0000 C CNN
F 2 "" H 5650 4000 60  0001 C CNN
F 3 "" H 5650 4000 60  0001 C CNN
	1    5650 4000
	1    0    0    -1  
$EndComp
$Comp
L resistor R1
U 1 1 684BA5ED
P 4750 3650
F 0 "R1" H 4800 3780 50  0000 C CNN
F 1 "100k" H 4800 3600 50  0000 C CNN
F 2 "" H 4800 3630 30  0000 C CNN
F 3 "" V 4800 3700 30  0000 C CNN
	1    4750 3650
	0    1    1    0   
$EndComp
$Comp
L resistor R2
U 1 1 684BA632
P 4750 4400
F 0 "R2" H 4800 4530 50  0000 C CNN
F 1 "500k" H 4800 4350 50  0000 C CNN
F 2 "" H 4800 4380 30  0000 C CNN
F 3 "" V 4800 4450 30  0000 C CNN
	1    4750 4400
	0    1    1    0   
$EndComp
$Comp
L resistor R3
U 1 1 684BA6CE
P 6200 3600
F 0 "R3" H 6250 3730 50  0000 C CNN
F 1 "10k" H 6250 3550 50  0000 C CNN
F 2 "" H 6250 3580 30  0000 C CNN
F 3 "" V 6250 3650 30  0000 C CNN
	1    6200 3600
	0    1    1    0   
$EndComp
$Comp
L DC v2
U 1 1 684BA74D
P 6900 3150
F 0 "v2" H 6700 3250 60  0000 C CNN
F 1 "DC" H 6700 3100 60  0000 C CNN
F 2 "R1" H 6600 3150 60  0000 C CNN
F 3 "" H 6900 3150 60  0000 C CNN
	1    6900 3150
	0    -1   -1   0   
$EndComp
$Comp
L sine v1
U 1 1 684BA7C9
P 3000 4100
F 0 "v1" H 2800 4200 60  0000 C CNN
F 1 "sine" H 2800 4050 60  0000 C CNN
F 2 "R1" H 2700 4100 60  0000 C CNN
F 3 "" H 3000 4100 60  0000 C CNN
	1    3000 4100
	0    1    1    0   
$EndComp
$Comp
L GND #PWR01
U 1 1 684BA8D9
P 2350 4250
F 0 "#PWR01" H 2350 4000 50  0001 C CNN
F 1 "GND" H 2350 4100 50  0000 C CNN
F 2 "" H 2350 4250 50  0001 C CNN
F 3 "" H 2350 4250 50  0001 C CNN
	1    2350 4250
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR02
U 1 1 684BA90F
P 5500 5100
F 0 "#PWR02" H 5500 4850 50  0001 C CNN
F 1 "GND" H 5500 4950 50  0000 C CNN
F 2 "" H 5500 5100 50  0001 C CNN
F 3 "" H 5500 5100 50  0001 C CNN
	1    5500 5100
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR03
U 1 1 684BA92C
P 7350 3300
F 0 "#PWR03" H 7350 3050 50  0001 C CNN
F 1 "GND" H 7350 3150 50  0000 C CNN
F 2 "" H 7350 3300 50  0001 C CNN
F 3 "" H 7350 3300 50  0001 C CNN
	1    7350 3300
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U2
U 1 1 684BAA39
P 6450 4100
F 0 "U2" H 6450 4600 60  0000 C CNN
F 1 "plot_v1" H 6650 4450 60  0000 C CNN
F 2 "" H 6450 4100 60  0000 C CNN
F 3 "" H 6450 4100 60  0000 C CNN
	1    6450 4100
	0    1    1    0   
$EndComp
Text GLabel 6500 3800 1    60   Input ~ 0
OUT
$Comp
L plot_v1 U1
U 1 1 684BACD5
P 4300 3450
F 0 "U1" H 4300 3950 60  0000 C CNN
F 1 "plot_v1" H 4500 3800 60  0000 C CNN
F 2 "" H 4300 3450 60  0000 C CNN
F 3 "" H 4300 3450 60  0000 C CNN
	1    4300 3450
	1    0    0    -1  
$EndComp
Text GLabel 3900 3650 0    60   Input ~ 0
IN
Wire Wire Line
	4800 3850 4800 4300
Wire Wire Line
	3900 4100 5150 4100
Connection ~ 4800 4100
Wire Wire Line
	5500 4700 5500 5100
Wire Wire Line
	4800 4600 4800 4950
Wire Wire Line
	4800 4950 5500 4950
Wire Wire Line
	4800 3550 4800 3150
Wire Wire Line
	4800 3150 6450 3150
Wire Wire Line
	5700 3150 5700 3400
Wire Wire Line
	6250 3150 6250 3500
Connection ~ 5700 3150
Wire Wire Line
	6150 4100 6650 4100
Wire Wire Line
	6250 3800 6250 4100
Connection ~ 6250 4100
Connection ~ 6250 3150
Wire Wire Line
	2550 4100 2350 4100
Wire Wire Line
	2350 4100 2350 4250
Connection ~ 5500 4950
Wire Wire Line
	7350 3150 7350 3300
Wire Wire Line
	6500 3800 6500 4100
Connection ~ 6500 4100
Wire Wire Line
	3450 4100 3600 4100
Wire Wire Line
	4300 3250 4300 4100
Connection ~ 4300 4100
Wire Wire Line
	3900 3650 4300 3650
Connection ~ 4300 3650
Wire Wire Line
	5750 4700 5750 4950
$Comp
L capacitor_polarised C1
U 1 1 684BABA8
P 3750 4100
F 0 "C1" H 3775 4200 50  0000 L CNN
F 1 "0.047u" H 3775 4000 50  0000 L CNN
F 2 "" H 3750 4100 50  0001 C CNN
F 3 "" H 3750 4100 50  0001 C CNN
	1    3750 4100
	0    1    1    0   
$EndComp
$EndSCHEMATC
