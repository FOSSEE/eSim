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
LIBS:CMOS_NAND_Gate-cache
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
L pulse v1
U 1 1 5EA263FE
P 6350 2700
F 0 "v1" H 6150 2800 60  0000 C CNN
F 1 "pulse" H 6150 2650 60  0000 C CNN
F 2 "R1" H 6050 2700 60  0000 C CNN
F 3 "" H 6350 2700 60  0000 C CNN
	1    6350 2700
	1    0    0    -1  
$EndComp
$Comp
L pulse v2
U 1 1 5EA263FF
P 6800 3950
F 0 "v2" H 6600 4050 60  0000 C CNN
F 1 "pulse" H 6600 3900 60  0000 C CNN
F 2 "R1" H 6500 3950 60  0000 C CNN
F 3 "" H 6800 3950 60  0000 C CNN
	1    6800 3950
	1    0    0    -1  
$EndComp
Text GLabel 6100 2250 0    60   Input ~ 0
inputA
Text GLabel 6750 3350 0    60   Input ~ 0
inputB
$Comp
L plot_v1 U2
U 1 1 5EA26400
P 6800 3550
F 0 "U2" H 6800 4050 60  0000 C CNN
F 1 "plot_v1" H 7000 3900 60  0000 C CNN
F 2 "" H 6800 3550 60  0000 C CNN
F 3 "" H 6800 3550 60  0000 C CNN
	1    6800 3550
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U1
U 1 1 5EA26401
P 6350 2450
F 0 "U1" H 6350 2950 60  0000 C CNN
F 1 "plot_v1" H 6550 2800 60  0000 C CNN
F 2 "" H 6350 2450 60  0000 C CNN
F 3 "" H 6350 2450 60  0000 C CNN
	1    6350 2450
	1    0    0    -1  
$EndComp
Wire Wire Line
	6800 3500 7400 3500
Wire Wire Line
	6350 3150 6350 4400
Connection ~ 6800 4400
Wire Wire Line
	6100 2250 6800 2250
Wire Wire Line
	6800 2250 6800 2850
Wire Wire Line
	6800 2850 7400 2850
Connection ~ 6350 2250
Wire Wire Line
	6750 3350 6800 3350
Wire Wire Line
	6800 3350 6800 3500
$Comp
L plot_v1 U3
U 1 1 5EA26402
P 8900 3200
F 0 "U3" H 8900 3700 60  0000 C CNN
F 1 "plot_v1" H 9100 3550 60  0000 C CNN
F 2 "" H 8900 3200 60  0000 C CNN
F 3 "" H 8900 3200 60  0000 C CNN
	1    8900 3200
	1    0    0    -1  
$EndComp
Wire Wire Line
	7400 2850 7400 2900
Wire Wire Line
	7400 3500 7400 3450
Connection ~ 8050 4400
$Comp
L GND #PWR1
U 1 1 5EA26403
P 8050 4550
F 0 "#PWR1" H 8050 4300 50  0001 C CNN
F 1 "GND" H 8050 4400 50  0000 C CNN
F 2 "" H 8050 4550 50  0001 C CNN
F 3 "" H 8050 4550 50  0001 C CNN
	1    8050 4550
	1    0    0    -1  
$EndComp
Wire Wire Line
	8900 3000 8900 3150
Wire Wire Line
	8900 3150 8750 3150
Text GLabel 8900 3150 3    60   Input ~ 0
out
$Comp
L CMOS_NAND X1
U 1 1 5EA26404
P 7950 3150
F 0 "X1" H 7850 3000 60  0000 C CNN
F 1 "CMOS_NAND" H 7950 3100 60  0000 C CNN
F 2 "" H 7950 3150 60  0001 C CNN
F 3 "" H 7950 3150 60  0001 C CNN
	1    7950 3150
	1    0    0    -1  
$EndComp
Wire Wire Line
	8050 4400 8050 4550
Wire Wire Line
	6350 4400 8050 4400
$EndSCHEMATC
