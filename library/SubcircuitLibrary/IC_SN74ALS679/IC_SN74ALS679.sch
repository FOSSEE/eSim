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
L SN74ALS679 X1
U 1 1 68661CB6
P 8500 5500
F 0 "X1" H 8600 4050 60  0000 C CNN
F 1 "SN74ALS679" H 8350 6500 60  0000 C CNN
F 2 "" H 8500 5500 60  0001 C CNN
F 3 "" H 8500 5500 60  0001 C CNN
	1    8500 5500
	1    0    0    -1  
$EndComp
$Comp
L adc_bridge_8 U21
U 1 1 68661D16
P 6900 4700
F 0 "U21" H 6900 4700 60  0000 C CNN
F 1 "adc_bridge_8" H 6900 4850 60  0000 C CNN
F 2 "" H 6900 4700 60  0000 C CNN
F 3 "" H 6900 4700 60  0000 C CNN
	1    6900 4700
	1    0    0    -1  
$EndComp
$Comp
L adc_bridge_4 U19
U 1 1 68661D59
P 6850 6600
F 0 "U19" H 6850 6600 60  0000 C CNN
F 1 "adc_bridge_4" H 6850 6900 60  0000 C CNN
F 2 "" H 6850 6600 60  0000 C CNN
F 3 "" H 6850 6600 60  0000 C CNN
	1    6850 6600
	1    0    0    -1  
$EndComp
$Comp
L adc_bridge_1 U20
U 1 1 68661DB5
P 6850 7250
F 0 "U20" H 6850 7250 60  0000 C CNN
F 1 "adc_bridge_1" H 6850 7400 60  0000 C CNN
F 2 "" H 6850 7250 60  0000 C CNN
F 3 "" H 6850 7250 60  0000 C CNN
	1    6850 7250
	1    0    0    -1  
$EndComp
$Comp
L adc_bridge_4 U18
U 1 1 68661DEE
P 6850 5900
F 0 "U18" H 6850 5900 60  0000 C CNN
F 1 "adc_bridge_4" H 6850 6200 60  0000 C CNN
F 2 "" H 6850 5900 60  0000 C CNN
F 3 "" H 6850 5900 60  0000 C CNN
	1    6850 5900
	1    0    0    -1  
$EndComp
$Comp
L pulse v1
U 1 1 68662002
P 1150 3050
F 0 "v1" H 950 3150 60  0000 C CNN
F 1 "pulse" H 950 3000 60  0000 C CNN
F 2 "R1" H 850 3050 60  0000 C CNN
F 3 "" H 1150 3050 60  0000 C CNN
	1    1150 3050
	0    1    1    0   
$EndComp
$Comp
L pulse v2
U 1 1 6866209F
P 1150 3400
F 0 "v2" H 950 3500 60  0000 C CNN
F 1 "pulse" H 950 3350 60  0000 C CNN
F 2 "R1" H 850 3400 60  0000 C CNN
F 3 "" H 1150 3400 60  0000 C CNN
	1    1150 3400
	0    1    1    0   
$EndComp
$Comp
L pulse v3
U 1 1 686620DA
P 1150 3750
F 0 "v3" H 950 3850 60  0000 C CNN
F 1 "pulse" H 950 3700 60  0000 C CNN
F 2 "R1" H 850 3750 60  0000 C CNN
F 3 "" H 1150 3750 60  0000 C CNN
	1    1150 3750
	0    1    1    0   
$EndComp
$Comp
L pulse v4
U 1 1 68662118
P 1150 4100
F 0 "v4" H 950 4200 60  0000 C CNN
F 1 "pulse" H 950 4050 60  0000 C CNN
F 2 "R1" H 850 4100 60  0000 C CNN
F 3 "" H 1150 4100 60  0000 C CNN
	1    1150 4100
	0    1    1    0   
$EndComp
$Comp
L pulse v5
U 1 1 68662159
P 1150 4450
F 0 "v5" H 950 4550 60  0000 C CNN
F 1 "pulse" H 950 4400 60  0000 C CNN
F 2 "R1" H 850 4450 60  0000 C CNN
F 3 "" H 1150 4450 60  0000 C CNN
	1    1150 4450
	0    1    1    0   
