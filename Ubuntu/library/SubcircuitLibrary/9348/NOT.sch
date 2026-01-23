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
LIBS:NOT-cache
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
L mosfet_n M1
U 1 1 66506BE9
P 5050 3000
F 0 "M1" H 5050 2850 50  0000 R CNN
F 1 "mosfet_n" H 5150 2950 50  0000 R CNN
F 2 "" H 5350 2700 29  0000 C CNN
F 3 "" H 5150 2800 60  0000 C CNN
	1    5050 3000
	1    0    0    -1  
$EndComp
$Comp
L mosfet_p M2
U 1 1 66506C9C
P 5100 2400
F 0 "M2" H 5050 2450 50  0000 R CNN
F 1 "mosfet_p" H 5150 2550 50  0000 R CNN
F 2 "" H 5350 2500 29  0000 C CNN
F 3 "" H 5150 2400 60  0000 C CNN
	1    5100 2400
	1    0    0    -1  
$EndComp
Wire Wire Line
	5250 2600 5250 3000
Wire Wire Line
	5350 2550 5500 2550
Wire Wire Line
	5500 2550 5500 2200
Wire Wire Line
	5500 2200 5250 2200
Wire Wire Line
	5250 3400 5250 3700
Wire Wire Line
	5350 3350 5350 3500
Wire Wire Line
	5350 3500 5250 3500
Connection ~ 5250 3500
Wire Wire Line
	5250 2200 5250 1600
Wire Wire Line
	4950 3200 4900 3200
Wire Wire Line
	4900 3200 4900 2400
Wire Wire Line
	4900 2400 4950 2400
Wire Wire Line
	5250 2800 5800 2800
Connection ~ 5250 2800
Wire Wire Line
	4900 2800 4500 2800
Connection ~ 4900 2800
$Comp
L PORT U1
U 1 1 66506E77
P 4250 2800
F 0 "U1" H 4300 2900 30  0000 C CNN
F 1 "PORT" H 4250 2800 30  0000 C CNN
F 2 "" H 4250 2800 60  0000 C CNN
F 3 "" H 4250 2800 60  0000 C CNN
	1    4250 2800
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 2 1 66506EC2
P 6050 2800
F 0 "U1" H 6100 2900 30  0000 C CNN
F 1 "PORT" H 6050 2800 30  0000 C CNN
F 2 "" H 6050 2800 60  0000 C CNN
F 3 "" H 6050 2800 60  0000 C CNN
	2    6050 2800
	-1   0    0    1   
$EndComp
$Comp
L PORT U1
U 3 1 665610BD
P 5000 1600
F 0 "U1" H 5050 1700 30  0000 C CNN
F 1 "PORT" H 5000 1600 30  0000 C CNN
F 2 "" H 5000 1600 60  0000 C CNN
F 3 "" H 5000 1600 60  0000 C CNN
	3    5000 1600
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 4 1 66561147
P 5000 3700
F 0 "U1" H 5050 3800 30  0000 C CNN
F 1 "PORT" H 5000 3700 30  0000 C CNN
F 2 "" H 5000 3700 60  0000 C CNN
F 3 "" H 5000 3700 60  0000 C CNN
	4    5000 3700
	1    0    0    -1  
$EndComp
$EndSCHEMATC
