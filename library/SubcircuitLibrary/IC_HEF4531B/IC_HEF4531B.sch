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
$Descr A3 16535 11693
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
L HEF4531B X1
U 1 1 685A4204
P 10850 6200
F 0 "X1" H 10900 5400 60  0000 C CNN
F 1 "HEF4531B" H 10850 6850 60  0000 C CNN
F 2 "" H 10850 6200 60  0001 C CNN
F 3 "" H 10850 6200 60  0001 C CNN
	1    10850 6200
	1    0    0    -1  
$EndComp
$Comp
L adc_bridge_8 U15
U 1 1 685A4222
P 9450 5850
F 0 "U15" H 9450 5850 60  0000 C CNN
F 1 "adc_bridge_8" H 9450 6000 60  0000 C CNN
F 2 "" H 9450 5850 60  0000 C CNN
F 3 "" H 9450 5850 60  0000 C CNN
	1    9450 5850
	1    0    0    -1  
$EndComp
$Comp
L adc_bridge_5 U14
U 1 1 685A4267
P 9400 7150
F 0 "U14" H 9400 7150 60  0000 C CNN
F 1 "adc_bridge_5" H 9400 7300 60  0000 C CNN
F 2 "" H 9400 7150 60  0000 C CNN
F 3 "" H 9400 7150 60  0000 C CNN
	1    9400 7150
	1    0    0    -1  
$EndComp
$Comp
L dac_bridge_1 U16
U 1 1 685A42DC
P 12300 6250
F 0 "U16" H 12300 6250 60  0000 C CNN
F 1 "dac_bridge_1" H 12300 6400 60  0000 C CNN
F 2 "" H 12300 6250 60  0000 C CNN
F 3 "" H 12300 6250 60  0000 C CNN
	1    12300 6250
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U17
U 1 1 685A430F
P 13200 6200
F 0 "U17" H 13200 6700 60  0000 C CNN
F 1 "plot_v1" H 13400 6550 60  0000 C CNN
F 2 "" H 13200 6200 60  0000 C CNN
F 3 "" H 13200 6200 60  0000 C CNN
	1    13200 6200
	0    1    1    0   
$EndComp
$Comp
L pulse v1
U 1 1 685A454B
P 3800 4900
F 0 "v1" H 3600 5000 60  0000 C CNN
F 1 "pulse" H 3600 4850 60  0000 C CNN
F 2 "R1" H 3500 4900 60  0000 C CNN
F 3 "" H 3800 4900 60  0000 C CNN
	1    3800 4900
	0    1    1    0   
$EndComp
$Comp
L pulse v2
U 1 1 685A4610
P 3800 5250
F 0 "v2" H 3600 5350 60  0000 C CNN
F 1 "pulse" H 3600 5200 60  0000 C CNN
F 2 "R1" H 3500 5250 60  0000 C CNN
F 3 "" H 3800 5250 60  0000 C CNN
	1    3800 5250
	0    1    1    0   
$EndComp
$Comp
L pulse v3
U 1 1 685A463F
P 3800 5600
F 0 "v3" H 3600 5700 60  0000 C CNN
F 1 "pulse" H 3600 5550 60  0000 C CNN
F 2 "R1" H 3500 5600 60  0000 C CNN
F 3 "" H 3800 5600 60  0000 C CNN
	1    3800 5600
	0    1    1    0   
$EndComp
$Comp
L pulse v4
U 1 1 685A4681
P 3800 5950
F 0 "v4" H 3600 6050 60  0000 C CNN
F 1 "pulse" H 3600 5900 60  0000 C CNN
F 2 "R1" H 3500 5950 60  0000 C CNN
F 3 "" H 3800 5950 60  0000 C CNN
	1    3800 5950
	0    1    1    0   
$EndComp
$Comp
L pulse v5
U 1 1 685A46BE
P 3800 6300
F 0 "v5" H 3600 6400 60  0000 C CNN
F 1 "pulse" H 3600 6250 60  0000 C CNN
F 2 "R1" H 3500 6300 60  0000 C CNN
F 3 "" H 3800 6300 60  0000 C CNN
	1    3800 6300
	0    1    1    0   