$EndComp
$Comp
L pulse v6
U 1 1 68662191
P 1150 4800
F 0 "v6" H 950 4900 60  0000 C CNN
F 1 "pulse" H 950 4750 60  0000 C CNN
F 2 "R1" H 850 4800 60  0000 C CNN
F 3 "" H 1150 4800 60  0000 C CNN
	1    1150 4800
	0    1    1    0   
$EndComp
$Comp
L pulse v7
U 1 1 686621D0
P 1150 5150
F 0 "v7" H 950 5250 60  0000 C CNN
F 1 "pulse" H 950 5100 60  0000 C CNN
F 2 "R1" H 850 5150 60  0000 C CNN
F 3 "" H 1150 5150 60  0000 C CNN
	1    1150 5150
	0    1    1    0   
$EndComp
$Comp
L pulse v8
U 1 1 68662232
P 1150 5500
F 0 "v8" H 950 5600 60  0000 C CNN
F 1 "pulse" H 950 5450 60  0000 C CNN
F 2 "R1" H 850 5500 60  0000 C CNN
F 3 "" H 1150 5500 60  0000 C CNN
	1    1150 5500
	0    1    1    0   
$EndComp
$Comp
L pulse v9
U 1 1 6866227F
P 1150 5850
F 0 "v9" H 950 5950 60  0000 C CNN
F 1 "pulse" H 950 5800 60  0000 C CNN
F 2 "R1" H 850 5850 60  0000 C CNN
F 3 "" H 1150 5850 60  0000 C CNN
	1    1150 5850
	0    1    1    0   
$EndComp
$Comp
L pulse v10
U 1 1 686622CF
P 1150 6200
F 0 "v10" H 950 6300 60  0000 C CNN
F 1 "pulse" H 950 6150 60  0000 C CNN
F 2 "R1" H 850 6200 60  0000 C CNN
F 3 "" H 1150 6200 60  0000 C CNN
	1    1150 6200
	0    1    1    0   
$EndComp
$Comp
L pulse v11
U 1 1 68662322
P 1150 6550
F 0 "v11" H 950 6650 60  0000 C CNN
F 1 "pulse" H 950 6500 60  0000 C CNN
F 2 "R1" H 850 6550 60  0000 C CNN
F 3 "" H 1150 6550 60  0000 C CNN
	1    1150 6550
	0    1    1    0   
$EndComp
$Comp
L pulse v12
U 1 1 6866236C
P 1150 6900
F 0 "v12" H 950 7000 60  0000 C CNN
F 1 "pulse" H 950 6850 60  0000 C CNN
F 2 "R1" H 850 6900 60  0000 C CNN
F 3 "" H 1150 6900 60  0000 C CNN
	1    1150 6900
	0    1    1    0   
$EndComp
$Comp
L pulse v13
U 1 1 68663B2A
P 1150 7350
F 0 "v13" H 950 7450 60  0000 C CNN
F 1 "pulse" H 950 7300 60  0000 C CNN
F 2 "R1" H 850 7350 60  0000 C CNN
F 3 "" H 1150 7350 60  0000 C CNN
	1    1150 7350
	0    1    1    0   
$EndComp
$Comp
L pulse v14
U 1 1 68663B82
P 1150 7700
F 0 "v14" H 950 7800 60  0000 C CNN
F 1 "pulse" H 950 7650 60  0000 C CNN
F 2 "R1" H 850 7700 60  0000 C CNN
F 3 "" H 1150 7700 60  0000 C CNN
	1    1150 7700
	0    1    1    0   
$EndComp
$Comp
L pulse v15
U 1 1 68663BD5
P 1150 8050
F 0 "v15" H 950 8150 60  0000 C CNN
F 1 "pulse" H 950 8000 60  0000 C CNN
F 2 "R1" H 850 8050 60  0000 C CNN
F 3 "" H 1150 8050 60  0000 C CNN
	1    1150 8050
	0    1    1    0   
$EndComp
$Comp
L pulse v16
U 1 1 68663C88
P 1150 8400
F 0 "v16" H 950 8500 60  0000 C CNN
F 1 "pulse" H 950 8350 60  0000 C CNN
F 2 "R1" H 850 8400 60  0000 C CNN
F 3 "" H 1150 8400 60  0000 C CNN
	1    1150 8400
	0    1    1    0   
$EndComp
$Comp
L pulse v17
U 1 1 68663CD6
P 1150 8750
F 0 "v17" H 950 8850 60  0000 C CNN
F 1 "pulse" H 950 8700 60  0000 C CNN
F 2 "R1" H 850 8750 60  0000 C CNN
F 3 "" H 1150 8750 60  0000 C CNN
	1    1150 8750
	0    1    1    0   
