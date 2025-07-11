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
L d_dff U7
U 1 1 6848332B
P 3300 4150
F 0 "U7" H 3300 4150 60  0000 C CNN
F 1 "d_dff" H 3300 4300 60  0000 C CNN
F 2 "" H 3300 4150 60  0000 C CNN
F 3 "" H 3300 4150 60  0000 C CNN
	1    3300 4150
	1    0    0    -1  
$EndComp
$Comp
L d_dff U17
U 1 1 68483390
P 4800 4150
F 0 "U17" H 4800 4150 60  0000 C CNN
F 1 "d_dff" H 4800 4300 60  0000 C CNN
F 2 "" H 4800 4150 60  0000 C CNN
F 3 "" H 4800 4150 60  0000 C CNN
	1    4800 4150
	1    0    0    -1  
$EndComp
$Comp
L d_dff U23
U 1 1 684833D7
P 6350 4150
F 0 "U23" H 6350 4150 60  0000 C CNN
F 1 "d_dff" H 6350 4300 60  0000 C CNN
F 2 "" H 6350 4150 60  0000 C CNN
F 3 "" H 6350 4150 60  0000 C CNN
	1    6350 4150
	1    0    0    -1  
$EndComp
$Comp
L d_dff U27
U 1 1 6848340C
P 7950 4150
F 0 "U27" H 7950 4150 60  0000 C CNN
F 1 "d_dff" H 7950 4300 60  0000 C CNN
F 2 "" H 7950 4150 60  0000 C CNN
F 3 "" H 7950 4150 60  0000 C CNN
	1    7950 4150
	1    0    0    -1  
$EndComp
$Comp
L d_inverter U2
U 1 1 68483465
P 1600 5000
F 0 "U2" H 1600 4900 60  0000 C CNN
F 1 "d_inverter" H 1600 5150 60  0000 C CNN
F 2 "" H 1650 4950 60  0000 C CNN
F 3 "" H 1650 4950 60  0000 C CNN
	1    1600 5000
	1    0    0    -1  
$EndComp
$Comp
L d_inverter U3
U 1 1 684834F0
P 2300 5000
F 0 "U3" H 2300 4900 60  0000 C CNN
F 1 "d_inverter" H 2300 5150 60  0000 C CNN
F 2 "" H 2350 4950 60  0000 C CNN
F 3 "" H 2350 4950 60  0000 C CNN
	1    2300 5000
	1    0    0    -1  
$EndComp
$Comp
L d_inverter U9
U 1 1 684835E3
P 3550 6900
F 0 "U9" H 3550 6800 60  0000 C CNN
F 1 "d_inverter" H 3550 7050 60  0000 C CNN
F 2 "" H 3600 6850 60  0000 C CNN
F 3 "" H 3600 6850 60  0000 C CNN
	1    3550 6900
	1    0    0    -1  
$EndComp
$Comp
L d_inverter U14
U 1 1 6848362E
P 4250 6900
F 0 "U14" H 4250 6800 60  0000 C CNN
F 1 "d_inverter" H 4250 7050 60  0000 C CNN
F 2 "" H 4300 6850 60  0000 C CNN
F 3 "" H 4300 6850 60  0000 C CNN
	1    4250 6900
	1    0    0    -1  
$EndComp
$Comp
L d_and U13
U 1 1 6848368A
P 4200 5800
F 0 "U13" H 4200 5800 60  0000 C CNN
F 1 "d_and" H 4250 5900 60  0000 C CNN
F 2 "" H 4200 5800 60  0000 C CNN
F 3 "" H 4200 5800 60  0000 C CNN
	1    4200 5800
	1    0    0    -1  
$EndComp
$Comp
L d_nor U18
U 1 1 6848371F
P 5100 5750
F 0 "U18" H 5100 5750 60  0000 C CNN
F 1 "d_nor" H 5150 5850 60  0000 C CNN
F 2 "" H 5100 5750 60  0000 C CNN
F 3 "" H 5100 5750 60  0000 C CNN
	1    5100 5750
	1    0    0    -1  
