EESchema Schematic File Version 2
LIBS:Zener_Characteristic-rescue
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
LIBS:transistors
LIBS:conn
LIBS:regul
LIBS:74xx
LIBS:cmos4000
LIBS:Zener_Characteristic-cache
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
L DC-RESCUE-Zener_Characteristic v1
U 1 1 56C6E03A
P 5350 3750
F 0 "v1" H 5150 3850 60  0000 C CNN
F 1 "DC" H 5150 3700 60  0000 C CNN
F 2 "R1" H 5050 3750 60  0000 C CNN
F 3 "" H 5350 3750 60  0000 C CNN
	1    5350 3750
	1    0    0    -1  
$EndComp
$Comp
L R R1
U 1 1 56C6E09D
P 5650 3250
F 0 "R1" H 5700 3380 50  0000 C CNN
F 1 "1k" H 5700 3300 50  0000 C CNN
F 2 "" H 5700 3230 30  0000 C CNN
F 3 "" V 5700 3300 30  0000 C CNN
	1    5650 3250
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR01
U 1 1 56C6E0D8
P 6050 4300
F 0 "#PWR01" H 6050 4050 50  0001 C CNN
F 1 "GND" H 6050 4150 50  0000 C CNN
F 2 "" H 6050 4300 50  0000 C CNN
F 3 "" H 6050 4300 50  0000 C CNN
	1    6050 4300
	1    0    0    -1  
$EndComp
Text GLabel 5300 3100 0    60   Input ~ 0
in
Text GLabel 6750 3050 2    60   Input ~ 0
out
$Comp
L plot_i2 U2
U 1 1 56C6E2C8
P 6200 3450
F 0 "U2" H 6200 3850 60  0000 C CNN
F 1 "plot_i2" H 6200 3550 60  0000 C CNN
F 2 "" H 6200 3450 60  0000 C CNN
F 3 "" H 6200 3450 60  0000 C CNN
	1    6200 3450
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U3
U 1 1 56C6E4F3
P 6550 3200
F 0 "U3" H 6550 3700 60  0000 C CNN
F 1 "plot_v1" H 6750 3550 60  0000 C CNN
F 2 "" H 6550 3200 60  0000 C CNN
F 3 "" H 6550 3200 60  0000 C CNN
	1    6550 3200
	1    0    0    -1  
$EndComp
Wire Wire Line
	5350 3300 5350 3200
Wire Wire Line
	6600 3200 6600 3650
Wire Wire Line
	5350 4200 5350 4250
Wire Wire Line
	5350 4250 6600 4250
Wire Wire Line
	6050 4300 6050 4250
Connection ~ 6050 4250
Wire Wire Line
	5300 3100 5450 3100
Wire Wire Line
	5450 3100 5450 3200
Connection ~ 5450 3200
Wire Wire Line
	6550 3000 6550 3200
Connection ~ 6550 3200
Wire Wire Line
	5350 3200 5550 3200
Wire Wire Line
	5850 3200 5900 3200
Wire Wire Line
	6500 3200 6600 3200
Wire Wire Line
	6750 3050 6750 3100
Wire Wire Line
	6750 3100 6550 3100
Connection ~ 6550 3100
$Comp
L zener U1
U 1 1 56C6ED25
P 6600 3950
F 0 "U1" H 6550 3850 60  0000 C CNN
F 1 "zener" H 6600 4050 60  0000 C CNN
F 2 "" H 6650 3950 60  0000 C CNN
F 3 "" H 6650 3950 60  0000 C CNN
	1    6600 3950
	0    -1   -1   0   
$EndComp
Wire Wire Line
	6600 4250 6600 4150
$EndSCHEMATC
