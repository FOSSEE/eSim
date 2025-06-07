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
L d_inverter U?
U 1 1 6810D6D0
P 4750 2900
F 0 "U?" H 4750 2800 60  0000 C CNN
F 1 "d_inverter" H 4750 3050 60  0000 C CNN
F 2 "" H 4800 2850 60  0000 C CNN
F 3 "" H 4800 2850 60  0000 C CNN
	1    4750 2900
	1    0    0    -1  
$EndComp
$Comp
L d_inverter U?
U 1 1 6810D6FB
P 4750 3650
F 0 "U?" H 4750 3550 60  0000 C CNN
F 1 "d_inverter" H 4750 3800 60  0000 C CNN
F 2 "" H 4800 3600 60  0000 C CNN
F 3 "" H 4800 3600 60  0000 C CNN
	1    4750 3650
	1    0    0    -1  
$EndComp
$Comp
L d_inverter U?
U 1 1 6810D736
P 4750 4350
F 0 "U?" H 4750 4250 60  0000 C CNN
F 1 "d_inverter" H 4750 4500 60  0000 C CNN
F 2 "" H 4800 4300 60  0000 C CNN
F 3 "" H 4800 4300 60  0000 C CNN
	1    4750 4350
	1    0    0    -1  
$EndComp
$Comp
L d_and U?
U 1 1 6810D763
P 6800 3000
F 0 "U?" H 6800 3000 60  0000 C CNN
F 1 "d_and" H 6850 3100 60  0000 C CNN
F 2 "" H 6800 3000 60  0000 C CNN
F 3 "" H 6800 3000 60  0000 C CNN
	1    6800 3000
	1    0    0    -1  
$EndComp
$Comp
L d_inverter U?
U 1 1 6810D7A6
P 6400 3700
F 0 "U?" H 6400 3600 60  0000 C CNN
F 1 "d_inverter" H 6400 3850 60  0000 C CNN
F 2 "" H 6450 3650 60  0000 C CNN
F 3 "" H 6450 3650 60  0000 C CNN
	1    6400 3700
	1    0    0    -1  
$EndComp
$Comp
L d_inverter U?
U 1 1 6810D7E7
P 6400 4050
F 0 "U?" H 6400 3950 60  0000 C CNN
F 1 "d_inverter" H 6400 4200 60  0000 C CNN
F 2 "" H 6450 4000 60  0000 C CNN
F 3 "" H 6450 4000 60  0000 C CNN
	1    6400 4050
	1    0    0    -1  
$EndComp
$Comp
L d_and U?
U 1 1 6810D820
P 7300 3900
F 0 "U?" H 7300 3900 60  0000 C CNN
F 1 "d_and" H 7350 4000 60  0000 C CNN
F 2 "" H 7300 3900 60  0000 C CNN
F 3 "" H 7300 3900 60  0000 C CNN
	1    7300 3900
	1    0    0    -1  
$EndComp
$Comp
L d_or U?
U 1 1 6810D85F
P 8400 3400
F 0 "U?" H 8400 3400 60  0000 C CNN
F 1 "d_or" H 8400 3500 60  0000 C CNN
F 2 "" H 8400 3400 60  0000 C CNN
F 3 "" H 8400 3400 60  0000 C CNN
	1    8400 3400
	1    0    0    -1  
$EndComp
Wire Wire Line
	5050 2900 6350 2900
Wire Wire Line
	6700 3700 6850 3700
Wire Wire Line
	6850 3700 6850 3800
Wire Wire Line
	6700 4050 6850 4050
Wire Wire Line
	6850 4050 6850 3900
Wire Wire Line
	5050 3650 6100 3650
Wire Wire Line
	6100 3650 6100 3700
Wire Wire Line
	5050 4350 5750 4350
Wire Wire Line
	5750 4350 5750 3000
Wire Wire Line
	5750 3000 6350 3000
Wire Wire Line
	6100 4050 5750 4050
Connection ~ 5750 4050
Wire Wire Line
	7750 3850 7850 3850
Wire Wire Line
	7850 3850 7850 3400
Wire Wire Line
	7850 3400 7950 3400
Wire Wire Line
	7250 2950 7450 2950
Wire Wire Line
	7450 2950 7450 3300
Wire Wire Line
	7450 3300 7950 3300
Wire Wire Line
	8850 3350 9100 3350
Wire Wire Line
	4450 2900 4300 2900
Wire Wire Line
	4450 3650 4350 3650
Wire Wire Line
	4450 4350 4400 4350
$Comp
L PORT U?
U 1 1 6810D9AE
P 4050 2900
F 0 "U?" H 4100 3000 30  0000 C CNN
F 1 "PORT" H 4050 2900 30  0000 C CNN
F 2 "" H 4050 2900 60  0000 C CNN
F 3 "" H 4050 2900 60  0000 C CNN
	1    4050 2900
	1    0    0    -1  
$EndComp
$Comp
L PORT U?
U 2 1 6810D9F3
P 4100 3650
F 0 "U?" H 4150 3750 30  0000 C CNN
F 1 "PORT" H 4100 3650 30  0000 C CNN
F 2 "" H 4100 3650 60  0000 C CNN
F 3 "" H 4100 3650 60  0000 C CNN
	2    4100 3650
	1    0    0    -1  
$EndComp
$Comp
L PORT U?
U 3 1 6810DA26
P 4150 4350
F 0 "U?" H 4200 4450 30  0000 C CNN
F 1 "PORT" H 4150 4350 30  0000 C CNN
F 2 "" H 4150 4350 60  0000 C CNN
F 3 "" H 4150 4350 60  0000 C CNN
	3    4150 4350
	1    0    0    -1  
$EndComp
$Comp
L PORT U?
U 4 1 6810DAAE
P 9350 3350
F 0 "U?" H 9400 3450 30  0000 C CNN
F 1 "PORT" H 9350 3350 30  0000 C CNN
F 2 "" H 9350 3350 60  0000 C CNN
F 3 "" H 9350 3350 60  0000 C CNN
	4    9350 3350
	-1   0    0    1   
$EndComp
$EndSCHEMATC
