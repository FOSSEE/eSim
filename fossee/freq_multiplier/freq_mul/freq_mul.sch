EESchema Schematic File Version 2
LIBS:freq_mul-rescue
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
LIBS:freq_mul-cache
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
L adc_bridge_1 U4
U 1 1 69A5B907
P 4100 3350
F 0 "U4" H 4100 3350 60  0000 C CNN
F 1 "adc_bridge_1" H 4100 3500 60  0000 C CNN
F 2 "" H 4100 3350 60  0000 C CNN
F 3 "" H 4100 3350 60  0000 C CNN
	1    4100 3350
	1    0    0    -1  
$EndComp
$Comp
L dac_bridge_1 U6
U 1 1 69A5B9A8
P 7550 3350
F 0 "U6" H 7550 3350 60  0000 C CNN
F 1 "dac_bridge_1" H 7550 3500 60  0000 C CNN
F 2 "" H 7550 3350 60  0000 C CNN
F 3 "" H 7550 3350 60  0000 C CNN
	1    7550 3350
	1    0    0    -1  
$EndComp
$Comp
L pulse v1
U 1 1 69A5BA13
P 1950 3350
F 0 "v1" H 1750 3450 60  0000 C CNN
F 1 "pulse" H 1750 3300 60  0000 C CNN
F 2 "R1" H 1650 3350 60  0000 C CNN
F 3 "" H 1950 3350 60  0000 C CNN
	1    1950 3350
	0    1    1    0   
$EndComp
$Comp
L GND #PWR01
U 1 1 69A5BA88
P 1300 3650
F 0 "#PWR01" H 1300 3400 50  0001 C CNN
F 1 "GND" H 1300 3500 50  0000 C CNN
F 2 "" H 1300 3650 50  0001 C CNN
F 3 "" H 1300 3650 50  0001 C CNN
	1    1300 3650
	1    0    0    -1  
$EndComp
$Comp
L PWR_FLAG #FLG02
U 1 1 69A5BAA4
P 1150 3200
F 0 "#FLG02" H 1150 3275 50  0001 C CNN
F 1 "PWR_FLAG" H 1150 3350 50  0000 C CNN
F 2 "" H 1150 3200 50  0001 C CNN
F 3 "" H 1150 3200 50  0001 C CNN
	1    1150 3200
	1    0    0    -1  
$EndComp
Wire Wire Line
	1500 3350 1300 3350
Wire Wire Line
	1300 3200 1300 3650
Wire Wire Line
	1150 3200 1300 3200
Connection ~ 1300 3350
Wire Wire Line
	2400 3350 3500 3350
Wire Wire Line
	3500 3350 3500 3300
Wire Wire Line
	4650 3300 5100 3300
Wire Wire Line
	6500 3300 6950 3300
$Comp
L plot_db U7
U 1 1 69A5BAF2
P 8800 3450
F 0 "U7" H 8800 3950 60  0000 C CNN
F 1 "plot_db" H 9000 3800 60  0000 C CNN
F 2 "" H 8800 3450 60  0000 C CNN
F 3 "" H 8800 3450 60  0000 C CNN
	1    8800 3450
	1    0    0    -1  
$EndComp
$Comp
L plot_db U1
U 1 1 69A5BB1D
P 2800 3400
F 0 "U1" H 2800 3900 60  0000 C CNN
F 1 "plot_db" H 3000 3750 60  0000 C CNN
F 2 "" H 2800 3400 60  0000 C CNN
F 3 "" H 2800 3400 60  0000 C CNN
	1    2800 3400
	1    0    0    -1  
$EndComp
Wire Wire Line
	2800 3200 2800 3350
Connection ~ 2800 3350
Wire Wire Line
	8100 3300 8500 3300
Wire Wire Line
	8500 3300 8500 3250
$Comp
L freq_mul U2
U 1 1 69A5BD31
P 2950 5200
F 0 "U2" H 5800 7000 60  0000 C CNN
F 1 "freq_mul" H 5800 7200 60  0000 C CNN
F 2 "" H 5800 7150 60  0000 C CNN
F 3 "" H 5800 7150 60  0000 C CNN
	1    2950 5200
	1    0    0    -1  
$EndComp
$Comp
L adc_bridge_1 U5
U 1 1 69A5BE69
P 4450 4400
F 0 "U5" H 4450 4400 60  0000 C CNN
F 1 "adc_bridge_1" H 4450 4550 60  0000 C CNN
F 2 "" H 4450 4400 60  0000 C CNN
F 3 "" H 4450 4400 60  0000 C CNN
	1    4450 4400
	1    0    0    -1  
$EndComp
$Comp
L pulse v2
U 1 1 69A5BE70
P 2300 4400
F 0 "v2" H 2100 4500 60  0000 C CNN
F 1 "pulse" H 2100 4350 60  0000 C CNN
F 2 "R1" H 2000 4400 60  0000 C CNN
F 3 "" H 2300 4400 60  0000 C CNN
	1    2300 4400
	0    1    1    0   
$EndComp
$Comp
L GND #PWR03
U 1 1 69A5BE77
P 1650 4700
F 0 "#PWR03" H 1650 4450 50  0001 C CNN
F 1 "GND" H 1650 4550 50  0000 C CNN
F 2 "" H 1650 4700 50  0001 C CNN
F 3 "" H 1650 4700 50  0001 C CNN
	1    1650 4700
	1    0    0    -1  
$EndComp
$Comp
L PWR_FLAG #FLG04
U 1 1 69A5BE7D
P 1500 4250
F 0 "#FLG04" H 1500 4325 50  0001 C CNN
F 1 "PWR_FLAG" H 1500 4400 50  0000 C CNN
F 2 "" H 1500 4250 50  0001 C CNN
F 3 "" H 1500 4250 50  0001 C CNN
	1    1500 4250
	1    0    0    -1  
$EndComp
Wire Wire Line
	1850 4400 1650 4400
Wire Wire Line
	1650 4250 1650 4700
Wire Wire Line
	1500 4250 1650 4250
Connection ~ 1650 4400
Wire Wire Line
	2750 4400 3850 4400
Wire Wire Line
	3850 4400 3850 4350
$Comp
L plot_db U3
U 1 1 69A5BE89
P 3150 4450
F 0 "U3" H 3150 4950 60  0000 C CNN
F 1 "plot_db" H 3350 4800 60  0000 C CNN
F 2 "" H 3150 4450 60  0000 C CNN
F 3 "" H 3150 4450 60  0000 C CNN
	1    3150 4450
	1    0    0    -1  
$EndComp
Wire Wire Line
	3150 4250 3150 4400
Connection ~ 3150 4400
Wire Wire Line
	5000 4350 5000 3450
Wire Wire Line
	5000 3450 5100 3450
Wire Wire Line
	5100 3450 5100 3400
Text GLabel 3250 3350 1    60   Input ~ 0
clki
Text GLabel 3700 4400 1    60   Input ~ 0
rst0
Text GLabel 8350 3300 1    60   Input ~ 0
clkout
Wire Wire Line
	8500 3250 8800 3250
$EndSCHEMATC