$EndComp
$Comp
L pulse v6
U 1 1 685A46F6
P 3800 6650
F 0 "v6" H 3600 6750 60  0000 C CNN
F 1 "pulse" H 3600 6600 60  0000 C CNN
F 2 "R1" H 3500 6650 60  0000 C CNN
F 3 "" H 3800 6650 60  0000 C CNN
	1    3800 6650
	0    1    1    0   
$EndComp
$Comp
L pulse v7
U 1 1 685A4756
P 3800 7000
F 0 "v7" H 3600 7100 60  0000 C CNN
F 1 "pulse" H 3600 6950 60  0000 C CNN
F 2 "R1" H 3500 7000 60  0000 C CNN
F 3 "" H 3800 7000 60  0000 C CNN
	1    3800 7000
	0    1    1    0   
$EndComp
$Comp
L pulse v8
U 1 1 685A479C
P 3800 7400
F 0 "v8" H 3600 7500 60  0000 C CNN
F 1 "pulse" H 3600 7350 60  0000 C CNN
F 2 "R1" H 3500 7400 60  0000 C CNN
F 3 "" H 3800 7400 60  0000 C CNN
	1    3800 7400
	0    1    1    0   
$EndComp
$Comp
L pulse v9
U 1 1 685A47DD
P 3800 7800
F 0 "v9" H 3600 7900 60  0000 C CNN
F 1 "pulse" H 3600 7750 60  0000 C CNN
F 2 "R1" H 3500 7800 60  0000 C CNN
F 3 "" H 3800 7800 60  0000 C CNN
	1    3800 7800
	0    1    1    0   
$EndComp
$Comp
L pulse v10
U 1 1 685A4823
P 3800 8150
F 0 "v10" H 3600 8250 60  0000 C CNN
F 1 "pulse" H 3600 8100 60  0000 C CNN
F 2 "R1" H 3500 8150 60  0000 C CNN
F 3 "" H 3800 8150 60  0000 C CNN
	1    3800 8150
	0    1    1    0   
$EndComp
$Comp
L pulse v11
U 1 1 685A4D6B
P 3800 8550
F 0 "v11" H 3600 8650 60  0000 C CNN
F 1 "pulse" H 3600 8500 60  0000 C CNN
F 2 "R1" H 3500 8550 60  0000 C CNN
F 3 "" H 3800 8550 60  0000 C CNN
	1    3800 8550
	0    1    1    0   
$EndComp
$Comp
L pulse v12
U 1 1 685A4DBD
P 3800 8950
F 0 "v12" H 3600 9050 60  0000 C CNN
F 1 "pulse" H 3600 8900 60  0000 C CNN
F 2 "R1" H 3500 8950 60  0000 C CNN
F 3 "" H 3800 8950 60  0000 C CNN
	1    3800 8950
	0    1    1    0   
$EndComp
$Comp
L pulse v13
U 1 1 685A4E0C
P 3800 9300
F 0 "v13" H 3600 9400 60  0000 C CNN
F 1 "pulse" H 3600 9250 60  0000 C CNN
F 2 "R1" H 3500 9300 60  0000 C CNN
F 3 "" H 3800 9300 60  0000 C CNN
	1    3800 9300
	0    1    1    0   
