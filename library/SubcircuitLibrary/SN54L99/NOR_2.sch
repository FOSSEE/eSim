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
L sky130_fd_pr__pfet_01v8 SC2
U 1 1 684CE7B8
P 4750 2600
F 0 "SC2" H 4800 2900 50  0000 C CNN
F 1 "sky130_fd_pr__pfet_01v8" H 5050 2687 50  0000 R CNN
F 2 "" H 4750 1100 50  0001 C CNN
F 3 "" H 4750 2600 50  0001 C CNN
	1    4750 2600
	1    0    0    -1  
$EndComp
$Comp
L sky130_fd_pr__pfet_01v8 SC3
U 1 1 684CE82E
P 5150 3400
F 0 "SC3" H 5200 3700 50  0000 C CNN
F 1 "sky130_fd_pr__pfet_01v8" H 5450 3487 50  0000 R CNN
F 2 "" H 5150 1900 50  0001 C CNN
F 3 "" H 5150 3400 50  0001 C CNN
	1    5150 3400
	-1   0    0    -1  
$EndComp
$Comp
L sky130_fd_pr__nfet_01v8 SC1
U 1 1 684CE88F
P 4050 4450
F 0 "SC1" H 4100 4750 50  0000 C CNN
F 1 "sky130_fd_pr__nfet_01v8" H 4350 4537 50  0000 R CNN
F 2 "" H 4050 2950 50  0001 C CNN
F 3 "" H 4050 4450 50  0001 C CNN
	1    4050 4450
	1    0    0    -1  
$EndComp
$Comp
L sky130_fd_pr__nfet_01v8 SC4
U 1 1 684CE8CA
P 5650 4450
F 0 "SC4" H 5700 4750 50  0000 C CNN
F 1 "sky130_fd_pr__nfet_01v8" H 5950 4537 50  0000 R CNN
F 2 "" H 5650 2950 50  0001 C CNN
F 3 "" H 5650 4450 50  0001 C CNN
	1    5650 4450
	-1   0    0    -1  
$EndComp
$Comp
L PORT U1
U 1 1 684CE919
P 3100 3450
F 0 "U1" H 3150 3550 30  0000 C CNN
F 1 "PORT" H 3100 3450 30  0000 C CNN
F 2 "" H 3100 3450 60  0000 C CNN
F 3 "" H 3100 3450 60  0000 C CNN
	1    3100 3450
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 4 1 684CE990
P 6350 3400
F 0 "U1" H 6400 3500 30  0000 C CNN
F 1 "PORT" H 6350 3400 30  0000 C CNN
F 2 "" H 6350 3400 60  0000 C CNN
F 3 "" H 6350 3400 60  0000 C CNN
	4    6350 3400
	-1   0    0    -1  
$EndComp
$Comp
L PORT U1
U 5 1 684CEA11
P 6450 3900
F 0 "U1" H 6500 4000 30  0000 C CNN
F 1 "PORT" H 6450 3900 30  0000 C CNN
F 2 "" H 6450 3900 60  0000 C CNN
F 3 "" H 6450 3900 60  0000 C CNN
	5    6450 3900
	-1   0    0    -1  
$EndComp
$Comp
L PORT U1
U 3 1 684CEA84
P 4700 2150
F 0 "U1" H 4750 2250 30  0000 C CNN
F 1 "PORT" H 4700 2150 30  0000 C CNN
F 2 "" H 4700 2150 60  0000 C CNN
F 3 "" H 4700 2150 60  0000 C CNN
	3    4700 2150
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 2 1 684CEB11
P 4650 5100
F 0 "U1" H 4700 5200 30  0000 C CNN
F 1 "PORT" H 4650 5100 30  0000 C CNN
F 2 "" H 4650 5100 60  0000 C CNN
F 3 "" H 4650 5100 60  0000 C CNN
	2    4650 5100
	1    0    0    -1  
$EndComp
$Comp
L SKY130mode scmode1
U 1 1 684CEB6E
P 8300 2900
F 0 "scmode1" H 8300 3050 98  0000 C CNB
F 1 "SKY130mode" H 8300 2800 118 0000 C CNB
F 2 "" H 8300 3050 60  0001 C CNN
F 3 "" H 8300 3050 60  0001 C CNN
	1    8300 2900
	1    0    0    -1  
$EndComp
Wire Wire Line
	4250 4150 5450 4150
Wire Wire Line
	4950 3700 4950 4150
Connection ~ 4950 4150
Wire Wire Line
	6200 3900 4950 3900
Connection ~ 4950 3900
Wire Wire Line
	4250 4750 5450 4750
Wire Wire Line
	5550 4450 5400 4450
Wire Wire Line
	5400 4450 5400 4750
Connection ~ 5400 4750
Wire Wire Line
	4150 4450 4300 4450
Wire Wire Line
	4300 4450 4300 4750
Connection ~ 4300 4750
Wire Wire Line
	4900 5100 4900 4750
Connection ~ 4900 4750
Wire Wire Line
	5450 3400 6100 3400
Wire Wire Line
	5950 3400 5950 4450
Connection ~ 5950 3400
Wire Wire Line
	4450 2600 3750 2600
Wire Wire Line
	3750 2600 3750 4450
Wire Wire Line
	3350 3450 3750 3450
Connection ~ 3750 3450
Wire Wire Line
	4950 2150 4950 2300
Wire Wire Line
	4850 2600 5000 2600
Wire Wire Line
	5000 2600 5000 2250
Wire Wire Line
	5000 2250 4950 2250
Connection ~ 4950 2250
Wire Wire Line
	4950 2900 4950 3100
Wire Wire Line
	5050 3400 4900 3400
Wire Wire Line
	4900 3400 4900 3050
Wire Wire Line
	4900 3050 4950 3050
Connection ~ 4950 3050
$EndSCHEMATC
