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
LIBS:abc-cache
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
L mosfet_n M1
U 1 1 682B5FFB
P 1900 1750
F 0 "M1" H 1900 1600 50  0000 R CNN
F 1 "mosfet_n" H 2000 1700 50  0000 R CNN
F 2 "" H 2200 1450 29  0000 C CNN
F 3 "" H 2000 1550 60  0000 C CNN
	1    1900 1750
	1    0    0    -1  
$EndComp
$Comp
L mosfet_p M3
U 1 1 682B5FFC
P 1950 1450
F 0 "M3" H 1900 1500 50  0000 R CNN
F 1 "mosfet_p" H 2000 1600 50  0000 R CNN
F 2 "" H 2200 1550 29  0000 C CNN
F 3 "" H 2000 1450 60  0000 C CNN
	1    1950 1450
	1    0    0    1   
$EndComp
$Comp
L eSim_Diode D7
U 1 1 682B5FFD
P 1350 1900
F 0 "D7" H 1350 2000 50  0000 C CNN
F 1 "eSim_Diode" H 1350 1800 50  0000 C CNN
F 2 "" H 1350 1900 60  0000 C CNN
F 3 "" H 1350 1900 60  0000 C CNN
	1    1350 1900
	0    -1   -1   0   
$EndComp
$Comp
L eSim_Diode D3
U 1 1 682B5FFE
P 950 1900
F 0 "D3" H 950 2000 50  0000 C CNN
F 1 "eSim_Diode" H 950 1800 50  0000 C CNN
F 2 "" H 950 1900 60  0000 C CNN
F 3 "" H 950 1900 60  0000 C CNN
	1    950  1900
	0    -1   -1   0   
$EndComp
$Comp
L resistor R1
U 1 1 682B5FFF
P 1100 1750
F 0 "R1" H 1150 1880 50  0000 C CNN
F 1 "resistor" H 1150 1700 50  0000 C CNN
F 2 "" H 1150 1730 30  0000 C CNN
F 3 "" V 1150 1800 30  0000 C CNN
	1    1100 1750
	1    0    0    -1  
$EndComp
$Comp
L eSim_Diode D2
U 1 1 682B6000
P 950 1500
F 0 "D2" H 950 1600 50  0000 C CNN
F 1 "eSim_Diode" H 950 1400 50  0000 C CNN
F 2 "" H 950 1500 60  0000 C CNN
F 3 "" H 950 1500 60  0000 C CNN
	1    950  1500
	0    1    1    0   
$EndComp
$Comp
L eSim_Diode D1
U 1 1 682B6001
P 950 1150
F 0 "D1" H 950 1250 50  0000 C CNN
F 1 "eSim_Diode" H 950 1050 50  0000 C CNN
F 2 "" H 950 1150 60  0000 C CNN
F 3 "" H 950 1150 60  0000 C CNN
	1    950  1150
	0    -1   -1   0   
$EndComp
$Comp
L eSim_Diode D9
U 1 1 682B6002
P 2500 1100
F 0 "D9" H 2500 1200 50  0000 C CNN
F 1 "eSim_Diode" H 2500 1000 50  0000 C CNN
F 2 "" H 2500 1100 60  0000 C CNN
F 3 "" H 2500 1100 60  0000 C CNN
	1    2500 1100
	0    -1   -1   0   
$EndComp
Text GLabel 2100 900  1    60   Input ~ 0
vdd
Text GLabel 2100 2250 3    60   Input ~ 0
vss
Wire Wire Line
	950  1000 2100 1000
Wire Wire Line
	2100 900  2100 1250
Wire Wire Line
	2100 900  2500 900 
Wire Wire Line
	2500 900  2500 950 
Connection ~ 2100 1000
Wire Wire Line
	2100 1250 2200 1250
Wire Wire Line
	2200 1250 2200 1300
Wire Wire Line
	2100 1650 2100 1750
Wire Wire Line
	1350 2150 2200 2150
Wire Wire Line
	2200 2150 2200 2100
Wire Wire Line
	2100 2150 2100 2250
Wire Wire Line
	1800 1450 1800 1950
Wire Wire Line
	1300 1700 1800 1700
Wire Wire Line
	1350 1700 1350 1750
Wire Wire Line
	950  1750 950  1650
Wire Wire Line
	800  1700 1000 1700