$EndComp
$Comp
L GND #PWR01
U 1 1 6866426A
P 700 3150
F 0 "#PWR01" H 700 2900 50  0001 C CNN
F 1 "GND" H 700 3000 50  0000 C CNN
F 2 "" H 700 3150 50  0001 C CNN
F 3 "" H 700 3150 50  0001 C CNN
	1    700  3150
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR02
U 1 1 686642BE
P 700 3500
F 0 "#PWR02" H 700 3250 50  0001 C CNN
F 1 "GND" H 700 3350 50  0000 C CNN
F 2 "" H 700 3500 50  0001 C CNN
F 3 "" H 700 3500 50  0001 C CNN
	1    700  3500
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR03
U 1 1 6866430B
P 700 3850
F 0 "#PWR03" H 700 3600 50  0001 C CNN
F 1 "GND" H 700 3700 50  0000 C CNN
F 2 "" H 700 3850 50  0001 C CNN
F 3 "" H 700 3850 50  0001 C CNN
	1    700  3850
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR04
U 1 1 68664358
P 700 4200
F 0 "#PWR04" H 700 3950 50  0001 C CNN
F 1 "GND" H 700 4050 50  0000 C CNN
F 2 "" H 700 4200 50  0001 C CNN
F 3 "" H 700 4200 50  0001 C CNN
	1    700  4200
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR05
U 1 1 686643A5
P 700 4550
F 0 "#PWR05" H 700 4300 50  0001 C CNN
F 1 "GND" H 700 4400 50  0000 C CNN
F 2 "" H 700 4550 50  0001 C CNN
F 3 "" H 700 4550 50  0001 C CNN
	1    700  4550
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR06
U 1 1 686643F2
P 700 4900
F 0 "#PWR06" H 700 4650 50  0001 C CNN
F 1 "GND" H 700 4750 50  0000 C CNN
F 2 "" H 700 4900 50  0001 C CNN
F 3 "" H 700 4900 50  0001 C CNN
	1    700  4900
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR07
U 1 1 6866443F
P 700 5250
F 0 "#PWR07" H 700 5000 50  0001 C CNN
F 1 "GND" H 700 5100 50  0000 C CNN
F 2 "" H 700 5250 50  0001 C CNN
F 3 "" H 700 5250 50  0001 C CNN
	1    700  5250
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR08
U 1 1 686644FA
P 700 5600
F 0 "#PWR08" H 700 5350 50  0001 C CNN
F 1 "GND" H 700 5450 50  0000 C CNN
F 2 "" H 700 5600 50  0001 C CNN
F 3 "" H 700 5600 50  0001 C CNN
	1    700  5600
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR09
U 1 1 68664547
P 700 5950
F 0 "#PWR09" H 700 5700 50  0001 C CNN
F 1 "GND" H 700 5800 50  0000 C CNN
F 2 "" H 700 5950 50  0001 C CNN
F 3 "" H 700 5950 50  0001 C CNN
	1    700  5950
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR010
U 1 1 68664594
P 700 6300
F 0 "#PWR010" H 700 6050 50  0001 C CNN
F 1 "GND" H 700 6150 50  0000 C CNN
F 2 "" H 700 6300 50  0001 C CNN
F 3 "" H 700 6300 50  0001 C CNN
	1    700  6300
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR011
U 1 1 686645E1
P 700 6650
F 0 "#PWR011" H 700 6400 50  0001 C CNN
F 1 "GND" H 700 6500 50  0000 C CNN
F 2 "" H 700 6650 50  0001 C CNN
F 3 "" H 700 6650 50  0001 C CNN
	1    700  6650
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR012
U 1 1 6866469C
P 700 7000
F 0 "#PWR012" H 700 6750 50  0001 C CNN
F 1 "GND" H 700 6850 50  0000 C CNN
F 2 "" H 700 7000 50  0001 C CNN
F 3 "" H 700 7000 50  0001 C CNN
	1    700  7000
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR013
U 1 1 686646E9
P 700 7450
F 0 "#PWR013" H 700 7200 50  0001 C CNN
F 1 "GND" H 700 7300 50  0000 C CNN
F 2 "" H 700 7450 50  0001 C CNN
F 3 "" H 700 7450 50  0001 C CNN
	1    700  7450
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR014
U 1 1 6866478E
P 700 7800
F 0 "#PWR014" H 700 7550 50  0001 C CNN
F 1 "GND" H 700 7650 50  0000 C CNN
F 2 "" H 700 7800 50  0001 C CNN
F 3 "" H 700 7800 50  0001 C CNN
	1    700  7800
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR015
U 1 1 686647DB
P 700 8150
F 0 "#PWR015" H 700 7900 50  0001 C CNN
F 1 "GND" H 700 8000 50  0000 C CNN
F 2 "" H 700 8150 50  0001 C CNN
F 3 "" H 700 8150 50  0001 C CNN
	1    700  8150
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR016
U 1 1 68664896
P 700 8500
F 0 "#PWR016" H 700 8250 50  0001 C CNN
F 1 "GND" H 700 8350 50  0000 C CNN
F 2 "" H 700 8500 50  0001 C CNN
F 3 "" H 700 8500 50  0001 C CNN
	1    700  8500
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR017
U 1 1 686648E3
P 700 8850
F 0 "#PWR017" H 700 8600 50  0001 C CNN
F 1 "GND" H 700 8700 50  0000 C CNN
F 2 "" H 700 8850 50  0001 C CNN
F 3 "" H 700 8850 50  0001 C CNN
	1    700  8850
	1    0    0    -1  
