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
L 74HC58 X1
U 1 1 68642DFD
P 6750 3850
F 0 "X1" H 6850 3050 60  0000 C CNN
F 1 "74HC58" H 6800 4450 60  0000 C CNN
F 2 "" H 6750 3850 60  0001 C CNN
F 3 "" H 6750 3850 60  0001 C CNN
	1    6750 3850
	1    0    0    -1  
$EndComp
$Comp
L adc_bridge_6 U12
U 1 1 68642E14
P 5250 3450
F 0 "U12" H 5250 3450 60  0000 C CNN
F 1 "adc_bridge_6" H 5250 3600 60  0000 C CNN
F 2 "" H 5250 3450 60  0000 C CNN
F 3 "" H 5250 3450 60  0000 C CNN
	1    5250 3450
	1    0    0    -1  
$EndComp
$Comp
L adc_bridge_4 U11
U 1 1 68642E45
P 5200 4400
F 0 "U11" H 5200 4400 60  0000 C CNN
F 1 "adc_bridge_4" H 5200 4700 60  0000 C CNN
F 2 "" H 5200 4400 60  0000 C CNN
F 3 "" H 5200 4400 60  0000 C CNN
	1    5200 4400
	1    0    0    -1  
$EndComp
$Comp
L dac_bridge_1 U13
U 1 1 68642E8D
P 8250 3500
F 0 "U13" H 8250 3500 60  0000 C CNN
F 1 "dac_bridge_1" H 8250 3650 60  0000 C CNN
F 2 "" H 8250 3500 60  0000 C CNN
F 3 "" H 8250 3500 60  0000 C CNN
	1    8250 3500
	1    0    0    -1  
$EndComp
$Comp
L dac_bridge_1 U14
U 1 1 68642EC6
P 8250 4250
F 0 "U14" H 8250 4250 60  0000 C CNN
F 1 "dac_bridge_1" H 8250 4400 60  0000 C CNN
F 2 "" H 8250 4250 60  0000 C CNN
F 3 "" H 8250 4250 60  0000 C CNN
	1    8250 4250
	1    0    0    -1  
$EndComp
$Comp
L pulse v1
U 1 1 68642F00
P 1200 2750
F 0 "v1" H 1000 2850 60  0000 C CNN
F 1 "pulse" H 1000 2700 60  0000 C CNN
F 2 "R1" H 900 2750 60  0000 C CNN
F 3 "" H 1200 2750 60  0000 C CNN
	1    1200 2750
	0    1    1    0   
$EndComp
$Comp
L pulse v2
U 1 1 68642F8B
P 1200 3100
F 0 "v2" H 1000 3200 60  0000 C CNN
F 1 "pulse" H 1000 3050 60  0000 C CNN
F 2 "R1" H 900 3100 60  0000 C CNN
F 3 "" H 1200 3100 60  0000 C CNN
	1    1200 3100
	0    1    1    0   
$EndComp
$Comp
L pulse v3
U 1 1 68642FC2
P 1200 3450
F 0 "v3" H 1000 3550 60  0000 C CNN
F 1 "pulse" H 1000 3400 60  0000 C CNN
F 2 "R1" H 900 3450 60  0000 C CNN
F 3 "" H 1200 3450 60  0000 C CNN
	1    1200 3450
	0    1    1    0   
$EndComp
$Comp
L pulse v4
U 1 1 68642FF8
P 1200 3800
F 0 "v4" H 1000 3900 60  0000 C CNN
F 1 "pulse" H 1000 3750 60  0000 C CNN
F 2 "R1" H 900 3800 60  0000 C CNN
F 3 "" H 1200 3800 60  0000 C CNN
	1    1200 3800
	0    1    1    0   