$EndComp
$Comp
L d_nand U5
U 1 1 68483777
P 2600 2050
F 0 "U5" H 2600 2050 60  0000 C CNN
F 1 "d_nand" H 2650 2150 60  0000 C CNN
F 2 "" H 2600 2050 60  0000 C CNN
F 3 "" H 2600 2050 60  0000 C CNN
	1    2600 2050
	0    -1   -1   0   
$EndComp
$Comp
L d_nand U8
U 1 1 684837BE
P 3350 2050
F 0 "U8" H 3350 2050 60  0000 C CNN
F 1 "d_nand" H 3400 2150 60  0000 C CNN
F 2 "" H 3350 2050 60  0000 C CNN
F 3 "" H 3350 2050 60  0000 C CNN
	1    3350 2050
	0    -1   -1   0   
$EndComp
$Comp
L d_nand U11
U 1 1 68483807
P 4050 2050
F 0 "U11" H 4050 2050 60  0000 C CNN
F 1 "d_nand" H 4100 2150 60  0000 C CNN
F 2 "" H 4050 2050 60  0000 C CNN
F 3 "" H 4050 2050 60  0000 C CNN
	1    4050 2050
	0    -1   -1   0   
$EndComp
$Comp
L d_nand U16
U 1 1 6848386E
P 4800 2050
F 0 "U16" H 4800 2050 60  0000 C CNN
F 1 "d_nand" H 4850 2150 60  0000 C CNN
F 2 "" H 4800 2050 60  0000 C CNN
F 3 "" H 4800 2050 60  0000 C CNN
	1    4800 2050
	0    -1   -1   0   
$EndComp
$Comp
L d_nand U21
U 1 1 684838C3
P 5500 2050
F 0 "U21" H 5500 2050 60  0000 C CNN
F 1 "d_nand" H 5550 2150 60  0000 C CNN
F 2 "" H 5500 2050 60  0000 C CNN
F 3 "" H 5500 2050 60  0000 C CNN
	1    5500 2050
	0    -1   -1   0   
$EndComp
$Comp
L d_nand U24
U 1 1 6848391E
P 6400 2050
F 0 "U24" H 6400 2050 60  0000 C CNN
F 1 "d_nand" H 6450 2150 60  0000 C CNN
F 2 "" H 6400 2050 60  0000 C CNN
F 3 "" H 6400 2050 60  0000 C CNN
	1    6400 2050
	0    -1   -1   0   
$EndComp
$Comp
L d_nand U26
U 1 1 68483993
P 7200 2050
F 0 "U26" H 7200 2050 60  0000 C CNN
F 1 "d_nand" H 7250 2150 60  0000 C CNN
F 2 "" H 7200 2050 60  0000 C CNN
F 3 "" H 7200 2050 60  0000 C CNN
	1    7200 2050
	0    -1   -1   0   
$EndComp
$Comp
L d_nand U29
U 1 1 684839E8
P 8150 2050
F 0 "U29" H 8150 2050 60  0000 C CNN
F 1 "d_nand" H 8200 2150 60  0000 C CNN
F 2 "" H 8150 2050 60  0000 C CNN
F 3 "" H 8150 2050 60  0000 C CNN
	1    8150 2050
	0    -1   -1   0   
$EndComp
$Comp
L d_inverter U4
U 1 1 68483B29
P 2550 1300
F 0 "U4" H 2550 1200 60  0000 C CNN
F 1 "d_inverter" H 2550 1450 60  0000 C CNN
F 2 "" H 2600 1250 60  0000 C CNN
F 3 "" H 2600 1250 60  0000 C CNN
	1    2550 1300
	0    -1   -1   0   
