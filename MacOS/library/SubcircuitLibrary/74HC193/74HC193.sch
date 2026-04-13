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
LIBS:4_bit_updown_counter-cache
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
L jk_mux X1
U 1 1 67CB2B93
P 2200 3950
F 0 "X1" H 2200 3950 60  0000 C CNN
F 1 "jk_mux" H 2200 4100 60  0000 C CNN
F 2 "" H 2200 3950 60  0001 C CNN
F 3 "" H 2200 3950 60  0001 C CNN
	1    2200 3950
	1    0    0    -1  
$EndComp
$Comp
L jk_mux X7
U 1 1 67CB2C1E
P 10000 3950
F 0 "X7" H 10000 3950 60  0000 C CNN
F 1 "jk_mux" H 10000 4100 60  0000 C CNN
F 2 "" H 10000 3950 60  0001 C CNN
F 3 "" H 10000 3950 60  0001 C CNN
	1    10000 3950
	1    0    0    -1  
$EndComp
$Comp
L jk_mux X3
U 1 1 67CB2CAB
P 4750 3950
F 0 "X3" H 4750 3950 60  0000 C CNN
F 1 "jk_mux" H 4750 4100 60  0000 C CNN
F 2 "" H 4750 3950 60  0001 C CNN
F 3 "" H 4750 3950 60  0001 C CNN
	1    4750 3950
	1    0    0    -1  
$EndComp
$Comp
L jk_mux X5
U 1 1 67CB2D02
P 7500 3950
F 0 "X5" H 7500 3950 60  0000 C CNN
F 1 "jk_mux" H 7500 4100 60  0000 C CNN
F 2 "" H 7500 3950 60  0001 C CNN
F 3 "" H 7500 3950 60  0001 C CNN
	1    7500 3950
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 5 1 67CBF733
P 1200 650
F 0 "U1" H 1250 750 30  0000 C CNN
F 1 "PORT" H 1200 650 30  0000 C CNN
F 2 "" H 1200 650 60  0000 C CNN
F 3 "" H 1200 650 60  0000 C CNN
	5    1200 650 
	0    1    1    0   
$EndComp
$Comp
L PORT U1
U 9 1 67CBF7BE
P 3750 650
F 0 "U1" H 3800 750 30  0000 C CNN
F 1 "PORT" H 3750 650 30  0000 C CNN
F 2 "" H 3750 650 60  0000 C CNN
F 3 "" H 3750 650 60  0000 C CNN
	9    3750 650 
	0    1    1    0   
$EndComp
$Comp
L PORT U1
U 11 1 67CBF857
P 6350 650
F 0 "U1" H 6400 750 30  0000 C CNN
F 1 "PORT" H 6350 650 30  0000 C CNN
F 2 "" H 6350 650 60  0000 C CNN
F 3 "" H 6350 650 60  0000 C CNN
	11   6350 650 
	0    1    1    0   
$EndComp
$Comp
L PORT U1
U 13 1 67CBF8E4
P 9000 650
F 0 "U1" H 9050 750 30  0000 C CNN
F 1 "PORT" H 9000 650 30  0000 C CNN
F 2 "" H 9000 650 60  0000 C CNN
F 3 "" H 9000 650 60  0000 C CNN
	13   9000 650 
	0    1    1    0   
$EndComp
Wire Wire Line
	1200 900  1200 3450
Wire Wire Line
	1200 3450 1650 3450
Wire Wire Line
	6350 900  6350 3450
Wire Wire Line
	6350 3450 6950 3450
Wire Wire Line
	9000 900  9000 3450
Wire Wire Line
	9000 3450 9450 3450
Wire Wire Line
	4200 3800 3950 3800
Wire Wire Line
	3950 3800 3950 3600
Connection ~ 3950 3600
Wire Wire Line
	6250 3600 6950 3600
Wire Wire Line
	6950 3800 6550 3800
Wire Wire Line
	6550 3800 6550 3600
Connection ~ 6550 3600
Wire Wire Line
	8900 3600 9450 3600
Wire Wire Line
	9450 3800 9150 3800
Wire Wire Line
	9150 3800 9150 3600