$EndComp
$Comp
L pulse v5
U 1 1 68643031
P 1200 4150
F 0 "v5" H 1000 4250 60  0000 C CNN
F 1 "pulse" H 1000 4100 60  0000 C CNN
F 2 "R1" H 900 4150 60  0000 C CNN
F 3 "" H 1200 4150 60  0000 C CNN
	1    1200 4150
	0    1    1    0   
$EndComp
$Comp
L pulse v6
U 1 1 68643077
P 1200 4500
F 0 "v6" H 1000 4600 60  0000 C CNN
F 1 "pulse" H 1000 4450 60  0000 C CNN
F 2 "R1" H 900 4500 60  0000 C CNN
F 3 "" H 1200 4500 60  0000 C CNN
	1    1200 4500
	0    1    1    0   
$EndComp
$Comp
L pulse v7
U 1 1 686430BA
P 1200 4850
F 0 "v7" H 1000 4950 60  0000 C CNN
F 1 "pulse" H 1000 4800 60  0000 C CNN
F 2 "R1" H 900 4850 60  0000 C CNN
F 3 "" H 1200 4850 60  0000 C CNN
	1    1200 4850
	0    1    1    0   
$EndComp
$Comp
L pulse v8
U 1 1 68643108
P 1200 5200
F 0 "v8" H 1000 5300 60  0000 C CNN
F 1 "pulse" H 1000 5150 60  0000 C CNN
F 2 "R1" H 900 5200 60  0000 C CNN
F 3 "" H 1200 5200 60  0000 C CNN
	1    1200 5200
	0    1    1    0   
$EndComp
$Comp
L pulse v9
U 1 1 6864314D
P 1200 5600
F 0 "v9" H 1000 5700 60  0000 C CNN
F 1 "pulse" H 1000 5550 60  0000 C CNN
F 2 "R1" H 900 5600 60  0000 C CNN
F 3 "" H 1200 5600 60  0000 C CNN
	1    1200 5600
	0    1    1    0   
$EndComp
$Comp
L pulse v10
U 1 1 686431CD
P 1200 5950
F 0 "v10" H 1000 6050 60  0000 C CNN
F 1 "pulse" H 1000 5900 60  0000 C CNN
F 2 "R1" H 900 5950 60  0000 C CNN
F 3 "" H 1200 5950 60  0000 C CNN
	1    1200 5950
	0    1    1    0   
$EndComp
$Comp
L plot_v1 U15
U 1 1 68643A22
P 9100 3450
F 0 "U15" H 9100 3950 60  0000 C CNN
F 1 "plot_v1" H 9300 3800 60  0000 C CNN
F 2 "" H 9100 3450 60  0000 C CNN
F 3 "" H 9100 3450 60  0000 C CNN
	1    9100 3450
	0    1    1    0   
$EndComp
$Comp
L plot_v1 U16
U 1 1 68643AD5
P 9150 4200
F 0 "U16" H 9150 4700 60  0000 C CNN
F 1 "plot_v1" H 9350 4550 60  0000 C CNN
F 2 "" H 9150 4200 60  0000 C CNN
F 3 "" H 9150 4200 60  0000 C CNN
	1    9150 4200
	0    1    1    0   
