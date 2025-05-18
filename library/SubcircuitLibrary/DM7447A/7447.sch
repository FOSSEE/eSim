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
LIBS:7447-cache
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
L d_nand U3
U 1 1 680723FC
P 1550 1450
F 0 "U3" H 1550 1450 60  0000 C CNN
F 1 "d_nand" H 1600 1550 60  0000 C CNN
F 2 "" H 1550 1450 60  0000 C CNN
F 3 "" H 1550 1450 60  0000 C CNN
	1    1550 1450
	1    0    0    -1  
$EndComp
$Comp
L d_nand U4
U 1 1 6807242F
P 1550 2450
F 0 "U4" H 1550 2450 60  0000 C CNN
F 1 "d_nand" H 1600 2550 60  0000 C CNN
F 2 "" H 1550 2450 60  0000 C CNN
F 3 "" H 1550 2450 60  0000 C CNN
	1    1550 2450
	1    0    0    -1  
$EndComp
$Comp
L d_nand U5
U 1 1 68072448
P 1650 3350
F 0 "U5" H 1650 3350 60  0000 C CNN
F 1 "d_nand" H 1700 3450 60  0000 C CNN
F 2 "" H 1650 3350 60  0000 C CNN
F 3 "" H 1650 3350 60  0000 C CNN
	1    1650 3350
	1    0    0    -1  
$EndComp
$Comp
L d_inverter U2
U 1 1 68072469
P 1500 4200
F 0 "U2" H 1500 4100 60  0000 C CNN
F 1 "d_inverter" H 1500 4350 60  0000 C CNN
F 2 "" H 1550 4150 60  0000 C CNN
F 3 "" H 1550 4150 60  0000 C CNN
	1    1500 4200
	1    0    0    -1  
$EndComp
$Comp
L d_inverter U6
U 1 1 6807248E
P 1850 7600
F 0 "U6" H 1850 7500 60  0000 C CNN
F 1 "d_inverter" H 1850 7750 60  0000 C CNN
F 2 "" H 1900 7550 60  0000 C CNN
F 3 "" H 1900 7550 60  0000 C CNN
	1    1850 7600
	1    0    0    -1  
$EndComp
$Comp
L 4_and X1
U 1 1 68072548
P 2200 6900
F 0 "X1" H 2250 6850 60  0000 C CNN
F 1 "4_and" H 2300 7000 60  0000 C CNN
F 2 "" H 2200 6900 60  0000 C CNN
F 3 "" H 2200 6900 60  0000 C CNN
	1    2200 6900
	0    -1   -1   0   
$EndComp
$Comp
L d_and U9
U 1 1 680725A5
P 2650 6850
F 0 "U9" H 2650 6850 60  0000 C CNN
F 1 "d_and" H 2700 6950 60  0000 C CNN
F 2 "" H 2650 6850 60  0000 C CNN
F 3 "" H 2650 6850 60  0000 C CNN
	1    2650 6850
	0    -1   -1   0   
$EndComp
$Comp
L d_nand U10
U 1 1 68072846
P 3100 1900
F 0 "U10" H 3100 1900 60  0000 C CNN
F 1 "d_nand" H 3150 2000 60  0000 C CNN
F 2 "" H 3100 1900 60  0000 C CNN
F 3 "" H 3100 1900 60  0000 C CNN
	1    3100 1900
	1    0    0    -1  
$EndComp
$Comp
L d_nand U11
U 1 1 6807288D
P 3100 2950
F 0 "U11" H 3100 2950 60  0000 C CNN
F 1 "d_nand" H 3150 3050 60  0000 C CNN
F 2 "" H 3100 2950 60  0000 C CNN
F 3 "" H 3100 2950 60  0000 C CNN
	1    3100 2950
	1    0    0    -1  
$EndComp
$Comp
L d_nand U12
U 1 1 680728CC
P 3100 3900
F 0 "U12" H 3100 3900 60  0000 C CNN
F 1 "d_nand" H 3150 4000 60  0000 C CNN
F 2 "" H 3100 3900 60  0000 C CNN
F 3 "" H 3100 3900 60  0000 C CNN
	1    3100 3900
	1    0    0    -1  
