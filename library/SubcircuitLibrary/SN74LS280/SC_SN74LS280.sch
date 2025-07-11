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
LIBS:SC_SN74LS280-cache
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
L 3_and X1
U 1 1 682F2EF6
P 4250 1150
F 0 "X1" H 4350 1100 60  0000 C CNN
F 1 "3_and" H 4400 1300 60  0000 C CNN
F 2 "" H 4250 1150 60  0000 C CNN
F 3 "" H 4250 1150 60  0000 C CNN
	1    4250 1150
	1    0    0    -1  
$EndComp
$Comp
L 3_and X2
U 1 1 682F2EF7
P 4250 1550
F 0 "X2" H 4350 1500 60  0000 C CNN
F 1 "3_and" H 4400 1700 60  0000 C CNN
F 2 "" H 4250 1550 60  0000 C CNN
F 3 "" H 4250 1550 60  0000 C CNN
	1    4250 1550
	1    0    0    -1  
$EndComp
$Comp
L 3_and X3
U 1 1 682F2EF8
P 4250 2000
F 0 "X3" H 4350 1950 60  0000 C CNN
F 1 "3_and" H 4400 2150 60  0000 C CNN
F 2 "" H 4250 2000 60  0000 C CNN
F 3 "" H 4250 2000 60  0000 C CNN
	1    4250 2000
	1    0    0    -1  
$EndComp
$Comp
L 3_and X4
U 1 1 682F2EF9
P 4250 2500
F 0 "X4" H 4350 2450 60  0000 C CNN
F 1 "3_and" H 4400 2650 60  0000 C CNN
F 2 "" H 4250 2500 60  0000 C CNN
F 3 "" H 4250 2500 60  0000 C CNN
	1    4250 2500
	1    0    0    -1  
$EndComp
$Comp
L 4_OR X13
U 1 1 682F2EFA
P 5550 1700
F 0 "X13" H 5700 1600 60  0000 C CNN
F 1 "4_OR" H 5700 1800 60  0000 C CNN
F 2 "" H 5550 1700 60  0000 C CNN
F 3 "" H 5550 1700 60  0000 C CNN
	1    5550 1700
	1    0    0    -1  
$EndComp
$Comp
L d_inverter U20
U 1 1 682F2EFB
P 6600 1700
F 0 "U20" H 6600 1600 60  0000 C CNN
F 1 "d_inverter" H 6600 1850 60  0000 C CNN
F 2 "" H 6650 1650 60  0000 C CNN
F 3 "" H 6650 1650 60  0000 C CNN
	1    6600 1700
	1    0    0    -1  
$EndComp
$Comp
L d_inverter U2
U 1 1 682F2EFC
P 1450 1250
F 0 "U2" H 1450 1150 60  0000 C CNN
F 1 "d_inverter" H 1450 1400 60  0000 C CNN
F 2 "" H 1500 1200 60  0000 C CNN
F 3 "" H 1500 1200 60  0000 C CNN
	1    1450 1250
	1    0    0    -1  
$EndComp
$Comp
L d_inverter U3
U 1 1 682F2EFD
P 1450 1800
F 0 "U3" H 1450 1700 60  0000 C CNN
F 1 "d_inverter" H 1450 1950 60  0000 C CNN
F 2 "" H 1500 1750 60  0000 C CNN
F 3 "" H 1500 1750 60  0000 C CNN
	1    1450 1800
	1    0    0    -1  
$EndComp
$Comp
L d_inverter U4
U 1 1 682F2EFE
P 1450 2350
F 0 "U4" H 1450 2250 60  0000 C CNN
F 1 "d_inverter" H 1450 2500 60  0000 C CNN
F 2 "" H 1500 2300 60  0000 C CNN
F 3 "" H 1500 2300 60  0000 C CNN
	1    1450 2350
	1    0    0    -1  
$EndComp
$Comp
L d_inverter U11
U 1 1 682F2EFF
P 3000 1200
F 0 "U11" H 3000 1100 60  0000 C CNN
F 1 "d_inverter" H 3000 1350 60  0000 C CNN
F 2 "" H 3050 1150 60  0000 C CNN
F 3 "" H 3050 1150 60  0000 C CNN
	1    3000 1200
	1    0    0    -1  
$EndComp
$Comp
L d_inverter U12
U 1 1 682F2F00
P 3000 1750
F 0 "U12" H 3000 1650 60  0000 C CNN
F 1 "d_inverter" H 3000 1900 60  0000 C CNN
F 2 "" H 3050 1700 60  0000 C CNN
F 3 "" H 3050 1700 60  0000 C CNN
	1    3000 1750
	1    0    0    -1  
