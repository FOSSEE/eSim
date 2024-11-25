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
LIBS:9348-cache
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
L DC v2
U 1 1 665D8345
P 12100 9750
F 0 "v2" H 11900 9850 60  0000 C CNN
F 1 "DC" H 11900 9700 60  0000 C CNN
F 2 "R1" H 11800 9750 60  0000 C CNN
F 3 "" H 12100 9750 60  0000 C CNN
	1    12100 9750
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR01
U 1 1 665D8444
P 8450 13300
F 0 "#PWR01" H 8450 13050 50  0001 C CNN
F 1 "GND" H 8450 13150 50  0000 C CNN
F 2 "" H 8450 13300 50  0001 C CNN
F 3 "" H 8450 13300 50  0001 C CNN
	1    8450 13300
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR02
U 1 1 665D862D
P 12100 10300
F 0 "#PWR02" H 12100 10050 50  0001 C CNN
F 1 "GND" H 12100 10150 50  0000 C CNN
F 2 "" H 12100 10300 50  0001 C CNN
F 3 "" H 12100 10300 50  0001 C CNN
	1    12100 10300
	1    0    0    -1  
$EndComp
$Comp
L resistor R1
U 1 1 665D89E2
P 10850 13400
F 0 "R1" H 10900 13530 50  0000 C CNN
F 1 "1000k" H 10900 13350 50  0000 C CNN
F 2 "" H 10900 13380 30  0000 C CNN
F 3 "" V 10900 13450 30  0000 C CNN
	1    10850 13400
	0    1    1    0   
$EndComp
$Comp
L resistor R2
U 1 1 665D8A58
P 11150 13200
F 0 "R2" H 11200 13330 50  0000 C CNN
F 1 "1000k" H 11200 13150 50  0000 C CNN
F 2 "" H 11200 13180 30  0000 C CNN
F 3 "" V 11200 13250 30  0000 C CNN
	1    11150 13200
	0    1    1    0   
$EndComp
$Comp
L GND #PWR03
U 1 1 665D8B2A
P 11200 13500
F 0 "#PWR03" H 11200 13250 50  0001 C CNN
F 1 "GND" H 11200 13350 50  0000 C CNN
F 2 "" H 11200 13500 50  0001 C CNN
F 3 "" H 11200 13500 50  0001 C CNN
	1    11200 13500
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR04
U 1 1 665D8B3F
P 10900 13700
F 0 "#PWR04" H 10900 13450 50  0001 C CNN
F 1 "GND" H 10900 13550 50  0000 C CNN
F 2 "" H 10900 13700 50  0001 C CNN
F 3 "" H 10900 13700 50  0001 C CNN
	1    10900 13700
	1    0    0    -1  
$EndComp
Text GLabel 10800 13250 1    60   Input ~ 0
PO
Text GLabel 11000 13000 1    60   Input ~ 0
PE
$Comp
L 9348_IC X1
U 1 1 665D8631
P 6900 13900
F 0 "X1" H 9600 15450 60  0000 C CNN
F 1 "9348_IC" H 9650 15550 60  0000 C CNN
F 2 "" H 6900 13900 60  0001 C CNN
F 3 "" H 6900 13900 60  0001 C CNN
	1    6900 13900
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U2
U 1 1 665D886F
P 10850 13100
F 0 "U2" H 10850 13600 60  0000 C CNN
F 1 "plot_v1" H 11050 13450 60  0000 C CNN
F 2 "" H 10850 13100 60  0000 C CNN
F 3 "" H 10850 13100 60  0000 C CNN
	1    10850 13100
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U1
U 1 1 665D88A7
P 10700 13350
F 0 "U1" H 10700 13850 60  0000 C CNN
F 1 "plot_v1" H 10900 13700 60  0000 C CNN
F 2 "" H 10700 13350 60  0000 C CNN
F 3 "" H 10700 13350 60  0000 C CNN
	1    10700 13350
	1    0    0    -1  
$EndComp
$Comp
L pulse v1
U 1 1 665D9003
P 5450 12050
F 0 "v1" H 5250 12150 60  0000 C CNN
F 1 "pulse" H 5250 12000 60  0000 C CNN
F 2 "R1" H 5150 12050 60  0000 C CNN
F 3 "" H 5450 12050 60  0000 C CNN
	1    5450 12050
	1    0    0    -1  