Connection ~ 950  1700
Connection ~ 1800 1700
Connection ~ 1350 1700
Wire Wire Line
	950  2050 1350 2050
Wire Wire Line
	1350 2050 1350 2150
Connection ~ 2100 2150
Wire Wire Line
	950  1300 950  1350
Text GLabel 2500 1250 3    60   Input ~ 0
vss
Text GLabel 1000 1350 2    60   Input ~ 0
vss
Wire Wire Line
	950  1350 1000 1350
Text GLabel 2200 1700 2    60   Input ~ 0
g
Text GLabel 800  1700 0    60   Input ~ 0
a
Wire Wire Line
	2100 1700 2200 1700
Connection ~ 2100 1700
$Comp
L mosfet_n M5
U 1 1 682B6229
P 4350 1750
F 0 "M5" H 4350 1600 50  0000 R CNN
F 1 "mosfet_n" H 4450 1700 50  0000 R CNN
F 2 "" H 4650 1450 29  0000 C CNN
F 3 "" H 4450 1550 60  0000 C CNN
	1    4350 1750
	1    0    0    -1  
$EndComp
$Comp
L mosfet_p M7
U 1 1 682B622F
P 4400 1450
F 0 "M7" H 4350 1500 50  0000 R CNN
F 1 "mosfet_p" H 4450 1600 50  0000 R CNN
F 2 "" H 4650 1550 29  0000 C CNN
F 3 "" H 4450 1450 60  0000 C CNN
	1    4400 1450
	1    0    0    1   
$EndComp
$Comp
L eSim_Diode D17
U 1 1 682B6235
P 3800 1900
F 0 "D17" H 3800 2000 50  0000 C CNN
F 1 "eSim_Diode" H 3800 1800 50  0000 C CNN
F 2 "" H 3800 1900 60  0000 C CNN
F 3 "" H 3800 1900 60  0000 C CNN
	1    3800 1900
	0    -1   -1   0   
$EndComp
$Comp
L eSim_Diode D13
U 1 1 682B623B
P 3400 1900
F 0 "D13" H 3400 2000 50  0000 C CNN
F 1 "eSim_Diode" H 3400 1800 50  0000 C CNN
F 2 "" H 3400 1900 60  0000 C CNN
F 3 "" H 3400 1900 60  0000 C CNN
	1    3400 1900
	0    -1   -1   0   
$EndComp
$Comp
L resistor R3
U 1 1 682B6241
P 3550 1750
F 0 "R3" H 3600 1880 50  0000 C CNN
F 1 "resistor" H 3600 1700 50  0000 C CNN
F 2 "" H 3600 1730 30  0000 C CNN
F 3 "" V 3600 1800 30  0000 C CNN
	1    3550 1750
	1    0    0    -1  
$EndComp
$Comp
L eSim_Diode D12
U 1 1 682B6247
P 3400 1500
F 0 "D12" H 3400 1600 50  0000 C CNN
F 1 "eSim_Diode" H 3400 1400 50  0000 C CNN
F 2 "" H 3400 1500 60  0000 C CNN
F 3 "" H 3400 1500 60  0000 C CNN
	1    3400 1500
	0    1    1    0   
$EndComp
$Comp
L eSim_Diode D11
U 1 1 682B624D
P 3400 1150
F 0 "D11" H 3400 1250 50  0000 C CNN
F 1 "eSim_Diode" H 3400 1050 50  0000 C CNN
F 2 "" H 3400 1150 60  0000 C CNN
F 3 "" H 3400 1150 60  0000 C CNN
	1    3400 1150
	0    -1   -1   0   
$EndComp
$Comp
L eSim_Diode D19
U 1 1 682B6253
P 4950 1100
F 0 "D19" H 4950 1200 50  0000 C CNN
F 1 "eSim_Diode" H 4950 1000 50  0000 C CNN
F 2 "" H 4950 1100 60  0000 C CNN
F 3 "" H 4950 1100 60  0000 C CNN
	1    4950 1100
	0    -1   -1   0   
$EndComp
Text GLabel 4550 900  1    60   Input ~ 0
vdd
Text GLabel 4550 2250 3    60   Input ~ 0
vss
Wire Wire Line
	3400 1000 4550 1000
Wire Wire Line
	4550 900  4550 1250
Wire Wire Line
	4550 900  4950 900 