$EndComp
$Comp
L d_inverter U13
U 1 1 682F2F01
P 3000 2300
F 0 "U13" H 3000 2200 60  0000 C CNN
F 1 "d_inverter" H 3000 2450 60  0000 C CNN
F 2 "" H 3050 2250 60  0000 C CNN
F 3 "" H 3050 2250 60  0000 C CNN
	1    3000 2300
	1    0    0    -1  
$EndComp
Connection ~ 2200 2350
Wire Wire Line
	2200 1100 2200 2350
Wire Wire Line
	3900 1100 2200 1100
Wire Wire Line
	2700 2350 2700 2300
Wire Wire Line
	1750 2350 2700 2350
Wire Wire Line
	2050 1850 3900 1850
Connection ~ 2050 1800
Wire Wire Line
	2050 1000 2050 1850
Wire Wire Line
	3900 1000 2050 1000
Wire Wire Line
	2700 1800 2700 1750
Wire Wire Line
	1750 1800 2700 1800
Connection ~ 1900 1400
Wire Wire Line
	1900 1950 3900 1950
Connection ~ 1900 1250
Wire Wire Line
	1900 1250 1900 1950
Wire Wire Line
	3900 1400 1900 1400
Wire Wire Line
	2700 1250 2700 1200
Wire Wire Line
	1750 1250 2700 1250
Wire Wire Line
	5000 1850 5200 1850
Wire Wire Line
	5000 2450 5000 1850
Wire Wire Line
	4750 2450 5000 2450
Wire Wire Line
	4950 1750 5200 1750
Wire Wire Line
	4950 1950 4950 1750
Wire Wire Line
	4750 1950 4950 1950
Wire Wire Line
	4950 1650 5200 1650
Wire Wire Line
	4950 1500 4950 1650
Wire Wire Line
	4750 1500 4950 1500
Wire Wire Line
	5050 1550 5200 1550
Wire Wire Line
	5050 1100 5050 1550
Wire Wire Line
	4750 1100 5050 1100
Wire Wire Line
	6100 1700 6300 1700
Wire Wire Line
	3900 1200 3300 1200
Wire Wire Line
	3500 1200 3500 2550
Wire Wire Line
	3500 2550 3900 2550
Connection ~ 3500 1200
Wire Wire Line
	3900 1600 3750 1600
Wire Wire Line
	3750 1600 3750 1750
Wire Wire Line
	3750 1750 3300 1750
Wire Wire Line
	3650 1750 3650 2450
Wire Wire Line
	3650 2450 3900 2450
Connection ~ 3650 1750
Wire Wire Line
	3900 2050 3900 2350
Wire Wire Line
	3900 2200 3300 2200
Wire Wire Line
	3300 2200 3300 2300
Connection ~ 3900 2200
$Comp
L 3_and X5
U 1 1 682F2F02
P 4300 3250
F 0 "X5" H 4400 3200 60  0000 C CNN
F 1 "3_and" H 4450 3400 60  0000 C CNN
F 2 "" H 4300 3250 60  0000 C CNN
F 3 "" H 4300 3250 60  0000 C CNN
	1    4300 3250
	1    0    0    -1  
$EndComp
$Comp
L 3_and X6
U 1 1 682F2F03
P 4300 3650
F 0 "X6" H 4400 3600 60  0000 C CNN
F 1 "3_and" H 4450 3800 60  0000 C CNN
F 2 "" H 4300 3650 60  0000 C CNN
F 3 "" H 4300 3650 60  0000 C CNN
	1    4300 3650
	1    0    0    -1  
$EndComp
$Comp
L 3_and X7
U 1 1 682F2F04
P 4300 4100
F 0 "X7" H 4400 4050 60  0000 C CNN
F 1 "3_and" H 4450 4250 60  0000 C CNN
F 2 "" H 4300 4100 60  0000 C CNN
F 3 "" H 4300 4100 60  0000 C CNN
	1    4300 4100
	1    0    0    -1  
$EndComp
$Comp
L 3_and X8
U 1 1 682F2F05
P 4300 4600
F 0 "X8" H 4400 4550 60  0000 C CNN
F 1 "3_and" H 4450 4750 60  0000 C CNN
F 2 "" H 4300 4600 60  0000 C CNN
F 3 "" H 4300 4600 60  0000 C CNN
	1    4300 4600
	1    0    0    -1  