$EndComp
$Comp
L dac_bridge_1 U22
U 1 1 68665549
P 10300 5600
F 0 "U22" H 10300 5600 60  0000 C CNN
F 1 "dac_bridge_1" H 10300 5750 60  0000 C CNN
F 2 "" H 10300 5600 60  0000 C CNN
F 3 "" H 10300 5600 60  0000 C CNN
	1    10300 5600
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U23
U 1 1 6866569A
P 11200 5550
F 0 "U23" H 11200 6050 60  0000 C CNN
F 1 "plot_v1" H 11400 5900 60  0000 C CNN
F 2 "" H 11200 5550 60  0000 C CNN
F 3 "" H 11200 5550 60  0000 C CNN
	1    11200 5550
	0    1    1    0   
$EndComp
Text GLabel 11100 5150 1    60   Input ~ 0
Y
$Comp
L plot_v1 U1
U 1 1 686659F6
P 1650 1150
F 0 "U1" H 1650 1650 60  0000 C CNN
F 1 "plot_v1" H 1850 1500 60  0000 C CNN
F 2 "" H 1650 1150 60  0000 C CNN
F 3 "" H 1650 1150 60  0000 C CNN
	1    1650 1150
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U2
U 1 1 68665BD6
P 1900 1150
F 0 "U2" H 1900 1650 60  0000 C CNN
F 1 "plot_v1" H 2100 1500 60  0000 C CNN
F 2 "" H 1900 1150 60  0000 C CNN
F 3 "" H 1900 1150 60  0000 C CNN
	1    1900 1150
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U3
U 1 1 68665C3E
P 2150 1150
F 0 "U3" H 2150 1650 60  0000 C CNN
F 1 "plot_v1" H 2350 1500 60  0000 C CNN
F 2 "" H 2150 1150 60  0000 C CNN
F 3 "" H 2150 1150 60  0000 C CNN
	1    2150 1150
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U4
U 1 1 68665CA5
P 2400 1150
F 0 "U4" H 2400 1650 60  0000 C CNN
F 1 "plot_v1" H 2600 1500 60  0000 C CNN
F 2 "" H 2400 1150 60  0000 C CNN
F 3 "" H 2400 1150 60  0000 C CNN
	1    2400 1150
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U5
U 1 1 68665D71
P 2650 1150
F 0 "U5" H 2650 1650 60  0000 C CNN
F 1 "plot_v1" H 2850 1500 60  0000 C CNN
F 2 "" H 2650 1150 60  0000 C CNN
F 3 "" H 2650 1150 60  0000 C CNN
	1    2650 1150
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U6
U 1 1 68665DE2
P 2900 1150
F 0 "U6" H 2900 1650 60  0000 C CNN
F 1 "plot_v1" H 3100 1500 60  0000 C CNN
F 2 "" H 2900 1150 60  0000 C CNN
F 3 "" H 2900 1150 60  0000 C CNN
	1    2900 1150
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U7
U 1 1 68665E52
P 3150 1150
F 0 "U7" H 3150 1650 60  0000 C CNN
F 1 "plot_v1" H 3350 1500 60  0000 C CNN
F 2 "" H 3150 1150 60  0000 C CNN
F 3 "" H 3150 1150 60  0000 C CNN
	1    3150 1150
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U8
U 1 1 68665EC9
P 3400 1150
F 0 "U8" H 3400 1650 60  0000 C CNN
F 1 "plot_v1" H 3600 1500 60  0000 C CNN
F 2 "" H 3400 1150 60  0000 C CNN
F 3 "" H 3400 1150 60  0000 C CNN
	1    3400 1150
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U9
U 1 1 68665F3F
P 3650 1150
F 0 "U9" H 3650 1650 60  0000 C CNN
F 1 "plot_v1" H 3850 1500 60  0000 C CNN
F 2 "" H 3650 1150 60  0000 C CNN
F 3 "" H 3650 1150 60  0000 C CNN
	1    3650 1150
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U10
U 1 1 68665FBC
P 3900 1150
F 0 "U10" H 3900 1650 60  0000 C CNN
F 1 "plot_v1" H 4100 1500 60  0000 C CNN
F 2 "" H 3900 1150 60  0000 C CNN
F 3 "" H 3900 1150 60  0000 C CNN
	1    3900 1150
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U11
U 1 1 6866603C
P 4150 1150
F 0 "U11" H 4150 1650 60  0000 C CNN
F 1 "plot_v1" H 4350 1500 60  0000 C CNN
F 2 "" H 4150 1150 60  0000 C CNN
F 3 "" H 4150 1150 60  0000 C CNN
	1    4150 1150
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U12
U 1 1 686660BB
P 4400 1150
F 0 "U12" H 4400 1650 60  0000 C CNN
F 1 "plot_v1" H 4600 1500 60  0000 C CNN
F 2 "" H 4400 1150 60  0000 C CNN
F 3 "" H 4400 1150 60  0000 C CNN
	1    4400 1150
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U13
U 1 1 68666141
P 4700 1150
F 0 "U13" H 4700 1650 60  0000 C CNN
F 1 "plot_v1" H 4900 1500 60  0000 C CNN
F 2 "" H 4700 1150 60  0000 C CNN
F 3 "" H 4700 1150 60  0000 C CNN
	1    4700 1150
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U14
U 1 1 686661D0
P 4950 1150
F 0 "U14" H 4950 1650 60  0000 C CNN
F 1 "plot_v1" H 5150 1500 60  0000 C CNN
F 2 "" H 4950 1150 60  0000 C CNN
F 3 "" H 4950 1150 60  0000 C CNN
	1    4950 1150
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U15
U 1 1 68666260
P 5200 1150
F 0 "U15" H 5200 1650 60  0000 C CNN
F 1 "plot_v1" H 5400 1500 60  0000 C CNN
F 2 "" H 5200 1150 60  0000 C CNN
F 3 "" H 5200 1150 60  0000 C CNN
	1    5200 1150
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U16
U 1 1 686662EF
P 5450 1150
F 0 "U16" H 5450 1650 60  0000 C CNN
F 1 "plot_v1" H 5650 1500 60  0000 C CNN
F 2 "" H 5450 1150 60  0000 C CNN
F 3 "" H 5450 1150 60  0000 C CNN
	1    5450 1150
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U17
U 1 1 6866637D
P 5750 1150
F 0 "U17" H 5750 1650 60  0000 C CNN
F 1 "plot_v1" H 5950 1500 60  0000 C CNN
F 2 "" H 5750 1150 60  0000 C CNN
F 3 "" H 5750 1150 60  0000 C CNN
	1    5750 1150
	1    0    0    -1  