$EndComp
$Comp
L GND #PWR01
U 1 1 685A50BB
P 3350 5000
F 0 "#PWR01" H 3350 4750 50  0001 C CNN
F 1 "GND" H 3350 4850 50  0000 C CNN
F 2 "" H 3350 5000 50  0001 C CNN
F 3 "" H 3350 5000 50  0001 C CNN
	1    3350 5000
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR02
U 1 1 685A50F3
P 3350 5350
F 0 "#PWR02" H 3350 5100 50  0001 C CNN
F 1 "GND" H 3350 5200 50  0000 C CNN
F 2 "" H 3350 5350 50  0001 C CNN
F 3 "" H 3350 5350 50  0001 C CNN
	1    3350 5350
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR03
U 1 1 685A512B
P 3350 5700
F 0 "#PWR03" H 3350 5450 50  0001 C CNN
F 1 "GND" H 3350 5550 50  0000 C CNN
F 2 "" H 3350 5700 50  0001 C CNN
F 3 "" H 3350 5700 50  0001 C CNN
	1    3350 5700
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR04
U 1 1 685A5163
P 3350 6050
F 0 "#PWR04" H 3350 5800 50  0001 C CNN
F 1 "GND" H 3350 5900 50  0000 C CNN
F 2 "" H 3350 6050 50  0001 C CNN
F 3 "" H 3350 6050 50  0001 C CNN
	1    3350 6050
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR05
U 1 1 685A519B
P 3350 6400
F 0 "#PWR05" H 3350 6150 50  0001 C CNN
F 1 "GND" H 3350 6250 50  0000 C CNN
F 2 "" H 3350 6400 50  0001 C CNN
F 3 "" H 3350 6400 50  0001 C CNN
	1    3350 6400
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR06
U 1 1 685A521B
P 3350 6750
F 0 "#PWR06" H 3350 6500 50  0001 C CNN
F 1 "GND" H 3350 6600 50  0000 C CNN
F 2 "" H 3350 6750 50  0001 C CNN
F 3 "" H 3350 6750 50  0001 C CNN
	1    3350 6750
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR07
U 1 1 685A5253
P 3350 7100
F 0 "#PWR07" H 3350 6850 50  0001 C CNN
F 1 "GND" H 3350 6950 50  0000 C CNN
F 2 "" H 3350 7100 50  0001 C CNN
F 3 "" H 3350 7100 50  0001 C CNN
	1    3350 7100
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR08
U 1 1 685A528B
P 3350 7500
F 0 "#PWR08" H 3350 7250 50  0001 C CNN
F 1 "GND" H 3350 7350 50  0000 C CNN
F 2 "" H 3350 7500 50  0001 C CNN
F 3 "" H 3350 7500 50  0001 C CNN
	1    3350 7500
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR09
U 1 1 685A52F9
P 3350 7900
F 0 "#PWR09" H 3350 7650 50  0001 C CNN
F 1 "GND" H 3350 7750 50  0000 C CNN
F 2 "" H 3350 7900 50  0001 C CNN
F 3 "" H 3350 7900 50  0001 C CNN
	1    3350 7900
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR010
U 1 1 685A5331
P 3350 8250
F 0 "#PWR010" H 3350 8000 50  0001 C CNN
F 1 "GND" H 3350 8100 50  0000 C CNN
F 2 "" H 3350 8250 50  0001 C CNN
F 3 "" H 3350 8250 50  0001 C CNN
	1    3350 8250
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR011
U 1 1 685A53B1
P 3350 8650
F 0 "#PWR011" H 3350 8400 50  0001 C CNN
F 1 "GND" H 3350 8500 50  0000 C CNN
F 2 "" H 3350 8650 50  0001 C CNN
F 3 "" H 3350 8650 50  0001 C CNN
	1    3350 8650
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR012
U 1 1 685A53E9
P 3350 9050
F 0 "#PWR012" H 3350 8800 50  0001 C CNN
F 1 "GND" H 3350 8900 50  0000 C CNN
F 2 "" H 3350 9050 50  0001 C CNN
F 3 "" H 3350 9050 50  0001 C CNN
	1    3350 9050
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR013
U 1 1 685A5421
P 3350 9400
F 0 "#PWR013" H 3350 9150 50  0001 C CNN
F 1 "GND" H 3350 9250 50  0000 C CNN
F 2 "" H 3350 9400 50  0001 C CNN
F 3 "" H 3350 9400 50  0001 C CNN
	1    3350 9400
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U8
U 1 1 685A5D91
P 6700 3050
F 0 "U8" H 6700 3550 60  0000 C CNN
F 1 "plot_v1" H 6900 3400 60  0000 C CNN
F 2 "" H 6700 3050 60  0000 C CNN
F 3 "" H 6700 3050 60  0000 C CNN
	1    6700 3050
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U9
U 1 1 685A5E64
P 7000 3050
F 0 "U9" H 7000 3550 60  0000 C CNN
F 1 "plot_v1" H 7200 3400 60  0000 C CNN
F 2 "" H 7000 3050 60  0000 C CNN
F 3 "" H 7000 3050 60  0000 C CNN
	1    7000 3050
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U10
U 1 1 685A5EB8
P 7250 3050
F 0 "U10" H 7250 3550 60  0000 C CNN
F 1 "plot_v1" H 7450 3400 60  0000 C CNN
F 2 "" H 7250 3050 60  0000 C CNN
F 3 "" H 7250 3050 60  0000 C CNN
	1    7250 3050
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U11
U 1 1 685A5F0D
P 7500 3050
F 0 "U11" H 7500 3550 60  0000 C CNN
F 1 "plot_v1" H 7700 3400 60  0000 C CNN
F 2 "" H 7500 3050 60  0000 C CNN
F 3 "" H 7500 3050 60  0000 C CNN
	1    7500 3050
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U12
U 1 1 685A5F65
P 7750 3050
F 0 "U12" H 7750 3550 60  0000 C CNN
F 1 "plot_v1" H 7950 3400 60  0000 C CNN
F 2 "" H 7750 3050 60  0000 C CNN
F 3 "" H 7750 3050 60  0000 C CNN
	1    7750 3050
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U13
U 1 1 685A5FC2
P 8000 3050
F 0 "U13" H 8000 3550 60  0000 C CNN
F 1 "plot_v1" H 8200 3400 60  0000 C CNN
F 2 "" H 8000 3050 60  0000 C CNN
F 3 "" H 8000 3050 60  0000 C CNN
	1    8000 3050
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U7
U 1 1 685A72F3
P 6450 3050
F 0 "U7" H 6450 3550 60  0000 C CNN
F 1 "plot_v1" H 6650 3400 60  0000 C CNN
F 2 "" H 6450 3050 60  0000 C CNN
F 3 "" H 6450 3050 60  0000 C CNN
	1    6450 3050
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U6
U 1 1 685A7358
P 6200 3050
F 0 "U6" H 6200 3550 60  0000 C CNN
F 1 "plot_v1" H 6400 3400 60  0000 C CNN
F 2 "" H 6200 3050 60  0000 C CNN
F 3 "" H 6200 3050 60  0000 C CNN
	1    6200 3050
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U5
U 1 1 685A740A
P 5950 3050
F 0 "U5" H 5950 3550 60  0000 C CNN
F 1 "plot_v1" H 6150 3400 60  0000 C CNN
F 2 "" H 5950 3050 60  0000 C CNN
F 3 "" H 5950 3050 60  0000 C CNN
	1    5950 3050
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U4
U 1 1 685A93C0
P 5700 3050
F 0 "U4" H 5700 3550 60  0000 C CNN
F 1 "plot_v1" H 5900 3400 60  0000 C CNN
F 2 "" H 5700 3050 60  0000 C CNN
F 3 "" H 5700 3050 60  0000 C CNN
	1    5700 3050
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U3
U 1 1 685A942A
P 5400 3050
F 0 "U3" H 5400 3550 60  0000 C CNN
F 1 "plot_v1" H 5600 3400 60  0000 C CNN
F 2 "" H 5400 3050 60  0000 C CNN
F 3 "" H 5400 3050 60  0000 C CNN
	1    5400 3050
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U2
U 1 1 685A9495
P 5150 3050
F 0 "U2" H 5150 3550 60  0000 C CNN
F 1 "plot_v1" H 5350 3400 60  0000 C CNN
F 2 "" H 5150 3050 60  0000 C CNN
F 3 "" H 5150 3050 60  0000 C CNN
	1    5150 3050
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U1
U 1 1 685A9509
P 4900 3050
F 0 "U1" H 4900 3550 60  0000 C CNN
F 1 "plot_v1" H 5100 3400 60  0000 C CNN
F 2 "" H 4900 3050 60  0000 C CNN
F 3 "" H 4900 3050 60  0000 C CNN
	1    4900 3050
	1    0    0    -1  