Connection ~ 9150 3600
$Comp
L PORT U1
U 1 1 67CBFD44
P 550 2050
F 0 "U1" H 600 2150 30  0000 C CNN
F 1 "PORT" H 550 2050 30  0000 C CNN
F 2 "" H 550 2050 60  0000 C CNN
F 3 "" H 550 2050 60  0000 C CNN
	1    550  2050
	1    0    0    -1  
$EndComp
Wire Wire Line
	3650 3600 4200 3600
Wire Wire Line
	3750 900  3750 3450
Wire Wire Line
	3750 3450 4200 3450
$Comp
L d_inverter U2
U 1 1 67CC08A9
P 1750 2450
F 0 "U2" H 1750 2350 60  0000 C CNN
F 1 "d_inverter" H 1750 2600 60  0000 C CNN
F 2 "" H 1800 2400 60  0000 C CNN
F 3 "" H 1800 2400 60  0000 C CNN
	1    1750 2450
	1    0    0    -1  
$EndComp
Wire Wire Line
	1450 2450 1450 2050
Connection ~ 1450 2050
$Comp
L PORT U1
U 7 1 67CC09D2
P 2200 7500
F 0 "U1" H 2250 7600 30  0000 C CNN
F 1 "PORT" H 2200 7500 30  0000 C CNN
F 2 "" H 2200 7500 60  0000 C CNN
F 3 "" H 2200 7500 60  0000 C CNN
	7    2200 7500
	0    -1   -1   0   
$EndComp
Wire Wire Line
	10000 6150 10000 4750
Wire Wire Line
	7500 6150 7500 4750
Connection ~ 7500 6150
Wire Wire Line
	4750 4750 4750 6150
Connection ~ 4750 6150
Wire Wire Line
	2200 4750 2200 7250
Connection ~ 2200 6150
Wire Wire Line
	2200 6150 10000 6150
$Comp
L PORT U1
U 2 1 67CC0EFA
P 550 7500
F 0 "U1" H 600 7600 30  0000 C CNN
F 1 "PORT" H 550 7500 30  0000 C CNN
F 2 "" H 550 7500 60  0000 C CNN
F 3 "" H 550 7500 60  0000 C CNN
	2    550  7500
	0    -1   -1   0   
$EndComp
$Comp
L PORT U1
U 4 1 67CC0FCB
P 950 7500
F 0 "U1" H 1000 7600 30  0000 C CNN
F 1 "PORT" H 950 7500 30  0000 C CNN
F 2 "" H 950 7500 60  0000 C CNN
F 3 "" H 950 7500 60  0000 C CNN
	4    950  7500
	0    -1   -1   0   
$EndComp
$Comp
L PORT U1
U 6 1 67CC1066
P 1400 7500
F 0 "U1" H 1450 7600 30  0000 C CNN
F 1 "PORT" H 1400 7500 30  0000 C CNN
F 2 "" H 1400 7500 60  0000 C CNN
F 3 "" H 1400 7500 60  0000 C CNN
	6    1400 7500
	0    -1   -1   0   
$EndComp
Wire Wire Line
	550  3950 550  7250
Wire Wire Line
	550  3950 1650 3950
Connection ~ 550  6000
Wire Wire Line
	550  6000 9200 6000
Wire Wire Line
	9200 6000 9200 3950
Wire Wire Line
	9200 3950 9450 3950
Wire Wire Line
	6950 3950 6700 3950
Wire Wire Line
	6700 3950 6700 6000
Connection ~ 6700 6000
Wire Wire Line
	4200 3950 3950 3950
Wire Wire Line
	3950 3950 3950 6000
Connection ~ 3950 6000
Wire Wire Line
	950  4100 950  7250
Wire Wire Line
	950  4100 1650 4100
Wire Wire Line
	1400 4350 1400 7250
Wire Wire Line
	1400 4350 1650 4350
Connection ~ 950  5800
Wire Wire Line
	950  5800 9300 5800
Wire Wire Line
	9300 5800 9300 4100
Wire Wire Line
	9300 4100 9450 4100
Wire Wire Line
	6950 4100 6800 4100
Wire Wire Line
	6800 4100 6800 5800
Connection ~ 6800 5800
Wire Wire Line
	4200 4100 4050 4100
