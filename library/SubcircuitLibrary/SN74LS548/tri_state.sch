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
LIBS:tri_state-cache
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
L sky130_fd_pr__pfet_01v8 SC1
U 1 1 686E04ED
P 5150 2450
F 0 "SC1" H 5200 2750 50  0000 C CNN
F 1 "sky130_fd_pr__pfet_01v8" H 5450 2537 50  0000 R CNN
F 2 "" H 5150 950 50  0001 C CNN
F 3 "" H 5150 2450 50  0001 C CNN
	1    5150 2450
	1    0    0    -1  
$EndComp
$Comp
L sky130_fd_pr__nfet_01v8 SC2
U 1 1 686E0554
P 5150 3250
F 0 "SC2" H 5200 3550 50  0000 C CNN
F 1 "sky130_fd_pr__nfet_01v8" H 5450 3337 50  0000 R CNN
F 2 "" H 5150 1750 50  0001 C CNN
F 3 "" H 5150 3250 50  0001 C CNN
	1    5150 3250
	1    0    0    -1  
$EndComp
$Comp
L SKY130mode scmode1
U 1 1 686E05B6
P 9300 2250
F 0 "scmode1" H 9300 2400 98  0000 C CNB
F 1 "SKY130mode" H 9300 2150 118 0000 C CNB
F 2 "" H 9300 2400 60  0001 C CNN
F 3 "" H 9300 2400 60  0001 C CNN
	1    9300 2250
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 1 1 686E061D
P 4200 2800
F 0 "U1" H 4250 2900 30  0000 C CNN
F 1 "PORT" H 4200 2800 30  0000 C CNN
F 2 "" H 4200 2800 60  0000 C CNN
F 3 "" H 4200 2800 60  0000 C CNN
	1    4200 2800
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 2 1 686E069C
P 5050 1900
F 0 "U1" H 5100 2000 30  0000 C CNN
F 1 "PORT" H 5050 1900 30  0000 C CNN
F 2 "" H 5050 1900 60  0000 C CNN
F 3 "" H 5050 1900 60  0000 C CNN
	2    5050 1900
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 3 1 686E0725
P 5100 3750
F 0 "U1" H 5150 3850 30  0000 C CNN
F 1 "PORT" H 5100 3750 30  0000 C CNN
F 2 "" H 5100 3750 60  0000 C CNN
F 3 "" H 5100 3750 60  0000 C CNN
	3    5100 3750
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 5 1 686E0750
P 6800 2800
F 0 "U1" H 6850 2900 30  0000 C CNN
F 1 "PORT" H 6800 2800 30  0000 C CNN
F 2 "" H 6800 2800 60  0000 C CNN
F 3 "" H 6800 2800 60  0000 C CNN
	5    6800 2800
	-1   0    0    1   
$EndComp
$Comp
L PORT U1
U 4 1 686E0793
P 6200 2150
F 0 "U1" H 6250 2250 30  0000 C CNN
F 1 "PORT" H 6200 2150 30  0000 C CNN
F 2 "" H 6200 2150 60  0000 C CNN
F 3 "" H 6200 2150 60  0000 C CNN
	4    6200 2150
	-1   0    0    1   
$EndComp
Wire Wire Line
	4850 2450 4850 3250
Wire Wire Line
	4450 2800 4850 2800
Connection ~ 4850 2800
Wire Wire Line
	5350 2750 5350 2950
Wire Wire Line
	5400 2450 5250 2450
Wire Wire Line
	5400 1900 5400 2450
Wire Wire Line
	5400 2150 5350 2150
Wire Wire Line
	5300 1900 5400 1900
Connection ~ 5400 2150
Wire Wire Line
	5250 3250 5400 3250
Wire Wire Line
	5400 3250 5400 3750
Wire Wire Line
	5400 3550 5350 3550
Wire Wire Line
	5400 3750 5350 3750
Connection ~ 5400 3550
Wire Wire Line
	5650 2800 5350 2800
Connection ~ 5350 2800
Wire Wire Line
	5950 2850 5950 2700
Wire Wire Line
	5550 2850 5950 2850
Wire Wire Line
	5550 2850 5550 2800
Connection ~ 5550 2800
Wire Wire Line
	6250 2800 6550 2800
Wire Wire Line
	5950 2300 5950 2150
$Comp
L sky130_fd_pr__nfet_01v8 SC3
U 1 1 686E7F5A
P 5950 2600
F 0 "SC3" H 6000 2900 50  0000 C CNN
F 1 "sky130_fd_pr__nfet_01v8" H 6250 2687 50  0000 R CNN
F 2 "" H 5950 1100 50  0001 C CNN
F 3 "" H 5950 2600 50  0001 C CNN
	1    5950 2600
	0    1    1    0   
$EndComp
$EndSCHEMATC
