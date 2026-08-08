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
L eSim_Diode D1
U 1 1 6A1808C5
P 5900 2600
F 0 "D1" H 5900 2700 50  0000 C CNN
F 1 "eSim_Diode" H 5900 2500 50  0000 C CNN
F 2 "" H 5900 2600 60  0000 C CNN
F 3 "" H 5900 2600 60  0000 C CNN
	1    5900 2600
	1    0    0    -1  
$EndComp
$Comp
L sine v1
U 1 1 6A180913
P 5050 2600
F 0 "v1" H 4850 2700 60  0000 C CNN
F 1 "sine" H 4850 2550 60  0000 C CNN
F 2 "R1" H 4750 2600 60  0000 C CNN
F 3 "" H 5050 2600 60  0000 C CNN
	1    5050 2600
	0    1    1    0   
$EndComp
Wire Wire Line
	5500 2600 5750 2600
$Comp
L resistor R1
U 1 1 6A180948
P 6300 2650
F 0 "R1" H 6350 2780 50  0000 C CNN
F 1 "1k" H 6350 2600 50  0000 C CNN
F 2 "" H 6350 2630 30  0000 C CNN
F 3 "" V 6350 2700 30  0000 C CNN
	1    6300 2650
	1    0    0    -1  
$EndComp
$Comp
L eSim_GND #PWR2
U 1 1 6A18096F
P 6650 2600
F 0 "#PWR2" H 6650 2350 50  0001 C CNN
F 1 "eSim_GND" H 6650 2450 50  0000 C CNN
F 2 "" H 6650 2600 50  0001 C CNN
F 3 "" H 6650 2600 50  0001 C CNN
	1    6650 2600
	0    -1   -1   0   
$EndComp
Wire Wire Line
	6650 2600 6500 2600
Wire Wire Line
	6200 2600 6050 2600
$Comp
L eSim_GND #PWR1
U 1 1 6A180996
P 4500 2600
F 0 "#PWR1" H 4500 2350 50  0001 C CNN
F 1 "eSim_GND" H 4500 2450 50  0000 C CNN
F 2 "" H 4500 2600 50  0001 C CNN
F 3 "" H 4500 2600 50  0001 C CNN
	1    4500 2600
	0    1    1    0   
$EndComp
Wire Wire Line
	4500 2600 4600 2600
$Comp
L plot_v1 U1
U 1 1 6A1809B8
P 6100 2650
F 0 "U1" H 6100 3150 60  0000 C CNN
F 1 "plot_v1" H 6300 3000 60  0000 C CNN
F 2 "" H 6100 2650 60  0000 C CNN
F 3 "" H 6100 2650 60  0000 C CNN
	1    6100 2650
	1    0    0    -1  
$EndComp
Wire Wire Line
	6100 2450 6100 2600
Connection ~ 6100 2600
Text GLabel 5900 2350 0    60   Input ~ 0
out
Wire Wire Line
	5900 2350 6050 2350
Wire Wire Line
	6050 2350 6050 2500
Wire Wire Line
	6050 2500 6100 2500
Connection ~ 6100 2500
Text GLabel 5450 2200 0    60   Input ~ 0
in
Wire Wire Line
	5450 2200 5550 2200
Wire Wire Line
	5550 2200 5550 2600
Connection ~ 5550 2600
$Comp
L plot_v1 U2
U 1 1 6A180A5D
P 5550 2400
F 0 "U2" H 5550 2900 60  0000 C CNN
F 1 "plot_v1" H 5750 2750 60  0000 C CNN
F 2 "" H 5550 2400 60  0000 C CNN
F 3 "" H 5550 2400 60  0000 C CNN
	1    5550 2400
	1    0    0    -1  
$EndComp
$EndSCHEMATC