$EndComp
Text GLabel 4800 2900 0    60   Input ~ 0
I0
Text GLabel 4800 3050 0    60   Input ~ 0
I1
Text GLabel 4800 3200 0    60   Input ~ 0
I2
Text GLabel 4800 3350 0    60   Input ~ 0
I3
Text GLabel 4800 3500 0    60   Input ~ 0
I4
Text GLabel 4800 3650 0    60   Input ~ 0
I5
Text GLabel 4800 3800 0    60   Input ~ 0
I6
Text GLabel 4800 3950 0    60   Input ~ 0
I7
Text GLabel 4800 4100 0    60   Input ~ 0
I8
Text GLabel 4800 4250 0    60   Input ~ 0
I9
Text GLabel 4800 4400 0    60   Input ~ 0
I10
Text GLabel 4800 4550 0    60   Input ~ 0
I11
Text GLabel 4800 4700 0    60   Input ~ 0
I12
Wire Wire Line
	10000 5800 10250 5800
Wire Wire Line
	10000 5900 10250 5900
Wire Wire Line
	10000 6000 10250 6000
Wire Wire Line
	10000 6100 10250 6100
Wire Wire Line
	10000 6200 10250 6200
Wire Wire Line
	10000 6300 10250 6300
Wire Wire Line
	10000 6400 10250 6400