$EndComp
$Comp
L 4_OR X14
U 1 1 682F2F06
P 5600 3800
F 0 "X14" H 5750 3700 60  0000 C CNN
F 1 "4_OR" H 5750 3900 60  0000 C CNN
F 2 "" H 5600 3800 60  0000 C CNN
F 3 "" H 5600 3800 60  0000 C CNN
	1    5600 3800
	1    0    0    -1  
$EndComp
$Comp
L d_inverter U21
U 1 1 682F2F07
P 6650 3800
F 0 "U21" H 6650 3700 60  0000 C CNN
F 1 "d_inverter" H 6650 3950 60  0000 C CNN
F 2 "" H 6700 3750 60  0000 C CNN
F 3 "" H 6700 3750 60  0000 C CNN
	1    6650 3800
	1    0    0    -1  
$EndComp
$Comp
L d_inverter U5
U 1 1 682F2F08
P 1500 3350
F 0 "U5" H 1500 3250 60  0000 C CNN
F 1 "d_inverter" H 1500 3500 60  0000 C CNN
F 2 "" H 1550 3300 60  0000 C CNN
F 3 "" H 1550 3300 60  0000 C CNN
	1    1500 3350
	1    0    0    -1  
$EndComp
$Comp
L d_inverter U6
U 1 1 682F2F09
P 1500 3900
F 0 "U6" H 1500 3800 60  0000 C CNN
F 1 "d_inverter" H 1500 4050 60  0000 C CNN
F 2 "" H 1550 3850 60  0000 C CNN
F 3 "" H 1550 3850 60  0000 C CNN
	1    1500 3900
	1    0    0    -1  
$EndComp
$Comp
L d_inverter U7
U 1 1 682F2F0A
P 1500 4450
F 0 "U7" H 1500 4350 60  0000 C CNN
F 1 "d_inverter" H 1500 4600 60  0000 C CNN
F 2 "" H 1550 4400 60  0000 C CNN
F 3 "" H 1550 4400 60  0000 C CNN
	1    1500 4450
	1    0    0    -1  
$EndComp
$Comp
L d_inverter U14
U 1 1 682F2F0B
P 3050 3300
F 0 "U14" H 3050 3200 60  0000 C CNN
F 1 "d_inverter" H 3050 3450 60  0000 C CNN
F 2 "" H 3100 3250 60  0000 C CNN
F 3 "" H 3100 3250 60  0000 C CNN
	1    3050 3300
	1    0    0    -1  
$EndComp
$Comp
L d_inverter U15
U 1 1 682F2F0C
P 3050 3850
F 0 "U15" H 3050 3750 60  0000 C CNN
F 1 "d_inverter" H 3050 4000 60  0000 C CNN
F 2 "" H 3100 3800 60  0000 C CNN
F 3 "" H 3100 3800 60  0000 C CNN
	1    3050 3850
	1    0    0    -1  
$EndComp
$Comp
L d_inverter U16
U 1 1 682F2F0D
P 3050 4400
F 0 "U16" H 3050 4300 60  0000 C CNN
F 1 "d_inverter" H 3050 4550 60  0000 C CNN
F 2 "" H 3100 4350 60  0000 C CNN
F 3 "" H 3100 4350 60  0000 C CNN
	1    3050 4400
	1    0    0    -1  
$EndComp
Connection ~ 2250 4450
Wire Wire Line
	2250 3200 2250 4450
Wire Wire Line
	3950 3200 2250 3200
Wire Wire Line
	2750 4450 2750 4400
Wire Wire Line
	1800 4450 2750 4450
Wire Wire Line
	2100 3950 3950 3950
Connection ~ 2100 3900
Wire Wire Line
	2100 3100 2100 3950
Wire Wire Line
	3950 3100 2100 3100
Wire Wire Line
	2750 3900 2750 3850
Wire Wire Line
	1800 3900 2750 3900
Connection ~ 1950 3500
Wire Wire Line
	1950 4050 3950 4050
Connection ~ 1950 3350
Wire Wire Line
	1950 3350 1950 4050
Wire Wire Line
	3950 3500 1950 3500
Wire Wire Line
	2750 3350 2750 3300
Wire Wire Line
	1800 3350 2750 3350
Wire Wire Line
	5050 3950 5250 3950
Wire Wire Line
	5050 4550 5050 3950
Wire Wire Line
	4800 4550 5050 4550
Wire Wire Line
	5000 3850 5250 3850
Wire Wire Line
	5000 4050 5000 3850
Wire Wire Line
	4800 4050 5000 4050
Wire Wire Line
	5000 3750 5250 3750
Wire Wire Line
	5000 3600 5000 3750