Wire Wire Line
	4050 4100 4050 5800
Connection ~ 4050 5800
Connection ~ 1400 5600
Wire Wire Line
	1400 5600 9450 5600
Wire Wire Line
	9450 5600 9450 4350
Wire Wire Line
	6950 4350 6950 5600
Connection ~ 6950 5600
Wire Wire Line
	4200 4350 4200 5600
Connection ~ 4200 5600
$Comp
L PORT U1
U 3 1 67CC156A
P 800 3600
F 0 "U1" H 850 3700 30  0000 C CNN
F 1 "PORT" H 800 3600 30  0000 C CNN
F 2 "" H 800 3600 60  0000 C CNN
F 3 "" H 800 3600 60  0000 C CNN
	3    800  3600
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 10 1 67CC170A
P 5650 3550
F 0 "U1" H 5700 3650 30  0000 C CNN
F 1 "PORT" H 5650 3550 30  0000 C CNN
F 2 "" H 5650 3550 60  0000 C CNN
F 3 "" H 5650 3550 60  0000 C CNN
	10   5650 3550
	-1   0    0    1   
$EndComp
$Comp
L PORT U1
U 12 1 67CC17C3
P 8400 3550
F 0 "U1" H 8450 3650 30  0000 C CNN
F 1 "PORT" H 8400 3550 30  0000 C CNN
F 2 "" H 8400 3550 60  0000 C CNN
F 3 "" H 8400 3550 60  0000 C CNN
	12   8400 3550
	-1   0    0    1   
$EndComp
$Comp
L PORT U1
U 14 1 67CC186C
P 11000 3550
F 0 "U1" H 11050 3650 30  0000 C CNN
F 1 "PORT" H 11000 3550 30  0000 C CNN
F 2 "" H 11000 3550 60  0000 C CNN
F 3 "" H 11000 3550 60  0000 C CNN
	14   11000 3550
	-1   0    0    1   
$EndComp
Wire Wire Line
	10750 3550 10550 3550
Wire Wire Line
	1050 3600 1650 3600
Wire Wire Line
	1650 3800 1350 3800
Wire Wire Line
	1350 3800 1350 3600
Connection ~ 1350 3600
Wire Wire Line
	800  2050 2350 2050
$Comp
L d_and U3
U 1 1 67CC2A19
P 2800 2150
F 0 "U3" H 2800 2150 60  0000 C CNN
F 1 "d_and" H 2850 2250 60  0000 C CNN
F 2 "" H 2800 2150 60  0000 C CNN
F 3 "" H 2800 2150 60  0000 C CNN
	1    2800 2150
	1    0    0    -1  
$EndComp
Wire Wire Line
	2350 2150 2350 3200
Wire Wire Line
	2350 3200 2800 3200
Wire Wire Line
	2800 3200 2800 3550
Connection ~ 2800 3550
$Comp
L d_and U4
U 1 1 67CC3A7A
P 3200 5200
F 0 "U4" H 3200 5200 60  0000 C CNN
F 1 "d_and" H 3250 5300 60  0000 C CNN
F 2 "" H 3200 5200 60  0000 C CNN
F 3 "" H 3200 5200 60  0000 C CNN
	1    3200 5200
	1    0    0    -1  
$EndComp
Wire Wire Line
	2050 2450 2600 2450
Wire Wire Line
	2600 2450 2600 5200
Wire Wire Line
	2600 5200 2750 5200
Wire Wire Line
	2750 4150 2750 5100
$Comp
L PORT U1
U 8 1 67CC1643
P 3050 3550
F 0 "U1" H 3100 3650 30  0000 C CNN
F 1 "PORT" H 3050 3550 30  0000 C CNN
F 2 "" H 3050 3550 60  0000 C CNN
F 3 "" H 3050 3550 60  0000 C CNN
	8    3050 3550
	-1   0    0    1   
$EndComp
Wire Wire Line
	2800 3550 2750 3550
$Comp
L d_or U5
U 1 1 67CC3CDE
P 3400 3950
F 0 "U5" H 3400 3950 60  0000 C CNN
F 1 "d_or" H 3400 4050 60  0000 C CNN
F 2 "" H 3400 3950 60  0000 C CNN
F 3 "" H 3400 3950 60  0000 C CNN
	1    3400 3950
	1    0    0    -1  