Wire Wire Line
	4950 900  4950 950 
Connection ~ 4550 1000
Wire Wire Line
	4550 1250 4650 1250
Wire Wire Line
	4650 1250 4650 1300
Wire Wire Line
	4550 1650 4550 1750
Wire Wire Line
	3800 2150 4650 2150
Wire Wire Line
	4650 2150 4650 2100
Wire Wire Line
	4550 2150 4550 2250
Wire Wire Line
	4250 1450 4250 1950
Wire Wire Line
	3750 1700 4250 1700
Wire Wire Line
	3800 1700 3800 1750
Wire Wire Line
	3400 1750 3400 1650
Wire Wire Line
	3250 1700 3450 1700
Connection ~ 3400 1700
Connection ~ 4250 1700
Connection ~ 3800 1700
Wire Wire Line
	3400 2050 3800 2050
Wire Wire Line
	3800 2050 3800 2150
Connection ~ 4550 2150
Wire Wire Line
	3400 1300 3400 1350
Text GLabel 4950 1250 3    60   Input ~ 0
vss
Text GLabel 3450 1350 2    60   Input ~ 0
vss
Wire Wire Line
	3400 1350 3450 1350
Text GLabel 4650 1700 2    60   Input ~ 0
h
Text GLabel 3250 1700 0    60   Input ~ 0
b
Wire Wire Line
	4550 1700 4650 1700
Connection ~ 4550 1700
$Comp
L mosfet_n M9
U 1 1 682B6351
P 6700 1750
F 0 "M9" H 6700 1600 50  0000 R CNN
F 1 "mosfet_n" H 6800 1700 50  0000 R CNN
F 2 "" H 7000 1450 29  0000 C CNN
F 3 "" H 6800 1550 60  0000 C CNN
	1    6700 1750
	1    0    0    -1  
$EndComp
$Comp
L mosfet_p M11
U 1 1 682B6357
P 6750 1450
F 0 "M11" H 6700 1500 50  0000 R CNN
F 1 "mosfet_p" H 6800 1600 50  0000 R CNN
F 2 "" H 7000 1550 29  0000 C CNN
F 3 "" H 6800 1450 60  0000 C CNN
	1    6750 1450
	1    0    0    1   
$EndComp
$Comp
L eSim_Diode D27
U 1 1 682B635D
P 6150 1900
F 0 "D27" H 6150 2000 50  0000 C CNN
F 1 "eSim_Diode" H 6150 1800 50  0000 C CNN
F 2 "" H 6150 1900 60  0000 C CNN
F 3 "" H 6150 1900 60  0000 C CNN
	1    6150 1900
	0    -1   -1   0   
$EndComp
$Comp
L eSim_Diode D23
U 1 1 682B6363
P 5750 1900
F 0 "D23" H 5750 2000 50  0000 C CNN
F 1 "eSim_Diode" H 5750 1800 50  0000 C CNN
F 2 "" H 5750 1900 60  0000 C CNN
F 3 "" H 5750 1900 60  0000 C CNN
	1    5750 1900
	0    -1   -1   0   
$EndComp
$Comp
L resistor R5
U 1 1 682B6369
P 5900 1750
F 0 "R5" H 5950 1880 50  0000 C CNN
F 1 "resistor" H 5950 1700 50  0000 C CNN
F 2 "" H 5950 1730 30  0000 C CNN
F 3 "" V 5950 1800 30  0000 C CNN
	1    5900 1750
	1    0    0    -1  
$EndComp
$Comp
L eSim_Diode D22
U 1 1 682B636F
P 5750 1500
F 0 "D22" H 5750 1600 50  0000 C CNN
F 1 "eSim_Diode" H 5750 1400 50  0000 C CNN
F 2 "" H 5750 1500 60  0000 C CNN
F 3 "" H 5750 1500 60  0000 C CNN
	1    5750 1500
	0    1    1    0   
$EndComp
$Comp
L eSim_Diode D21
U 1 1 682B6375
P 5750 1150
F 0 "D21" H 5750 1250 50  0000 C CNN
F 1 "eSim_Diode" H 5750 1050 50  0000 C CNN
F 2 "" H 5750 1150 60  0000 C CNN
F 3 "" H 5750 1150 60  0000 C CNN
	1    5750 1150
	0    -1   -1   0   
