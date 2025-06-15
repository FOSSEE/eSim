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
L d_nor U2
U 1 1 67ECC038
P 5250 3400
F 0 "U2" H 5250 3400 60  0000 C CNN
F 1 "d_nor" H 5300 3500 60  0000 C CNN
F 2 "" H 5250 3400 60  0000 C CNN
F 3 "" H 5250 3400 60  0000 C CNN
	1    5250 3400
	1    0    0    -1  
$EndComp
$Comp
L d_nor U3
U 1 1 67ECC07F
P 6150 3450
F 0 "U3" H 6150 3450 60  0000 C CNN
F 1 "d_nor" H 6200 3550 60  0000 C CNN
F 2 "" H 6150 3450 60  0000 C CNN
F 3 "" H 6150 3450 60  0000 C CNN
	1    6150 3450
	1    0    0    -1  
$EndComp
Wire Wire Line
	5700 3450 5550 3450
Wire Wire Line
	5550 3450 5550 3500
Wire Wire Line
	5550 3500 4800 3500
$Comp
L PORT U1
U 1 1 67ECC0BA
P 4550 3300
F 0 "U1" H 4600 3400 30  0000 C CNN
F 1 "PORT" H 4550 3300 30  0000 C CNN
F 2 "" H 4550 3300 60  0000 C CNN
F 3 "" H 4550 3300 60  0000 C CNN
	1    4550 3300
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 2 1 67ECC0FF
P 4550 3400
F 0 "U1" H 4600 3500 30  0000 C CNN
F 1 "PORT" H 4550 3400 30  0000 C CNN
F 2 "" H 4550 3400 60  0000 C CNN
F 3 "" H 4550 3400 60  0000 C CNN
	2    4550 3400
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 3 1 67ECC12C
P 4550 3500
F 0 "U1" H 4600 3600 30  0000 C CNN
F 1 "PORT" H 4550 3500 30  0000 C CNN
F 2 "" H 4550 3500 60  0000 C CNN
F 3 "" H 4550 3500 60  0000 C CNN
	3    4550 3500
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 4 1 67ECC14F
P 6850 3400
F 0 "U1" H 6900 3500 30  0000 C CNN
F 1 "PORT" H 6850 3400 30  0000 C CNN
F 2 "" H 6850 3400 60  0000 C CNN
F 3 "" H 6850 3400 60  0000 C CNN
	4    6850 3400
	-1   0    0    1   
$EndComp
$EndSCHEMATC