$EndComp
$Comp
L pulse v3
U 1 1 665D91B6
P 5950 12300
F 0 "v3" H 5750 12400 60  0000 C CNN
F 1 "pulse" H 5750 12250 60  0000 C CNN
F 2 "R1" H 5650 12300 60  0000 C CNN
F 3 "" H 5950 12300 60  0000 C CNN
	1    5950 12300
	1    0    0    -1  
$EndComp
$Comp
L pulse v4
U 1 1 665D9225
P 6300 12500
F 0 "v4" H 6100 12600 60  0000 C CNN
F 1 "pulse" H 6100 12450 60  0000 C CNN
F 2 "R1" H 6000 12500 60  0000 C CNN
F 3 "" H 6300 12500 60  0000 C CNN
	1    6300 12500
	1    0    0    -1  
$EndComp
$Comp
L pulse v5
U 1 1 665D929D
P 6650 12700
F 0 "v5" H 6450 12800 60  0000 C CNN
F 1 "pulse" H 6450 12650 60  0000 C CNN
F 2 "R1" H 6350 12700 60  0000 C CNN
F 3 "" H 6650 12700 60  0000 C CNN
	1    6650 12700
	1    0    0    -1  
$EndComp
$Comp
L pulse v6
U 1 1 665D945D
P 6950 12950
F 0 "v6" H 6750 13050 60  0000 C CNN
F 1 "pulse" H 6750 12900 60  0000 C CNN
F 2 "R1" H 6650 12950 60  0000 C CNN
F 3 "" H 6950 12950 60  0000 C CNN
	1    6950 12950
	1    0    0    -1  
$EndComp
$Comp
L pulse v7
U 1 1 665D94F4
P 7250 13200
F 0 "v7" H 7050 13300 60  0000 C CNN
F 1 "pulse" H 7050 13150 60  0000 C CNN
F 2 "R1" H 6950 13200 60  0000 C CNN
F 3 "" H 7250 13200 60  0000 C CNN
	1    7250 13200
	1    0    0    -1  
$EndComp
$Comp
L pulse v8
U 1 1 665D9594
P 7550 13450
F 0 "v8" H 7350 13550 60  0000 C CNN
F 1 "pulse" H 7350 13400 60  0000 C CNN
F 2 "R1" H 7250 13450 60  0000 C CNN
F 3 "" H 7550 13450 60  0000 C CNN
	1    7550 13450
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR05
U 1 1 665D96C9
P 5450 12600
F 0 "#PWR05" H 5450 12350 50  0001 C CNN
F 1 "GND" H 5450 12450 50  0000 C CNN
F 2 "" H 5450 12600 50  0001 C CNN
F 3 "" H 5450 12600 50  0001 C CNN
	1    5450 12600
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR06
U 1 1 665D9702
P 5950 12850
F 0 "#PWR06" H 5950 12600 50  0001 C CNN
F 1 "GND" H 5950 12700 50  0000 C CNN
F 2 "" H 5950 12850 50  0001 C CNN
F 3 "" H 5950 12850 50  0001 C CNN
	1    5950 12850
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR07
U 1 1 665D9727
P 6300 13050
F 0 "#PWR07" H 6300 12800 50  0001 C CNN
F 1 "GND" H 6300 12900 50  0000 C CNN
F 2 "" H 6300 13050 50  0001 C CNN
F 3 "" H 6300 13050 50  0001 C CNN
	1    6300 13050
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR08
U 1 1 665D974C
P 6650 13250
F 0 "#PWR08" H 6650 13000 50  0001 C CNN
F 1 "GND" H 6650 13100 50  0000 C CNN
F 2 "" H 6650 13250 50  0001 C CNN
F 3 "" H 6650 13250 50  0001 C CNN
	1    6650 13250
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR09
U 1 1 665D97C5
P 6950 13500
F 0 "#PWR09" H 6950 13250 50  0001 C CNN
F 1 "GND" H 6950 13350 50  0000 C CNN
F 2 "" H 6950 13500 50  0001 C CNN
F 3 "" H 6950 13500 50  0001 C CNN
	1    6950 13500
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR010
U 1 1 665D98AE
P 7250 13750
F 0 "#PWR010" H 7250 13500 50  0001 C CNN
F 1 "GND" H 7250 13600 50  0000 C CNN
F 2 "" H 7250 13750 50  0001 C CNN
F 3 "" H 7250 13750 50  0001 C CNN
	1    7250 13750
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR011
U 1 1 665D99DD
P 7550 14000
F 0 "#PWR011" H 7550 13750 50  0001 C CNN
F 1 "GND" H 7550 13850 50  0000 C CNN
F 2 "" H 7550 14000 50  0001 C CNN
F 3 "" H 7550 14000 50  0001 C CNN
	1    7550 14000
	1    0    0    -1  