Wire Wire Line
	4800 3600 5000 3600
Wire Wire Line
	5100 3650 5250 3650
Wire Wire Line
	5100 3200 5100 3650
Wire Wire Line
	4800 3200 5100 3200
Wire Wire Line
	6150 3800 6350 3800
Wire Wire Line
	3950 3300 3350 3300
Wire Wire Line
	3550 3300 3550 4650
Wire Wire Line
	3550 4650 3950 4650
Connection ~ 3550 3300
Wire Wire Line
	3950 3700 3800 3700
Wire Wire Line
	3800 3700 3800 3850
Wire Wire Line
	3800 3850 3350 3850
Wire Wire Line
	3700 3850 3700 4550
Wire Wire Line
	3700 4550 3950 4550
Connection ~ 3700 3850
Wire Wire Line
	3950 4150 3950 4450
Wire Wire Line
	3950 4300 3350 4300
Wire Wire Line
	3350 4300 3350 4400
Connection ~ 3950 4300
$Comp
L 3_and X9
U 1 1 682F2F0E
P 4300 5450
F 0 "X9" H 4400 5400 60  0000 C CNN
F 1 "3_and" H 4450 5600 60  0000 C CNN
F 2 "" H 4300 5450 60  0000 C CNN
F 3 "" H 4300 5450 60  0000 C CNN
	1    4300 5450
	1    0    0    -1  
$EndComp
$Comp
L 3_and X10
U 1 1 682F2F0F
P 4300 5850
F 0 "X10" H 4400 5800 60  0000 C CNN
F 1 "3_and" H 4450 6000 60  0000 C CNN
F 2 "" H 4300 5850 60  0000 C CNN
F 3 "" H 4300 5850 60  0000 C CNN
	1    4300 5850
	1    0    0    -1  
$EndComp
$Comp
L 3_and X11
U 1 1 682F2F10
P 4300 6300
F 0 "X11" H 4400 6250 60  0000 C CNN
F 1 "3_and" H 4450 6450 60  0000 C CNN
F 2 "" H 4300 6300 60  0000 C CNN
F 3 "" H 4300 6300 60  0000 C CNN
	1    4300 6300
	1    0    0    -1  
$EndComp
$Comp
L 3_and X12
U 1 1 682F2F11
P 4300 6800
F 0 "X12" H 4400 6750 60  0000 C CNN
F 1 "3_and" H 4450 6950 60  0000 C CNN
F 2 "" H 4300 6800 60  0000 C CNN
F 3 "" H 4300 6800 60  0000 C CNN
	1    4300 6800
	1    0    0    -1  
$EndComp
$Comp
L 4_OR X15
U 1 1 682F2F12
P 5600 6000
F 0 "X15" H 5750 5900 60  0000 C CNN
F 1 "4_OR" H 5750 6100 60  0000 C CNN
F 2 "" H 5600 6000 60  0000 C CNN
F 3 "" H 5600 6000 60  0000 C CNN
	1    5600 6000
	1    0    0    -1  
$EndComp
$Comp
L d_inverter U22
U 1 1 682F2F13
P 6650 6000
F 0 "U22" H 6650 5900 60  0000 C CNN
F 1 "d_inverter" H 6650 6150 60  0000 C CNN
F 2 "" H 6700 5950 60  0000 C CNN
F 3 "" H 6700 5950 60  0000 C CNN
	1    6650 6000
	1    0    0    -1  
$EndComp
$Comp
L d_inverter U8
U 1 1 682F2F14
P 1500 5550
F 0 "U8" H 1500 5450 60  0000 C CNN
F 1 "d_inverter" H 1500 5700 60  0000 C CNN
F 2 "" H 1550 5500 60  0000 C CNN
F 3 "" H 1550 5500 60  0000 C CNN
	1    1500 5550
	1    0    0    -1  
$EndComp
$Comp
L d_inverter U9
U 1 1 682F2F15
P 1500 6100
F 0 "U9" H 1500 6000 60  0000 C CNN
F 1 "d_inverter" H 1500 6250 60  0000 C CNN
F 2 "" H 1550 6050 60  0000 C CNN
F 3 "" H 1550 6050 60  0000 C CNN
	1    1500 6100
	1    0    0    -1  
$EndComp
$Comp
L d_inverter U10
U 1 1 682F2F16
P 1500 6650
F 0 "U10" H 1500 6550 60  0000 C CNN
F 1 "d_inverter" H 1500 6800 60  0000 C CNN
F 2 "" H 1550 6600 60  0000 C CNN
F 3 "" H 1550 6600 60  0000 C CNN
	1    1500 6650
	1    0    0    -1  
