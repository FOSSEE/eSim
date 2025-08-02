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
U 1 1 684B982F
P 5350 2950
F 0 "SC1" H 5400 3250 50  0000 C CNN
F 1 "sky130_fd_pr__pfet_01v8" H 5650 3037 50  0000 R CNN
F 2 "" H 5350 1450 50  0001 C CNN
F 3 "" H 5350 2950 50  0001 C CNN
	1    5350 2950
	1    0    0    -1  
$EndComp
$Comp
L sky130_fd_pr__nfet_01v8 SC2
U 1 1 684B9856
P 5350 3800
F 0 "SC2" H 5400 4100 50  0000 C CNN
F 1 "sky130_fd_pr__nfet_01v8" H 5650 3887 50  0000 R CNN
F 2 "" H 5350 2300 50  0001 C CNN
F 3 "" H 5350 3800 50  0001 C CNN
	1    5350 3800
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 1 1 684B98AD
P 4550 3300
F 0 "U1" H 4600 3400 30  0000 C CNN
F 1 "PORT" H 4550 3300 30  0000 C CNN
F 2 "" H 4550 3300 60  0000 C CNN
F 3 "" H 4550 3300 60  0000 C CNN
	1    4550 3300
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 4 1 684B98D8
P 6300 3350
F 0 "U1" H 6350 3450 30  0000 C CNN
F 1 "PORT" H 6300 3350 30  0000 C CNN
F 2 "" H 6300 3350 60  0000 C CNN
F 3 "" H 6300 3350 60  0000 C CNN
	4    6300 3350
	-1   0    0    -1  
$EndComp
$Comp
L PORT U1
U 3 1 684B9935
P 5300 4350
F 0 "U1" H 5350 4450 30  0000 C CNN
F 1 "PORT" H 5300 4350 30  0000 C CNN
F 2 "" H 5300 4350 60  0000 C CNN
F 3 "" H 5300 4350 60  0000 C CNN
	3    5300 4350
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 2 1 684B999A
P 5300 2350
F 0 "U1" H 5350 2450 30  0000 C CNN
F 1 "PORT" H 5300 2350 30  0000 C CNN
F 2 "" H 5300 2350 60  0000 C CNN
F 3 "" H 5300 2350 60  0000 C CNN
	2    5300 2350
	1    0    0    -1  
$EndComp
$Comp
L SKY130mode scmode1
U 1 1 684B99CD
P 7950 3000
F 0 "scmode1" H 7950 3150 98  0000 C CNB
F 1 "SKY130mode" H 7950 2900 118 0000 C CNB
F 2 "" H 7950 3150 60  0001 C CNN
F 3 "" H 7950 3150 60  0001 C CNN
	1    7950 3000
	1    0    0    -1  
$EndComp
Wire Wire Line
	5550 2650 5550 2350
Wire Wire Line
	5450 2950 5600 2950
Wire Wire Line
	5600 2950 5600 2550
Wire Wire Line
	5600 2550 5550 2550
Connection ~ 5550 2550
Wire Wire Line
	5550 3250 5550 3500
Wire Wire Line
	6050 3350 5550 3350
Connection ~ 5550 3350
Wire Wire Line
	5050 2950 5050 3800
Wire Wire Line
	4800 3300 5050 3300
Connection ~ 5050 3300
Wire Wire Line
	5450 3800 5600 3800
Wire Wire Line
	5600 3800 5600 4150
Wire Wire Line
	5600 4150 5550 4150
Wire Wire Line
	5550 4100 5550 4350
Connection ~ 5550 4150
$EndSCHEMATC
