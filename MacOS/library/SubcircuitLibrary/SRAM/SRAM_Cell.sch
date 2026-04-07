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
LIBS:SRAM_Cell-cache
EELAYER 25 0
EELAYER END
$Descr A1 33110 23386
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
L mosfet_n M3
U 1 1 664DB399
P 13050 9700
F 0 "M3" H 13050 9550 50  0000 R CNN
F 1 "mosfet_n" H 13150 9650 50  0000 R CNN
F 2 "" H 13350 9400 29  0000 C CNN
F 3 "" H 13150 9500 60  0000 C CNN
	1    13050 9700
	-1   0    0    -1  
$EndComp
$Comp
L mosfet_n M4
U 1 1 664DB424
P 14600 9700
F 0 "M4" H 14600 9550 50  0000 R CNN
F 1 "mosfet_n" H 14700 9650 50  0000 R CNN
F 2 "" H 14900 9400 29  0000 C CNN
F 3 "" H 14700 9500 60  0000 C CNN
	1    14600 9700
	1    0    0    -1  
$EndComp
$Comp
L mosfet_n M6
U 1 1 664DB4D1
P 16050 9000
F 0 "M6" H 16050 8850 50  0000 R CNN
F 1 "mosfet_n" H 16150 8950 50  0000 R CNN
F 2 "" H 16350 8700 29  0000 C CNN
F 3 "" H 16150 8800 60  0000 C CNN
	1    16050 9000
	0    1    1    0   
$EndComp
$Comp
L mosfet_p M2
U 1 1 664DB525
P 13000 8550
F 0 "M2" H 12950 8600 50  0000 R CNN
F 1 "mosfet_p" H 13050 8700 50  0000 R CNN
F 2 "" H 13250 8650 29  0000 C CNN
F 3 "" H 13050 8550 60  0000 C CNN
	1    13000 8550
	-1   0    0    -1  
$EndComp
$Comp
L mosfet_p M5
U 1 1 664DB56F
P 14650 8550
F 0 "M5" H 14600 8600 50  0000 R CNN
F 1 "mosfet_p" H 14700 8700 50  0000 R CNN
F 2 "" H 14900 8650 29  0000 C CNN
F 3 "" H 14700 8550 60  0000 C CNN
	1    14650 8550
	1    0    0    -1  
$EndComp
Wire Wire Line
	12850 9700 12850 8750
Wire Wire Line
	12850 10100 12850 10250
Wire Wire Line
	12850 10250 14800 10250
Wire Wire Line
	14800 10250 14800 10100
Wire Wire Line
	14900 10050 14900 10200
Wire Wire Line
	14900 10200 14800 10200
Connection ~ 14800 10200
Wire Wire Line
	14800 9700 14800 8750
Wire Wire Line
	14800 8350 14800 8100
Wire Wire Line
	14900 8700 15000 8700
Wire Wire Line
	15000 8700 15000 8300
Wire Wire Line
	15000 8300 14800 8300
Connection ~ 14800 8300
Wire Wire Line
	14800 8100 12850 8100
Wire Wire Line
	12850 8100 12850 8350
Wire Wire Line
	12750 10050 12750 10200
Wire Wire Line
	12750 10200 12850 10200
Connection ~ 12850 10200
Wire Wire Line
	13150 8550 13300 8550
Wire Wire Line
	13300 8550 13300 9900
Wire Wire Line
	13300 9900 13150 9900
Wire Wire Line
	14500 8550 14300 8550
Wire Wire Line
	14300 8550 14300 9900
Wire Wire Line
	14300 9900 14500 9900
Connection ~ 14800 9200
$Comp
L mosfet_n M1
U 1 1 664DBBE8
P 11600 9000
F 0 "M1" H 11600 8850 50  0000 R CNN
F 1 "mosfet_n" H 11700 8950 50  0000 R CNN
F 2 "" H 11900 8700 29  0000 C CNN
F 3 "" H 11700 8800 60  0000 C CNN
	1    11600 9000
	0    -1   1    0   
$EndComp
Connection ~ 12850 9200
Connection ~ 13300 9100
Wire Wire Line
	12950 9100 12950 9300
Wire Wire Line
	12950 9300 14300 9300