$EndComp
$Comp
L d_inverter U17
U 1 1 682F2F17
P 3050 5500
F 0 "U17" H 3050 5400 60  0000 C CNN
F 1 "d_inverter" H 3050 5650 60  0000 C CNN
F 2 "" H 3100 5450 60  0000 C CNN
F 3 "" H 3100 5450 60  0000 C CNN
	1    3050 5500
	1    0    0    -1  
$EndComp
$Comp
L d_inverter U18
U 1 1 682F2F18
P 3050 6050
F 0 "U18" H 3050 5950 60  0000 C CNN
F 1 "d_inverter" H 3050 6200 60  0000 C CNN
F 2 "" H 3100 6000 60  0000 C CNN
F 3 "" H 3100 6000 60  0000 C CNN
	1    3050 6050
	1    0    0    -1  
$EndComp
$Comp
L d_inverter U19
U 1 1 682F2F19
P 3050 6600
F 0 "U19" H 3050 6500 60  0000 C CNN
F 1 "d_inverter" H 3050 6750 60  0000 C CNN
F 2 "" H 3100 6550 60  0000 C CNN
F 3 "" H 3100 6550 60  0000 C CNN
	1    3050 6600
	1    0    0    -1  
$EndComp
Connection ~ 2250 6650
Wire Wire Line
	2250 5400 2250 6650
Wire Wire Line
	3950 5400 2250 5400
Wire Wire Line
	2750 6650 2750 6600
Wire Wire Line
	1800 6650 2750 6650
Wire Wire Line
	2100 6150 3950 6150
Connection ~ 2100 6100
Wire Wire Line
	2100 5300 2100 6150
Wire Wire Line
	3950 5300 2100 5300
Wire Wire Line
	2750 6100 2750 6050
Wire Wire Line
	1800 6100 2750 6100
Connection ~ 1950 5700
Wire Wire Line
	1950 6250 3950 6250
Connection ~ 1950 5550
Wire Wire Line
	1950 5550 1950 6250
Wire Wire Line
	3950 5700 1950 5700
Wire Wire Line
	2750 5550 2750 5500
Wire Wire Line
	1800 5550 2750 5550
Wire Wire Line
	5050 6150 5250 6150
Wire Wire Line
	5050 6750 5050 6150
Wire Wire Line
	4800 6750 5050 6750
Wire Wire Line
	5000 6050 5250 6050
Wire Wire Line
	5000 6250 5000 6050
Wire Wire Line
	4800 6250 5000 6250
Wire Wire Line
	5000 5950 5250 5950
Wire Wire Line
	5000 5800 5000 5950
Wire Wire Line
	4800 5800 5000 5800
Wire Wire Line
	5100 5850 5250 5850
Wire Wire Line
	5100 5400 5100 5850
Wire Wire Line
	4800 5400 5100 5400
Wire Wire Line
	6150 6000 6350 6000
Wire Wire Line
	3950 5500 3350 5500
Wire Wire Line
	3550 5500 3550 6850
Wire Wire Line
	3550 6850 3950 6850
Connection ~ 3550 5500
Wire Wire Line
	3950 5900 3800 5900
Wire Wire Line
	3800 5900 3800 6050
Wire Wire Line
	3800 6050 3350 6050
Wire Wire Line
	3700 6050 3700 6750
Wire Wire Line
	3700 6750 3950 6750
Connection ~ 3700 6050
Wire Wire Line
	3950 6350 3950 6650
Wire Wire Line
	3950 6500 3350 6500
Wire Wire Line
	3350 6500 3350 6600
Connection ~ 3950 6500
$Comp
L 3_and X16
U 1 1 682F2F1A
P 9050 1300
F 0 "X16" H 9150 1250 60  0000 C CNN
F 1 "3_and" H 9200 1450 60  0000 C CNN
F 2 "" H 9050 1300 60  0000 C CNN
F 3 "" H 9050 1300 60  0000 C CNN
	1    9050 1300
	1    0    0    -1  
$EndComp
$Comp
L 3_and X17
U 1 1 682F2F1B
P 9050 1950
F 0 "X17" H 9150 1900 60  0000 C CNN
F 1 "3_and" H 9200 2100 60  0000 C CNN
F 2 "" H 9050 1950 60  0000 C CNN
F 3 "" H 9050 1950 60  0000 C CNN
	1    9050 1950
	1    0    0    -1  