$EndComp
Wire Wire Line
	3650 3600 3650 3750
Wire Wire Line
	3650 3750 3850 3750
Wire Wire Line
	3850 3750 3850 3900
Wire Wire Line
	3250 2100 3250 3300
Wire Wire Line
	3250 3300 2950 3300
Wire Wire Line
	2950 3300 2950 3850
Wire Wire Line
	2950 3950 2950 4750
Wire Wire Line
	2950 4750 3650 4750
Wire Wire Line
	3650 4750 3650 5150
Wire Wire Line
	5300 3550 5400 3550
Connection ~ 5350 3550
$Comp
L d_and U6
U 1 1 67CC3FFA
P 5400 2400
F 0 "U6" H 5400 2400 60  0000 C CNN
F 1 "d_and" H 5450 2500 60  0000 C CNN
F 2 "" H 5400 2400 60  0000 C CNN
F 3 "" H 5400 2400 60  0000 C CNN
	1    5400 2400
	1    0    0    -1  
$EndComp
Connection ~ 3250 2300
Wire Wire Line
	3250 2300 4950 2300
Wire Wire Line
	5350 3550 5350 2750
Wire Wire Line
	5350 2750 4950 2750
Wire Wire Line
	4950 2750 4950 2400
$Comp
L d_and U7
U 1 1 67CC414B
P 5650 5250
F 0 "U7" H 5650 5250 60  0000 C CNN
F 1 "d_and" H 5700 5350 60  0000 C CNN
F 2 "" H 5650 5250 60  0000 C CNN
F 3 "" H 5650 5250 60  0000 C CNN
	1    5650 5250
	1    0    0    -1  
$EndComp
Connection ~ 3650 5100
Wire Wire Line
	3650 5100 5200 5100
Wire Wire Line
	5200 5100 5200 5150
Wire Wire Line
	5300 4150 5300 4950
Wire Wire Line
	5300 4950 5000 4950
Wire Wire Line
	5000 4950 5000 5250
Wire Wire Line
	5000 5250 5200 5250
$Comp
L d_or U8
U 1 1 67CC429C
P 5950 4050
F 0 "U8" H 5950 4050 60  0000 C CNN
F 1 "d_or" H 5950 4150 60  0000 C CNN
F 2 "" H 5950 4050 60  0000 C CNN
F 3 "" H 5950 4050 60  0000 C CNN
	1    5950 4050
	1    0    0    -1  
$EndComp
Wire Wire Line
	6250 3600 6250 3900
Wire Wire Line
	6250 3900 6400 3900
Wire Wire Line
	6400 3900 6400 4000
Wire Wire Line
	5850 2350 5850 2950
Wire Wire Line
	5850 2950 5500 2950
Wire Wire Line
	5500 2950 5500 3950
Wire Wire Line
	5500 4050 5500 4750
Wire Wire Line
	5500 4750 6100 4750
Wire Wire Line
	6100 4750 6100 5200
Wire Wire Line
	8150 3550 8050 3550
Connection ~ 8100 3550
$Comp
L d_and U9
U 1 1 67CC4593
P 7950 2500
F 0 "U9" H 7950 2500 60  0000 C CNN
F 1 "d_and" H 8000 2600 60  0000 C CNN
F 2 "" H 7950 2500 60  0000 C CNN
F 3 "" H 7950 2500 60  0000 C CNN
	1    7950 2500
	1    0    0    -1  
$EndComp
Wire Wire Line
	8100 3550 8100 2900
Wire Wire Line
	8100 2900 7500 2900
Wire Wire Line
	7500 2900 7500 2500
Connection ~ 5850 2400
Wire Wire Line
	5850 2400 7500 2400
$Comp
L d_and U10
U 1 1 67CC472D
P 8250 5150
F 0 "U10" H 8250 5150 60  0000 C CNN
F 1 "d_and" H 8300 5250 60  0000 C CNN
F 2 "" H 8250 5150 60  0000 C CNN
F 3 "" H 8250 5150 60  0000 C CNN
	1    8250 5150
	1    0    0    -1  
