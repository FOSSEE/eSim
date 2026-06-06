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
L sky130_fd_pr__pfet_01v8 SC1
U 1 1 68464E7B
P 3850 1600
F 0 "SC1" H 3900 1900 50  0000 C CNN
F 1 "sky130_fd_pr__pfet_01v8" H 4150 1687 50  0000 R CNN
F 2 "" H 3850 100 50  0001 C CNN
F 3 "" H 3850 1600 50  0001 C CNN
	1    3850 1600
	1    0    0    -1  
$EndComp
$Comp
L sky130_fd_pr__pfet_01v8 SC2
U 1 1 68465252
P 3850 2400
F 0 "SC2" H 3900 2700 50  0000 C CNN
F 1 "sky130_fd_pr__pfet_01v8" H 4150 2487 50  0000 R CNN
F 2 "" H 3850 900 50  0001 C CNN
F 3 "" H 3850 2400 50  0001 C CNN
	1    3850 2400
	1    0    0    -1  
$EndComp
$Comp
L sky130_fd_pr__nfet_01v8 SC3
U 1 1 68465307
P 3850 3400
F 0 "SC3" H 3900 3700 50  0000 C CNN
F 1 "sky130_fd_pr__nfet_01v8" H 4150 3487 50  0000 R CNN
F 2 "" H 3850 1900 50  0001 C CNN
F 3 "" H 3850 3400 50  0001 C CNN
	1    3850 3400
	1    0    0    -1  
$EndComp
$Comp
L sky130_fd_pr__nfet_01v8 SC4
U 1 1 68465392
P 3850 4200
F 0 "SC4" H 3900 4500 50  0000 C CNN
F 1 "sky130_fd_pr__nfet_01v8" H 4150 4287 50  0000 R CNN
F 2 "" H 3850 2700 50  0001 C CNN
F 3 "" H 3850 4200 50  0001 C CNN
	1    3850 4200
	1    0    0    -1  
$EndComp
$Comp
L sky130_fd_pr__pfet_01v8 SC5
U 1 1 68465403
P 4850 2200
F 0 "SC5" H 4900 2500 50  0000 C CNN
F 1 "sky130_fd_pr__pfet_01v8" H 5150 2287 50  0000 R CNN
F 2 "" H 4850 700 50  0001 C CNN
F 3 "" H 4850 2200 50  0001 C CNN
	1    4850 2200
	0    -1   -1   0   
$EndComp
$Comp
L sky130_fd_pr__nfet_01v8 SC6
U 1 1 6846558D
P 4850 3600
F 0 "SC6" H 4900 3900 50  0000 C CNN
F 1 "sky130_fd_pr__nfet_01v8" H 5150 3687 50  0000 R CNN
F 2 "" H 4850 2100 50  0001 C CNN
F 3 "" H 4850 3600 50  0001 C CNN
	1    4850 3600
	0    1    1    0   
$EndComp
$Comp
L sky130_fd_pr__pfet_01v8 SC7
U 1 1 68465896
P 5900 1900
F 0 "SC7" H 5950 2200 50  0000 C CNN
F 1 "sky130_fd_pr__pfet_01v8" H 6200 1987 50  0000 R CNN
F 2 "" H 5900 400 50  0001 C CNN
F 3 "" H 5900 1900 50  0001 C CNN
	1    5900 1900
	1    0    0    -1  
$EndComp
$Comp
L sky130_fd_pr__nfet_01v8 SC8
U 1 1 68465B12
P 5900 3900
F 0 "SC8" H 5950 4200 50  0000 C CNN
F 1 "sky130_fd_pr__nfet_01v8" H 6200 3987 50  0000 R CNN
F 2 "" H 5900 2400 50  0001 C CNN
F 3 "" H 5900 3900 50  0001 C CNN
	1    5900 3900
	1    0    0    -1  
$EndComp
Wire Wire Line
	6100 2200 6100 3600
Wire Wire Line
	5600 1900 5600 3900
Wire Wire Line
	4050 2700 4050 3100
Wire Wire Line
	4050 2900 5600 2900
Connection ~ 5600 2900
Connection ~ 4050 2900
Wire Wire Line
	4850 2500 4850 3300
Connection ~ 4850 2900
Wire Wire Line
	4050 1900 4050 2100
Wire Wire Line
	4550 2000 4050 2000
Connection ~ 4050 2000
Wire Wire Line
	4050 1300 6100 1300
Wire Wire Line
	6100 1300 6100 1600