Wire Wire Line
	10000 6500 10250 6500
Wire Wire Line
	9950 7100 9950 6600
Wire Wire Line
	9950 6600 10250 6600
Wire Wire Line
	9950 7200 10100 7200
Wire Wire Line
	10100 7200 10100 6700
Wire Wire Line
	9950 7300 10150 7300
Wire Wire Line
	10150 7300 10150 6800
Wire Wire Line
	9950 7400 10200 7400
Wire Wire Line
	10200 7400 10200 6900
Wire Wire Line
	9950 7500 10250 7500
Wire Wire Line
	10250 7500 10250 7000
Wire Wire Line
	10200 6900 10250 6900
Wire Wire Line
	10150 6800 10250 6800
Wire Wire Line
	10100 6700 10250 6700
Wire Wire Line
	11450 6200 11700 6200
Wire Wire Line
	12850 6200 13400 6200
Wire Wire Line
	4250 4900 8850 4900
Wire Wire Line
	8850 4900 8850 5800
Wire Wire Line
	4250 5250 8800 5250
Wire Wire Line
	8800 5250 8800 5900
Wire Wire Line
	8800 5900 8850 5900
Wire Wire Line
	4250 5600 8750 5600
Wire Wire Line
	8750 5600 8750 6000
Wire Wire Line
	8750 6000 8850 6000
Wire Wire Line
	4250 5950 8700 5950
Wire Wire Line
	8700 5950 8700 6100
Wire Wire Line
	8700 6100 8850 6100
Wire Wire Line
	4250 6300 8700 6300
Wire Wire Line
	8700 6300 8700 6200
Wire Wire Line
	8700 6200 8850 6200
Wire Wire Line
	4250 6650 8750 6650
Wire Wire Line
	8750 6650 8750 6300
Wire Wire Line
	8750 6300 8850 6300
Wire Wire Line
	4250 7000 8800 7000
Wire Wire Line
	8800 7000 8800 6400
Wire Wire Line
	8800 6400 8850 6400
Wire Wire Line
	4250 7400 8200 7400
Wire Wire Line
	8200 7400 8200 6500
Wire Wire Line
	8200 6500 8850 6500
