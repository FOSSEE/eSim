EESchema Schematic File Version 2
LIBS:CD4027B_JK_FF-rescue
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
LIBS:CD4027B_JK_FF-cache
EELAYER 25 0
EELAYER END
$Descr A0 46811 33110
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
L BUFFER X1
U 1 1 6655919C
P 5950 12400
F 0 "X1" H 8150 12350 60  0000 C CNN
F 1 "BUFFER" H 8150 12450 60  0000 C CNN
F 2 "" H 5950 12400 60  0001 C CNN
F 3 "" H 5950 12400 60  0001 C CNN
	1    5950 12400
	1    0    0    -1  
$EndComp
$Comp
L NOT_Gate X2
U 1 1 66559541
P 7250 10800
F 0 "X2" H 7850 10600 60  0000 C CNN
F 1 "NOT_Gate" H 7900 11000 60  0000 C CNN
F 2 "" H 7250 10800 60  0001 C CNN
F 3 "" H 7250 10800 60  0001 C CNN
	1    7250 10800
	1    0    0    -1  
$EndComp
$Comp
L NOT_Gate X3
U 1 1 66559588
P 7250 13950
F 0 "X3" H 7850 13750 60  0000 C CNN
F 1 "NOT_Gate" H 7900 14150 60  0000 C CNN
F 2 "" H 7250 13950 60  0001 C CNN
F 3 "" H 7250 13950 60  0001 C CNN
	1    7250 13950
	1    0    0    -1  
$EndComp
$Comp
L NOT_Gate X4
U 1 1 6655962E
P 7250 15350
F 0 "X4" H 7850 15150 60  0000 C CNN
F 1 "NOT_Gate" H 7900 15550 60  0000 C CNN
F 2 "" H 7250 15350 60  0001 C CNN
F 3 "" H 7250 15350 60  0001 C CNN
	1    7250 15350
	1    0    0    -1  
$EndComp
$Comp
L NOT_Gate X5
U 1 1 6655967E
P 7250 16500
F 0 "X5" H 7850 16300 60  0000 C CNN
F 1 "NOT_Gate" H 7900 16700 60  0000 C CNN
F 2 "" H 7250 16500 60  0001 C CNN
F 3 "" H 7250 16500 60  0001 C CNN
	1    7250 16500
	1    0    0    -1  
$EndComp
$Comp
L NOT_Gate X6
U 1 1 665596FD
P 8250 16500
F 0 "X6" H 8850 16300 60  0000 C CNN
F 1 "NOT_Gate" H 8900 16700 60  0000 C CNN
F 2 "" H 8250 16500 60  0001 C CNN
F 3 "" H 8250 16500 60  0001 C CNN
	1    8250 16500
	1    0    0    -1  
$EndComp
$Comp
L NOT_Gate X8
U 1 1 665597EB
P 9200 13150
F 0 "X8" H 9800 12950 60  0000 C CNN
F 1 "NOT_Gate" H 9850 13350 60  0000 C CNN
F 2 "" H 9200 13150 60  0001 C CNN
F 3 "" H 9200 13150 60  0001 C CNN
	1    9200 13150
	1    0    0    -1  
$EndComp
$Comp
L AND_Gate X10
U 1 1 66559AC4
P 11650 12900
F 0 "X10" H 12850 12650 60  0000 C CNN
F 1 "AND_Gate" H 12800 13150 60  0000 C CNN
F 2 "" H 11650 12900 60  0001 C CNN
F 3 "" H 11650 12900 60  0001 C CNN
	1    11650 12900
	1    0    0    -1  
$EndComp
$Comp
L mosfet_n M2
U 1 1 66559CA1
P 14200 13400
F 0 "M2" H 14200 13250 50  0000 R CNN
F 1 "mosfet_n" H 14300 13350 50  0000 R CNN
F 2 "" H 14500 13100 29  0000 C CNN
F 3 "" H 14300 13200 60  0000 C CNN
	1    14200 13400
	0    1    -1   0   
$EndComp
$Comp
L mosfet_p M1
U 1 1 66559D02
P 14000 12550
F 0 "M1" H 13950 12600 50  0000 R CNN
F 1 "mosfet_p" H 14050 12700 50  0000 R CNN
F 2 "" H 14250 12650 29  0000 C CNN
F 3 "" H 14050 12550 60  0000 C CNN
	1    14000 12550
	0    1    1    0   