$EndComp
$Comp
L d_nand U13
U 1 1 680729B3
P 3100 4400
F 0 "U13" H 3100 4400 60  0000 C CNN
F 1 "d_nand" H 3150 4500 60  0000 C CNN
F 2 "" H 3100 4400 60  0000 C CNN
F 3 "" H 3100 4400 60  0000 C CNN
	1    3100 4400
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 1 1 68072AB2
P 700 1300
F 0 "U1" H 750 1400 30  0000 C CNN
F 1 "PORT" H 700 1300 30  0000 C CNN
F 2 "" H 700 1300 60  0000 C CNN
F 3 "" H 700 1300 60  0000 C CNN
	1    700  1300
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 2 1 68072AEF
P 700 2300
F 0 "U1" H 750 2400 30  0000 C CNN
F 1 "PORT" H 700 2300 30  0000 C CNN
F 2 "" H 700 2300 60  0000 C CNN
F 3 "" H 700 2300 60  0000 C CNN
	2    700  2300
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 3 1 68072B26
P 700 3200
F 0 "U1" H 750 3300 30  0000 C CNN
F 1 "PORT" H 700 3200 30  0000 C CNN
F 2 "" H 700 3200 60  0000 C CNN
F 3 "" H 700 3200 60  0000 C CNN
	3    700  3200
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 4 1 68072B65
P 750 4200
F 0 "U1" H 800 4300 30  0000 C CNN
F 1 "PORT" H 750 4200 30  0000 C CNN
F 2 "" H 750 4200 60  0000 C CNN
F 3 "" H 750 4200 60  0000 C CNN
	4    750  4200
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 5 1 68072B9E
P 750 4750
F 0 "U1" H 800 4850 30  0000 C CNN
F 1 "PORT" H 750 4750 30  0000 C CNN
F 2 "" H 750 4750 60  0000 C CNN
F 3 "" H 750 4750 60  0000 C CNN
	5    750  4750
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 6 1 68072C7D
P 750 7000
F 0 "U1" H 800 7100 30  0000 C CNN
F 1 "PORT" H 750 7000 30  0000 C CNN
F 2 "" H 750 7000 60  0000 C CNN
F 3 "" H 750 7000 60  0000 C CNN
	6    750  7000
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 7 1 68072D0E
P 750 7550
F 0 "U1" H 800 7650 30  0000 C CNN
F 1 "PORT" H 750 7550 30  0000 C CNN
F 2 "" H 750 7550 60  0000 C CNN
F 3 "" H 750 7550 60  0000 C CNN
	7    750  7550
	1    0    0    -1  
$EndComp
$Comp
L d_and U14
U 1 1 68072ECF
P 6000 850
F 0 "U14" H 6000 850 60  0000 C CNN
F 1 "d_and" H 6050 950 60  0000 C CNN
F 2 "" H 6000 850 60  0000 C CNN
F 3 "" H 6000 850 60  0000 C CNN
	1    6000 850 
	1    0    0    -1  
$EndComp
$Comp
L d_and U15
U 1 1 68072F20
P 6000 1200
F 0 "U15" H 6000 1200 60  0000 C CNN
F 1 "d_and" H 6050 1300 60  0000 C CNN
F 2 "" H 6000 1200 60  0000 C CNN
F 3 "" H 6000 1200 60  0000 C CNN
	1    6000 1200
	1    0    0    -1  
$EndComp
$Comp
L 4_and X10
U 1 1 68072F61
P 5950 1550
F 0 "X10" H 6000 1500 60  0000 C CNN
F 1 "4_and" H 6050 1650 60  0000 C CNN
F 2 "" H 5950 1550 60  0000 C CNN
F 3 "" H 5950 1550 60  0000 C CNN
	1    5950 1550
	1    0    0    -1  
$EndComp
$Comp
L d_and U16
U 1 1 68072FE7
P 6000 2000
F 0 "U16" H 6000 2000 60  0000 C CNN
F 1 "d_and" H 6050 2100 60  0000 C CNN
F 2 "" H 6000 2000 60  0000 C CNN
F 3 "" H 6000 2000 60  0000 C CNN
	1    6000 2000
	1    0    0    -1  
$EndComp
$Comp
L 3_and X2
U 1 1 68073046
P 5900 2350
F 0 "X2" H 6000 2300 60  0000 C CNN
F 1 "3_and" H 6050 2500 60  0000 C CNN
F 2 "" H 5900 2350 60  0000 C CNN
F 3 "" H 5900 2350 60  0000 C CNN
	1    5900 2350
	1    0    0    -1  
$EndComp
$Comp
L 3_and X3
U 1 1 68073109
P 5900 2700
F 0 "X3" H 6000 2650 60  0000 C CNN
F 1 "3_and" H 6050 2850 60  0000 C CNN
F 2 "" H 5900 2700 60  0000 C CNN
F 3 "" H 5900 2700 60  0000 C CNN
	1    5900 2700
	1    0    0    -1  
$EndComp
$Comp
L d_and U17
U 1 1 68073276
P 6000 3050
F 0 "U17" H 6000 3050 60  0000 C CNN
F 1 "d_and" H 6050 3150 60  0000 C CNN
F 2 "" H 6000 3050 60  0000 C CNN
F 3 "" H 6000 3050 60  0000 C CNN
	1    6000 3050
	1    0    0    -1  
