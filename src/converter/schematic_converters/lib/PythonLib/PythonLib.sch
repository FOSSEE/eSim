EESchema Schematic File Version 2  date 
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
EELAYER 25  0
EELAYER END
$Descr A4 11700 8267
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
L GND #PWR1
U 1 1 26896853
P 1400 1300
F 0 "#PWR1" H 2800 2600 30  0001 L CNN
F 1 "EGND" H 2800 2680 30  0001 L CNN
	1    1400 1300
	1    0    0    -1
$EndComp
$Comp
L DigStim_PSPICE DSTM1
U 1 1 65650313
P 1100 800
F 0 "DSTM1" H 1100 800 30  0000 L CNN
F 1 "DigStim" H 1100 880 30  0000 L CNN
	1    1100 800
	1    0    0    -1
$EndComp
$Comp
L 74393_PSPICE U1
U 1 1 74278898
P 1100 800
F 0 "U1" H 1100 800 30  0000 L CNN
F 1 "74393" H 1100 880 30  0000 L CNN
	1    1100 800
	1    0    0    -1
$EndComp
$Comp
L titleblk_PSPICE titleblk
U 1 1 65897942
P 9700 7200
F 0 "titleblk" H 19400 14400 30  0001 L CNN
F 1 "titleblk" H 19400 14480 30  0001 L CNN
	1    9700 7200
	1    0    0    -1
$EndComp
$Comp
L nodeMarker_PSPICE nodeMarker
U 1 1 73577965
P 1100 800
F 0 "nodeMarker" H 2200 1600 30  0001 L CNN
F 1 "nodeMarker" H 2200 1680 30  0001 L CNN
	1    1100 800
	1    0    0    -1
$EndComp
$Comp
L nodeMarker_PSPICE nodeMarker
U 1 1 39494157
P 1700 800
F 0 "nodeMarker" H 3400 1600 30  0001 L CNN
F 1 "nodeMarker" H 3400 1680 30  0001 L CNN
	1    1700 800
	1    0    0    -1
$EndComp
$Comp
L nodeMarker_PSPICE nodeMarker
U 1 1 61874635
P 1700 900
F 0 "nodeMarker" H 3400 1800 30  0001 L CNN
F 1 "nodeMarker" H 3400 1880 30  0001 L CNN
	1    1700 900
	1    0    0    -1
$EndComp
$Comp
L nodeMarker_PSPICE nodeMarker
U 1 1 86034845
P 1700 1000
F 0 "nodeMarker" H 3400 2000 30  0001 L CNN
F 1 "nodeMarker" H 3400 2080 30  0001 L CNN
	1    1700 1000
	1    0    0    -1
$EndComp
$Comp
L nodeMarker_PSPICE nodeMarker
U 1 1 47771856
P 1700 1100
F 0 "nodeMarker" H 3400 2200 30  0001 L CNN
F 1 "nodeMarker" H 3400 2280 30  0001 L CNN
	1    1700 1100
	1    0    0    -1
$EndComp
Connection ~ 1100 800
Connection ~ 1100 800
Connection ~ 1400 1300
Connection ~ 1100 800
Connection ~ 1700 800
Connection ~ 1700 900
Connection ~ 1700 1000
Connection ~ 1700 1100
$EndSCHEMATC
