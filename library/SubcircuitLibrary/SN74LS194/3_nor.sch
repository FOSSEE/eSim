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
L d_or U2
U 1 1 693D4349
P 4900 2850
F 0 "U2" H 4900 2850 60  0000 C CNN
F 1 "d_or" H 4900 2950 60  0000 C CNN
F 2 "" H 4900 2850 60  0000 C CNN
F 3 "" H 4900 2850 60  0000 C CNN
	1    4900 2850
	1    0    0    -1  
$EndComp
$Comp
L d_or U3
U 1 1 693D43A8
P 5250 3200
F 0 "U3" H 5250 3200 60  0000 C CNN
F 1 "d_or" H 5250 3300 60  0000 C CNN
F 2 "" H 5250 3200 60  0000 C CNN
F 3 "" H 5250 3200 60  0000 C CNN
	1    5250 3200
	1    0    0    -1  
$EndComp
$Comp
L d_inverter U4
U 1 1 693D4429
P 6200 3150
F 0 "U4" H 6200 3050 60  0000 C CNN
F 1 "d_inverter" H 6200 3300 60  0000 C CNN
F 2 "" H 6250 3100 60  0000 C CNN
F 3 "" H 6250 3100 60  0000 C CNN
	1    6200 3150
	1    0    0    -1  
$EndComp
Wire Wire Line
	4450 2750 4250 2750
Wire Wire Line
	4450 2850 4250 2850
Wire Wire Line
	5350 2800 5400 2800
Wire Wire Line
	5400 2800 5400 3000
Wire Wire Line
	5400 3000 4550 3000
Wire Wire Line
	4550 3000 4550 3100
Wire Wire Line
	4550 3100 4800 3100
Wire Wire Line
	4800 3200 4350 3200
Wire Wire Line
	5700 3150 5900 3150
Wire Wire Line
	6500 3150 6650 3150
$Comp
L PORT U1
U 4 1 693D44E1
P 6650 3400
F 0 "U1" H 6700 3500 30  0000 C CNN
F 1 "PORT" H 6650 3400 30  0000 C CNN
F 2 "" H 6650 3400 60  0000 C CNN
F 3 "" H 6650 3400 60  0000 C CNN
	4    6650 3400
	0    -1   -1   0   
$EndComp
$Comp
L PORT U1
U 3 1 693D4566
P 4100 3200
F 0 "U1" H 4150 3300 30  0000 C CNN
F 1 "PORT" H 4100 3200 30  0000 C CNN
F 2 "" H 4100 3200 60  0000 C CNN
F 3 "" H 4100 3200 60  0000 C CNN
	3    4100 3200
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 1 1 693D45B1
P 4000 2750
F 0 "U1" H 4050 2850 30  0000 C CNN
F 1 "PORT" H 4000 2750 30  0000 C CNN
F 2 "" H 4000 2750 60  0000 C CNN
F 3 "" H 4000 2750 60  0000 C CNN
	1    4000 2750
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 2 1 693D45E6
P 4000 2850
F 0 "U1" H 4050 2950 30  0000 C CNN
F 1 "PORT" H 4000 2850 30  0000 C CNN
F 2 "" H 4000 2850 60  0000 C CNN
F 3 "" H 4000 2850 60  0000 C CNN
	2    4000 2850
	1    0    0    -1  
$EndComp
$EndSCHEMATC