$EndComp
$Comp
L d_inverter U6
U 1 1 68483BAA
P 3300 1300
F 0 "U6" H 3300 1200 60  0000 C CNN
F 1 "d_inverter" H 3300 1450 60  0000 C CNN
F 2 "" H 3350 1250 60  0000 C CNN
F 3 "" H 3350 1250 60  0000 C CNN
	1    3300 1300
	0    -1   -1   0   
$EndComp
$Comp
L d_inverter U10
U 1 1 68483C2B
P 4000 1300
F 0 "U10" H 4000 1200 60  0000 C CNN
F 1 "d_inverter" H 4000 1450 60  0000 C CNN
F 2 "" H 4050 1250 60  0000 C CNN
F 3 "" H 4050 1250 60  0000 C CNN
	1    4000 1300
	0    -1   -1   0   
$EndComp
$Comp
L d_inverter U15
U 1 1 68483C8A
P 4750 1300
F 0 "U15" H 4750 1200 60  0000 C CNN
F 1 "d_inverter" H 4750 1450 60  0000 C CNN
F 2 "" H 4800 1250 60  0000 C CNN
F 3 "" H 4800 1250 60  0000 C CNN
	1    4750 1300
	0    -1   -1   0   
$EndComp
$Comp
L d_inverter U19
U 1 1 68483CE9
P 5450 1300
F 0 "U19" H 5450 1200 60  0000 C CNN
F 1 "d_inverter" H 5450 1450 60  0000 C CNN
F 2 "" H 5500 1250 60  0000 C CNN
F 3 "" H 5500 1250 60  0000 C CNN
	1    5450 1300
	0    -1   -1   0   
$EndComp
$Comp
L d_inverter U22
U 1 1 68483D50
P 6350 1300
F 0 "U22" H 6350 1200 60  0000 C CNN
F 1 "d_inverter" H 6350 1450 60  0000 C CNN
F 2 "" H 6400 1250 60  0000 C CNN
F 3 "" H 6400 1250 60  0000 C CNN
	1    6350 1300
	0    -1   -1   0   
$EndComp
$Comp
L d_inverter U25
U 1 1 68483DDF
P 7150 1300
F 0 "U25" H 7150 1200 60  0000 C CNN
F 1 "d_inverter" H 7150 1450 60  0000 C CNN
F 2 "" H 7200 1250 60  0000 C CNN
F 3 "" H 7200 1250 60  0000 C CNN
	1    7150 1300
	0    -1   -1   0   
$EndComp
$Comp
L d_inverter U28
U 1 1 68483E68
P 8100 1300
F 0 "U28" H 8100 1200 60  0000 C CNN
F 1 "d_inverter" H 8100 1450 60  0000 C CNN
F 2 "" H 8150 1250 60  0000 C CNN
F 3 "" H 8150 1250 60  0000 C CNN
	1    8100 1300
	0    -1   -1   0   
$EndComp
$Comp
L d_inverter U30
U 1 1 68483ED5
P 9450 1200
F 0 "U30" H 9450 1100 60  0000 C CNN
F 1 "d_inverter" H 9450 1350 60  0000 C CNN
F 2 "" H 9500 1150 60  0000 C CNN
F 3 "" H 9500 1150 60  0000 C CNN
	1    9450 1200
	0    -1   -1   0   
$EndComp
$Comp
L d_inverter U31
U 1 1 68483F50
P 9450 1950
F 0 "U31" H 9450 1850 60  0000 C CNN
F 1 "d_inverter" H 9450 2100 60  0000 C CNN
F 2 "" H 9500 1900 60  0000 C CNN
F 3 "" H 9500 1900 60  0000 C CNN
	1    9450 1950
	0    -1   -1   0   
$EndComp
$Comp
L d_inverter U32
U 1 1 68483FC1
P 9450 2650
F 0 "U32" H 9450 2550 60  0000 C CNN
F 1 "d_inverter" H 9450 2800 60  0000 C CNN
F 2 "" H 9500 2600 60  0000 C CNN
F 3 "" H 9500 2600 60  0000 C CNN
	1    9450 2650
	0    -1   -1   0   