Wire Wire Line
	4050 4500 6100 4500
Wire Wire Line
	6100 4500 6100 4200
Wire Wire Line
	5150 2000 5500 2000
Wire Wire Line
	5500 2000 5500 4500
Connection ~ 5500 4500
Wire Wire Line
	5150 3800 5400 3800
Wire Wire Line
	5400 3800 5400 1300
Connection ~ 5400 1300
Wire Wire Line
	3550 1600 3350 1600
Wire Wire Line
	3350 1600 3350 4200
Wire Wire Line
	3350 4200 3550 4200
Wire Wire Line
	4050 3700 4050 3900
Wire Wire Line
	4550 3800 4050 3800
Connection ~ 4050 3800
Wire Wire Line
	4850 3700 4850 3900
Wire Wire Line
	4850 3900 4450 3900
Wire Wire Line
	4450 3900 4450 3800
Connection ~ 4450 3800
Wire Wire Line
	3950 4200 4100 4200
Wire Wire Line
	4100 4200 4100 4500
Connection ~ 4100 4500
Wire Wire Line
	6000 3900 6150 3900
Wire Wire Line
	6150 3900 6150 4250
Wire Wire Line
	6150 4250 6100 4250
Connection ~ 6100 4250
Wire Wire Line
	3950 3400 4150 3400
Wire Wire Line
	4150 3400 4150 3800
Connection ~ 4150 3800
Wire Wire Line
	3950 2400 4100 2400
Wire Wire Line
	4100 2400 4100 2000
Connection ~ 4100 2000
Wire Wire Line
	4850 2100 4850 1950
Wire Wire Line
	4850 1950 4500 1950
Wire Wire Line
	4500 1950 4500 2000
Connection ~ 4500 2000
Wire Wire Line
	3950 1600 4100 1600
Wire Wire Line
	4100 1600 4100 1300
Connection ~ 4100 1300
Wire Wire Line
	6000 1900 6150 1900
Wire Wire Line
	6150 1900 6150 1500
Wire Wire Line
	6150 1500 6100 1500
Connection ~ 6100 1500
Wire Wire Line
	3550 2400 3350 2400
Connection ~ 3350 2400
Wire Wire Line
	3550 3400 3350 3400
Connection ~ 3350 3400
$Comp
L PORT U1
U 1 1 68466403
P 2850 2900
F 0 "U1" H 2900 3000 30  0000 C CNN
F 1 "PORT" H 2850 2900 30  0000 C CNN
F 2 "" H 2850 2900 60  0000 C CNN
F 3 "" H 2850 2900 60  0000 C CNN
	1    2850 2900
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 2 1 684664D8
P 4500 1050
F 0 "U1" H 4550 1150 30  0000 C CNN
F 1 "PORT" H 4500 1050 30  0000 C CNN
F 2 "" H 4500 1050 60  0000 C CNN
F 3 "" H 4500 1050 60  0000 C CNN
	2    4500 1050
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 4 1 68466579
P 6600 2950
F 0 "U1" H 6650 3050 30  0000 C CNN
F 1 "PORT" H 6600 2950 30  0000 C CNN
F 2 "" H 6600 2950 60  0000 C CNN
F 3 "" H 6600 2950 60  0000 C CNN
	4    6600 2950
	-1   0    0    1   
$EndComp
$Comp
L PORT U1
U 3 1 68466640
P 4600 4800
F 0 "U1" H 4650 4900 30  0000 C CNN
F 1 "PORT" H 4600 4800 30  0000 C CNN
F 2 "" H 4600 4800 60  0000 C CNN
F 3 "" H 4600 4800 60  0000 C CNN
	3    4600 4800
	1    0    0    -1  
$EndComp
Wire Wire Line
	4850 4800 4850 4500
Connection ~ 4850 4500
Wire Wire Line
	3100 2900 3350 2900
Connection ~ 3350 2900
Wire Wire Line
	6350 2950 6100 2950
Connection ~ 6100 2950
Wire Wire Line
	4750 1050 4750 1300
Connection ~ 4750 1300
$Comp
L SKY130mode scmode1
U 1 1 6846736A
P 8750 3650
F 0 "scmode1" H 8750 3800 98  0000 C CNB
F 1 "SKY130mode" H 8750 3550 118 0000 C CNB
F 2 "" H 8750 3800 60  0001 C CNN
F 3 "" H 8750 3800 60  0001 C CNN
	1    8750 3650
	1    0    0    -1  
$EndComp
$EndSCHEMATC