$EndComp
$Comp
L mosfet_n M4
U 1 1 6655A8AA
P 17250 14750
F 0 "M4" H 17250 14600 50  0000 R CNN
F 1 "mosfet_n" H 17350 14700 50  0000 R CNN
F 2 "" H 17550 14450 29  0000 C CNN
F 3 "" H 17350 14550 60  0000 C CNN
	1    17250 14750
	0    1    1    0   
$EndComp
$Comp
L mosfet_p M3
U 1 1 6655A8B0
P 17050 15600
F 0 "M3" H 17000 15650 50  0000 R CNN
F 1 "mosfet_p" H 17100 15750 50  0000 R CNN
F 2 "" H 17300 15700 29  0000 C CNN
F 3 "" H 17100 15600 60  0000 C CNN
	1    17050 15600
	0    1    -1   0   
$EndComp
$Comp
L mosfet_n M6
U 1 1 6655B2E5
P 22300 11600
F 0 "M6" H 22300 11450 50  0000 R CNN
F 1 "mosfet_n" H 22400 11550 50  0000 R CNN
F 2 "" H 22600 11300 29  0000 C CNN
F 3 "" H 22400 11400 60  0000 C CNN
	1    22300 11600
	0    1    1    0   
$EndComp
$Comp
L mosfet_p M5
U 1 1 6655B2EB
P 22100 12450
F 0 "M5" H 22050 12500 50  0000 R CNN
F 1 "mosfet_p" H 22150 12600 50  0000 R CNN
F 2 "" H 22350 12550 29  0000 C CNN
F 3 "" H 22150 12450 60  0000 C CNN
	1    22100 12450
	0    1    -1   0   
$EndComp
$Comp
L mosfet_n M8
U 1 1 6655B609
P 25900 15700
F 0 "M8" H 25900 15550 50  0000 R CNN
F 1 "mosfet_n" H 26000 15650 50  0000 R CNN
F 2 "" H 26200 15400 29  0000 C CNN
F 3 "" H 26000 15500 60  0000 C CNN
	1    25900 15700
	0    1    -1   0   
$EndComp
$Comp
L mosfet_p M7
U 1 1 6655B60F
P 25700 14850
F 0 "M7" H 25650 14900 50  0000 R CNN
F 1 "mosfet_p" H 25750 15000 50  0000 R CNN
F 2 "" H 25950 14950 29  0000 C CNN
F 3 "" H 25750 14850 60  0000 C CNN
	1    25700 14850
	0    1    1    0   
$EndComp
$Comp
L BUFFER X14
U 1 1 6655F896
P 29950 11800
F 0 "X14" H 32150 11750 60  0000 C CNN
F 1 "BUFFER" H 32150 11850 60  0000 C CNN
F 2 "" H 29950 11800 60  0001 C CNN
F 3 "" H 29950 11800 60  0001 C CNN
	1    29950 11800
	1    0    0    -1  
$EndComp
$Comp
L BUFFER X15
U 1 1 6655FBAD
P 30000 16550
F 0 "X15" H 32200 16500 60  0000 C CNN
F 1 "BUFFER" H 32200 16600 60  0000 C CNN
F 2 "" H 30000 16550 60  0001 C CNN
F 3 "" H 30000 16550 60  0001 C CNN
	1    30000 16550
	1    0    0    -1  
$EndComp
Wire Wire Line
	8850 12400 9500 12400
Wire Wire Line
	9500 10050 9500 13150
Wire Wire Line
	9500 13150 9550 13150
Wire Wire Line
	10250 13150 10850 13150
Wire Wire Line
	10850 13150 10850 13350
Wire Wire Line
	10850 13500 8300 13500
Wire Wire Line
	8300 13500 8300 13950
Wire Wire Line
	10400 12450 12400 12450
Wire Wire Line
	12400 12450 12400 12800
Wire Wire Line
	12400 13000 11750 13000
Wire Wire Line
	11750 13000 11750 13400
Wire Wire Line
	13350 12700 13350 13200
Wire Wire Line
	13350 12700 13800 12700
Wire Wire Line
	13350 13200 13800 13200
Connection ~ 13350 12900
Wire Wire Line
	14400 13200 14200 13200
Wire Wire Line
	14400 12700 14400 13200
