EESchema Schematic File Version 2
LIBS:CD4015BC_edge-rescue
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
LIBS:CD4015BC_edge-cache
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
Text GLabel 2250 1850 0    60   Input ~ 0
da
Text GLabel 2250 2150 0    60   Input ~ 0
clka
Text GLabel 2250 2700 0    60   Input ~ 0
ra
Wire Wire Line
	2250 1850 2400 1850
Wire Wire Line
	2250 2150 2400 2150
Wire Wire Line
	2250 2700 7900 2700
Connection ~ 2950 2700
Connection ~ 4650 2700
Connection ~ 6250 2700
Wire Wire Line
	3500 1850 4100 1850
Wire Wire Line
	5200 1850 5700 1850
Wire Wire Line
	6800 1850 7350 1850
Connection ~ 2350 2150
Text GLabel 2250 3650 0    60   Input ~ 0
db
Text GLabel 2250 3950 0    60   Input ~ 0
clkb
Text GLabel 2250 4500 0    60   Input ~ 0
rb
Wire Wire Line
	2250 3650 2400 3650
Wire Wire Line
	2250 3950 2400 3950
Wire Wire Line
	2250 4500 7900 4500
Connection ~ 2950 4500
Connection ~ 4650 4500
Connection ~ 6250 4500
Wire Wire Line
	3500 3650 4100 3650
Wire Wire Line
	5200 3650 5700 3650
Wire Wire Line
	6800 3650 7350 3650
Wire Wire Line
	2350 3950 2350 4600
Wire Wire Line
	2350 4600 7350 4600
Wire Wire Line
	4100 4600 4100 3950
Connection ~ 2350 3950
Wire Wire Line
	5700 4600 5700 3950
Connection ~ 4100 4600
Wire Wire Line
	7350 4600 7350 3950
Connection ~ 5700 4600
Text GLabel 3600 1850 1    60   Input ~ 0
qa1
Text GLabel 5300 1850 1    60   Input ~ 0
qa2
Text GLabel 6900 1850 1    60   Input ~ 0
qa3
Text GLabel 8550 1850 2    60   Input ~ 0
qa4
Wire Wire Line
	8450 1850 8550 1850
Text GLabel 3600 3650 1    60   Input ~ 0
qb1
Text GLabel 5300 3650 1    60   Input ~ 0
qb2
Text GLabel 6900 3650 1    60   Input ~ 0
qb3
Text GLabel 8550 3650 2    60   Input ~ 0
qb4
Wire Wire Line
	8450 3650 8550 3650
Wire Wire Line
	2350 2150 2350 2800
Wire Wire Line
	2350 2800 7350 2800
Wire Wire Line
	4100 2800 4100 2150
Wire Wire Line
	5700 2800 5700 2150
Connection ~ 4100 2800
Wire Wire Line
	7350 2800 7350 2150
Connection ~ 5700 2800
$Comp
L dff_edge X1
U 1 1 68066A43
P 2950 2150
F 0 "X1" H 2950 2150 60  0000 C CNN
F 1 "dff_edge" H 2950 2250 60  0000 C CNN
F 2 "" H 2950 2150 60  0001 C CNN
F 3 "" H 2950 2150 60  0001 C CNN
	1    2950 2150
	1    0    0    -1  
$EndComp
$Comp
L dff_edge X3
U 1 1 68066A7D
P 4650 2150
F 0 "X3" H 4650 2150 60  0000 C CNN
F 1 "dff_edge" H 4650 2250 60  0000 C CNN
F 2 "" H 4650 2150 60  0001 C CNN
F 3 "" H 4650 2150 60  0001 C CNN
	1    4650 2150
	1    0    0    -1  
$EndComp
$Comp
L dff_edge X5
U 1 1 68066A9A
P 6250 2150
F 0 "X5" H 6250 2150 60  0000 C CNN
F 1 "dff_edge" H 6250 2250 60  0000 C CNN
F 2 "" H 6250 2150 60  0001 C CNN
F 3 "" H 6250 2150 60  0001 C CNN
	1    6250 2150
	1    0    0    -1  
$EndComp
$Comp
L dff_edge X7
U 1 1 68066AFF
P 7900 2150
F 0 "X7" H 7900 2150 60  0000 C CNN
F 1 "dff_edge" H 7900 2250 60  0000 C CNN
F 2 "" H 7900 2150 60  0001 C CNN
F 3 "" H 7900 2150 60  0001 C CNN
	1    7900 2150
	1    0    0    -1  
$EndComp
$Comp
L dff_edge X2
U 1 1 68066B8E
P 2950 3950
F 0 "X2" H 2950 3950 60  0000 C CNN
F 1 "dff_edge" H 2950 4050 60  0000 C CNN
F 2 "" H 2950 3950 60  0001 C CNN
F 3 "" H 2950 3950 60  0001 C CNN
	1    2950 3950
	1    0    0    -1  
$EndComp
$Comp
L dff_edge X4
U 1 1 68066BF3
P 4650 3950
F 0 "X4" H 4650 3950 60  0000 C CNN
F 1 "dff_edge" H 4650 4050 60  0000 C CNN
F 2 "" H 4650 3950 60  0001 C CNN
F 3 "" H 4650 3950 60  0001 C CNN
	1    4650 3950
	1    0    0    -1  
$EndComp
$Comp
L dff_edge X6
U 1 1 68066C6E
P 6250 3950
F 0 "X6" H 6250 3950 60  0000 C CNN
F 1 "dff_edge" H 6250 4050 60  0000 C CNN
F 2 "" H 6250 3950 60  0001 C CNN
F 3 "" H 6250 3950 60  0001 C CNN
	1    6250 3950
	1    0    0    -1  
$EndComp
$Comp
L dff_edge X8
U 1 1 68066CA3
P 7900 3950
F 0 "X8" H 7900 3950 60  0000 C CNN
F 1 "dff_edge" H 7900 4050 60  0000 C CNN
F 2 "" H 7900 3950 60  0001 C CNN
F 3 "" H 7900 3950 60  0001 C CNN
	1    7900 3950
	1    0    0    -1  
$EndComp
$EndSCHEMATC