$EndComp
$Comp
L plot_v1 U1
U 1 1 68643C77
P 1750 1100
F 0 "U1" H 1750 1600 60  0000 C CNN
F 1 "plot_v1" H 1950 1450 60  0000 C CNN
F 2 "" H 1750 1100 60  0000 C CNN
F 3 "" H 1750 1100 60  0000 C CNN
	1    1750 1100
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U2
U 1 1 68643E17
P 2000 1100
F 0 "U2" H 2000 1600 60  0000 C CNN
F 1 "plot_v1" H 2200 1450 60  0000 C CNN
F 2 "" H 2000 1100 60  0000 C CNN
F 3 "" H 2000 1100 60  0000 C CNN
	1    2000 1100
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U3
U 1 1 68643E66
P 2250 1100
F 0 "U3" H 2250 1600 60  0000 C CNN
F 1 "plot_v1" H 2450 1450 60  0000 C CNN
F 2 "" H 2250 1100 60  0000 C CNN
F 3 "" H 2250 1100 60  0000 C CNN
	1    2250 1100
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U4
U 1 1 68643EBC
P 2500 1100
F 0 "U4" H 2500 1600 60  0000 C CNN
F 1 "plot_v1" H 2700 1450 60  0000 C CNN
F 2 "" H 2500 1100 60  0000 C CNN
F 3 "" H 2500 1100 60  0000 C CNN
	1    2500 1100
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U5
U 1 1 68643F21
P 2750 1100
F 0 "U5" H 2750 1600 60  0000 C CNN
F 1 "plot_v1" H 2950 1450 60  0000 C CNN
F 2 "" H 2750 1100 60  0000 C CNN
F 3 "" H 2750 1100 60  0000 C CNN
	1    2750 1100
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U6
U 1 1 68643F79
P 3000 1100
F 0 "U6" H 3000 1600 60  0000 C CNN
F 1 "plot_v1" H 3200 1450 60  0000 C CNN
F 2 "" H 3000 1100 60  0000 C CNN
F 3 "" H 3000 1100 60  0000 C CNN
	1    3000 1100
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U7
U 1 1 68643FD8
P 3250 1100
F 0 "U7" H 3250 1600 60  0000 C CNN
F 1 "plot_v1" H 3450 1450 60  0000 C CNN
F 2 "" H 3250 1100 60  0000 C CNN
F 3 "" H 3250 1100 60  0000 C CNN
	1    3250 1100
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U8
U 1 1 68644036
P 3500 1100
F 0 "U8" H 3500 1600 60  0000 C CNN
F 1 "plot_v1" H 3700 1450 60  0000 C CNN
F 2 "" H 3500 1100 60  0000 C CNN
F 3 "" H 3500 1100 60  0000 C CNN
	1    3500 1100
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U9
U 1 1 686440A1
P 3750 1100
F 0 "U9" H 3750 1600 60  0000 C CNN
F 1 "plot_v1" H 3950 1450 60  0000 C CNN
F 2 "" H 3750 1100 60  0000 C CNN
F 3 "" H 3750 1100 60  0000 C CNN
	1    3750 1100
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U10
U 1 1 68644109
P 4000 1100
F 0 "U10" H 4000 1600 60  0000 C CNN
F 1 "plot_v1" H 4200 1450 60  0000 C CNN
F 2 "" H 4000 1100 60  0000 C CNN
F 3 "" H 4000 1100 60  0000 C CNN
	1    4000 1100
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR01
U 1 1 68646726
P 750 2850
F 0 "#PWR01" H 750 2600 50  0001 C CNN
F 1 "GND" H 750 2700 50  0000 C CNN
F 2 "" H 750 2850 50  0001 C CNN
F 3 "" H 750 2850 50  0001 C CNN
	1    750  2850
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR02
U 1 1 68646789
P 750 3200
F 0 "#PWR02" H 750 2950 50  0001 C CNN
F 1 "GND" H 750 3050 50  0000 C CNN
F 2 "" H 750 3200 50  0001 C CNN
F 3 "" H 750 3200 50  0001 C CNN
	1    750  3200
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR03
U 1 1 686467E5
P 750 3550
F 0 "#PWR03" H 750 3300 50  0001 C CNN
F 1 "GND" H 750 3400 50  0000 C CNN
F 2 "" H 750 3550 50  0001 C CNN
F 3 "" H 750 3550 50  0001 C CNN
	1    750  3550
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR04
U 1 1 68646841
P 750 3900
F 0 "#PWR04" H 750 3650 50  0001 C CNN
F 1 "GND" H 750 3750 50  0000 C CNN
F 2 "" H 750 3900 50  0001 C CNN
F 3 "" H 750 3900 50  0001 C CNN
	1    750  3900
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR05
U 1 1 6864689D
P 750 4250
F 0 "#PWR05" H 750 4000 50  0001 C CNN
F 1 "GND" H 750 4100 50  0000 C CNN
F 2 "" H 750 4250 50  0001 C CNN
F 3 "" H 750 4250 50  0001 C CNN
	1    750  4250
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR06
U 1 1 6864692F
P 750 4600
F 0 "#PWR06" H 750 4350 50  0001 C CNN
F 1 "GND" H 750 4450 50  0000 C CNN
F 2 "" H 750 4600 50  0001 C CNN
F 3 "" H 750 4600 50  0001 C CNN
	1    750  4600
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR07
U 1 1 6864698B
P 750 4950
F 0 "#PWR07" H 750 4700 50  0001 C CNN
F 1 "GND" H 750 4800 50  0000 C CNN
F 2 "" H 750 4950 50  0001 C CNN
F 3 "" H 750 4950 50  0001 C CNN
	1    750  4950
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR08
U 1 1 686469E7
P 750 5300
F 0 "#PWR08" H 750 5050 50  0001 C CNN
F 1 "GND" H 750 5150 50  0000 C CNN
F 2 "" H 750 5300 50  0001 C CNN
F 3 "" H 750 5300 50  0001 C CNN
	1    750  5300
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR09
U 1 1 68646A43
P 750 5700
F 0 "#PWR09" H 750 5450 50  0001 C CNN
F 1 "GND" H 750 5550 50  0000 C CNN
F 2 "" H 750 5700 50  0001 C CNN
F 3 "" H 750 5700 50  0001 C CNN
	1    750  5700
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR010
U 1 1 68646AF0
P 750 6050
F 0 "#PWR010" H 750 5800 50  0001 C CNN
F 1 "GND" H 750 5900 50  0000 C CNN
F 2 "" H 750 6050 50  0001 C CNN
F 3 "" H 750 6050 50  0001 C CNN
	1    750  6050
	1    0    0    -1  
