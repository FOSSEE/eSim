EESchema Schematic File Version 2
LIBS:Halfwave_Rectifier-rescue
LIBS:eSim_Analog
LIBS:eSim_Devices
LIBS:eSim_Digital
LIBS:eSim_Hybrid
LIBS:eSim_Miscellaneous
LIBS:eSim_Plot
LIBS:eSim_Power
LIBS:eSim_Sources
LIBS:eSim_Subckt
LIBS:eSim_User
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
LIBS:eSim_PSpice
LIBS:Halfwave_Rectifier-cache
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
L D-RESCUE-Halfwave_Rectifier D1
U 1 1 5593CBB8
P 5700 2900
F 0 "D1" H 5700 3000 50  0000 C CNN
F 1 "D" H 5700 2800 50  0000 C CNN
F 2 "" H 5700 2900 60  0000 C CNN
F 3 "" H 5700 2900 60  0000 C CNN
	1    5700 2900
	1    0    0    -1  
$EndComp
$Comp
L R-RESCUE-Halfwave_Rectifier R1
U 1 1 5593CC2C
P 6300 3350
F 0 "R1" V 6380 3350 50  0000 C CNN
F 1 "1k" V 6300 3350 50  0000 C CNN
F 2 "" V 6230 3350 30  0000 C CNN
F 3 "" H 6300 3350 30  0000 C CNN
	1    6300 3350
	1    0    0    -1  
$EndComp
$Comp
L sine v1
U 1 1 5593CC81
P 5050 3400
F 0 "v1" H 4850 3500 60  0000 C CNN
F 1 "sine" H 4850 3350 60  0000 C CNN
F 2 "R1" H 4750 3400 60  0000 C CNN
F 3 "" H 5050 3400 60  0000 C CNN
	1    5050 3400
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR01
U 1 1 5593CCF2
P 5700 4050
F 0 "#PWR01" H 5700 3800 50  0001 C CNN
F 1 "GND" H 5700 3900 50  0000 C CNN
F 2 "" H 5700 4050 60  0000 C CNN
F 3 "" H 5700 4050 60  0000 C CNN
	1    5700 4050
	1    0    0    -1  
$EndComp
$Comp
L PWR_FLAG #FLG02
U 1 1 5593CD49
P 5700 3800
F 0 "#FLG02" H 5700 3895 50  0001 C CNN
F 1 "PWR_FLAG" H 5700 3980 50  0000 C CNN
F 2 "" H 5700 3800 60  0000 C CNN
F 3 "" H 5700 3800 60  0000 C CNN
	1    5700 3800
	1    0    0    -1  
$EndComp
Text GLabel 5000 2750 0    60   Input ~ 0
IN
Text GLabel 6400 2800 2    60   Input ~ 0
OUT
$Comp
L plot_v1 U2
U 1 1 56D86A9A
P 5100 2900
F 0 "U2" H 5100 3400 60  0000 C CNN
F 1 "plot_v1" H 5300 3250 60  0000 C CNN
F 2 "" H 5100 2900 60  0000 C CNN
F 3 "" H 5100 2900 60  0000 C CNN
	1    5100 2900
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U3
U 1 1 56D86ADF
P 6300 2950
F 0 "U3" H 6300 3450 60  0000 C CNN
F 1 "plot_v1" H 6500 3300 60  0000 C CNN
F 2 "" H 6300 2950 60  0000 C CNN
F 3 "" H 6300 2950 60  0000 C CNN
	1    6300 2950
	1    0    0    -1  
$EndComp
Wire Wire Line
	5050 2950 5050 2900
Wire Wire Line
	5050 2900 5550 2900
Wire Wire Line
	5850 2900 6300 2900
Wire Wire Line
	6300 2900 6300 3200
Wire Wire Line
	6300 3500 6300 3900
Wire Wire Line
	6300 3900 5050 3900
Wire Wire Line
	5050 3900 5050 3850
Wire Wire Line
	5700 3800 5700 4050
Connection ~ 5700 3900
Wire Wire Line
	5000 2750 5250 2750
Wire Wire Line
	5250 2750 5250 2900
Connection ~ 5250 2900
Wire Wire Line
	6100 2800 6400 2800
Wire Wire Line
	6100 2800 6100 2900
Connection ~ 6100 2900
Wire Wire Line
	5100 2700 5100 2750
Connection ~ 5100 2750
Wire Wire Line
	6300 2750 6300 2800
Connection ~ 6300 2800
$EndSCHEMATC