$EndComp
$Comp
L 3_and X18
U 1 1 682F2F1C
P 9050 2600
F 0 "X18" H 9150 2550 60  0000 C CNN
F 1 "3_and" H 9200 2750 60  0000 C CNN
F 2 "" H 9050 2600 60  0000 C CNN
F 3 "" H 9050 2600 60  0000 C CNN
	1    9050 2600
	1    0    0    -1  
$EndComp
$Comp
L 3_and X19
U 1 1 682F2F1D
P 9050 3200
F 0 "X19" H 9150 3150 60  0000 C CNN
F 1 "3_and" H 9200 3350 60  0000 C CNN
F 2 "" H 9050 3200 60  0000 C CNN
F 3 "" H 9050 3200 60  0000 C CNN
	1    9050 3200
	1    0    0    -1  
$EndComp
$Comp
L 4_OR X24
U 1 1 682F2F1E
P 10150 2300
F 0 "X24" H 10300 2200 60  0000 C CNN
F 1 "4_OR" H 10300 2400 60  0000 C CNN
F 2 "" H 10150 2300 60  0000 C CNN
F 3 "" H 10150 2300 60  0000 C CNN
	1    10150 2300
	1    0    0    -1  
$EndComp
$Comp
L d_inverter U23
U 1 1 682F2F1F
P 7400 1700
F 0 "U23" H 7400 1600 60  0000 C CNN
F 1 "d_inverter" H 7400 1850 60  0000 C CNN
F 2 "" H 7450 1650 60  0000 C CNN
F 3 "" H 7450 1650 60  0000 C CNN
	1    7400 1700
	1    0    0    -1  
$EndComp
$Comp
L 3_and X20
U 1 1 682F2F20
P 9050 4000
F 0 "X20" H 9150 3950 60  0000 C CNN
F 1 "3_and" H 9200 4150 60  0000 C CNN
F 2 "" H 9050 4000 60  0000 C CNN
F 3 "" H 9050 4000 60  0000 C CNN
	1    9050 4000
	1    0    0    -1  
$EndComp
$Comp
L 3_and X21
U 1 1 682F2F21
P 9050 4650
F 0 "X21" H 9150 4600 60  0000 C CNN
F 1 "3_and" H 9200 4800 60  0000 C CNN
F 2 "" H 9050 4650 60  0000 C CNN
F 3 "" H 9050 4650 60  0000 C CNN
	1    9050 4650
	1    0    0    -1  
$EndComp
$Comp
L 3_and X22
U 1 1 682F2F22
P 9050 5300
F 0 "X22" H 9150 5250 60  0000 C CNN
F 1 "3_and" H 9200 5450 60  0000 C CNN
F 2 "" H 9050 5300 60  0000 C CNN
F 3 "" H 9050 5300 60  0000 C CNN
	1    9050 5300
	1    0    0    -1  
$EndComp
$Comp
L 3_and X23
U 1 1 682F2F23
P 9050 5900
F 0 "X23" H 9150 5850 60  0000 C CNN
F 1 "3_and" H 9200 6050 60  0000 C CNN
F 2 "" H 9050 5900 60  0000 C CNN
F 3 "" H 9050 5900 60  0000 C CNN
	1    9050 5900
	1    0    0    -1  
$EndComp
$Comp
L 4_OR X25
U 1 1 682F2F24
P 10150 5000
F 0 "X25" H 10300 4900 60  0000 C CNN
F 1 "4_OR" H 10300 5100 60  0000 C CNN
F 2 "" H 10150 5000 60  0000 C CNN
F 3 "" H 10150 5000 60  0000 C CNN
	1    10150 5000
	1    0    0    -1  
$EndComp
$Comp
L d_inverter U24
U 1 1 682F2F25
P 7400 4400
F 0 "U24" H 7400 4300 60  0000 C CNN
F 1 "d_inverter" H 7400 4550 60  0000 C CNN
F 2 "" H 7450 4350 60  0000 C CNN
F 3 "" H 7450 4350 60  0000 C CNN
	1    7400 4400
	1    0    0    -1  
$EndComp
$Comp
L d_inverter U26
U 1 1 682F2F26
P 10900 2600
F 0 "U26" H 10900 2500 60  0000 C CNN
F 1 "d_inverter" H 10900 2750 60  0000 C CNN
F 2 "" H 10950 2550 60  0000 C CNN
F 3 "" H 10950 2550 60  0000 C CNN
	1    10900 2600
	0    1    1    0   
$EndComp
$Comp
L d_inverter U27
U 1 1 682F2F27
P 10900 5300
F 0 "U27" H 10900 5200 60  0000 C CNN
F 1 "d_inverter" H 10900 5450 60  0000 C CNN
F 2 "" H 10950 5250 60  0000 C CNN
F 3 "" H 10950 5250 60  0000 C CNN
	1    10900 5300
	0    1    1    0   
