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
LIBS:device
LIBS:transistors
LIBS:conn
LIBS:linear
LIBS:regul
LIBS:74xx
LIBS:cmos4000
LIBS:eSim_Analog
LIBS:eSim_Devices
LIBS:eSim_Digital
LIBS:eSim_Hybrid
LIBS:eSim_Miscellaneous
LIBS:eSim_PSpice
LIBS:eSim_Plot
LIBS:eSim_Power
LIBS:eSim_Sources
LIBS:eSim_Subckt
LIBS:eSim_User
LIBS:d_source-cache
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
L d_source U1
U 1 1 5D1B0712
P 3000 4100
F 0 "U1" H 3000 4100 60  0000 C CNN
F 1 "d_source" H 3000 4200 60  0000 C CNN
F 2 "" H 3000 4100 60  0000 C CNN
F 3 "" H 3000 4100 60  0000 C CNN
	1    3000 4100
	1    0    0    -1  
$EndComp
$Comp
L dac_bridge_4 U2
U 1 1 5D1B0713
P 4750 4050
F 0 "U2" H 4750 4050 60  0000 C CNN
F 1 "dac_bridge_4" H 4750 4350 60  0000 C CNN
F 2 "" H 4750 4050 60  0000 C CNN
F 3 "" H 4750 4050 60  0000 C CNN
	1    4750 4050
	1    0    0    -1  
$EndComp
Wire Wire Line
	4200 3850 3650 3850
Wire Wire Line
	3650 3850 3650 3950
Wire Wire Line
	3650 4000 3850 4000
Wire Wire Line
	3850 4000 3850 3950
Wire Wire Line
	3850 3950 4200 3950
Wire Wire Line
	3650 4050 4200 4050
Wire Wire Line
	3650 4100 3650 4150
Wire Wire Line
	3650 4150 4200 4150
$Comp
L plot_v1 U3
U 1 1 5D1B0714
P 5700 3300
F 0 "U3" H 5700 3800 60  0000 C CNN
F 1 "plot_v1" H 5900 3650 60  0000 C CNN
F 2 "" H 5700 3300 60  0000 C CNN
F 3 "" H 5700 3300 60  0000 C CNN
	1    5700 3300
	0    1    1    0   
$EndComp
$Comp
L plot_v1 U4
U 1 1 5D1B0715
P 5700 3650
F 0 "U4" H 5700 4150 60  0000 C CNN
F 1 "plot_v1" H 5900 4000 60  0000 C CNN
F 2 "" H 5700 3650 60  0000 C CNN
F 3 "" H 5700 3650 60  0000 C CNN
	1    5700 3650
	0    1    1    0   
$EndComp
$Comp
L plot_v1 U5
U 1 1 5D1B0716
P 5700 3950
F 0 "U5" H 5700 4450 60  0000 C CNN
F 1 "plot_v1" H 5900 4300 60  0000 C CNN
F 2 "" H 5700 3950 60  0000 C CNN
F 3 "" H 5700 3950 60  0000 C CNN
	1    5700 3950
	0    1    1    0   
$EndComp
$Comp
L plot_v1 U6
U 1 1 5D1B0717
P 5700 4250
F 0 "U6" H 5700 4750 60  0000 C CNN
F 1 "plot_v1" H 5900 4600 60  0000 C CNN
F 2 "" H 5700 4250 60  0000 C CNN
F 3 "" H 5700 4250 60  0000 C CNN
	1    5700 4250
	0    1    1    0   
$EndComp
Wire Wire Line
	5900 4250 5600 4250
Wire Wire Line
	5600 4250 5600 4150
Wire Wire Line
	5600 4150 5300 4150
Wire Wire Line
	5900 3950 5650 3950
Wire Wire Line
	5650 3950 5650 4050
Wire Wire Line
	5650 4050 5300 4050
Wire Wire Line
	5300 3950 5550 3950
Wire Wire Line
	5550 3950 5550 3650
Wire Wire Line
	5550 3650 5900 3650
Wire Wire Line
	5300 3850 5400 3850
Wire Wire Line
	5400 3850 5400 3300
Wire Wire Line
	5400 3300 5900 3300
Text GLabel 5750 3150 1    60   Output ~ 0
out1
Text GLabel 5750 3600 1    60   Output ~ 0
out2
Text GLabel 5800 3900 1    60   Output ~ 0
out3
Text GLabel 5750 4350 3    60   Output ~ 0
out4
Wire Wire Line
	5750 4350 5750 4250
Connection ~ 5750 4250
Wire Wire Line
	5800 3900 5800 3950
Connection ~ 5800 3950
Wire Wire Line
	5750 3600 5750 3650
Connection ~ 5750 3650
Wire Wire Line
	5750 3150 5750 3300
Connection ~ 5750 3300
$EndSCHEMATC