$EndComp
$Comp
L eSim_Diode D29
U 1 1 682B637B
P 7300 1100
F 0 "D29" H 7300 1200 50  0000 C CNN
F 1 "eSim_Diode" H 7300 1000 50  0000 C CNN
F 2 "" H 7300 1100 60  0000 C CNN
F 3 "" H 7300 1100 60  0000 C CNN
	1    7300 1100
	0    -1   -1   0   
$EndComp
Text GLabel 6900 900  1    60   Input ~ 0
vdd
Text GLabel 6900 2250 3    60   Input ~ 0
vss
Wire Wire Line
	5750 1000 6900 1000
Wire Wire Line
	6900 900  6900 1250
Wire Wire Line
	6900 900  7300 900 
Wire Wire Line
	7300 900  7300 950 
Connection ~ 6900 1000
Wire Wire Line
	6900 1250 7000 1250
Wire Wire Line
	7000 1250 7000 1300
Wire Wire Line
	6900 1650 6900 1750
Wire Wire Line
	6150 2150 7000 2150
Wire Wire Line
	7000 2150 7000 2100
Wire Wire Line
	6900 2150 6900 2250
Wire Wire Line
	6600 1450 6600 1950
Wire Wire Line
	6100 1700 6600 1700
Wire Wire Line
	6150 1700 6150 1750
Wire Wire Line
	5750 1750 5750 1650
Wire Wire Line
	5600 1700 5800 1700
Connection ~ 5750 1700
Connection ~ 6600 1700
Connection ~ 6150 1700
Wire Wire Line
	5750 2050 6150 2050
Wire Wire Line
	6150 2050 6150 2150
Connection ~ 6900 2150
Wire Wire Line
	5750 1300 5750 1350
Text GLabel 7300 1250 3    60   Input ~ 0
vss
Text GLabel 5800 1350 2    60   Input ~ 0
vss
Wire Wire Line
	5750 1350 5800 1350
Text GLabel 7000 1700 2    60   Input ~ 0
i
Text GLabel 5600 1700 0    60   Input ~ 0
c
Wire Wire Line
	6900 1700 7000 1700
Connection ~ 6900 1700
$Comp
L mosfet_n M2
U 1 1 682B65F9
P 1900 3850
F 0 "M2" H 1900 3700 50  0000 R CNN
F 1 "mosfet_n" H 2000 3800 50  0000 R CNN
F 2 "" H 2200 3550 29  0000 C CNN
F 3 "" H 2000 3650 60  0000 C CNN
	1    1900 3850
	1    0    0    -1  
$EndComp
$Comp
L mosfet_p M4
U 1 1 682B65FF
P 1950 3550
F 0 "M4" H 1900 3600 50  0000 R CNN
F 1 "mosfet_p" H 2000 3700 50  0000 R CNN
F 2 "" H 2200 3650 29  0000 C CNN
F 3 "" H 2000 3550 60  0000 C CNN
	1    1950 3550
	1    0    0    1   
$EndComp
$Comp
L eSim_Diode D8
U 1 1 682B6605
P 1350 4000
F 0 "D8" H 1350 4100 50  0000 C CNN
F 1 "eSim_Diode" H 1350 3900 50  0000 C CNN
F 2 "" H 1350 4000 60  0000 C CNN
F 3 "" H 1350 4000 60  0000 C CNN
	1    1350 4000
	0    -1   -1   0   
$EndComp
$Comp
L eSim_Diode D6
U 1 1 682B660B
P 950 4000
F 0 "D6" H 950 4100 50  0000 C CNN
F 1 "eSim_Diode" H 950 3900 50  0000 C CNN
F 2 "" H 950 4000 60  0000 C CNN
F 3 "" H 950 4000 60  0000 C CNN
	1    950  4000
	0    -1   -1   0   
$EndComp
$Comp
L resistor R2
U 1 1 682B6611
P 1100 3850
F 0 "R2" H 1150 3980 50  0000 C CNN
F 1 "resistor" H 1150 3800 50  0000 C CNN
F 2 "" H 1150 3830 30  0000 C CNN
F 3 "" V 1150 3900 30  0000 C CNN
	1    1100 3850
	1    0    0    -1  