$EndComp
Text GLabel 9000 3050 1    60   Input ~ 0
Y1
Wire Wire Line
	1650 2750 4650 2750
Wire Wire Line
	4650 2750 4650 3400
Wire Wire Line
	1650 3100 4550 3100
Wire Wire Line
	4550 3100 4550 3500
Wire Wire Line
	4550 3500 4650 3500
Wire Wire Line
	1650 3450 4450 3450
Wire Wire Line
	4450 3450 4450 3600
Wire Wire Line
	4450 3600 4650 3600
Wire Wire Line
	4650 3700 4450 3700
Wire Wire Line
	4450 3700 4450 3800
Wire Wire Line
	4450 3800 1650 3800
Wire Wire Line
	4650 3800 4500 3800
Wire Wire Line
	4500 3800 4500 4150
Wire Wire Line
	4500 4150 1650 4150
Wire Wire Line
	4650 3900 2500 3900
Wire Wire Line
	2500 3900 2500 4500
Wire Wire Line
	1650 4850 2650 4850
Wire Wire Line
	2650 4850 2650 4200
Wire Wire Line
	2650 4200 4650 4200
Wire Wire Line
	4650 4300 2800 4300
Wire Wire Line
	2800 4300 2800 5200
Wire Wire Line
	2800 5200 1650 5200
Wire Wire Line
	1650 5600 2950 5600
Wire Wire Line
	2950 5600 2950 4400
Wire Wire Line
	2950 4400 4650 4400
Wire Wire Line
	4650 4500 3100 4500
Wire Wire Line
	3100 4500 3100 5950
Wire Wire Line
	3100 5950 1650 5950
Wire Wire Line
	5800 3400 6100 3400
Wire Wire Line
	6100 3500 5800 3500
Wire Wire Line
	5800 3600 6100 3600
Wire Wire Line
	6100 3700 5800 3700
