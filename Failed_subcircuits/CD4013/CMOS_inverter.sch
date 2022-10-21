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
LIBS:CMOS_inverter-cache
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
L mosfet_p M2
U 1 1 62DA908D
P 5150 2200
F 0 "M2" H 5100 2250 50  0000 R CNN
F 1 "mosfet_p" H 5200 2350 50  0000 R CNN
F 2 "" H 5400 2300 29  0000 C CNN
F 3 "" H 5200 2200 60  0000 C CNN
	1    5150 2200
	1    0    0    1   
$EndComp
$Comp
L mosfet_n M1
U 1 1 62DA908E
P 5100 2800
F 0 "M1" H 5100 2650 50  0000 R CNN
F 1 "mosfet_n" H 5200 2750 50  0000 R CNN
F 2 "" H 5400 2500 29  0000 C CNN
F 3 "" H 5200 2600 60  0000 C CNN
	1    5100 2800
	1    0    0    -1  
$EndComp
Wire Wire Line
	5300 2000 5300 1650
Wire Wire Line
	5300 1800 5400 1800
Wire Wire Line
	5400 1800 5400 2050
Connection ~ 5300 1800
Wire Wire Line
	5300 3200 5300 3600
Wire Wire Line
	5400 3150 5400 3350
Wire Wire Line
	5400 3350 5300 3350
Connection ~ 5300 3350
Wire Wire Line
	5000 2200 4800 2200
Wire Wire Line
	4800 2200 4800 3000
Wire Wire Line
	4800 3000 5000 3000
Wire Wire Line
	5300 2400 5300 2800
Wire Wire Line
	5300 2600 5900 2600
Connection ~ 5300 2600
Wire Wire Line
	4800 2600 4300 2600
Connection ~ 4800 2600
$Comp
L PORT U1
U 2 1 62DA908F
P 5300 1400
F 0 "U1" H 5350 1500 30  0000 C CNN
F 1 "PORT" H 5300 1400 30  0000 C CNN
F 2 "" H 5300 1400 60  0000 C CNN
F 3 "" H 5300 1400 60  0000 C CNN
	2    5300 1400
	0    1    1    0   
$EndComp
$Comp
L PORT U1
U 3 1 62DA9090
P 5300 3850
F 0 "U1" H 5350 3950 30  0000 C CNN
F 1 "PORT" H 5300 3850 30  0000 C CNN
F 2 "" H 5300 3850 60  0000 C CNN
F 3 "" H 5300 3850 60  0000 C CNN
	3    5300 3850
	0    -1   -1   0   
$EndComp
$Comp
L PORT U1
U 1 1 62DA9091
P 4050 2600
F 0 "U1" H 4100 2700 30  0000 C CNN
F 1 "PORT" H 4050 2600 30  0000 C CNN
F 2 "" H 4050 2600 60  0000 C CNN
F 3 "" H 4050 2600 60  0000 C CNN
	1    4050 2600
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 4 1 62DA9092
P 6150 2600
F 0 "U1" H 6200 2700 30  0000 C CNN
F 1 "PORT" H 6150 2600 30  0000 C CNN
F 2 "" H 6150 2600 60  0000 C CNN
F 3 "" H 6150 2600 60  0000 C CNN
	4    6150 2600
	-1   0    0    1   
$EndComp
$EndSCHEMATC