$EndComp
$Comp
L 3_and X4
U 1 1 680732D1
P 5900 3350
F 0 "X4" H 6000 3300 60  0000 C CNN
F 1 "3_and" H 6050 3500 60  0000 C CNN
F 2 "" H 5900 3350 60  0000 C CNN
F 3 "" H 5900 3350 60  0000 C CNN
	1    5900 3350
	1    0    0    -1  
$EndComp
$Comp
L 3_and X5
U 1 1 68073324
P 5900 3700
F 0 "X5" H 6000 3650 60  0000 C CNN
F 1 "3_and" H 6050 3850 60  0000 C CNN
F 2 "" H 5900 3700 60  0000 C CNN
F 3 "" H 5900 3700 60  0000 C CNN
	1    5900 3700
	1    0    0    -1  
$EndComp
$Comp
L 3_and X6
U 1 1 6807337B
P 5900 4050
F 0 "X6" H 6000 4000 60  0000 C CNN
F 1 "3_and" H 6050 4200 60  0000 C CNN
F 2 "" H 5900 4050 60  0000 C CNN
F 3 "" H 5900 4050 60  0000 C CNN
	1    5900 4050
	1    0    0    -1  
$EndComp
$Comp
L 3_and X7
U 1 1 680733D8
P 5900 4400
F 0 "X7" H 6000 4350 60  0000 C CNN
F 1 "3_and" H 6050 4550 60  0000 C CNN
F 2 "" H 5900 4400 60  0000 C CNN
F 3 "" H 5900 4400 60  0000 C CNN
	1    5900 4400
	1    0    0    -1  
$EndComp
$Comp
L d_buffer U21
U 1 1 68073437
P 6050 4800
F 0 "U21" H 6050 4750 60  0000 C CNN
F 1 "d_buffer" H 6050 4850 60  0000 C CNN
F 2 "" H 6050 4800 60  0000 C CNN
F 3 "" H 6050 4800 60  0000 C CNN
	1    6050 4800
	1    0    0    -1  
$EndComp
$Comp
L d_and U18
U 1 1 68073568
P 6000 5250
F 0 "U18" H 6000 5250 60  0000 C CNN
F 1 "d_and" H 6050 5350 60  0000 C CNN
F 2 "" H 6000 5250 60  0000 C CNN
F 3 "" H 6000 5250 60  0000 C CNN
	1    6000 5250
	1    0    0    -1  
$EndComp
$Comp
L d_and U19
U 1 1 680735CF
P 6000 5500
F 0 "U19" H 6000 5500 60  0000 C CNN
F 1 "d_and" H 6050 5600 60  0000 C CNN
F 2 "" H 6000 5500 60  0000 C CNN
F 3 "" H 6000 5500 60  0000 C CNN
	1    6000 5500
	1    0    0    -1  
$EndComp
$Comp
L d_and U20
U 1 1 68073632
P 6000 5750
F 0 "U20" H 6000 5750 60  0000 C CNN
F 1 "d_and" H 6050 5850 60  0000 C CNN
F 2 "" H 6000 5750 60  0000 C CNN
F 3 "" H 6000 5750 60  0000 C CNN
	1    6000 5750
	1    0    0    -1  
$EndComp
$Comp
L 3_and X8
U 1 1 6807370E
P 5900 6100
F 0 "X8" H 6000 6050 60  0000 C CNN
F 1 "3_and" H 6050 6250 60  0000 C CNN
F 2 "" H 5900 6100 60  0000 C CNN
F 3 "" H 5900 6100 60  0000 C CNN
	1    5900 6100
	1    0    0    -1  
$EndComp
$Comp
L 3_and X9
U 1 1 68073773
P 5900 6450
F 0 "X9" H 6000 6400 60  0000 C CNN
F 1 "3_and" H 6050 6600 60  0000 C CNN
F 2 "" H 5900 6450 60  0000 C CNN
F 3 "" H 5900 6450 60  0000 C CNN
	1    5900 6450
	1    0    0    -1  
$EndComp
$Comp
L 4_and X11
U 1 1 680737DA
P 5950 6850
F 0 "X11" H 6000 6800 60  0000 C CNN
F 1 "4_and" H 6050 6950 60  0000 C CNN
F 2 "" H 5950 6850 60  0000 C CNN
F 3 "" H 5950 6850 60  0000 C CNN
	1    5950 6850
	1    0    0    -1  
$EndComp
Wire Wire Line
	950  1300 1100 1300
Wire Wire Line
	1100 1300 1100 1350
Wire Wire Line
	950  2300 1100 2300
Wire Wire Line
	1100 2300 1100 2350
Wire Wire Line
	1100 1450 1100 7800
Wire Wire Line
	1100 7800 5550 7800
Wire Wire Line
	5550 7800 5550 7000
Wire Wire Line
	950  3200 1200 3200
Wire Wire Line
	1200 3200 1200 3250