Wire Wire Line
	14200 12700 14400 12700
Wire Wire Line
	13850 13100 13700 13100
Wire Wire Line
	13700 13100 13700 13200
Connection ~ 13700 13200
Wire Wire Line
	13850 12800 13850 12900
Wire Wire Line
	13850 12900 14250 12900
Wire Wire Line
	14250 12900 14250 12700
Connection ~ 14250 12700
Wire Wire Line
	16200 11850 14700 11850
Wire Wire Line
	14700 11850 14700 15200
Wire Wire Line
	14700 12950 14400 12950
Connection ~ 14400 12950
Wire Wire Line
	16400 14950 16850 14950
Wire Wire Line
	16400 15450 16850 15450
Wire Wire Line
	17450 15450 17250 15450
Wire Wire Line
	17250 14950 17450 14950
Connection ~ 17300 14950
Wire Wire Line
	14700 15200 16400 15200
Wire Wire Line
	16400 14950 16400 15450
Connection ~ 14700 12950
Connection ~ 16400 15200
Wire Wire Line
	17450 14950 17450 15450
Wire Wire Line
	17450 15250 19850 15250
Wire Wire Line
	19850 15250 19850 14150
Connection ~ 17450 15250
Wire Wire Line
	19550 12250 19550 12050
Wire Wire Line
	17800 12050 21450 12050
Wire Wire Line
	8300 10800 26200 10800
Wire Wire Line
	20050 10800 20050 12250
Wire Wire Line
	21450 11800 21900 11800
Wire Wire Line
	21450 12300 21900 12300
Wire Wire Line
	22500 12300 22300 12300
Wire Wire Line
	22300 11800 22500 11800
Wire Wire Line
	21450 11800 21450 12300
Connection ~ 21450 12050
Wire Wire Line
	22500 11800 22500 12300
Wire Wire Line
	22500 12100 26650 12100
Connection ~ 22500 12100
Connection ~ 19550 12050
Wire Wire Line
	25050 15000 25500 15000
Wire Wire Line
	25050 15500 25500 15500
Wire Wire Line
	26100 15500 25900 15500
Wire Wire Line
	25900 15000 26100 15000
Wire Wire Line
	25550 15400 25400 15400
Wire Wire Line
	25400 15400 25400 15500
Connection ~ 25400 15500
Wire Wire Line
	25550 15100 25550 15200
Wire Wire Line
	25550 15200 25950 15200
Wire Wire Line
	25950 15200 25950 15000
Connection ~ 25950 15000
Wire Wire Line
	25050 15000 25050 15500
Connection ~ 25050 15250
Wire Wire Line
	26100 15000 26100 15500
Wire Wire Line
	26100 15300 28800 15300
Connection ~ 26100 15300
Wire Wire Line
	23550 15250 23550 12100
Connection ~ 23550 12100
Wire Wire Line
	23550 15250 25050 15250
Wire Wire Line
	26200 10800 26200 11600
Connection ~ 20050 10800
Wire Wire Line
	27750 11800 31600 11800
Wire Wire Line
	30900 15000 30900 11800
Wire Wire Line
	30350 15000 30900 15000
Wire Wire Line
	30350 15500 31000 15500
Wire Wire Line
	31000 15500 31000 16100
Wire Wire Line
	31000 16100 8300 16100
Wire Wire Line
	8300 16100 8300 15350
Wire Wire Line
	16200 12350 15450 12350
Wire Wire Line
	15450 12350 15450 16100
Connection ~ 15450 16100
Wire Wire Line
	16900 15350 16900 15250
Wire Wire Line
	16900 15250 17300 15250
Wire Wire Line
	17300 15250 17300 15450
Connection ~ 17300 15450
Wire Wire Line
	16900 15050 16750 15050
Wire Wire Line
	16750 15050 16750 14950
Connection ~ 16750 14950
Wire Wire Line
	21950 12200 21950 12050
Wire Wire Line
	21950 12050 22350 12050
Wire Wire Line
	22350 12050 22350 12300
Connection ~ 22350 12300
Wire Wire Line
	21950 11900 21850 11900
Wire Wire Line
	21850 11900 21850 11800
Connection ~ 21850 11800
Wire Wire Line
	9500 10050 29300 10050
Wire Wire Line
	29300 10050 29300 11800