$EndComp
Wire Wire Line
	7450 4650 7800 4650
Wire Wire Line
	7800 4750 7450 4750
Wire Wire Line
	7800 4850 7450 4850
Wire Wire Line
	7800 4950 7450 4950
Wire Wire Line
	7800 5050 7450 5050
Wire Wire Line
	7800 5150 7450 5150
Wire Wire Line
	7800 5250 7450 5250
Wire Wire Line
	7450 5350 7800 5350
Wire Wire Line
	7400 5700 7400 5450
Wire Wire Line
	7400 5450 7800 5450
Wire Wire Line
	7400 5800 7500 5800
Wire Wire Line
	7500 5800 7500 5650
Wire Wire Line
	7500 5650 7800 5650
Wire Wire Line
	7800 5750 7550 5750
Wire Wire Line
	7550 5750 7550 5900
Wire Wire Line
	7550 5900 7400 5900
Wire Wire Line
	7400 6000 7600 6000
Wire Wire Line
	7600 6000 7600 5850
Wire Wire Line
	7600 5850 7800 5850
Wire Wire Line
	7400 6400 7400 6350
Wire Wire Line
	7400 6350 7800 6350
Wire Wire Line
	7400 6500 7800 6500
Wire Wire Line
	7400 6600 7800 6600