$EndComp
$Comp
L eSim_Diode D5
U 1 1 682B6617
P 950 3600
F 0 "D5" H 950 3700 50  0000 C CNN
F 1 "eSim_Diode" H 950 3500 50  0000 C CNN
F 2 "" H 950 3600 60  0000 C CNN
F 3 "" H 950 3600 60  0000 C CNN
	1    950  3600
	0    1    1    0   
$EndComp
$Comp
L eSim_Diode D4
U 1 1 682B661D
P 950 3250
F 0 "D4" H 950 3350 50  0000 C CNN
F 1 "eSim_Diode" H 950 3150 50  0000 C CNN
F 2 "" H 950 3250 60  0000 C CNN
F 3 "" H 950 3250 60  0000 C CNN
	1    950  3250
	0    -1   -1   0   
$EndComp
$Comp
L eSim_Diode D10
U 1 1 682B6623
P 2500 3200
F 0 "D10" H 2500 3300 50  0000 C CNN
F 1 "eSim_Diode" H 2500 3100 50  0000 C CNN
F 2 "" H 2500 3200 60  0000 C CNN
F 3 "" H 2500 3200 60  0000 C CNN
	1    2500 3200
	0    -1   -1   0   
$EndComp
Text GLabel 2100 3000 1    60   Input ~ 0
vdd
Text GLabel 2100 4350 3    60   Input ~ 0
vss
Wire Wire Line
	950  3100 2100 3100
Wire Wire Line
	2100 3000 2100 3350
Wire Wire Line
	2100 3000 2500 3000
Wire Wire Line
	2500 3000 2500 3050
Connection ~ 2100 3100
Wire Wire Line
	2100 3350 2200 3350
Wire Wire Line
	2200 3350 2200 3400
Wire Wire Line
	2100 3750 2100 3850
Wire Wire Line
	1350 4250 2200 4250
Wire Wire Line
	2200 4250 2200 4200
Wire Wire Line
	2100 4250 2100 4350
Wire Wire Line
	1800 3550 1800 4050
Wire Wire Line
	1300 3800 1800 3800
Wire Wire Line
	1350 3800 1350 3850
Wire Wire Line
	950  3850 950  3750
Wire Wire Line
	800  3800 1000 3800
Connection ~ 950  3800
Connection ~ 1800 3800
Connection ~ 1350 3800
Wire Wire Line
	950  4150 1350 4150
Wire Wire Line
	1350 4150 1350 4250
Connection ~ 2100 4250
Wire Wire Line
	950  3400 950  3450
Text GLabel 2500 3350 3    60   Input ~ 0
vss
Text GLabel 1000 3450 2    60   Input ~ 0
vss
Wire Wire Line
	950  3450 1000 3450
Text GLabel 2200 3800 2    60   Input ~ 0
j
Text GLabel 800  3800 0    60   Input ~ 0
d
Wire Wire Line
	2100 3800 2200 3800
Connection ~ 2100 3800
$Comp
L mosfet_n M6
U 1 1 682B6649
P 4350 3850
F 0 "M6" H 4350 3700 50  0000 R CNN
F 1 "mosfet_n" H 4450 3800 50  0000 R CNN
F 2 "" H 4650 3550 29  0000 C CNN
F 3 "" H 4450 3650 60  0000 C CNN
	1    4350 3850
	1    0    0    -1  
$EndComp
$Comp
L mosfet_p M8
U 1 1 682B664F
P 4400 3550
F 0 "M8" H 4350 3600 50  0000 R CNN
F 1 "mosfet_p" H 4450 3700 50  0000 R CNN
F 2 "" H 4650 3650 29  0000 C CNN
F 3 "" H 4450 3550 60  0000 C CNN
	1    4400 3550
	1    0    0    1   
$EndComp
$Comp
L eSim_Diode D18
U 1 1 682B6655
P 3800 4000
F 0 "D18" H 3800 4100 50  0000 C CNN
F 1 "eSim_Diode" H 3800 3900 50  0000 C CNN
F 2 "" H 3800 4000 60  0000 C CNN
F 3 "" H 3800 4000 60  0000 C CNN
	1    3800 4000
	0    -1   -1   0   
$EndComp
$Comp
L eSim_Diode D16
U 1 1 682B665B
P 3400 4000
F 0 "D16" H 3400 4100 50  0000 C CNN
F 1 "eSim_Diode" H 3400 3900 50  0000 C CNN
F 2 "" H 3400 4000 60  0000 C CNN
F 3 "" H 3400 4000 60  0000 C CNN
	1    3400 4000
	0    -1   -1   0   