Wire Wire Line
	1000 4200 1200 4200
Connection ~ 1100 2450
Connection ~ 1100 3350
Wire Wire Line
	1200 3350 1100 3350
Wire Wire Line
	2000 1400 3700 1400
Wire Wire Line
	2650 1400 2650 1800
Wire Wire Line
	2650 1900 2400 1900
Wire Wire Line
	2000 2400 5350 2400
Wire Wire Line
	2650 2400 2650 2850
Wire Wire Line
	2650 2950 2400 2950
Connection ~ 2400 2950
Wire Wire Line
	2100 3300 3150 3300
Wire Wire Line
	2600 3300 2600 3800
Wire Wire Line
	2600 3800 2650 3800
Wire Wire Line
	2650 3900 2400 3900
Connection ~ 2400 3900
Wire Wire Line
	1800 4200 5050 4200
Wire Wire Line
	2650 4200 2650 4300
Wire Wire Line
	2400 4400 2650 4400
Connection ~ 2400 4400
Wire Wire Line
	2350 6250 2200 6250
Wire Wire Line
	2200 6250 2200 6400
Wire Wire Line
	2450 6250 2600 6250
Wire Wire Line
	2600 6250 2600 6400
Wire Wire Line
	1000 4750 1850 4750
Wire Wire Line
	1000 7550 1550 7550
Wire Wire Line
	1550 7550 1550 7600
Wire Wire Line
	2150 7600 2150 7300
$Comp
L d_nor U27
U 1 1 68075D1B
P 7850 3200
F 0 "U27" H 7850 3200 60  0000 C CNN
F 1 "d_nor" H 7900 3300 60  0000 C CNN
F 2 "" H 7850 3200 60  0000 C CNN
F 3 "" H 7850 3200 60  0000 C CNN
	1    7850 3200
	1    0    0    -1  
$EndComp
$Comp
L d_nor U26
U 1 1 68075ED6
P 7800 5100
F 0 "U26" H 7800 5100 60  0000 C CNN
F 1 "d_nor" H 7850 5200 60  0000 C CNN
F 2 "" H 7800 5100 60  0000 C CNN
F 3 "" H 7800 5100 60  0000 C CNN
	1    7800 5100
	1    0    0    -1  
$EndComp
$Comp
L d_nor U28
U 1 1 68076083
P 7900 6750
F 0 "U28" H 7900 6750 60  0000 C CNN
F 1 "d_nor" H 7950 6850 60  0000 C CNN
F 2 "" H 7900 6750 60  0000 C CNN
F 3 "" H 7900 6750 60  0000 C CNN
	1    7900 6750
	1    0    0    -1  
$EndComp
Wire Wire Line
	3700 1100 3700 7300
Wire Wire Line
	3700 1100 5550 1100
Connection ~ 2650 1400
Wire Wire Line
	3550 1850 3850 1850
Wire Wire Line
	3850 1400 3850 6300
Wire Wire Line
	3850 1400 5550 1400
Wire Wire Line
	5350 2400 5350 2300
Wire Wire Line
	5350 2300 5550 2300
Connection ~ 2650 2400
Wire Wire Line
	4700 2900 3550 2900
Wire Wire Line
	4700 750  4700 6400
Wire Wire Line
	4700 2650 5550 2650
Wire Wire Line
	3150 3400 5550 3400
Wire Wire Line
	3150 3300 3150 3400
Connection ~ 2600 3300
Wire Wire Line
	4000 4450 5550 4450
Wire Wire Line
	4000 4450 4000 3850
Wire Wire Line
	4000 3850 3550 3850
Wire Wire Line
	5050 6900 5550 6900
Wire Wire Line
	5050 1700 5050 7450
Connection ~ 2650 4200
Wire Wire Line
	3550 4350 3550 3050
Wire Wire Line
	3550 3050 5550 3050
Wire Wire Line
	3700 2550 5550 2550
Connection ~ 3700 1400
Wire Wire Line
	3700 3200 5550 3200
Connection ~ 3700 2550
Wire Wire Line
	3700 3900 5550 3900
Connection ~ 3700 3200
Wire Wire Line
	3700 7300 2650 7300
Connection ~ 3700 3900
Wire Wire Line
	3850 2200 5550 2200
Connection ~ 3850 1850
Wire Wire Line
	3850 3550 5550 3550
Connection ~ 3850 2200
Wire Wire Line
	3850 4250 5550 4250
Connection ~ 3850 3550
Wire Wire Line
	3850 4800 5550 4800
Connection ~ 3850 4250
Wire Wire Line
	3850 5400 5550 5400
Connection ~ 3850 4800
Wire Wire Line
	3850 5950 5550 5950
Connection ~ 3850 5400
Wire Wire Line
	3850 6300 5550 6300
Connection ~ 3850 5950
Wire Wire Line
	4000 1500 4000 3800