$EndComp
$Comp
L d_inverter U25
U 1 1 682F2F28
P 7500 6000
F 0 "U25" H 7500 5900 60  0000 C CNN
F 1 "d_inverter" H 7500 6150 60  0000 C CNN
F 2 "" H 7550 5950 60  0000 C CNN
F 3 "" H 7550 5950 60  0000 C CNN
	1    7500 6000
	1    0    0    -1  
$EndComp
Wire Wire Line
	10900 2300 10700 2300
Wire Wire Line
	9550 1250 9800 1250
Wire Wire Line
	9800 1250 9800 2150
Wire Wire Line
	9550 1900 9550 2250
Wire Wire Line
	9550 2250 9800 2250
Wire Wire Line
	9550 2550 9550 2350
Wire Wire Line
	9550 2350 9800 2350
Wire Wire Line
	9800 2450 9800 3150
Wire Wire Line
	9800 3150 9550 3150
Wire Wire Line
	10700 5000 10900 5000
Wire Wire Line
	9550 3950 9800 3950
Wire Wire Line
	9800 3950 9800 4850
Wire Wire Line
	9550 4600 9550 4950
Wire Wire Line
	9550 4950 9800 4950
Wire Wire Line
	9550 5250 9550 5050
Wire Wire Line
	9550 5050 9800 5050
Wire Wire Line
	9800 5150 9800 5850
Wire Wire Line
	9800 5850 9550 5850
Wire Wire Line
	6900 1700 7100 1700
Wire Wire Line
	6950 1150 6950 4400
Wire Wire Line
	6950 4400 7100 4400
Wire Wire Line
	6950 6000 7200 6000
Wire Wire Line
	8700 1350 7700 1350
Wire Wire Line
	7700 1350 7700 5250
Wire Wire Line
	7700 3050 8700 3050
Connection ~ 7700 1700
Wire Wire Line
	7000 1700 7000 5850
Wire Wire Line
	7000 1800 8700 1800
Connection ~ 7000 1700
Wire Wire Line
	7000 2450 8700 2450
Connection ~ 7000 1800
Wire Wire Line
	7000 4050 8700 4050
Connection ~ 7000 2450
Wire Wire Line
	7000 5850 8700 5850
Connection ~ 7000 4050
Wire Wire Line
	8700 5950 7050 5950
Wire Wire Line
	7050 1250 7050 6000
Connection ~ 7050 6000
Wire Wire Line
	8700 5350 7050 5350
Connection ~ 7050 5950
Wire Wire Line
	8700 1900 7050 1900
Connection ~ 7050 5350
Wire Wire Line
	8700 1250 7050 1250
Connection ~ 7050 1900
Wire Wire Line
	6950 1150 8700 1150
Connection ~ 6950 3800
Wire Wire Line
	6950 3800 6950 5750
Wire Wire Line
	8700 2550 6950 2550
Connection ~ 6950 2550
Wire Wire Line
	8700 2000 8100 2000
Wire Wire Line
	8100 2000 8100 5150
Wire Wire Line
	8100 3150 8700 3150
Wire Wire Line
	8700 2650 8350 2650
Wire Wire Line
	8350 2650 8350 6000
Wire Wire Line
	8350 3250 8700 3250
Wire Wire Line
	8350 3950 8700 3950
Connection ~ 8350 3250
Wire Wire Line
	8350 4700 8700 4700
Connection ~ 8350 3950
Wire Wire Line
	8350 6000 7800 6000
Connection ~ 8350 4700
Wire Wire Line
	8100 4400 7700 4400
Connection ~ 8100 3150
Wire Wire Line
	8700 3850 8100 3850
Connection ~ 8100 3850
Wire Wire Line
	8100 5150 8700 5150
Connection ~ 8100 4400
Wire Wire Line
	7700 4600 8700 4600
Connection ~ 7700 3050
Wire Wire Line
	7700 5250 8700 5250
Connection ~ 7700 4600
Wire Wire Line
	6950 5750 8700 5750
Connection ~ 6950 4500
Wire Wire Line
	3900 1500 2200 1500
Connection ~ 2200 1500
Wire Wire Line
	3950 5800 2250 5800
Connection ~ 2250 5800
Wire Wire Line
	3950 3600 2250 3600
Connection ~ 2250 3600
Wire Wire Line
	6950 4500 8700 4500
