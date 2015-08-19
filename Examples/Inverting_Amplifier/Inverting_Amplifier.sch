EESchema Schematic File Version 2
LIBS:eSim_Analog
LIBS:eSim_Devices
LIBS:eSim_Digital
LIBS:eSim_Hybrid
LIBS:eSim_Miscellaneous
LIBS:eSim_Sources
LIBS:eSim_Subckt
LIBS:eSim_User
LIBS:Inverting_Amplifier-rescue
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
LIBS:Inverting_Amplifier-cache
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
L UA741 X1
U 1 1 558820F5
P 5500 3400
F 0 "X1" H 5650 3400 60  0000 C CNN
F 1 "UA741" H 5750 3250 60  0000 C CNN
F 2 "" H 5500 3400 60  0000 C CNN
F 3 "" H 5500 3400 60  0000 C CNN
	1    5500 3400
	1    0    0    -1  
$EndComp
$Comp
L GND-RESCUE-Inverting_Amplifier #PWR01
U 1 1 5588243E
P 3550 3950
F 0 "#PWR01" H 3550 3950 30  0001 C CNN
F 1 "GND" H 3550 3880 30  0001 C CNN
F 2 "" H 3550 3950 60  0000 C CNN
F 3 "" H 3550 3950 60  0000 C CNN
	1    3550 3950
	1    0    0    -1  
$EndComp
$Comp
L GND-RESCUE-Inverting_Amplifier #PWR02
U 1 1 558824A7
P 6800 3450
F 0 "#PWR02" H 6800 3450 30  0001 C CNN
F 1 "GND" H 6800 3380 30  0001 C CNN
F 2 "" H 6800 3450 60  0000 C CNN
F 3 "" H 6800 3450 60  0000 C CNN
	1    6800 3450
	1    0    0    -1  
$EndComp
Text GLabel 6200 3250 0    60   Input ~ 0
Out
Text GLabel 4750 3700 0    60   Input ~ 0
In
$Comp
L PWR_FLAG #FLG03
U 1 1 55882796
P 6750 3300
F 0 "#FLG03" H 6750 3395 50  0001 C CNN
F 1 "PWR_FLAG" H 6750 3480 50  0000 C CNN
F 2 "" H 6750 3300 60  0000 C CNN
F 3 "" H 6750 3300 60  0000 C CNN
	1    6750 3300
	1    0    0    -1  
$EndComp
$Comp
L GND-RESCUE-Inverting_Amplifier #PWR04
U 1 1 55882C4B
P 4700 3300
F 0 "#PWR04" H 4700 3300 30  0001 C CNN
F 1 "GND" H 4700 3230 30  0001 C CNN
F 2 "" H 4700 3300 60  0000 C CNN
F 3 "" H 4700 3300 60  0000 C CNN
	1    4700 3300
	1    0    0    -1  
$EndComp
$Comp
L sine v1
U 1 1 55882CA5
P 4100 3700
F 0 "v1" H 3900 3800 60  0000 C CNN
F 1 "sine" H 3900 3650 60  0000 C CNN
F 2 "R1" H 3800 3700 60  0000 C CNN
F 3 "" H 4100 3700 60  0000 C CNN
	1    4100 3700
	0    1    1    0   
$EndComp
Wire Wire Line
	4550 3500 4550 3700
Wire Wire Line
	6050 3400 6300 3400
Wire Wire Line
	6600 3400 6800 3400
Wire Wire Line
	6800 3400 6800 3450
Wire Wire Line
	3650 3700 3550 3700
Wire Wire Line
	3550 3700 3550 3950
Connection ~ 4600 3500
Wire Wire Line
	6200 3250 6200 3400
Connection ~ 6200 3400
Wire Wire Line
	6750 3300 6750 3400
Connection ~ 6750 3400
Wire Wire Line
	5950 4050 6100 4050
Wire Wire Line
	6100 4050 6100 3400
Connection ~ 6100 3400
Wire Wire Line
	5100 4050 5650 4050
Wire Wire Line
	5100 3500 5100 4050
Connection ~ 5100 3500
Wire Wire Line
	5200 3300 5300 3300
Wire Wire Line
	4900 3300 4700 3300
Wire Wire Line
	4700 3500 4550 3500
Wire Wire Line
	5000 3500 5300 3500
$Comp
L R R2
U 1 1 55D44FCE
P 5000 3350
F 0 "R2" H 5050 3480 50  0000 C CNN
F 1 "1k" H 5050 3400 50  0000 C CNN
F 2 "" H 5050 3330 30  0000 C CNN
F 3 "" V 5050 3400 30  0000 C CNN
	1    5000 3350
	1    0    0    -1  
$EndComp
$Comp
L R R1
U 1 1 55D45007
P 4800 3550
F 0 "R1" H 4850 3680 50  0000 C CNN
F 1 "1k" H 4850 3600 50  0000 C CNN
F 2 "" H 4850 3530 30  0000 C CNN
F 3 "" V 4850 3600 30  0000 C CNN
	1    4800 3550
	1    0    0    -1  
$EndComp
$Comp
L R R5
U 1 1 55D450F9
P 5750 4100
F 0 "R5" H 5800 4230 50  0000 C CNN
F 1 "2k" H 5800 4150 50  0000 C CNN
F 2 "" H 5800 4080 30  0000 C CNN
F 3 "" V 5800 4150 30  0000 C CNN
	1    5750 4100
	1    0    0    -1  
$EndComp
$Comp
L R R3
U 1 1 55D4519D
P 6400 3450
F 0 "R3" H 6450 3580 50  0000 C CNN
F 1 "1k" H 6450 3500 50  0000 C CNN
F 2 "" H 6450 3430 30  0000 C CNN
F 3 "" V 6450 3500 30  0000 C CNN
	1    6400 3450
	1    0    0    -1  
$EndComp
Wire Wire Line
	4600 3500 4600 3600
Wire Wire Line
	4600 3600 4750 3600
Wire Wire Line
	4750 3600 4750 3700
$EndSCHEMATC