$EndComp
$Comp
L pulse v9
U 1 1 665D9F79
P 11650 13300
F 0 "v9" H 11450 13400 60  0000 C CNN
F 1 "pulse" H 11450 13250 60  0000 C CNN
F 2 "R1" H 11350 13300 60  0000 C CNN
F 3 "" H 11650 13300 60  0000 C CNN
	1    11650 13300
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR012
U 1 1 665D9F80
P 11650 13850
F 0 "#PWR012" H 11650 13600 50  0001 C CNN
F 1 "GND" H 11650 13700 50  0000 C CNN
F 2 "" H 11650 13850 50  0001 C CNN
F 3 "" H 11650 13850 50  0001 C CNN
	1    11650 13850
	1    0    0    -1  
$EndComp
$Comp
L pulse v10
U 1 1 665DA020
P 12200 13050
F 0 "v10" H 12000 13150 60  0000 C CNN
F 1 "pulse" H 12000 13000 60  0000 C CNN
F 2 "R1" H 11900 13050 60  0000 C CNN
F 3 "" H 12200 13050 60  0000 C CNN
	1    12200 13050
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR013
U 1 1 665DA027
P 12200 13600
F 0 "#PWR013" H 12200 13350 50  0001 C CNN
F 1 "GND" H 12200 13450 50  0000 C CNN
F 2 "" H 12200 13600 50  0001 C CNN
F 3 "" H 12200 13600 50  0001 C CNN
	1    12200 13600
	1    0    0    -1  
$EndComp
$Comp
L pulse v11
U 1 1 665DA07B
P 12650 12800
F 0 "v11" H 12450 12900 60  0000 C CNN
F 1 "pulse" H 12450 12750 60  0000 C CNN
F 2 "R1" H 12350 12800 60  0000 C CNN
F 3 "" H 12650 12800 60  0000 C CNN
	1    12650 12800
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR014
U 1 1 665DA082
P 12650 13350
F 0 "#PWR014" H 12650 13100 50  0001 C CNN
F 1 "GND" H 12650 13200 50  0000 C CNN
F 2 "" H 12650 13350 50  0001 C CNN
F 3 "" H 12650 13350 50  0001 C CNN
	1    12650 13350
	1    0    0    -1  
$EndComp
$Comp
L pulse v12
U 1 1 665DA0D3
P 13100 12550
F 0 "v12" H 12900 12650 60  0000 C CNN
F 1 "pulse" H 12900 12500 60  0000 C CNN
F 2 "R1" H 12800 12550 60  0000 C CNN
F 3 "" H 13100 12550 60  0000 C CNN
	1    13100 12550
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR015
U 1 1 665DA0DA
P 13100 13100
F 0 "#PWR015" H 13100 12850 50  0001 C CNN
F 1 "GND" H 13100 12950 50  0000 C CNN
F 2 "" H 13100 13100 50  0001 C CNN
F 3 "" H 13100 13100 50  0001 C CNN
	1    13100 13100
	1    0    0    -1  