Wire Wire Line
	4000 1500 5550 1500
Connection ~ 4000 2400
Wire Wire Line
	4000 3650 5550 3650
Wire Wire Line
	4000 3800 4150 3800
Wire Wire Line
	4150 3800 4150 7650
Wire Wire Line
	4150 4000 5550 4000
Connection ~ 4000 3650
Wire Wire Line
	4150 5150 5550 5150
Connection ~ 4150 4000
Wire Wire Line
	4150 6700 5550 6700
Connection ~ 4150 5150
Wire Wire Line
	5050 7450 2550 7450
Wire Wire Line
	2550 7450 2550 7300
Connection ~ 5050 6900
Wire Wire Line
	4700 750  5550 750 
Connection ~ 4700 2650
Wire Wire Line
	5550 1900 4700 1900
Connection ~ 4700 1900
Wire Wire Line
	4700 3300 5550 3300
Connection ~ 4700 2900
Wire Wire Line
	4700 4350 5550 4350
Connection ~ 4700 3300
Wire Wire Line
	4700 5500 5550 5500
Connection ~ 4700 4350
Wire Wire Line
	4700 5650 5550 5650
Connection ~ 4700 5500
Wire Wire Line
	4700 6400 5550 6400
Connection ~ 4700 5650
Wire Wire Line
	4350 1600 4350 7550
Wire Wire Line
	4350 1600 5550 1600
Connection ~ 4350 3400
Wire Wire Line
	4350 3750 5550 3750
Wire Wire Line
	4350 5750 5550 5750
Connection ~ 4350 3750
Wire Wire Line
	4350 6050 5550 6050
Connection ~ 4350 5750
Wire Wire Line
	4350 6800 5550 6800
Connection ~ 4350 6050
Wire Wire Line
	4350 7550 2350 7550
Wire Wire Line
	2350 7550 2350 7300
Connection ~ 4350 6800
Wire Wire Line
	4500 1200 4500 6500
Wire Wire Line
	4500 1200 5550 1200
Connection ~ 4500 4450
Wire Wire Line
	5550 2400 5400 2400
Wire Wire Line
	5400 2400 5400 3000
Wire Wire Line
	5400 3000 4500 3000
Connection ~ 4500 3000
Wire Wire Line
	5550 2750 5400 2750
Connection ~ 5400 2750
Wire Wire Line
	5550 2950 5400 2950
Connection ~ 5400 2950
Wire Wire Line
	5550 4100 4500 4100
Connection ~ 4500 4100
Wire Wire Line
	4500 5250 5550 5250
Wire Wire Line
	4500 6500 5550 6500
Connection ~ 4500 5250
Wire Wire Line
	4200 850  4200 3050
Wire Wire Line
	4200 850  5550 850 
Connection ~ 4200 3050
Wire Wire Line
	5550 2000 4200 2000
Wire Wire Line
	4200 2000 4200 1950
Connection ~ 4200 1950
Wire Wire Line
	4150 7650 2250 7650
Wire Wire Line
	2250 7650 2250 7300
Connection ~ 4150 6700
Wire Wire Line
	5050 6150 5550 6150
Connection ~ 5050 6150
Wire Wire Line
	5550 1700 5050 1700
Connection ~ 5050 4200
$Comp
L d_nor U22
U 1 1 6807B01F
P 7400 950
F 0 "U22" H 7400 950 60  0000 C CNN
F 1 "d_nor" H 7450 1050 60  0000 C CNN
F 2 "" H 7400 950 60  0000 C CNN
F 3 "" H 7400 950 60  0000 C CNN
	1    7400 950 
	1    0    0    -1  
$EndComp
$Comp
L d_nor U29
U 1 1 6807B09C
P 8550 900
F 0 "U29" H 8550 900 60  0000 C CNN
F 1 "d_nor" H 8600 1000 60  0000 C CNN
F 2 "" H 8550 900 60  0000 C CNN
F 3 "" H 8550 900 60  0000 C CNN
	1    8550 900 
	1    0    0    -1  
$EndComp
$Comp
L d_nor U35
U 1 1 6807B127
P 9000 1450
F 0 "U35" H 9000 1450 60  0000 C CNN
F 1 "d_nor" H 9050 1550 60  0000 C CNN
F 2 "" H 9000 1450 60  0000 C CNN
F 3 "" H 9000 1450 60  0000 C CNN
	1    9000 1450
	1    0    0    -1  
$EndComp
$Comp
L d_nor U23
U 1 1 6807B65C
P 7400 2100
F 0 "U23" H 7400 2100 60  0000 C CNN
F 1 "d_nor" H 7450 2200 60  0000 C CNN
F 2 "" H 7400 2100 60  0000 C CNN
F 3 "" H 7400 2100 60  0000 C CNN
	1    7400 2100
	1    0    0    -1  