$EndComp
Connection ~ 6100 5150
Wire Wire Line
	6100 5150 7800 5150
Wire Wire Line
	8050 4150 8050 4850
Wire Wire Line
	8050 4850 7800 4850
Wire Wire Line
	7800 4850 7800 5050
$Comp
L d_or U11
U 1 1 67CC48C6
P 8650 4100
F 0 "U11" H 8650 4100 60  0000 C CNN
F 1 "d_or" H 8650 4200 60  0000 C CNN
F 2 "" H 8650 4100 60  0000 C CNN
F 3 "" H 8650 4100 60  0000 C CNN
	1    8650 4100
	1    0    0    -1  
$EndComp
Wire Wire Line
	8900 3600 8900 3900
Wire Wire Line
	8900 3900 9100 3900
Wire Wire Line
	9100 3900 9100 4050
Wire Wire Line
	8400 2450 8400 3350
Wire Wire Line
	8400 3350 8200 3350
Wire Wire Line
	8200 3350 8200 4000
Wire Wire Line
	8700 5100 8700 4350
Wire Wire Line
	8700 4350 8200 4350
Wire Wire Line
	8200 4350 8200 4100
Wire Wire Line
	9400 1750 8600 1750
Wire Wire Line
	8600 1750 8600 2700
Wire Wire Line
	8600 2700 8400 2700
Connection ~ 8400 2700
Wire Wire Line
	9400 1850 9400 2850
Wire Wire Line
	9400 2850 10650 2850
Wire Wire Line
	10650 2850 10650 3550
Connection ~ 10650 3550
$Comp
L PORT U1
U 15 1 67D6C2D6
P 11100 2350
F 0 "U1" H 11150 2450 30  0000 C CNN
F 1 "PORT" H 11100 2350 30  0000 C CNN
F 2 "" H 11100 2350 60  0000 C CNN
F 3 "" H 11100 2350 60  0000 C CNN
	15   11100 2350
	0    -1   -1   0   
$EndComp
$Comp
L d_nand U13
U 1 1 67D6D209
P 10200 5550
F 0 "U13" H 10200 5550 60  0000 C CNN
F 1 "d_nand" H 10250 5650 60  0000 C CNN
F 2 "" H 10200 5550 60  0000 C CNN
F 3 "" H 10200 5550 60  0000 C CNN
	1    10200 5550
	1    0    0    -1  
$EndComp
Wire Wire Line
	10550 4150 10550 5100
Wire Wire Line
	10550 5100 9750 5100
Wire Wire Line
	9750 5100 9750 5450
Wire Wire Line
	9750 5550 8900 5550
Wire Wire Line
	8900 5550 8900 4900
Wire Wire Line
	8900 4900 8700 4900
Connection ~ 8700 4900
$Comp
L PORT U1
U 16 1 67D6D424
P 10900 5500
F 0 "U1" H 10950 5600 30  0000 C CNN
F 1 "PORT" H 10900 5500 30  0000 C CNN
F 2 "" H 10900 5500 60  0000 C CNN
F 3 "" H 10900 5500 60  0000 C CNN
	16   10900 5500
	-1   0    0    1   
$EndComp
$Comp
L d_and U12
U 1 1 67DEB3AC
P 9850 1850
F 0 "U12" H 9850 1850 60  0000 C CNN
F 1 "d_and" H 9900 1950 60  0000 C CNN
F 2 "" H 9850 1850 60  0000 C CNN
F 3 "" H 9850 1850 60  0000 C CNN
	1    9850 1850
	1    0    0    -1  
$EndComp
$Comp
L d_inverter U14
U 1 1 67DEB593
P 10600 1300
F 0 "U14" H 10600 1200 60  0000 C CNN
F 1 "d_inverter" H 10600 1450 60  0000 C CNN
F 2 "" H 10650 1250 60  0000 C CNN
F 3 "" H 10650 1250 60  0000 C CNN
	1    10600 1300
	1    0    0    -1  
$EndComp
Wire Wire Line
	10300 1800 10300 1300
Wire Wire Line
	10900 1300 11100 1300
Wire Wire Line
	11100 1300 11100 2100
$EndSCHEMATC