$EndComp
$Comp
L d_nor U20
U 1 1 6848433F
P 5450 6650
F 0 "U20" H 5450 6650 60  0000 C CNN
F 1 "d_nor" H 5500 6750 60  0000 C CNN
F 2 "" H 5450 6650 60  0000 C CNN
F 3 "" H 5450 6650 60  0000 C CNN
	1    5450 6650
	1    0    0    -1  
$EndComp
NoConn ~ 3300 3500
NoConn ~ 4800 3500
NoConn ~ 6350 3500
NoConn ~ 7950 3500
Wire Wire Line
	1900 5000 2000 5000
Wire Wire Line
	2600 5000 7950 5000
Wire Wire Line
	3300 5000 3300 4750
Wire Wire Line
	4800 5000 4800 4750
Connection ~ 3300 5000
Wire Wire Line
	6350 5000 6350 4750
Connection ~ 4800 5000
Wire Wire Line
	7950 5000 7950 4750
Connection ~ 6350 5000
Wire Wire Line
	4350 6400 5000 6400
Wire Wire Line
	5000 6400 5000 6550
Wire Wire Line
	5000 6650 5000 6900
Wire Wire Line
	5000 6900 4550 6900
Wire Wire Line
	3950 6900 3850 6900
Wire Wire Line
	9450 1650 9450 1500
Wire Wire Line
	9450 2350 9450 2250
Wire Wire Line
	9450 2950 9450 3800
Wire Wire Line
	9450 3800 8500 3800
Wire Wire Line
	6900 3800 7400 3800
Wire Wire Line
	4250 3800 3850 3800
Wire Wire Line
	5800 3800 5650 3800
Wire Wire Line
	5650 3800 5650 5700
Wire Wire Line
	5650 5700 5550 5700
Wire Wire Line
	3850 3200 3850 5250
Wire Wire Line
	3850 5250 3500 5250
Wire Wire Line
	3500 5250 3500 5800
Wire Wire Line
	3500 5800 3750 5800
Wire Wire Line
	2750 4450 2750 5150
Wire Wire Line
	2750 5150 7400 5150
Wire Wire Line
	4250 5150 4250 4450
Wire Wire Line
	5800 5150 5800 4450
Connection ~ 4250 5150
Wire Wire Line
	7400 5150 7400 4450
Connection ~ 5800 5150
Wire Wire Line
	5900 6600 5900 5150
Connection ~ 5900 5150
Wire Wire Line
	2750 3800 2500 3800
Wire Wire Line
	2500 3800 2500 2500
Wire Wire Line
	8150 2500 8150 3100
Wire Wire Line
	8150 3100 9450 3100
Connection ~ 9450 3100
Wire Wire Line
	2600 2500 2600 3200
Wire Wire Line
	2600 3200 6300 3200
Wire Wire Line
	6300 3200 6300 2500
Connection ~ 3850 3200
Connection ~ 3850 4450
Wire Wire Line
	3250 2500 3250 3300
Wire Wire Line
	3250 3300 5400 3300
Wire Wire Line
	5400 3300 5400 2500
Wire Wire Line
	4050 3800 4050 3300
Connection ~ 4050 3300
Connection ~ 4050 3800
Wire Wire Line
	2500 2650 4800 2650
Wire Wire Line
	4800 2500 4800 2950
Connection ~ 2500 2650
Wire Wire Line
	4800 2950 9050 2950
Wire Wire Line
	9050 2950 9050 4450
Wire Wire Line
	9050 4450 8500 4450
Connection ~ 4800 2650
Wire Wire Line
	4050 2500 4050 3100
Wire Wire Line
	4050 2950 3950 2950
Wire Wire Line
	3950 2950 3950 5450
Wire Wire Line
	3950 5450 3750 5450
