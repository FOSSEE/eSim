EESchema Schematic File Version 2
LIBS:CMOS_Buf-rescue
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
LIBS:CMOS_Buf-cache
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
L PORT U1
U 1 1 68655FBD
P 3950 3050
F 0 "U1" H 4000 3150 30  0000 C CNN
F 1 "PORT" H 3950 3050 30  0000 C CNN
F 2 "" H 3950 3050 60  0000 C CNN
F 3 "" H 3950 3050 60  0000 C CNN
	1    3950 3050
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 3 1 68655FF0
P 4050 3300
F 0 "U1" H 4100 3400 30  0000 C CNN
F 1 "PORT" H 4050 3300 30  0000 C CNN
F 2 "" H 4050 3300 60  0000 C CNN
F 3 "" H 4050 3300 60  0000 C CNN
	3    4050 3300
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 2 1 68656163
P 3950 3550
F 0 "U1" H 4000 3650 30  0000 C CNN
F 1 "PORT" H 3950 3550 30  0000 C CNN
F 2 "" H 3950 3550 60  0000 C CNN
F 3 "" H 3950 3550 60  0000 C CNN
	2    3950 3550
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 4 1 68656242
P 7050 3300
F 0 "U1" H 7100 3400 30  0000 C CNN
F 1 "PORT" H 7050 3300 30  0000 C CNN
F 2 "" H 7050 3300 60  0000 C CNN
F 3 "" H 7050 3300 60  0000 C CNN
	4    7050 3300
	-1   0    0    -1  
$EndComp
$Comp
L SKY130mode scmode1
U 1 1 68656379
P 7900 4200
F 0 "scmode1" H 7900 4350 98  0000 C CNB
F 1 "SKY130mode" H 7900 4100 118 0000 C CNB
F 2 "" H 7900 4350 60  0001 C CNN
F 3 "" H 7900 4350 60  0001 C CNN
	1    7900 4200
	1    0    0    -1  
$EndComp
$Comp
L CMOS_INVTR X1
U 1 1 686A07F2
P 4700 3300
F 0 "X1" H 4700 3300 60  0000 C CNN
F 1 "CMOS_INVTR" H 4750 3100 60  0000 C CNN
F 2 "" H 4700 3300 60  0001 C CNN
F 3 "" H 4700 3300 60  0001 C CNN
	1    4700 3300
	1    0    0    -1  
$EndComp
$Comp
L CMOS_INVTR X2
U 1 1 686A0855
P 6250 3300
F 0 "X2" H 6250 3300 60  0000 C CNN
F 1 "CMOS_INVTR" H 6300 3100 60  0000 C CNN
F 2 "" H 6250 3300 60  0001 C CNN
F 3 "" H 6250 3300 60  0001 C CNN
	1    6250 3300
	1    0    0    -1  
$EndComp
Wire Wire Line
	5250 3300 5850 3300
Wire Wire Line
	4300 3050 4300 3200
Wire Wire Line
	4200 3050 5850 3050
Wire Wire Line
	5850 3050 5850 3200
Wire Wire Line
	4300 3400 4300 3550
Wire Wire Line
	5850 3550 4200 3550
Wire Wire Line
	5850 3400 5850 3550
Connection ~ 4300 3050
Connection ~ 4300 3550
$EndSCHEMATC