Wire Wire Line
	4250 7800 8300 7800
Wire Wire Line
	8300 7800 8300 7100
Wire Wire Line
	4250 8150 8450 8150
Wire Wire Line
	8450 8150 8450 7200
Wire Wire Line
	8300 7100 8800 7100
Wire Wire Line
	8450 7200 8800 7200
Wire Wire Line
	4250 8550 8600 8550
Wire Wire Line
	8600 8550 8600 7300
Wire Wire Line
	8600 7300 8800 7300
Wire Wire Line
	4250 8950 8700 8950
Wire Wire Line
	8700 8950 8700 7400
Wire Wire Line
	8700 7400 8800 7400
Wire Wire Line
	4250 9300 8800 9300
Wire Wire Line
	8800 9300 8800 7500
Wire Wire Line
	3350 4900 3350 5000
Wire Wire Line
	3350 5250 3350 5350
Wire Wire Line
	3350 5600 3350 5700
Wire Wire Line
	3350 5950 3350 6050
Wire Wire Line
	3350 6300 3350 6400
Wire Wire Line
	3350 6650 3350 6750
Wire Wire Line
	3350 7000 3350 7100
Wire Wire Line
	3350 7400 3350 7500
Wire Wire Line
	3350 7800 3350 7900
Wire Wire Line
	3350 8150 3350 8250
Wire Wire Line
	3350 8550 3350 8650
Wire Wire Line
	3350 8950 3350 9050
Wire Wire Line
	3350 9300 3350 9400
Wire Wire Line
	4900 2850 4900 4900
Connection ~ 4900 4900
Wire Wire Line
	5150 2850 5150 5250
Connection ~ 5150 5250
Wire Wire Line
	5400 2850 5400 5600
Connection ~ 5400 5600
Wire Wire Line
	5700 2850 5700 5950
Connection ~ 5700 5950
Wire Wire Line
	5950 2850 5950 6300
Connection ~ 5950 6300
Wire Wire Line
	6200 2850 6200 6650
Connection ~ 6200 6650
Wire Wire Line
	6450 2850 6450 7000
Connection ~ 6450 7000
Wire Wire Line
	6700 2850 6700 7400
Connection ~ 6700 7400
Wire Wire Line
	7000 2850 7000 7800
Connection ~ 7000 7800
Wire Wire Line
	7250 2850 7250 8150
Connection ~ 7250 8150
Wire Wire Line
	7500 2850 7500 8550
Connection ~ 7500 8550
Wire Wire Line
	7750 2850 7750 8950
Connection ~ 7750 8950
Wire Wire Line
	8000 2850 8000 9300
Connection ~ 8000 9300
Wire Wire Line
	4800 2900 4900 2900
Connection ~ 4900 2900
Wire Wire Line
	4800 3050 5150 3050
Connection ~ 5150 3050
Wire Wire Line
	4800 3200 5400 3200
Connection ~ 5400 3200
Wire Wire Line
	4800 3350 5700 3350
Connection ~ 5700 3350
Wire Wire Line
	4800 3500 5950 3500
Connection ~ 5950 3500
Wire Wire Line
	4800 3650 6200 3650
Connection ~ 6200 3650
Wire Wire Line
	4800 3800 6450 3800
Connection ~ 6450 3800
Wire Wire Line
	4800 3950 6700 3950
Connection ~ 6700 3950
Wire Wire Line
	4800 4100 7000 4100
Connection ~ 7000 4100
Wire Wire Line
	4800 4250 7250 4250
Connection ~ 7250 4250
Wire Wire Line
	4800 4400 7500 4400
Connection ~ 7500 4400
Wire Wire Line
	4800 4550 7750 4550
Connection ~ 7750 4550
Wire Wire Line
	4800 4700 8000 4700
Connection ~ 8000 4700
Text GLabel 13100 5800 1    60   Input ~ 0
OUT
Wire Wire Line
	13100 5800 13100 6200
Connection ~ 13100 6200
$EndSCHEMATC