$EndComp
$Comp
L resistor R4
U 1 1 682B6661
P 3550 3850
F 0 "R4" H 3600 3980 50  0000 C CNN
F 1 "resistor" H 3600 3800 50  0000 C CNN
F 2 "" H 3600 3830 30  0000 C CNN
F 3 "" V 3600 3900 30  0000 C CNN
	1    3550 3850
	1    0    0    -1  
$EndComp
$Comp
L eSim_Diode D15
U 1 1 682B6667
P 3400 3600
F 0 "D15" H 3400 3700 50  0000 C CNN
F 1 "eSim_Diode" H 3400 3500 50  0000 C CNN
F 2 "" H 3400 3600 60  0000 C CNN
F 3 "" H 3400 3600 60  0000 C CNN
	1    3400 3600
	0    1    1    0   
$EndComp
$Comp
L eSim_Diode D14
U 1 1 682B666D
P 3400 3250
F 0 "D14" H 3400 3350 50  0000 C CNN
F 1 "eSim_Diode" H 3400 3150 50  0000 C CNN
F 2 "" H 3400 3250 60  0000 C CNN
F 3 "" H 3400 3250 60  0000 C CNN
	1    3400 3250
	0    -1   -1   0   
$EndComp
$Comp
L eSim_Diode D20
U 1 1 682B6673
P 4950 3200
F 0 "D20" H 4950 3300 50  0000 C CNN
F 1 "eSim_Diode" H 4950 3100 50  0000 C CNN
F 2 "" H 4950 3200 60  0000 C CNN
F 3 "" H 4950 3200 60  0000 C CNN
	1    4950 3200
	0    -1   -1   0   
$EndComp
Text GLabel 4550 3000 1    60   Input ~ 0
vdd
Text GLabel 4550 4350 3    60   Input ~ 0
vss
Wire Wire Line
	3400 3100 4550 3100
Wire Wire Line
	4550 3000 4550 3350
Wire Wire Line
	4550 3000 4950 3000
Wire Wire Line
	4950 3000 4950 3050
Connection ~ 4550 3100
Wire Wire Line
	4550 3350 4650 3350
Wire Wire Line
	4650 3350 4650 3400
Wire Wire Line
	4550 3750 4550 3850
Wire Wire Line
	3800 4250 4650 4250
Wire Wire Line
	4650 4250 4650 4200
Wire Wire Line
	4550 4250 4550 4350
Wire Wire Line
	4250 3550 4250 4050
Wire Wire Line
	3750 3800 4250 3800
Wire Wire Line
	3800 3800 3800 3850
Wire Wire Line
	3400 3850 3400 3750
Wire Wire Line
	3250 3800 3450 3800
Connection ~ 3400 3800
Connection ~ 4250 3800
Connection ~ 3800 3800
Wire Wire Line
	3400 4150 3800 4150
Wire Wire Line
	3800 4150 3800 4250
Connection ~ 4550 4250
Wire Wire Line
	3400 3400 3400 3450
Text GLabel 4950 3350 3    60   Input ~ 0
vss
Text GLabel 3450 3450 2    60   Input ~ 0
vss
Wire Wire Line
	3400 3450 3450 3450
Text GLabel 4650 3800 2    60   Input ~ 0
k
Text GLabel 3250 3800 0    60   Input ~ 0
e
Wire Wire Line
	4550 3800 4650 3800
Connection ~ 4550 3800
$Comp
L mosfet_n M10
U 1 1 682B6699
P 6700 3850
F 0 "M10" H 6700 3700 50  0000 R CNN
F 1 "mosfet_n" H 6800 3800 50  0000 R CNN
F 2 "" H 7000 3550 29  0000 C CNN
F 3 "" H 6800 3650 60  0000 C CNN
	1    6700 3850
	1    0    0    -1  
$EndComp
$Comp
L mosfet_p M12
U 1 1 682B669F
P 6750 3550
F 0 "M12" H 6700 3600 50  0000 R CNN
F 1 "mosfet_p" H 6800 3700 50  0000 R CNN
F 2 "" H 7000 3650 29  0000 C CNN
F 3 "" H 6800 3550 60  0000 C CNN
	1    6750 3550
	1    0    0    1   