Wire Wire Line
	7800 6600 7800 6650
Wire Wire Line
	7400 6700 7400 6800
Wire Wire Line
	7400 6800 7800 6800
Wire Wire Line
	7400 7200 7400 6950
Wire Wire Line
	7400 6950 7800 6950
Wire Wire Line
	1600 3050 6300 3050
Wire Wire Line
	6300 3050 6300 4650
Wire Wire Line
	1600 3400 6150 3400
Wire Wire Line
	6150 3400 6150 4750
Wire Wire Line
	6150 4750 6300 4750
Wire Wire Line
	1600 3750 6100 3750
Wire Wire Line
	6100 3750 6100 4850
Wire Wire Line
	6100 4850 6300 4850
Wire Wire Line
	1600 4100 6000 4100
Wire Wire Line
	6000 4100 6000 4950
Wire Wire Line
	6000 4950 6300 4950
Wire Wire Line
	1600 4450 5900 4450
Wire Wire Line
	5900 4450 5900 5050
Wire Wire Line
	5900 5050 6300 5050
Wire Wire Line
	1600 4800 5800 4800
Wire Wire Line
	5800 4800 5800 5150
Wire Wire Line
	5800 5150 6300 5150
Wire Wire Line
	1600 5150 5700 5150
Wire Wire Line
	5700 5150 5700 5250
Wire Wire Line
	5700 5250 6300 5250
Wire Wire Line
	6300 5350 1600 5350
Wire Wire Line
	1600 5350 1600 5500
Wire Wire Line
	6300 5700 1600 5700
Wire Wire Line
	1600 5700 1600 5850
Wire Wire Line
	6300 5800 1650 5800
Wire Wire Line
	1650 5800 1650 6200
Wire Wire Line
	1650 6200 1600 6200
Wire Wire Line
	1750 6550 1600 6550
Wire Wire Line
	1750 5900 1750 6550
Wire Wire Line
	1750 5900 6300 5900
Wire Wire Line
	6300 6000 1850 6000
Wire Wire Line
	1850 6000 1850 6900
Wire Wire Line
	1850 6900 1600 6900
Wire Wire Line
	1600 7350 2400 7350
Wire Wire Line
	2400 7350 2400 6400
Wire Wire Line
	2400 6400 6300 6400
Wire Wire Line
	6300 6500 2500 6500
Wire Wire Line
	2500 6500 2500 7700
Wire Wire Line
	2500 7700 1600 7700
Wire Wire Line
	2650 8050 1600 8050
Wire Wire Line
	2650 6600 2650 8050
Wire Wire Line
	2650 6600 6300 6600
Wire Wire Line
	6300 6700 2800 6700
Wire Wire Line
	2800 6700 2800 8400
Wire Wire Line
	2800 8400 1600 8400
Wire Wire Line
	1600 8750 6250 8750
Wire Wire Line
	6250 8750 6250 7200
Wire Wire Line
	700  8850 700  8750
Wire Wire Line
	700  8500 700  8400
Wire Wire Line
	700  8150 700  8050
Wire Wire Line
	700  7800 700  7700
Wire Wire Line
	700  7350 700  7450
Wire Wire Line
	700  7000 700  6900
Wire Wire Line
	700  6550 700  6650
Wire Wire Line
	700  6200 700  6300
Wire Wire Line
	700  5850 700  5950
Wire Wire Line
	700  5600 700  5500
Wire Wire Line
	700  5250 700  5150
Wire Wire Line
	700  4900 700  4800
Wire Wire Line
	700  4550 700  4450
Wire Wire Line
	700  4200 700  4100
Wire Wire Line
	700  3850 700  3750
Wire Wire Line
	700  3500 700  3400
Wire Wire Line
	700  3050 700  3150
