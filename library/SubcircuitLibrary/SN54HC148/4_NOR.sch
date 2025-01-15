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
L mosfet_p M3
U 1 1 665EEF98
P 14800 6650
F 0 "M3" H 14750 6700 50  0000 R CNN
F 1 "mosfet_p" H 14850 6800 50  0000 R CNN
F 2 "" H 15050 6750 29  0000 C CNN
F 3 "" H 14850 6650 60  0000 C CNN
	1    14800 6650
	1    0    0    -1  
$EndComp
$Comp
L mosfet_p M4
U 1 1 665EEFDA
P 14800 7300
F 0 "M4" H 14750 7350 50  0000 R CNN
F 1 "mosfet_p" H 14850 7450 50  0000 R CNN
F 2 "" H 15050 7400 29  0000 C CNN
F 3 "" H 14850 7300 60  0000 C CNN
	1    14800 7300
	1    0    0    -1  
$EndComp
$Comp
L mosfet_p M5
U 1 1 665EF01A
P 14800 7900
F 0 "M5" H 14750 7950 50  0000 R CNN
F 1 "mosfet_p" H 14850 8050 50  0000 R CNN
F 2 "" H 15050 8000 29  0000 C CNN
F 3 "" H 14850 7900 60  0000 C CNN
	1    14800 7900
	1    0    0    -1  
$EndComp
$Comp
L mosfet_p M6
U 1 1 665EF055
P 14800 8550
F 0 "M6" H 14750 8600 50  0000 R CNN
F 1 "mosfet_p" H 14850 8700 50  0000 R CNN
F 2 "" H 15050 8650 29  0000 C CNN
F 3 "" H 14850 8550 60  0000 C CNN
	1    14800 8550
	1    0    0    -1  
$EndComp
$Comp
L mosfet_n M1
U 1 1 665EF0CB
P 13550 9100
F 0 "M1" H 13550 8950 50  0000 R CNN
F 1 "mosfet_n" H 13650 9050 50  0000 R CNN
F 2 "" H 13850 8800 29  0000 C CNN
F 3 "" H 13650 8900 60  0000 C CNN
	1    13550 9100
	1    0    0    -1  
$EndComp
$Comp
L mosfet_n M2
U 1 1 665EF101
P 14350 9100
F 0 "M2" H 14350 8950 50  0000 R CNN
F 1 "mosfet_n" H 14450 9050 50  0000 R CNN
F 2 "" H 14650 8800 29  0000 C CNN
F 3 "" H 14450 8900 60  0000 C CNN
	1    14350 9100
	1    0    0    -1  
$EndComp
$Comp
L mosfet_n M7
U 1 1 665EF135
P 15000 9100
F 0 "M7" H 15000 8950 50  0000 R CNN
F 1 "mosfet_n" H 15100 9050 50  0000 R CNN
F 2 "" H 15300 8800 29  0000 C CNN
F 3 "" H 15100 8900 60  0000 C CNN
	1    15000 9100
	1    0    0    -1  
$EndComp
$Comp
L mosfet_n M8
U 1 1 665EF164
P 15650 9100
F 0 "M8" H 15650 8950 50  0000 R CNN
F 1 "mosfet_n" H 15750 9050 50  0000 R CNN
F 2 "" H 15950 8800 29  0000 C CNN
F 3 "" H 15750 8900 60  0000 C CNN
	1    15650 9100
	1    0    0    -1  
$EndComp
Wire Wire Line
	14950 6850 14950 7100
Wire Wire Line
	14950 7500 14950 7700
Wire Wire Line
	14950 8100 14950 8350
Wire Wire Line
	14950 8750 14950 8900
Wire Wire Line
	13750 9100 13750 8900
Wire Wire Line
	13750 8900 15850 8900
Wire Wire Line
	14550 9100 14550 8900
Connection ~ 14550 8900
Wire Wire Line
	15850 8900 15850 9100
Connection ~ 14950 8900
Wire Wire Line
	15200 9100 15200 8900
Connection ~ 15200 8900
Wire Wire Line
	13750 9500 13750 9650
Wire Wire Line
	13750 9650 15850 9650
Wire Wire Line
	15850 9650 15850 9500
Wire Wire Line
	15950 9450 15950 9550
Wire Wire Line
	15950 9550 15850 9550
Connection ~ 15850 9550
Wire Wire Line
	15300 9450 15300 9550
Wire Wire Line
	15300 9550 15200 9550
Wire Wire Line
	15200 9500 15200 9650
Connection ~ 15200 9650
Connection ~ 15200 9550
Wire Wire Line
	14550 9500 14550 9650
Connection ~ 14550 9650
Wire Wire Line
	14650 9450 14650 9550