Connection ~ 29300 11800
Connection ~ 9500 12550
Connection ~ 30900 11800
Wire Wire Line
	27850 15300 27850 16550
Wire Wire Line
	27850 16550 31650 16550
Connection ~ 27850 15300
Wire Wire Line
	8300 16500 8600 16500
Wire Wire Line
	9300 16500 9650 16500
Wire Wire Line
	9650 16500 9650 14700
Wire Wire Line
	9650 14700 12150 14700
Wire Wire Line
	12150 14700 12150 12100
Wire Wire Line
	12150 12100 14000 12100
Wire Wire Line
	14000 11100 14000 12400
Wire Wire Line
	14000 13500 14000 16900
Wire Wire Line
	8400 16900 17050 16900
Wire Wire Line
	8400 16900 8400 16500
Connection ~ 8400 16500
Wire Wire Line
	14000 11100 25700 11100
Wire Wire Line
	22100 11100 22100 11500
Connection ~ 14000 12100
Wire Wire Line
	22100 12600 22100 15800
Wire Wire Line
	22100 14300 14000 14300
Connection ~ 14000 14300
Wire Wire Line
	17050 14650 12150 14650
Connection ~ 12150 14650
Wire Wire Line
	17050 16900 17050 15750
Connection ~ 14000 16900
Wire Wire Line
	22100 15800 25700 15800
Connection ~ 22100 14300
Wire Wire Line
	25700 11100 25700 14700
Connection ~ 22100 11100
Wire Wire Line
	7600 10800 7200 10800
Wire Wire Line
	7100 12400 7600 12400
Wire Wire Line
	7600 13950 7100 13950
Wire Wire Line
	7600 15350 7100 15350
Wire Wire Line
	7600 16500 6950 16500
Wire Wire Line
	32850 11800 33750 11800
Wire Wire Line
	32900 16550 34550 16550
$Comp
L PORT U1
U 5 1 665633EE
P 6700 16500
F 0 "U1" H 6750 16600 30  0000 C CNN
F 1 "PORT" H 6700 16500 30  0000 C CNN
F 2 "" H 6700 16500 60  0000 C CNN
F 3 "" H 6700 16500 60  0000 C CNN
	5    6700 16500
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 2 1 66563716
P 6850 12400
F 0 "U1" H 6900 12500 30  0000 C CNN
F 1 "PORT" H 6850 12400 30  0000 C CNN
F 2 "" H 6850 12400 60  0000 C CNN
F 3 "" H 6850 12400 60  0000 C CNN
	2    6850 12400
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 3 1 66563993
P 6850 13950
F 0 "U1" H 6900 14050 30  0000 C CNN
F 1 "PORT" H 6850 13950 30  0000 C CNN
F 2 "" H 6850 13950 60  0000 C CNN
F 3 "" H 6850 13950 60  0000 C CNN
	3    6850 13950
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 4 1 66563AB1
P 6850 15350
F 0 "U1" H 6900 15450 30  0000 C CNN
F 1 "PORT" H 6850 15350 30  0000 C CNN
F 2 "" H 6850 15350 60  0000 C CNN
F 3 "" H 6850 15350 60  0000 C CNN
	4    6850 15350
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 1 1 66563B94
P 6950 10800
F 0 "U1" H 7000 10900 30  0000 C CNN
F 1 "PORT" H 6950 10800 30  0000 C CNN
F 2 "" H 6950 10800 60  0000 C CNN
F 3 "" H 6950 10800 60  0000 C CNN
	1    6950 10800
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 6 1 66563E84
P 34000 11800
F 0 "U1" H 34050 11900 30  0000 C CNN
F 1 "PORT" H 34000 11800 30  0000 C CNN
F 2 "" H 34000 11800 60  0000 C CNN
F 3 "" H 34000 11800 60  0000 C CNN
	6    34000 11800
	-1   0    0    -1  
$EndComp
$Comp
L PORT U1
U 7 1 6656403F
P 34800 16550
F 0 "U1" H 34850 16650 30  0000 C CNN
F 1 "PORT" H 34800 16550 30  0000 C CNN
F 2 "" H 34800 16550 60  0000 C CNN
F 3 "" H 34800 16550 60  0000 C CNN
	7    34800 16550
	-1   0    0    -1  