$EndComp
$Comp
L d_nor U30
U 1 1 6807B662
P 8550 2050
F 0 "U30" H 8550 2050 60  0000 C CNN
F 1 "d_nor" H 8600 2150 60  0000 C CNN
F 2 "" H 8550 2050 60  0000 C CNN
F 3 "" H 8550 2050 60  0000 C CNN
	1    8550 2050
	1    0    0    -1  
$EndComp
$Comp
L d_nor U36
U 1 1 6807B668
P 9000 2600
F 0 "U36" H 9000 2600 60  0000 C CNN
F 1 "d_nor" H 9050 2700 60  0000 C CNN
F 2 "" H 9000 2600 60  0000 C CNN
F 3 "" H 9000 2600 60  0000 C CNN
	1    9000 2600
	1    0    0    -1  
$EndComp
$Comp
L d_nor U24
U 1 1 6807B7A0
P 7400 3800
F 0 "U24" H 7400 3800 60  0000 C CNN
F 1 "d_nor" H 7450 3900 60  0000 C CNN
F 2 "" H 7400 3800 60  0000 C CNN
F 3 "" H 7400 3800 60  0000 C CNN
	1    7400 3800
	1    0    0    -1  
$EndComp
$Comp
L d_nor U31
U 1 1 6807B7A6
P 8550 3750
F 0 "U31" H 8550 3750 60  0000 C CNN
F 1 "d_nor" H 8600 3850 60  0000 C CNN
F 2 "" H 8550 3750 60  0000 C CNN
F 3 "" H 8550 3750 60  0000 C CNN
	1    8550 3750
	1    0    0    -1  
$EndComp
$Comp
L d_nor U37
U 1 1 6807B7AC
P 9000 4300
F 0 "U37" H 9000 4300 60  0000 C CNN
F 1 "d_nor" H 9050 4400 60  0000 C CNN
F 2 "" H 9000 4300 60  0000 C CNN
F 3 "" H 9000 4300 60  0000 C CNN
	1    9000 4300
	1    0    0    -1  
$EndComp
$Comp
L d_nor U25
U 1 1 6807BABC
P 7400 5650
F 0 "U25" H 7400 5650 60  0000 C CNN
F 1 "d_nor" H 7450 5750 60  0000 C CNN
F 2 "" H 7400 5650 60  0000 C CNN
F 3 "" H 7400 5650 60  0000 C CNN
	1    7400 5650
	1    0    0    -1  
$EndComp
$Comp
L d_nor U32
U 1 1 6807BAC2
P 8550 5600
F 0 "U32" H 8550 5600 60  0000 C CNN
F 1 "d_nor" H 8600 5700 60  0000 C CNN
F 2 "" H 8550 5600 60  0000 C CNN
F 3 "" H 8550 5600 60  0000 C CNN
	1    8550 5600
	1    0    0    -1  
$EndComp
$Comp
L d_nor U38
U 1 1 6807BAC8
P 9000 6150
F 0 "U38" H 9000 6150 60  0000 C CNN
F 1 "d_nor" H 9050 6250 60  0000 C CNN
F 2 "" H 9000 6150 60  0000 C CNN
F 3 "" H 9000 6150 60  0000 C CNN
	1    9000 6150
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 8 1 6807C68E
P 10900 1400
F 0 "U1" H 10950 1500 30  0000 C CNN
F 1 "PORT" H 10900 1400 30  0000 C CNN
F 2 "" H 10900 1400 60  0000 C CNN
F 3 "" H 10900 1400 60  0000 C CNN
	8    10900 1400
	-1   0    0    1   
$EndComp
$Comp
L PORT U1
U 9 1 6807D315
P 10900 2550
F 0 "U1" H 10950 2650 30  0000 C CNN
F 1 "PORT" H 10900 2550 30  0000 C CNN
F 2 "" H 10900 2550 60  0000 C CNN
F 3 "" H 10900 2550 60  0000 C CNN
	9    10900 2550
	-1   0    0    1   
$EndComp
$Comp
L PORT U1
U 10 1 6807D3B8
P 10900 3150
F 0 "U1" H 10950 3250 30  0000 C CNN
F 1 "PORT" H 10900 3150 30  0000 C CNN
F 2 "" H 10900 3150 60  0000 C CNN
F 3 "" H 10900 3150 60  0000 C CNN
	10   10900 3150
	-1   0    0    1   
$EndComp
$Comp
L PORT U1
U 11 1 6807D457
P 10900 4250
F 0 "U1" H 10950 4350 30  0000 C CNN
F 1 "PORT" H 10900 4250 30  0000 C CNN
F 2 "" H 10900 4250 60  0000 C CNN
F 3 "" H 10900 4250 60  0000 C CNN
	11   10900 4250
	-1   0    0    1   
