EESchema Schematic File Version 2
LIBS:power
LIBS:device
LIBS:transistors
LIBS:conn
LIBS:linear
LIBS:regul
LIBS:74xx
LIBS:cmos4000
LIBS:adc-dac
LIBS:memory
LIBS:xilinx
LIBS:special
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
LIBS:valves
LIBS:eSim_Analog
LIBS:eSim_Devices
LIBS:eSim_Digital
LIBS:eSim_Hybrid
LIBS:eSim_Sources
LIBS:eSim_Subckt
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
L half_adder X1
U 1 1 558AA064
P 3800 3350
F 0 "X1" H 4700 3850 60  0000 C CNN
F 1 "half_adder" H 4700 3750 60  0000 C CNN
F 2 "" H 3800 3350 60  0000 C CNN
F 3 "" H 3800 3350 60  0000 C CNN
	1    3800 3350
	1    0    0    -1  
$EndComp
$Comp
L half_adder X2
U 1 1 558AA0C1
P 5700 3350
F 0 "X2" H 6600 3850 60  0000 C CNN
F 1 "half_adder" H 6600 3750 60  0000 C CNN
F 2 "" H 5700 3350 60  0000 C CNN
F 3 "" H 5700 3350 60  0000 C CNN
	1    5700 3350
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 1 1 558AA277
P 3450 2650
F 0 "U1" H 3500 2750 30  0000 C CNN
F 1 "PORT" H 3450 2650 30  0000 C CNN
F 2 "" H 3450 2650 60  0000 C CNN
F 3 "" H 3450 2650 60  0000 C CNN
	1    3450 2650
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 2 1 558AA29E
P 3450 3250
F 0 "U1" H 3500 3350 30  0000 C CNN
F 1 "PORT" H 3450 3250 30  0000 C CNN
F 2 "" H 3450 3250 60  0000 C CNN
F 3 "" H 3450 3250 60  0000 C CNN
	2    3450 3250
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 3 1 558AA2D8
P 5650 2300
F 0 "U1" H 5700 2400 30  0000 C CNN
F 1 "PORT" H 5650 2300 30  0000 C CNN
F 2 "" H 5650 2300 60  0000 C CNN
F 3 "" H 5650 2300 60  0000 C CNN
	3    5650 2300
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 4 1 558AA378
P 7900 2650
F 0 "U1" H 7950 2750 30  0000 C CNN
F 1 "PORT" H 7900 2650 30  0000 C CNN
F 2 "" H 7900 2650 60  0000 C CNN
F 3 "" H 7900 2650 60  0000 C CNN
	4    7900 2650
	-1   0    0    1   
$EndComp
$Comp
L PORT U1
U 5 1 558AA3E0
P 8700 3400
F 0 "U1" H 8750 3500 30  0000 C CNN
F 1 "PORT" H 8700 3400 30  0000 C CNN
F 2 "" H 8700 3400 60  0000 C CNN
F 3 "" H 8700 3400 60  0000 C CNN
	5    8700 3400
	-1   0    0    1   
$EndComp
$Comp
L d_or U2
U 1 1 558AA43B
P 7900 3450
F 0 "U2" H 7900 3450 60  0000 C CNN
F 1 "d_or" H 7900 3550 60  0000 C CNN
F 2 "" H 7900 3450 60  0000 C CNN
F 3 "" H 7900 3450 60  0000 C CNN
	1    7900 3450
	1    0    0    -1  
$EndComp
Wire Wire Line
	3700 2650 4100 2650
Wire Wire Line
	3700 3250 4100 3250
Wire Wire Line
	5250 2650 5650 2650
Wire Wire Line
	5650 2650 5650 3250
Wire Wire Line
	5650 3250 6000 3250
Wire Wire Line
	5900 2300 5900 2650
Wire Wire Line
	5900 2650 6000 2650
Wire Wire Line
	7150 2650 7650 2650
Wire Wire Line
	7150 3250 7350 3250
Wire Wire Line
	7350 3250 7350 3350
Wire Wire Line
	7350 3350 7450 3350
Wire Wire Line
	5250 3250 5400 3250
Wire Wire Line
	5400 3250 5400 3450
Wire Wire Line
	5400 3450 7450 3450
Wire Wire Line
	8350 3400 8450 3400
Text Notes 3850 2500 0    60   ~ 0
IN1
Text Notes 3850 3150 0    60   ~ 0
IN2
Text Notes 6000 2350 0    60   ~ 0
CIN
Text Notes 7350 2550 0    60   ~ 0
SUM
Text Notes 8300 3200 0    60   ~ 0
COUT
$EndSCHEMATC