Wire Wire Line
	5800 3800 6100 3800
Wire Wire Line
	6100 3900 5800 3900
Wire Wire Line
	5750 4200 6100 4200
Wire Wire Line
	6100 4300 5750 4300
Wire Wire Line
	5750 4400 6100 4400
Wire Wire Line
	6100 4500 5750 4500
Wire Wire Line
	7450 3800 7450 3450
Wire Wire Line
	7450 3450 7650 3450
Wire Wire Line
	7450 4050 7450 4200
Wire Wire Line
	7450 4200 7650 4200
Wire Wire Line
	8800 3450 9300 3450
Wire Wire Line
	9350 4200 8800 4200
Wire Wire Line
	2500 4500 1650 4500
Wire Wire Line
	1750 900  1750 2750
Connection ~ 1750 2750
Wire Wire Line
	2000 900  2000 3100
Connection ~ 2000 3100
Wire Wire Line
	2250 900  2250 3450
Connection ~ 2250 3450
Wire Wire Line
	2500 900  2500 3800
Connection ~ 2500 3800
Wire Wire Line
	2750 900  2750 4150
Connection ~ 2750 4150
Wire Wire Line
	3000 900  3000 3900
Connection ~ 3000 3900
Wire Wire Line
	3250 900  3250 4200
Connection ~ 3250 4200
Wire Wire Line
	3500 900  3500 4300
Connection ~ 3500 4300
Wire Wire Line
	3750 900  3750 4400
Connection ~ 3750 4400
Wire Wire Line
	4000 900  4000 4500
Connection ~ 4000 4500
Wire Wire Line
	750  5950 750  6050
Wire Wire Line
	750  5600 750  5700
Wire Wire Line
	750  5300 750  5200
Wire Wire Line
	750  4950 750  4850
Wire Wire Line
	750  4250 750  4150
Wire Wire Line
	750  4500 750  4600
Wire Wire Line
	750  3900 750  3800
Wire Wire Line
	750  3550 750  3450
Wire Wire Line
	750  3200 750  3100
Wire Wire Line
	750  2850 750  2750
Wire Wire Line
	9000 3050 9000 3450
Connection ~ 9000 3450
Text GLabel 9050 4800 3    60   Input ~ 0
Y2
Wire Wire Line
	9050 4800 9050 4200
Connection ~ 9050 4200
Text GLabel 900  950  0    60   Input ~ 0
A1
Text GLabel 900  1100 0    60   Input ~ 0
B1
Text GLabel 900  1250 0    60   Input ~ 0
C1
Text GLabel 900  1400 0    60   Input ~ 0
D1
Text GLabel 900  1550 0    60   Input ~ 0
E1
Text GLabel 900  1700 0    60   Input ~ 0
F1
Text GLabel 900  1900 0    60   Input ~ 0
A2
Text GLabel 900  2050 0    60   Input ~ 0
B2
Text GLabel 900  2200 0    60   Input ~ 0
C2
Text GLabel 900  2350 0    60   Input ~ 0
D2
Wire Wire Line
	900  950  1750 950 
Connection ~ 1750 950 
Wire Wire Line
	900  1100 2000 1100
Connection ~ 2000 1100
Wire Wire Line
	900  1250 2250 1250
Connection ~ 2250 1250
Wire Wire Line
	900  1400 2500 1400
Connection ~ 2500 1400
Wire Wire Line
	900  1550 2750 1550
Connection ~ 2750 1550
Wire Wire Line
	900  1700 3000 1700
Connection ~ 3000 1700
Wire Wire Line
	900  1900 3250 1900
Connection ~ 3250 1900
Wire Wire Line
	900  2050 3500 2050
Connection ~ 3500 2050
Wire Wire Line
	900  2200 3750 2200
Connection ~ 3750 2200
Wire Wire Line
	900  2350 4000 2350
Connection ~ 4000 2350
$EndSCHEMATC