$EndComp
$Comp
L eSim_Diode D28
U 1 1 682B66A5
P 6150 4000
F 0 "D28" H 6150 4100 50  0000 C CNN
F 1 "eSim_Diode" H 6150 3900 50  0000 C CNN
F 2 "" H 6150 4000 60  0000 C CNN
F 3 "" H 6150 4000 60  0000 C CNN
	1    6150 4000
	0    -1   -1   0   
$EndComp
$Comp
L eSim_Diode D26
U 1 1 682B66AB
P 5750 4000
F 0 "D26" H 5750 4100 50  0000 C CNN
F 1 "eSim_Diode" H 5750 3900 50  0000 C CNN
F 2 "" H 5750 4000 60  0000 C CNN
F 3 "" H 5750 4000 60  0000 C CNN
	1    5750 4000
	0    -1   -1   0   
$EndComp
$Comp
L resistor R6
U 1 1 682B66B1
P 5900 3850
F 0 "R6" H 5950 3980 50  0000 C CNN
F 1 "resistor" H 5950 3800 50  0000 C CNN
F 2 "" H 5950 3830 30  0000 C CNN
F 3 "" V 5950 3900 30  0000 C CNN
	1    5900 3850
	1    0    0    -1  
$EndComp
$Comp
L eSim_Diode D25
U 1 1 682B66B7
P 5750 3600
F 0 "D25" H 5750 3700 50  0000 C CNN
F 1 "eSim_Diode" H 5750 3500 50  0000 C CNN
F 2 "" H 5750 3600 60  0000 C CNN
F 3 "" H 5750 3600 60  0000 C CNN
	1    5750 3600
	0    1    1    0   
$EndComp
$Comp
L eSim_Diode D24
U 1 1 682B66BD
P 5750 3250
F 0 "D24" H 5750 3350 50  0000 C CNN
F 1 "eSim_Diode" H 5750 3150 50  0000 C CNN
F 2 "" H 5750 3250 60  0000 C CNN
F 3 "" H 5750 3250 60  0000 C CNN
	1    5750 3250
	0    -1   -1   0   
$EndComp
$Comp
L eSim_Diode D30
U 1 1 682B66C3
P 7300 3200
F 0 "D30" H 7300 3300 50  0000 C CNN
F 1 "eSim_Diode" H 7300 3100 50  0000 C CNN
F 2 "" H 7300 3200 60  0000 C CNN
F 3 "" H 7300 3200 60  0000 C CNN
	1    7300 3200
	0    -1   -1   0   
$EndComp
Text GLabel 6900 3000 1    60   Input ~ 0
vdd
Text GLabel 6900 4350 3    60   Input ~ 0
vss
Wire Wire Line
	5750 3100 6900 3100
Wire Wire Line
	6900 3000 6900 3350
Wire Wire Line
	6900 3000 7300 3000
Wire Wire Line
	7300 3000 7300 3050
Connection ~ 6900 3100
Wire Wire Line
	6900 3350 7000 3350
Wire Wire Line
	7000 3350 7000 3400
Wire Wire Line
	6900 3750 6900 3850
Wire Wire Line
	6150 4250 7000 4250
Wire Wire Line
	7000 4250 7000 4200
Wire Wire Line
	6900 4250 6900 4350
Wire Wire Line
	6600 3550 6600 4050
Wire Wire Line
	6100 3800 6600 3800
Wire Wire Line
	6150 3800 6150 3850
Wire Wire Line
	5750 3850 5750 3750
Wire Wire Line
	5600 3800 5800 3800
Connection ~ 5750 3800
Connection ~ 6600 3800
Connection ~ 6150 3800
Wire Wire Line
	5750 4150 6150 4150
Wire Wire Line
	6150 4150 6150 4250
Connection ~ 6900 4250
Wire Wire Line
	5750 3400 5750 3450
Text GLabel 7300 3350 3    60   Input ~ 0
vss
Text GLabel 5800 3450 2    60   Input ~ 0
vss
Wire Wire Line
	5750 3450 5800 3450
Text GLabel 7000 3800 2    60   Input ~ 0
l
Text GLabel 5600 3800 0    60   Input ~ 0
f
Wire Wire Line
	6900 3800 7000 3800
Connection ~ 6900 3800
$EndSCHEMATC
