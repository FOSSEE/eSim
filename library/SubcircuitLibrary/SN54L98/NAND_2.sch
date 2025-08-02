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
LIBS:NAND_2-cache
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
U 1 1 684AF0E9
P 4200 2050
F 0 "SC2" H 4250 2350 50  0000 C CNN
F 1 "sky130_fd_pr__pfet_01v8" H 4500 2137 50  0000 R CNN
F 2 "" H 4200 550 50  0001 C CNN
F 3 "" H 4200 2050 50  0001 C CNN
	1    4200 2050
	1    0    0    -1  
$EndComp
$Comp
L sky130_fd_pr__nfet_01v8 SC1
U 1 1 684AF1CF
P 4450 2850
F 0 "SC1" H 4500 3150 50  0000 C CNN
F 1 "sky130_fd_pr__nfet_01v8" H 4750 2937 50  0000 R CNN
F 2 "" H 4450 1350 50  0001 C CNN
F 3 "" H 4450 2850 50  0001 C CNN
	1    4450 2850
	1    0    0    -1  
$EndComp
$Comp
L sky130_fd_pr__nfet_01v8 SC4
U 1 1 684AF20C
P 4850 3550
F 0 "SC4" H 4900 3850 50  0000 C CNN
F 1 "sky130_fd_pr__nfet_01v8" H 5150 3637 50  0000 R CNN
F 2 "" H 4850 2050 50  0001 C CNN
F 3 "" H 4850 3550 50  0001 C CNN
	1    4850 3550
	-1   0    0    -1  
$EndComp
$Comp
L PORT U1
U 3 1 684AF271
P 4350 1550
F 0 "U1" H 4400 1650 30  0000 C CNN
F 1 "PORT" H 4350 1550 30  0000 C CNN
F 2 "" H 4350 1550 60  0000 C CNN
F 3 "" H 4350 1550 60  0000 C CNN
	3    4350 1550
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 1 1 684AF336
P 3550 2650
F 0 "U1" H 3600 2750 30  0000 C CNN
F 1 "PORT" H 3550 2650 30  0000 C CNN
F 2 "" H 3550 2650 60  0000 C CNN
F 3 "" H 3550 2650 60  0000 C CNN
	1    3550 2650
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 4 1 684AF413
P 5750 2450
F 0 "U1" H 5800 2550 30  0000 C CNN
F 1 "PORT" H 5750 2450 30  0000 C CNN
F 2 "" H 5750 2450 60  0000 C CNN
F 3 "" H 5750 2450 60  0000 C CNN
	4    5750 2450
	-1   0    0    -1  
$EndComp
$Comp
L PORT U1
U 5 1 684AF82C
P 5750 3300
F 0 "U1" H 5800 3400 30  0000 C CNN
F 1 "PORT" H 5750 3300 30  0000 C CNN
F 2 "" H 5750 3300 60  0000 C CNN
F 3 "" H 5750 3300 60  0000 C CNN
	5    5750 3300
	-1   0    0    -1  
$EndComp
$Comp
L PORT U1
U 2 1 684AF895
P 4400 4000
F 0 "U1" H 4450 4100 30  0000 C CNN
F 1 "PORT" H 4400 4000 30  0000 C CNN
F 2 "" H 4400 4000 60  0000 C CNN
F 3 "" H 4400 4000 60  0000 C CNN
	2    4400 4000
	1    0    0    -1  
$EndComp
$Comp
L SKY130mode scmode1
U 1 1 684AFD6B
P 7350 2150
F 0 "scmode1" H 7350 2300 98  0000 C CNB
F 1 "SKY130mode" H 7350 2050 118 0000 C CNB
F 2 "" H 7350 2300 60  0001 C CNN
F 3 "" H 7350 2300 60  0001 C CNN
	1    7350 2150
	1    0    0    -1  
$EndComp
$Comp
L sky130_fd_pr__pfet_01v8 SC3
U 1 1 684CF41D
P 5000 2050
F 0 "SC3" H 5050 2350 50  0000 C CNN
F 1 "sky130_fd_pr__pfet_01v8" H 5300 2137 50  0000 R CNN
F 2 "" H 5000 550 50  0001 C CNN
F 3 "" H 5000 2050 50  0001 C CNN
	1    5000 2050
	-1   0    0    -1  
$EndComp
Wire Wire Line
	4400 1750 4800 1750
Wire Wire Line
	4600 1550 4600 1750
Connection ~ 4600 1750
Wire Wire Line
	4300 2050 4450 2050
Wire Wire Line
	4450 2050 4450 1750
Connection ~ 4450 1750
Wire Wire Line
	4900 2050 4750 2050
Wire Wire Line
	4750 2050 4750 1750
Connection ~ 4750 1750
Wire Wire Line
	4400 2350 4800 2350
Wire Wire Line
	4650 2550 4650 2350
Connection ~ 4650 2350
Wire Wire Line
	5500 2450 4650 2450
Connection ~ 4650 2450
Wire Wire Line
	3900 2050 3900 2850
Wire Wire Line
	3900 2850 4150 2850
Wire Wire Line
	3800 2650 3900 2650
Connection ~ 3900 2650
Wire Wire Line
	5300 2050 5300 3550
Wire Wire Line
	5300 3550 5150 3550
Wire Wire Line
	5500 3300 5300 3300
Connection ~ 5300 3300
Wire Wire Line
	4550 2850 4700 2850
Wire Wire Line
	4700 2850 4700 3200
Wire Wire Line
	4700 3200 4650 3200
Wire Wire Line
	4650 3150 4650 3250
Connection ~ 4650 3200
Wire Wire Line
	4650 3850 4650 4000
Wire Wire Line
	4750 3550 4600 3550
Wire Wire Line
	4600 3550 4600 3900
Wire Wire Line
	4600 3900 4650 3900
Connection ~ 4650 3900
$EndSCHEMATC