Wire Wire Line
	3750 5450 3750 5700
Wire Wire Line
	5350 4450 5350 5450
Wire Wire Line
	5350 5450 4650 5450
Wire Wire Line
	4650 5450 4650 5650
Wire Wire Line
	3350 2500 3350 2850
Wire Wire Line
	3350 2850 7100 2850
Wire Wire Line
	7100 2850 7100 2500
Wire Wire Line
	5350 4450 5500 4450
Wire Wire Line
	5500 4450 5500 2850
Connection ~ 5500 2850
Wire Wire Line
	3950 2500 3950 2750
Wire Wire Line
	3950 2750 6400 2750
Wire Wire Line
	6400 2750 6400 2500
Wire Wire Line
	5350 3800 5350 2750
Connection ~ 5350 2750
Wire Wire Line
	4700 2500 4700 3050
Wire Wire Line
	4700 3050 7200 3050
Wire Wire Line
	7200 2500 7200 3800
Connection ~ 7200 3800
Connection ~ 7200 3050
Wire Wire Line
	4050 3100 8050 3100
Wire Wire Line
	8050 3100 8050 2500
Connection ~ 4050 2950
Wire Wire Line
	6900 4450 6900 3100
Connection ~ 6900 3100
Wire Wire Line
	5500 2500 5500 2550
Wire Wire Line
	5500 2550 8150 2550
Connection ~ 8150 2550
$Comp
L PORT U1
U 1 1 684881B5
P 3300 750
F 0 "U1" H 3350 850 30  0000 C CNN
F 1 "PORT" H 3300 750 30  0000 C CNN
F 2 "" H 3300 750 60  0000 C CNN
F 3 "" H 3300 750 60  0000 C CNN
	1    3300 750 
	0    1    1    0   
$EndComp
$Comp
L PORT U1
U 2 1 684882DE
P 2550 750
F 0 "U1" H 2600 850 30  0000 C CNN
F 1 "PORT" H 2550 750 30  0000 C CNN
F 2 "" H 2550 750 60  0000 C CNN
F 3 "" H 2550 750 60  0000 C CNN
	2    2550 750 
	0    1    1    0   
$EndComp
$Comp
L PORT U1
U 3 1 6848834F
P 4000 750
F 0 "U1" H 4050 850 30  0000 C CNN
F 1 "PORT" H 4000 750 30  0000 C CNN
F 2 "" H 4000 750 60  0000 C CNN
F 3 "" H 4000 750 60  0000 C CNN
	3    4000 750 
	0    1    1    0   
$EndComp
$Comp
L PORT U1
U 4 1 684883C0
P 6350 750
F 0 "U1" H 6400 850 30  0000 C CNN
F 1 "PORT" H 6350 750 30  0000 C CNN
F 2 "" H 6350 750 60  0000 C CNN
F 3 "" H 6350 750 60  0000 C CNN
	4    6350 750 
	0    1    1    0   
$EndComp
$Comp
L PORT U1
U 5 1 6848844F
P 7150 750
F 0 "U1" H 7200 850 30  0000 C CNN
F 1 "PORT" H 7150 750 30  0000 C CNN
F 2 "" H 7150 750 60  0000 C CNN
F 3 "" H 7150 750 60  0000 C CNN
	5    7150 750 
	0    1    1    0   
$EndComp
$Comp
L PORT U1
U 6 1 684884D8
P 1100 900
F 0 "U1" H 1150 1000 30  0000 C CNN
F 1 "PORT" H 1100 900 30  0000 C CNN
F 2 "" H 1100 900 60  0000 C CNN
F 3 "" H 1100 900 60  0000 C CNN
	6    1100 900 
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 7 1 68488553
P 4750 750
F 0 "U1" H 4800 850 30  0000 C CNN
F 1 "PORT" H 4750 750 30  0000 C CNN
F 2 "" H 4750 750 60  0000 C CNN
F 3 "" H 4750 750 60  0000 C CNN
	7    4750 750 
	0    1    1    0   