Connection ~ 14300 9300
Wire Wire Line
	14700 9100 13300 9100
Wire Wire Line
	11300 9200 11600 9200
Wire Wire Line
	16050 9200 16400 9200
Wire Wire Line
	13850 10250 13850 10600
Connection ~ 13850 10250
Wire Wire Line
	13900 8100 13900 7750
Connection ~ 13900 8100
Wire Wire Line
	11800 7450 15850 7450
Wire Wire Line
	13900 7450 13900 6950
Connection ~ 13900 7450
$Comp
L PORT U1
U 3 1 664DC1D5
P 11050 9200
F 0 "U1" H 11100 9300 30  0000 C CNN
F 1 "PORT" H 11050 9200 30  0000 C CNN
F 2 "" H 11050 9200 60  0000 C CNN
F 3 "" H 11050 9200 60  0000 C CNN
	3    11050 9200
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 2 1 664DC2F4
P 13650 6950
F 0 "U1" H 13700 7050 30  0000 C CNN
F 1 "PORT" H 13650 6950 30  0000 C CNN
F 2 "" H 13650 6950 60  0000 C CNN
F 3 "" H 13650 6950 60  0000 C CNN
	2    13650 6950
	1    0    0    1   
$EndComp
$Comp
L PORT U1
U 4 1 664DC337
P 16650 9200
F 0 "U1" H 16700 9300 30  0000 C CNN
F 1 "PORT" H 16650 9200 30  0000 C CNN
F 2 "" H 16650 9200 60  0000 C CNN
F 3 "" H 16650 9200 60  0000 C CNN
	4    16650 9200
	-1   0    0    1   
$EndComp
$Comp
L PORT U1
U 5 1 664DC38A
P 13600 10600
F 0 "U1" H 13650 10700 30  0000 C CNN
F 1 "PORT" H 13600 10600 30  0000 C CNN
F 2 "" H 13600 10600 60  0000 C CNN
F 3 "" H 13600 10600 60  0000 C CNN
	5    13600 10600
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 1 1 664DC3B9
P 13650 7750
F 0 "U1" H 13700 7850 30  0000 C CNN
F 1 "PORT" H 13650 7750 30  0000 C CNN
F 2 "" H 13650 7750 60  0000 C CNN
F 3 "" H 13650 7750 60  0000 C CNN
	1    13650 7750
	1    0    0    -1  
$EndComp
Wire Wire Line
	12750 8700 12650 8700
Wire Wire Line
	12650 8700 12650 8300
Wire Wire Line
	12650 8300 12850 8300
Connection ~ 12850 8300
Wire Wire Line
	12000 9200 12850 9200
Wire Wire Line
	12950 9100 12850 9100
Connection ~ 12850 9100
Wire Wire Line
	14800 9200 15650 9200
Wire Wire Line
	14700 9100 14700 9150
Wire Wire Line
	14700 9150 14800 9150
Connection ~ 14800 9150
Wire Wire Line
	15700 10400 15700 9300
Wire Wire Line
	12150 10400 15700 10400
Connection ~ 13850 10400
Wire Wire Line
	11950 9300 12150 9300
Wire Wire Line
	12150 9300 12150 10400
Wire Wire Line
	15850 7450 15850 8900
Wire Wire Line
	11800 7450 11800 8900
$Comp
L PORT U1
U 6 1 665419C9
P 12400 8900
F 0 "U1" H 12450 9000 30  0000 C CNN
F 1 "PORT" H 12400 8900 30  0000 C CNN
F 2 "" H 12400 8900 60  0000 C CNN
F 3 "" H 12400 8900 60  0000 C CNN
	6    12400 8900
	0    1    1    0   
$EndComp
$Comp
L PORT U1
U 7 1 66541A4E
P 15300 8900
F 0 "U1" H 15350 9000 30  0000 C CNN
F 1 "PORT" H 15300 8900 30  0000 C CNN
F 2 "" H 15300 8900 60  0000 C CNN
F 3 "" H 15300 8900 60  0000 C CNN
	7    15300 8900
	0    1    1    0   
$EndComp
Wire Wire Line
	12400 9150 12400 9200
Connection ~ 12400 9200
Wire Wire Line
	15300 9150 15300 9200
Connection ~ 15300 9200
$EndSCHEMATC