Wire Wire Line
	9700 5550 9150 5550
Wire Wire Line
	10850 5550 11400 5550
Wire Wire Line
	11100 5150 11100 5550
Connection ~ 11100 5550
Wire Wire Line
	1650 950  1650 3050
Connection ~ 1650 3050
Wire Wire Line
	1900 950  1900 3400
Connection ~ 1900 3400
Wire Wire Line
	2150 950  2150 3750
Connection ~ 2150 3750
Wire Wire Line
	2400 950  2400 4100
Connection ~ 2400 4100
Wire Wire Line
	2650 950  2650 4450
Connection ~ 2650 4450
Wire Wire Line
	2900 950  2900 4800
Connection ~ 2900 4800
Wire Wire Line
	3150 950  3150 5150
Connection ~ 3150 5150
Wire Wire Line
	3400 950  3400 5350
Connection ~ 3400 5350
Wire Wire Line
	3650 950  3650 5700
Connection ~ 3650 5700
Wire Wire Line
	3900 950  3900 5800
Connection ~ 3900 5800
Wire Wire Line
	4150 950  4150 5900
Connection ~ 4150 5900
Wire Wire Line
	4400 950  4400 6000
Connection ~ 4400 6000
Wire Wire Line
	4700 950  4700 6400
Connection ~ 4700 6400
Wire Wire Line
	4950 950  4950 6500
Connection ~ 4950 6500
Wire Wire Line
	5200 950  5200 6600
Connection ~ 5200 6600
Wire Wire Line
	5450 950  5450 6700
Connection ~ 5450 6700
Wire Wire Line
	5750 950  5750 8750
Connection ~ 5750 8750
Text GLabel 1000 1000 0    60   Input ~ 0
A1
Text GLabel 1000 1150 0    60   Input ~ 0
A2
Text GLabel 1000 1300 0    60   Input ~ 0
A3
Text GLabel 1000 1450 0    60   Input ~ 0
A4
Text GLabel 1000 1600 0    60   Input ~ 0
A5
Text GLabel 1000 1750 0    60   Input ~ 0
A6
Text GLabel 1000 1900 0    60   Input ~ 0
A7
Text GLabel 1000 2050 0    60   Input ~ 0
A8
Text GLabel 1000 2200 0    60   Input ~ 0
A9
Text GLabel 1000 2350 0    60   Input ~ 0
A10
Text GLabel 1000 2500 0    60   Input ~ 0
A11
Text GLabel 1000 2650 0    60   Input ~ 0
A12
Wire Wire Line
	1000 1000 1650 1000
Connection ~ 1650 1000
Wire Wire Line
	1000 1150 1900 1150
Connection ~ 1900 1150
Wire Wire Line
	1000 1300 2150 1300
Connection ~ 2150 1300
Wire Wire Line
	1000 1450 2400 1450
Connection ~ 2400 1450
Wire Wire Line
	1000 1600 2650 1600
Connection ~ 2650 1600
Wire Wire Line
	1000 1750 2900 1750
Connection ~ 2900 1750
Wire Wire Line
	1000 1900 3150 1900
Connection ~ 3150 1900
Wire Wire Line
	1000 2050 3400 2050
Connection ~ 3400 2050
Wire Wire Line
	1000 2200 3650 2200
Connection ~ 3650 2200
Wire Wire Line
	1000 2350 3900 2350
Connection ~ 3900 2350
Wire Wire Line
	1000 2500 4150 2500
Connection ~ 4150 2500
Wire Wire Line
	1000 2650 4400 2650
Connection ~ 4400 2650
Text GLabel 6850 1100 2    60   Input ~ 0
P0
Text GLabel 6850 1300 2    60   Input ~ 0
P1
Text GLabel 6850 1500 2    60   Input ~ 0
P2
Text GLabel 6850 1700 2    60   Input ~ 0
P3
Text GLabel 6900 1950 2    60   Input ~ 0
G
Wire Wire Line
	6850 1100 4700 1100
Connection ~ 4700 1100
Wire Wire Line
	6850 1300 4950 1300
Connection ~ 4950 1300
Wire Wire Line
	6850 1500 5200 1500
Connection ~ 5200 1500
Wire Wire Line
	6850 1700 5450 1700
Connection ~ 5450 1700
Wire Wire Line
	6900 1950 5750 1950
Connection ~ 5750 1950
$EndSCHEMATC