Wire Wire Line
	14650 9550 14550 9550
Connection ~ 14550 9550
Wire Wire Line
	13850 9450 13850 9550
Wire Wire Line
	13850 9550 13750 9550
Connection ~ 13750 9550
Wire Wire Line
	15050 8700 15250 8700
Wire Wire Line
	15250 8700 15250 8300
Wire Wire Line
	15250 8300 14950 8300
Connection ~ 14950 8300
Wire Wire Line
	15050 8050 15250 8050
Wire Wire Line
	15250 8050 15250 7650
Wire Wire Line
	15250 7650 14950 7650
Connection ~ 14950 7650
Wire Wire Line
	15050 7450 15250 7450
Wire Wire Line
	15250 7450 15250 7050
Wire Wire Line
	15250 7050 14950 7050
Connection ~ 14950 7050
Wire Wire Line
	15050 6800 15250 6800
Wire Wire Line
	15250 6800 15250 6450
Wire Wire Line
	15250 6450 14950 6450
Wire Wire Line
	14950 6450 14950 6100
Wire Wire Line
	14650 6650 13250 6650
Wire Wire Line
	14650 7300 13250 7300
Wire Wire Line
	14650 7900 13250 7900
Wire Wire Line
	14650 8550 13250 8550
Wire Wire Line
	13550 6650 13550 9000
Wire Wire Line
	13550 9000 13350 9000
Wire Wire Line
	13350 9000 13350 9300
Wire Wire Line
	13350 9300 13450 9300
Connection ~ 13550 6650
Wire Wire Line
	14100 7300 14100 9300
Wire Wire Line
	14100 9300 14250 9300
Connection ~ 14100 7300
Wire Wire Line
	14550 7900 14550 8150
Wire Wire Line
	14550 8150 14750 8150
Wire Wire Line
	14750 8150 14750 9300
Wire Wire Line
	14750 9300 14900 9300
Connection ~ 14550 7900
Wire Wire Line
	14500 8550 14500 8800
Wire Wire Line
	14500 8800 15550 8800
Wire Wire Line
	15550 8800 15550 9300
Connection ~ 14500 8550
Wire Wire Line
	14900 9650 14900 10300
Connection ~ 14900 9650
Wire Wire Line
	14950 8850 16650 8850
Connection ~ 14950 8850
$Comp
L PORT U1
U 1 1 665EFE97
P 13000 6650
F 0 "U1" H 13050 6750 30  0000 C CNN
F 1 "PORT" H 13000 6650 30  0000 C CNN
F 2 "" H 13000 6650 60  0000 C CNN
F 3 "" H 13000 6650 60  0000 C CNN
	1    13000 6650
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 2 1 665EFEBE
P 13000 7300
F 0 "U1" H 13050 7400 30  0000 C CNN
F 1 "PORT" H 13000 7300 30  0000 C CNN
F 2 "" H 13000 7300 60  0000 C CNN
F 3 "" H 13000 7300 60  0000 C CNN
	2    13000 7300
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 3 1 665EFF07
P 13000 7900
F 0 "U1" H 13050 8000 30  0000 C CNN
F 1 "PORT" H 13000 7900 30  0000 C CNN
F 2 "" H 13000 7900 60  0000 C CNN
F 3 "" H 13000 7900 60  0000 C CNN
	3    13000 7900
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 4 1 665EFF7C
P 13000 8550
F 0 "U1" H 13050 8650 30  0000 C CNN
F 1 "PORT" H 13000 8550 30  0000 C CNN
F 2 "" H 13000 8550 60  0000 C CNN
F 3 "" H 13000 8550 60  0000 C CNN
	4    13000 8550
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 5 1 665EFFF1
P 14650 10300
F 0 "U1" H 14700 10400 30  0000 C CNN
F 1 "PORT" H 14650 10300 30  0000 C CNN
F 2 "" H 14650 10300 60  0000 C CNN
F 3 "" H 14650 10300 60  0000 C CNN
	5    14650 10300
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 6 1 665F0046
P 14700 6100
F 0 "U1" H 14750 6200 30  0000 C CNN
F 1 "PORT" H 14700 6100 30  0000 C CNN
F 2 "" H 14700 6100 60  0000 C CNN
F 3 "" H 14700 6100 60  0000 C CNN
	6    14700 6100
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 7 1 665F007B
P 16900 8850
F 0 "U1" H 16950 8950 30  0000 C CNN
F 1 "PORT" H 16900 8850 30  0000 C CNN
F 2 "" H 16900 8850 60  0000 C CNN
F 3 "" H 16900 8850 60  0000 C CNN
	7    16900 8850
	-1   0    0    -1  
$EndComp
$EndSCHEMATC
