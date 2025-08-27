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
LIBS:TL783-cache
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
L lm_741 X1
U 1 1 6783F56B
P 4850 3350
F 0 "X1" H 4650 3350 60  0000 C CNN
F 1 "lm_741" H 4750 3100 60  0000 C CNN
F 2 "" H 4850 3350 60  0000 C CNN
F 3 "" H 4850 3350 60  0000 C CNN
	1    4850 3350
	1    0    0    -1  
$EndComp
$Comp
L zener U1
U 1 1 6783F56C
P 4200 4300
F 0 "U1" H 4150 4200 60  0000 C CNN
F 1 "zener" H 4200 4400 60  0000 C CNN
F 2 "" H 4250 4300 60  0000 C CNN
F 3 "" H 4250 4300 60  0000 C CNN
	1    4200 4300
	0    -1   -1   0   
$EndComp
$Comp
L mosfet_n M1
U 1 1 6783F56D
P 6100 3150
F 0 "M1" H 6100 3000 50  0000 R CNN
F 1 "mosfet_n" H 6200 3100 50  0000 R CNN
F 2 "" H 6400 2850 29  0000 C CNN
F 3 "" H 6200 2950 60  0000 C CNN
	1    6100 3150
	1    0    0    -1  
$EndComp
$Comp
L resistor R1
U 1 1 6783F56E
P 6400 4000
F 0 "R1" H 6450 4130 50  0000 C CNN
F 1 "1k" H 6450 3950 50  0000 C CNN
F 2 "" H 6450 3980 30  0000 C CNN
F 3 "" V 6450 4050 30  0000 C CNN
	1    6400 4000
	0    1    1    0   
$EndComp
$Comp
L resistor R2
U 1 1 6783F56F
P 6400 4450
F 0 "R2" H 6450 4580 50  0000 C CNN
F 1 "39k" H 6450 4400 50  0000 C CNN
F 2 "" H 6450 4430 30  0000 C CNN
F 3 "" V 6450 4500 30  0000 C CNN
	1    6400 4450
	0    1    1    0   
$EndComp
Wire Wire Line
	4300 3450 4200 3450
Wire Wire Line
	4200 3450 4200 4000
Wire Wire Line
	4300 3200 3900 3200
Wire Wire Line
	3900 3200 3900 3900
Wire Wire Line
	3900 3900 7000 3900
Wire Wire Line
	6450 4200 6450 4350
Connection ~ 6450 3900
Wire Wire Line
	6300 3550 6300 3900
Connection ~ 6300 3900
Wire Wire Line
	6400 3500 6400 3700
Wire Wire Line
	6400 3700 6300 3700
Connection ~ 6300 3700
Wire Wire Line
	6300 3150 6300 2800
Wire Wire Line
	4200 4500 5950 4500
Wire Wire Line
	5950 4500 5950 4300
Wire Wire Line
	5950 4300 7100 4300
Connection ~ 6450 4300
$Comp
L PORT U2
U 1 1 6783F570
P 6050 2800
F 0 "U2" H 6100 2900 30  0000 C CNN
F 1 "PORT" H 6050 2800 30  0000 C CNN
F 2 "" H 6050 2800 60  0000 C CNN
F 3 "" H 6050 2800 60  0000 C CNN
	1    6050 2800
	1    0    0    -1  
$EndComp
$Comp
L eSim_GND #PWR01
U 1 1 6783F573
P 6450 4800
F 0 "#PWR01" H 6450 4550 50  0001 C CNN
F 1 "eSim_GND" H 6450 4650 50  0000 C CNN
F 2 "" H 6450 4800 50  0001 C CNN
F 3 "" H 6450 4800 50  0001 C CNN
	1    6450 4800
	1    0    0    -1  
$EndComp
Wire Wire Line
	6450 4650 6450 4800
Wire Wire Line
	5400 3350 6000 3350
$Comp
L eSim_GND #PWR02
U 1 1 6783F576
P 4700 3800
F 0 "#PWR02" H 4700 3550 50  0001 C CNN
F 1 "eSim_GND" H 4700 3650 50  0000 C CNN
F 2 "" H 4700 3800 50  0001 C CNN
F 3 "" H 4700 3800 50  0001 C CNN
	1    4700 3800
	1    0    0    -1  
$EndComp
$Comp
L PORT U2
U 2 1 6783F747
P 7250 3900
F 0 "U2" H 7300 4000 30  0000 C CNN
F 1 "PORT" H 7250 3900 30  0000 C CNN
F 2 "" H 7250 3900 60  0000 C CNN
F 3 "" H 7250 3900 60  0000 C CNN
	2    7250 3900
	-1   0    0    1   
$EndComp
$Comp
L PORT U2
U 3 1 6783F790
P 7350 4300
F 0 "U2" H 7400 4400 30  0000 C CNN
F 1 "PORT" H 7350 4300 30  0000 C CNN
F 2 "" H 7350 4300 60  0000 C CNN
F 3 "" H 7350 4300 60  0000 C CNN
	3    7350 4300
	-1   0    0    1   
$EndComp
$Comp
L DC v1
U 1 1 679E3CD2
P 6900 2950
F 0 "v1" H 6700 3050 60  0000 C CNN
F 1 "53" H 6700 2900 60  0000 C CNN
F 2 "R1" H 6600 2950 60  0000 C CNN
F 3 "" H 6900 2950 60  0000 C CNN
	1    6900 2950
	0    -1   -1   0   
$EndComp
Wire Wire Line
	6450 2950 6300 2950
Connection ~ 6300 2950
$Comp
L eSim_GND #PWR03
U 1 1 679E3EBE
P 7400 3050
F 0 "#PWR03" H 7400 2800 50  0001 C CNN
F 1 "eSim_GND" H 7400 2900 50  0000 C CNN
F 2 "" H 7400 3050 50  0001 C CNN
F 3 "" H 7400 3050 50  0001 C CNN
	1    7400 3050
	1    0    0    -1  
$EndComp
Wire Wire Line
	7350 2950 7400 2950
Wire Wire Line
	7400 2950 7400 3050
$EndSCHEMATC