$EndComp
$Comp
L pulse v13
U 1 1 665DA129
P 13550 12250
F 0 "v13" H 13350 12350 60  0000 C CNN
F 1 "pulse" H 13350 12200 60  0000 C CNN
F 2 "R1" H 13250 12250 60  0000 C CNN
F 3 "" H 13550 12250 60  0000 C CNN
	1    13550 12250
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR016
U 1 1 665DA130
P 13550 12800
F 0 "#PWR016" H 13550 12550 50  0001 C CNN
F 1 "GND" H 13550 12650 50  0000 C CNN
F 2 "" H 13550 12800 50  0001 C CNN
F 3 "" H 13550 12800 50  0001 C CNN
	1    13550 12800
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U4
U 1 1 665DA47E
P 6100 11600
F 0 "U4" H 6100 12100 60  0000 C CNN
F 1 "plot_v1" H 6300 11950 60  0000 C CNN
F 2 "" H 6100 11600 60  0000 C CNN
F 3 "" H 6100 11600 60  0000 C CNN
	1    6100 11600
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U5
U 1 1 665DA5EF
P 6600 11600
F 0 "U5" H 6600 12100 60  0000 C CNN
F 1 "plot_v1" H 6800 11950 60  0000 C CNN
F 2 "" H 6600 11600 60  0000 C CNN
F 3 "" H 6600 11600 60  0000 C CNN
	1    6600 11600
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U6
U 1 1 665DA65D
P 7050 11600
F 0 "U6" H 7050 12100 60  0000 C CNN
F 1 "plot_v1" H 7250 11950 60  0000 C CNN
F 2 "" H 7050 11600 60  0000 C CNN
F 3 "" H 7050 11600 60  0000 C CNN
	1    7050 11600
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U7
U 1 1 665DA6BC
P 7450 11600
F 0 "U7" H 7450 12100 60  0000 C CNN
F 1 "plot_v1" H 7650 11950 60  0000 C CNN
F 2 "" H 7450 11600 60  0000 C CNN
F 3 "" H 7450 11600 60  0000 C CNN
	1    7450 11600
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U8
U 1 1 665DA71E
P 7850 11600
F 0 "U8" H 7850 12100 60  0000 C CNN
F 1 "plot_v1" H 8050 11950 60  0000 C CNN
F 2 "" H 7850 11600 60  0000 C CNN
F 3 "" H 7850 11600 60  0000 C CNN
	1    7850 11600
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U9
U 1 1 665DA77F
P 8350 11600
F 0 "U9" H 8350 12100 60  0000 C CNN
F 1 "plot_v1" H 8550 11950 60  0000 C CNN
F 2 "" H 8350 11600 60  0000 C CNN
F 3 "" H 8350 11600 60  0000 C CNN
	1    8350 11600
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U10
U 1 1 665DB369
P 10950 11800
F 0 "U10" H 10950 12300 60  0000 C CNN
F 1 "plot_v1" H 11150 12150 60  0000 C CNN
F 2 "" H 10950 11800 60  0000 C CNN
F 3 "" H 10950 11800 60  0000 C CNN
	1    10950 11800
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U11
U 1 1 665DB509
P 11500 11800
F 0 "U11" H 11500 12300 60  0000 C CNN
F 1 "plot_v1" H 11700 12150 60  0000 C CNN
F 2 "" H 11500 11800 60  0000 C CNN
F 3 "" H 11500 11800 60  0000 C CNN
	1    11500 11800
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U12
U 1 1 665DB584
P 11950 11800
F 0 "U12" H 11950 12300 60  0000 C CNN
F 1 "plot_v1" H 12150 12150 60  0000 C CNN
F 2 "" H 11950 11800 60  0000 C CNN
F 3 "" H 11950 11800 60  0000 C CNN
	1    11950 11800
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U13
U 1 1 665DB662
P 12400 11800
F 0 "U13" H 12400 12300 60  0000 C CNN
F 1 "plot_v1" H 12600 12150 60  0000 C CNN
F 2 "" H 12400 11800 60  0000 C CNN
F 3 "" H 12400 11800 60  0000 C CNN
	1    12400 11800
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U14
U 1 1 665DB6D7
P 12800 11800
F 0 "U14" H 12800 12300 60  0000 C CNN
F 1 "plot_v1" H 13000 12150 60  0000 C CNN
F 2 "" H 12800 11800 60  0000 C CNN
F 3 "" H 12800 11800 60  0000 C CNN
	1    12800 11800
	1    0    0    -1  
$EndComp
Wire Wire Line
	12100 9300 10650 9300
Wire Wire Line
	10650 9300 10650 11500
Wire Wire Line
	12100 10300 12100 10200
Wire Wire Line
	5450 11500 8600 11500
Wire Wire Line
	8450 12000 8600 12000
Wire Wire Line
	6650 12250 8600 12250
Wire Wire Line
	6950 12500 8600 12500
Wire Wire Line
	7250 12750 8600 12750
Wire Wire Line
	7550 13000 8600 13000
Wire Wire Line
	8600 13250 8450 13250
Wire Wire Line
	8450 13250 8450 13300
Wire Wire Line
	10650 13000 11200 13000
Wire Wire Line
	11200 13000 11200 13100
Wire Wire Line
	10650 13250 10900 13250
Wire Wire Line
	10900 13250 10900 13300