$EndComp
$Comp
L NAND_Gate X11
U 1 1 665618D6
P 14700 12600
F 0 "X11" H 17700 13050 60  0000 C CNN
F 1 "NAND_Gate" H 17150 12850 60  0000 C CNN
F 2 "" H 14700 12600 60  0001 C CNN
F 3 "" H 14700 12600 60  0001 C CNN
	1    14700 12600
	1    0    0    -1  
$EndComp
$Comp
L NAND_Gate X12
U 1 1 66561C17
P 19300 10750
F 0 "X12" H 22300 11200 60  0000 C CNN
F 1 "NAND_Gate" H 21750 11000 60  0000 C CNN
F 2 "" H 19300 10750 60  0001 C CNN
F 3 "" H 19300 10750 60  0001 C CNN
	1    19300 10750
	0    1    1    0   
$EndComp
$Comp
L NAND_Gate X13
U 1 1 66561E2E
P 24650 12400
F 0 "X13" H 27650 12850 60  0000 C CNN
F 1 "NAND_Gate" H 27100 12650 60  0000 C CNN
F 2 "" H 24650 12400 60  0001 C CNN
F 3 "" H 24650 12400 60  0001 C CNN
	1    24650 12400
	1    0    0    -1  
$EndComp
$Comp
L NAND_Gate X16
U 1 1 66561F1A
P 32350 15700
F 0 "X16" H 35350 16150 60  0000 C CNN
F 1 "NAND_Gate" H 34800 15950 60  0000 C CNN
F 2 "" H 32350 15700 60  0001 C CNN
F 3 "" H 32350 15700 60  0001 C CNN
	1    32350 15700
	-1   0    0    -1  
$EndComp
Wire Wire Line
	16200 11850 16200 12000
Wire Wire Line
	16200 12000 16700 12000
Wire Wire Line
	16200 12350 16200 12200
Wire Wire Line
	16200 12200 16700 12200
Wire Wire Line
	16700 12200 16700 12250
Wire Wire Line
	17800 12100 17800 12050
Wire Wire Line
	19650 12750 19650 12250
Wire Wire Line
	19650 12250 19550 12250
Wire Wire Line
	19900 12750 19900 12250
Wire Wire Line
	19900 12250 20050 12250
Wire Wire Line
	19800 13850 19800 14150
Wire Wire Line
	19800 14150 19850 14150
Wire Wire Line
	26200 11600 26650 11600
Wire Wire Line
	26650 11600 26650 11800
Wire Wire Line
	26650 12100 26650 12050
Wire Wire Line
	27750 11900 27750 11800
Wire Wire Line
	29250 15200 28800 15200
Wire Wire Line
	28800 15200 28800 15300
Wire Wire Line
	30350 15000 30350 15100
Wire Wire Line
	30350 15350 30350 15500
Wire Wire Line
	7850 10500 9850 10500
Wire Wire Line
	9850 10500 9850 12100
Wire Wire Line
	9850 12000 11200 12000
Wire Wire Line
	11200 12000 11200 13050
Connection ~ 9850 12000
Wire Wire Line
	9800 12850 9750 12850
Wire Wire Line
	9750 12850 9750 12700
Wire Wire Line
	9750 12700 11200 12700
Connection ~ 11200 12700
Wire Wire Line
	12850 12500 12850 12250
Wire Wire Line
	12850 12250 11200 12250
Connection ~ 11200 12250
Wire Wire Line
	17150 11700 10950 11700
Wire Wire Line
	10950 11700 10950 12000
Connection ~ 10950 12000
Wire Wire Line
	20550 13200 20200 13200
Wire Wire Line
	20550 11300 20550 13200
Wire Wire Line
	20550 11500 17000 11500
Wire Wire Line
	17000 11500 17000 11700
Connection ~ 17000 11700
Wire Wire Line
	27100 11500 27100 11300
Wire Wire Line
	20550 11300 29900 11300
Connection ~ 20550 11500
Wire Wire Line
	29900 11250 29900 14800
Connection ~ 27100 11300
Wire Wire Line
	32200 11250 29900 11250
Connection ~ 29900 11300
Wire Wire Line
	32150 12350 32150 15500
Wire Wire Line
	32150 15500 33400 15500
Wire Wire Line
	33400 15500 33400 17100
Wire Wire Line
	33400 17100 32200 17100
Wire Wire Line
	32250 16000 32250 14250