$EndComp
$Comp
L PORT U1
U 12 1 6807D4F4
P 10900 5050
F 0 "U1" H 10950 5150 30  0000 C CNN
F 1 "PORT" H 10900 5050 30  0000 C CNN
F 2 "" H 10900 5050 60  0000 C CNN
F 3 "" H 10900 5050 60  0000 C CNN
	12   10900 5050
	-1   0    0    1   
$EndComp
$Comp
L PORT U1
U 13 1 6807D719
P 10900 6100
F 0 "U1" H 10950 6200 30  0000 C CNN
F 1 "PORT" H 10900 6100 30  0000 C CNN
F 2 "" H 10900 6100 60  0000 C CNN
F 3 "" H 10900 6100 60  0000 C CNN
	13   10900 6100
	-1   0    0    1   
$EndComp
$Comp
L PORT U1
U 14 1 6807D7BA
P 10900 6700
F 0 "U1" H 10950 6800 30  0000 C CNN
F 1 "PORT" H 10900 6700 30  0000 C CNN
F 2 "" H 10900 6700 60  0000 C CNN
F 3 "" H 10900 6700 60  0000 C CNN
	14   10900 6700
	-1   0    0    1   
$EndComp
Wire Wire Line
	6450 800  6950 800 
Wire Wire Line
	6950 800  6950 850 
Wire Wire Line
	6450 1150 6950 1150
Wire Wire Line
	6950 1150 6950 950 
Wire Wire Line
	6450 1950 6950 1950
Wire Wire Line
	7950 2050 7850 2050
Wire Wire Line
	7950 1950 7950 2050
Wire Wire Line
	7950 1950 8100 1950
Wire Wire Line
	7950 2000 8100 2000
Wire Wire Line
	8100 2000 8100 2050
Connection ~ 7950 2000
Wire Wire Line
	9000 2000 9000 2400
Wire Wire Line
	9000 2400 8550 2400
Wire Wire Line
	8550 2400 8550 2500
Wire Wire Line
	6400 1550 8550 1550
Wire Wire Line
	8550 1550 8550 1450
Wire Wire Line
	7850 900  7850 800 
Wire Wire Line
	7850 800  8100 800 
Wire Wire Line
	7900 800  7900 900 
Wire Wire Line
	7900 900  8100 900 
Connection ~ 7900 800 
Wire Wire Line
	9000 850  9000 1150
Wire Wire Line
	9000 1150 8550 1150
Wire Wire Line
	8550 1150 8550 1350
Wire Wire Line
	6400 2300 6950 2300
Wire Wire Line
	6950 2300 6950 2100
Wire Wire Line
	6950 1950 6950 2000
Wire Wire Line
	6400 2650 8550 2650
Wire Wire Line
	8550 2650 8550 2600
Wire Wire Line
	6450 3000 7400 3000
Wire Wire Line
	7400 3000 7400 3100
Wire Wire Line
	6400 3300 7400 3300
Wire Wire Line
	7400 3300 7400 3200
Wire Wire Line
	6400 3650 6950 3650
Wire Wire Line
	6950 3650 6950 3700
Wire Wire Line
	6400 4000 6400 3800
Wire Wire Line
	6400 3800 6950 3800
Wire Wire Line
	6400 4350 8550 4350
Wire Wire Line
	8550 4350 8550 4300
Wire Wire Line
	7850 3750 7850 3650
Wire Wire Line
	7850 3650 8100 3650
Wire Wire Line
	7950 3650 7950 3750
Wire Wire Line
	7950 3750 8100 3750
Connection ~ 7950 3650
Wire Wire Line
	9000 3700 9000 4100
Wire Wire Line
	9000 4100 8550 4100
Wire Wire Line
	8550 4100 8550 4200
Wire Wire Line
	6700 4800 7350 4800
Wire Wire Line
	7350 4800 7350 5000
Wire Wire Line
	6450 5200 7350 5200
Wire Wire Line
	7350 5200 7350 5100
Wire Wire Line
	6400 6400 7450 6400
Wire Wire Line
	7450 6400 7450 6650
Wire Wire Line
	6450 6850 7450 6850
Wire Wire Line
	7450 6850 7450 6750
Wire Wire Line
	6450 5450 6950 5450
Wire Wire Line
	6950 5450 6950 5550
Wire Wire Line
	6450 5700 6950 5700
Wire Wire Line
	6950 5700 6950 5650
Wire Wire Line
	6400 6050 8300 6050
Wire Wire Line
	8300 6050 8300 6150
Wire Wire Line
	8300 6150 8550 6150
Wire Wire Line
	9000 5550 9000 5850
Wire Wire Line
	9000 5850 8550 5850
Wire Wire Line
	8550 5850 8550 6050
Wire Wire Line
	8100 5500 8000 5500