Wire Wire Line
	11200 13500 11200 13400
Wire Wire Line
	10900 13700 10900 13600
Wire Wire Line
	10700 13150 10700 13250
Connection ~ 10700 13250
Wire Wire Line
	10850 12900 10850 13000
Connection ~ 10850 13000
Wire Wire Line
	8600 11750 8450 11750
Wire Wire Line
	5450 11600 5450 11500
Wire Wire Line
	5950 11850 8450 11850
Wire Wire Line
	8450 11850 8450 11750
Wire Wire Line
	6300 12050 8450 12050
Wire Wire Line
	8450 12050 8450 12000
Wire Wire Line
	5450 12600 5450 12500
Wire Wire Line
	5950 12850 5950 12750
Wire Wire Line
	6300 13050 6300 12950
Wire Wire Line
	6650 13250 6650 13150
Wire Wire Line
	6950 13500 6950 13400
Wire Wire Line
	7250 13750 7250 13650
Wire Wire Line
	7550 14000 7550 13900
Wire Wire Line
	11650 12850 11650 12750
Wire Wire Line
	11650 13850 11650 13750
Wire Wire Line
	11650 12750 10650 12750
Wire Wire Line
	12200 12500 12200 12600
Wire Wire Line
	12200 13600 12200 13500
Wire Wire Line
	10650 12500 12200 12500
Wire Wire Line
	12650 12250 12650 12350
Wire Wire Line
	12650 13350 12650 13250
Wire Wire Line
	10650 12250 12650 12250
Wire Wire Line
	13100 12000 13100 12100
Wire Wire Line
	13100 13100 13100 13000
Wire Wire Line
	10650 12000 13100 12000
Wire Wire Line
	13550 11700 13550 11800
Wire Wire Line
	13550 12800 13550 12700
Wire Wire Line
	10650 11700 13550 11700
Wire Wire Line
	10650 11700 10650 11750
Wire Wire Line
	5650 11400 5650 11500
Connection ~ 5650 11500
Wire Wire Line
	6600 11400 6600 12050
Connection ~ 6600 12050
Wire Wire Line
	7050 11400 7050 12250
Connection ~ 7050 12250
Wire Wire Line
	7450 11400 7450 12500
Connection ~ 7450 12500
Wire Wire Line
	7850 11400 7850 12750
Connection ~ 7850 12750
Wire Wire Line
	10950 11600 10950 12750
Connection ~ 10950 12750
Wire Wire Line
	11500 11600 11500 12500
Connection ~ 11500 12500
Wire Wire Line
	11950 11600 11950 12250
Connection ~ 11950 12250
Wire Wire Line
	12400 11600 12400 12000
Connection ~ 12400 12000
Wire Wire Line
	12800 11600 12800 11700
Connection ~ 12800 11700
Connection ~ 6100 11850
Wire Wire Line
	6100 11400 6100 11850
Wire Wire Line
	8350 11400 8250 11400
Wire Wire Line
	8250 11400 8250 12900
Wire Wire Line
	8250 12900 8400 12900
Wire Wire Line
	8400 12900 8400 13000
Connection ~ 8400 13000
$Comp
L plot_v1 U3
U 1 1 665DA85F
P 5650 11600
F 0 "U3" H 5650 12100 60  0000 C CNN
F 1 "plot_v1" H 5850 11950 60  0000 C CNN
F 2 "" H 5650 11600 60  0000 C CNN
F 3 "" H 5650 11600 60  0000 C CNN
	1    5650 11600
	1    0    0    -1  
$EndComp
Text GLabel 5500 11500 1    60   Input ~ 0
i5
Text GLabel 6250 11850 1    60   Input ~ 0
i6
Text GLabel 6850 12050 1    60   Input ~ 0
i7
Text GLabel 7200 12250 1    60   Input ~ 0
i8
Text GLabel 7350 12500 1    60   Input ~ 0
i9
Text GLabel 7600 12750 1    60   Input ~ 0
i10
Text GLabel 7850 13000 1    60   Input ~ 0
i11
Text GLabel 11150 11700 1    60   Input ~ 0
i4
Text GLabel 11300 12000 1    60   Input ~ 0
i3
Text GLabel 11600 12250 1    60   Input ~ 0
i2
Text GLabel 11750 12500 1    60   Input ~ 0
i1
Text GLabel 11450 12750 1    60   Input ~ 0
i0
$EndSCHEMATC