Wire Wire Line
	32250 14250 29900 14250
Connection ~ 29900 14250
Wire Wire Line
	29900 15600 29900 17300
Wire Wire Line
	7500 17300 32350 17300
Wire Wire Line
	32350 17300 32350 17100
Connection ~ 32350 17100
Wire Wire Line
	27100 12300 27100 15800
Wire Wire Line
	27100 15800 29900 15800
Connection ~ 29900 15800
Wire Wire Line
	19400 13200 17150 13200
Wire Wire Line
	17150 13200 17150 12500
Wire Wire Line
	18400 13200 18400 17300
Connection ~ 29900 17300
Connection ~ 18400 13200
Wire Wire Line
	12850 13300 12850 17300
Connection ~ 18400 17300
Wire Wire Line
	11200 13800 11200 17300
Connection ~ 12850 17300
Wire Wire Line
	9850 12850 10300 12850
Wire Wire Line
	10300 12850 10300 17300
Connection ~ 11200 17300
Wire Wire Line
	9800 13450 9800 17300
Connection ~ 10300 17300
Wire Wire Line
	8850 16800 8850 17300
Connection ~ 9800 17300
Wire Wire Line
	7850 16800 7850 17300
Connection ~ 8850 17300
Wire Wire Line
	7850 15050 8450 15050
Wire Wire Line
	7850 15650 7850 16050
Wire Wire Line
	7850 16050 7500 16050
Wire Wire Line
	7500 11100 7500 17300
Connection ~ 7850 17300
Wire Wire Line
	8100 15050 8100 13650
Wire Wire Line
	8100 13650 7850 13650
Connection ~ 8100 15050
Wire Wire Line
	7850 14250 7500 14250
Connection ~ 7500 16050
Wire Wire Line
	8150 12950 7500 12950
Connection ~ 7500 14250
Wire Wire Line
	8200 10500 8200 11850
Connection ~ 8200 10500
Wire Wire Line
	8900 10500 8900 9100
Connection ~ 8900 10500
Wire Wire Line
	17050 17300 17050 18350
Connection ~ 17050 17300
$Comp
L PORT U1
U 8 1 665684DE
P 8650 9100
F 0 "U1" H 8700 9200 30  0000 C CNN
F 1 "PORT" H 8650 9100 30  0000 C CNN
F 2 "" H 8650 9100 60  0000 C CNN
F 3 "" H 8650 9100 60  0000 C CNN
	8    8650 9100
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 9 1 665688E7
P 16800 18350
F 0 "U1" H 16850 18450 30  0000 C CNN
F 1 "PORT" H 16800 18350 30  0000 C CNN
F 2 "" H 16800 18350 60  0000 C CNN
F 3 "" H 16800 18350 60  0000 C CNN
	9    16800 18350
	1    0    0    -1  
$EndComp
Wire Wire Line
	7850 11100 7500 11100
Connection ~ 7500 12950
Wire Wire Line
	7850 16200 7850 16100
Wire Wire Line
	7850 16100 8250 16100
Wire Wire Line
	8250 16100 8250 16000
Wire Wire Line
	8250 16000 8850 16000
Wire Wire Line
	8850 16000 8850 16200
Wire Wire Line
	8450 15050 8450 16000
Connection ~ 8450 16000
Wire Wire Line
	8050 13650 8050 13100
Wire Wire Line
	8050 13100 9150 13100
Wire Wire Line
	9150 13100 9150 10500
Connection ~ 9150 10500
Connection ~ 8050 13650
$Comp
L OR_Gate X9
U 1 1 6656C753
P 10250 13400
F 0 "X9" H 11650 13200 60  0000 C CNN
F 1 "OR_Gate" H 11700 13300 60  0000 C CNN
F 2 "" H 10250 13400 60  0001 C CNN
F 3 "" H 10250 13400 60  0001 C CNN
	1    10250 13400
	1    0    0    -1  
$EndComp
$Comp
L OR_Gate X7
U 1 1 6656C890
P 8900 12450
F 0 "X7" H 10300 12250 60  0000 C CNN
F 1 "OR_Gate" H 10350 12350 60  0000 C CNN
F 2 "" H 8900 12450 60  0001 C CNN
F 3 "" H 8900 12450 60  0001 C CNN
	1    8900 12450
	1    0    0    -1  
$EndComp
$EndSCHEMATC