$EndComp
$Comp
L PORT U1
U 8 1 684885EA
P 1100 1250
F 0 "U1" H 1150 1350 30  0000 C CNN
F 1 "PORT" H 1100 1250 30  0000 C CNN
F 2 "" H 1100 1250 60  0000 C CNN
F 3 "" H 1100 1250 60  0000 C CNN
	8    1100 1250
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 9 1 68488671
P 1100 1550
F 0 "U1" H 1150 1650 30  0000 C CNN
F 1 "PORT" H 1100 1550 30  0000 C CNN
F 2 "" H 1100 1550 60  0000 C CNN
F 3 "" H 1100 1550 60  0000 C CNN
	9    1100 1550
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 10 1 68488710
P 8100 750
F 0 "U1" H 8150 850 30  0000 C CNN
F 1 "PORT" H 8100 750 30  0000 C CNN
F 2 "" H 8100 750 60  0000 C CNN
F 3 "" H 8100 750 60  0000 C CNN
	10   8100 750 
	0    1    1    0   
$EndComp
$Comp
L PORT U1
U 11 1 68488821
P 5450 750
F 0 "U1" H 5500 850 30  0000 C CNN
F 1 "PORT" H 5450 750 30  0000 C CNN
F 2 "" H 5450 750 60  0000 C CNN
F 3 "" H 5450 750 60  0000 C CNN
	11   5450 750 
	0    1    1    0   
$EndComp
$Comp
L PORT U1
U 12 1 68488904
P 9450 650
F 0 "U1" H 9500 750 30  0000 C CNN
F 1 "PORT" H 9450 650 30  0000 C CNN
F 2 "" H 9450 650 60  0000 C CNN
F 3 "" H 9450 650 60  0000 C CNN
	12   9450 650 
	0    1    1    0   
$EndComp
$Comp
L PORT U1
U 13 1 684889EF
P 3000 6900
F 0 "U1" H 3050 7000 30  0000 C CNN
F 1 "PORT" H 3000 6900 30  0000 C CNN
F 2 "" H 3000 6900 60  0000 C CNN
F 3 "" H 3000 6900 60  0000 C CNN
	13   3000 6900
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 14 1 68488A94
P 3500 6400
F 0 "U1" H 3550 6500 30  0000 C CNN
F 1 "PORT" H 3500 6400 30  0000 C CNN
F 2 "" H 3500 6400 60  0000 C CNN
F 3 "" H 3500 6400 60  0000 C CNN
	14   3500 6400
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 16 1 68488BD6
P 1100 1850
F 0 "U1" H 1150 1950 30  0000 C CNN
F 1 "PORT" H 1100 1850 30  0000 C CNN
F 2 "" H 1100 1850 60  0000 C CNN
F 3 "" H 1100 1850 60  0000 C CNN
	16   1100 1850
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 15 1 68488CE5
P 1050 5000
F 0 "U1" H 1100 5100 30  0000 C CNN
F 1 "PORT" H 1050 5000 30  0000 C CNN
F 2 "" H 1050 5000 60  0000 C CNN
F 3 "" H 1050 5000 60  0000 C CNN
	15   1050 5000
	1    0    0    -1  
$EndComp
NoConn ~ 1350 900 
NoConn ~ 1350 1250
NoConn ~ 1350 1550
NoConn ~ 1350 1850
$Comp
L d_inverter U12
U 1 1 6848CA5F
P 4050 6400
F 0 "U12" H 4050 6300 60  0000 C CNN
F 1 "d_inverter" H 4050 6550 60  0000 C CNN
F 2 "" H 4100 6350 60  0000 C CNN
F 3 "" H 4100 6350 60  0000 C CNN
	1    4050 6400
	1    0    0    -1  
$EndComp
$EndSCHEMATC