Wire Wire Line
	8000 5500 8000 5600
Wire Wire Line
	8000 5600 8100 5600
Wire Wire Line
	7850 5600 7850 5550
Wire Wire Line
	7850 5550 8000 5550
Connection ~ 8000 5550
Wire Wire Line
	2400 5300 1850 5300
Connection ~ 2400 5300
Wire Wire Line
	1850 5300 1850 4750
Wire Wire Line
	2400 1900 2400 5350
Wire Wire Line
	1000 7000 1750 7000
$Comp
L d_nand U33
U 1 1 6808DDE8
P 2450 5800
F 0 "U33" H 2450 5800 60  0000 C CNN
F 1 "d_nand" H 2500 5900 60  0000 C CNN
F 2 "" H 2450 5800 60  0000 C CNN
F 3 "" H 2450 5800 60  0000 C CNN
	1    2450 5800
	0    -1   -1   0   
$EndComp
Wire Wire Line
	1750 6400 1750 7300
Wire Wire Line
	1750 7300 2050 7300
Wire Wire Line
	1750 6400 1100 6400
Connection ~ 1100 6400
Connection ~ 1750 7000
$Comp
L d_inverter U39
U 1 1 68161C40
P 10050 1400
F 0 "U39" H 10050 1300 60  0000 C CNN
F 1 "d_inverter" H 10050 1550 60  0000 C CNN
F 2 "" H 10100 1350 60  0000 C CNN
F 3 "" H 10100 1350 60  0000 C CNN
	1    10050 1400
	1    0    0    -1  
$EndComp
Wire Wire Line
	9450 1400 9750 1400
Wire Wire Line
	10350 1400 10650 1400
$Comp
L d_inverter U40
U 1 1 6816223F
P 10050 2550
F 0 "U40" H 10050 2450 60  0000 C CNN
F 1 "d_inverter" H 10050 2700 60  0000 C CNN
F 2 "" H 10100 2500 60  0000 C CNN
F 3 "" H 10100 2500 60  0000 C CNN
	1    10050 2550
	1    0    0    -1  
$EndComp
Wire Wire Line
	9450 2550 9750 2550
Wire Wire Line
	10350 2550 10650 2550
$Comp
L d_inverter U34
U 1 1 6816284C
P 9800 3150
F 0 "U34" H 9800 3050 60  0000 C CNN
F 1 "d_inverter" H 9800 3300 60  0000 C CNN
F 2 "" H 9850 3100 60  0000 C CNN
F 3 "" H 9850 3100 60  0000 C CNN
	1    9800 3150
	1    0    0    -1  
$EndComp
Wire Wire Line
	8300 3150 9500 3150
Wire Wire Line
	10100 3150 10650 3150
$Comp
L d_inverter U41
U 1 1 68162B94
P 10050 4250
F 0 "U41" H 10050 4150 60  0000 C CNN
F 1 "d_inverter" H 10050 4400 60  0000 C CNN
F 2 "" H 10100 4200 60  0000 C CNN
F 3 "" H 10100 4200 60  0000 C CNN
	1    10050 4250
	1    0    0    -1  
$EndComp
Wire Wire Line
	9450 4250 9750 4250
Wire Wire Line
	10350 4250 10650 4250
$Comp
L d_inverter U8
U 1 1 6816304F
P 9700 5050
F 0 "U8" H 9700 4950 60  0000 C CNN
F 1 "d_inverter" H 9700 5200 60  0000 C CNN
F 2 "" H 9750 5000 60  0000 C CNN
F 3 "" H 9750 5000 60  0000 C CNN
	1    9700 5050
	1    0    0    -1  
$EndComp
Wire Wire Line
	8250 5050 9400 5050
Wire Wire Line
	10000 5050 10650 5050
$Comp
L d_inverter U42
U 1 1 68163399
P 10100 6100
F 0 "U42" H 10100 6000 60  0000 C CNN
F 1 "d_inverter" H 10100 6250 60  0000 C CNN
F 2 "" H 10150 6050 60  0000 C CNN
F 3 "" H 10150 6050 60  0000 C CNN
	1    10100 6100
	1    0    0    -1  
$EndComp
Wire Wire Line
	9450 6100 9800 6100
Wire Wire Line
	10400 6100 10650 6100
$Comp
L d_inverter U7
U 1 1 681636FC
P 9650 6700
F 0 "U7" H 9650 6600 60  0000 C CNN
F 1 "d_inverter" H 9650 6850 60  0000 C CNN
F 2 "" H 9700 6650 60  0000 C CNN
F 3 "" H 9700 6650 60  0000 C CNN
	1    9650 6700
	1    0    0    -1  
$EndComp
Wire Wire Line
	8350 6700 9350 6700
Wire Wire Line
	9950 6700 10650 6700
$EndSCHEMATC