$Comp
L PORT U1
U 1 1 68314B94
P 950 5550
F 0 "U1" H 1000 5650 30  0000 C CNN
F 1 "PORT" H 950 5550 30  0000 C CNN
F 2 "" H 950 5550 60  0000 C CNN
F 3 "" H 950 5550 60  0000 C CNN
	1    950  5550
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 2 1 68314DAB
P 950 6100
F 0 "U1" H 1000 6200 30  0000 C CNN
F 1 "PORT" H 950 6100 30  0000 C CNN
F 2 "" H 950 6100 60  0000 C CNN
F 3 "" H 950 6100 60  0000 C CNN
	2    950  6100
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 3 1 68314E64
P 950 7250
F 0 "U1" H 1000 7350 30  0000 C CNN
F 1 "PORT" H 950 7250 30  0000 C CNN
F 2 "" H 950 7250 60  0000 C CNN
F 3 "" H 950 7250 60  0000 C CNN
	3    950  7250
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 4 1 68314F01
P 950 6650
F 0 "U1" H 1000 6750 30  0000 C CNN
F 1 "PORT" H 950 6650 30  0000 C CNN
F 2 "" H 950 6650 60  0000 C CNN
F 3 "" H 950 6650 60  0000 C CNN
	4    950  6650
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 5 1 68315AEE
P 10650 2900
F 0 "U1" H 10700 3000 30  0000 C CNN
F 1 "PORT" H 10650 2900 30  0000 C CNN
F 2 "" H 10650 2900 60  0000 C CNN
F 3 "" H 10650 2900 60  0000 C CNN
	5    10650 2900
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 6 1 68315BA1
P 10650 5600
F 0 "U1" H 10700 5700 30  0000 C CNN
F 1 "PORT" H 10650 5600 30  0000 C CNN
F 2 "" H 10650 5600 60  0000 C CNN
F 3 "" H 10650 5600 60  0000 C CNN
	6    10650 5600
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 7 1 68315FD8
P 950 750
F 0 "U1" H 1000 850 30  0000 C CNN
F 1 "PORT" H 950 750 30  0000 C CNN
F 2 "" H 950 750 60  0000 C CNN
F 3 "" H 950 750 60  0000 C CNN
	7    950  750 
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 8 1 683160CB
P 900 1250
F 0 "U1" H 950 1350 30  0000 C CNN
F 1 "PORT" H 900 1250 30  0000 C CNN
F 2 "" H 900 1250 60  0000 C CNN
F 3 "" H 900 1250 60  0000 C CNN
	8    900  1250
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 9 1 6831616C
P 900 1800
F 0 "U1" H 950 1900 30  0000 C CNN
F 1 "PORT" H 900 1800 30  0000 C CNN
F 2 "" H 900 1800 60  0000 C CNN
F 3 "" H 900 1800 60  0000 C CNN
	9    900  1800
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 10 1 6831623B
P 900 2350
F 0 "U1" H 950 2450 30  0000 C CNN
F 1 "PORT" H 900 2350 30  0000 C CNN
F 2 "" H 900 2350 60  0000 C CNN
F 3 "" H 900 2350 60  0000 C CNN
	10   900  2350
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 11 1 683162EE
P 950 3350
F 0 "U1" H 1000 3450 30  0000 C CNN
F 1 "PORT" H 950 3350 30  0000 C CNN
F 2 "" H 950 3350 60  0000 C CNN
F 3 "" H 950 3350 60  0000 C CNN
	11   950  3350
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 12 1 68316715
P 950 3900
F 0 "U1" H 1000 4000 30  0000 C CNN
F 1 "PORT" H 950 3900 30  0000 C CNN
F 2 "" H 950 3900 60  0000 C CNN
F 3 "" H 950 3900 60  0000 C CNN
	12   950  3900
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 13 1 683167DC
P 950 4450
F 0 "U1" H 1000 4550 30  0000 C CNN
F 1 "PORT" H 950 4450 30  0000 C CNN
F 2 "" H 950 4450 60  0000 C CNN
F 3 "" H 950 4450 60  0000 C CNN
	13   950  4450
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 14 1 68316895
P 950 5000
F 0 "U1" H 1000 5100 30  0000 C CNN
F 1 "PORT" H 950 5000 30  0000 C CNN
F 2 "" H 950 5000 60  0000 C CNN
F 3 "" H 950 5000 60  0000 C CNN
	14   950  5000
	1    0    0    -1  
$EndComp
NoConn ~ 1200 5000
NoConn ~ 1200 7250
NoConn ~ 1200 750 
$EndSCHEMATC
