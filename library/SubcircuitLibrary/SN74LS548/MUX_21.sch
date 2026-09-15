EESchema Schematic File Version 2
LIBS:MUX_21-rescue
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
LIBS:MUX_21-cache
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
L sky130_fd_pr__nfet_01v8 SC1
U 1 1 68711FE2
P 4700 2000
F 0 "SC1" H 4750 2300 50  0000 C CNN
F 1 "sky130_fd_pr__nfet_01v8" H 5000 2087 50  0000 R CNN
F 2 "" H 4700 500 50  0001 C CNN
F 3 "" H 4700 2000 50  0001 C CNN
	1    4700 2000
	0    1    1    0   
$EndComp
$Comp
L sky130_fd_pr__nfet_01v8 SC2
U 1 1 68712114
P 6200 2300
F 0 "SC2" H 6250 2600 50  0000 C CNN
F 1 "sky130_fd_pr__nfet_01v8" H 6500 2387 50  0000 R CNN
F 2 "" H 6200 800 50  0001 C CNN
F 3 "" H 6200 2300 50  0001 C CNN
	1    6200 2300
	0    1    1    0   
$EndComp
Wire Wire Line
	4250 1650 5250 1650
Wire Wire Line
	4700 1700 4700 1650
Connection ~ 4700 1650
Wire Wire Line
	4400 2200 4250 2200
Wire Wire Line
	4700 2100 4700 2250
Wire Wire Line
	4700 2250 4350 2250
Wire Wire Line
	4350 2250 4350 2200
Connection ~ 4350 2200
Wire Wire Line
	6200 1650 6200 2000
Wire Wire Line
	5900 2500 4250 2500
Wire Wire Line
	6200 2400 6200 2550
Wire Wire Line
	6200 2550 5800 2550
Wire Wire Line
	5800 2550 5800 2500
Connection ~ 5800 2500
Wire Wire Line
	5000 2200 6850 2200
Wire Wire Line
	6500 2200 6500 2500
Connection ~ 6500 2200
$Comp
L PORT U1
U 1 1 687121FA
P 4000 1650
F 0 "U1" H 4050 1750 30  0000 C CNN
F 1 "PORT" H 4000 1650 30  0000 C CNN
F 2 "" H 4000 1650 60  0000 C CNN
F 3 "" H 4000 1650 60  0000 C CNN
	1    4000 1650
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 2 1 68712241
P 4000 2200
F 0 "U1" H 4050 2300 30  0000 C CNN
F 1 "PORT" H 4000 2200 30  0000 C CNN
F 2 "" H 4000 2200 60  0000 C CNN
F 3 "" H 4000 2200 60  0000 C CNN
	2    4000 2200
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 3 1 6871226C
P 4000 2500
F 0 "U1" H 4050 2600 30  0000 C CNN
F 1 "PORT" H 4000 2500 30  0000 C CNN
F 2 "" H 4000 2500 60  0000 C CNN
F 3 "" H 4000 2500 60  0000 C CNN
	3    4000 2500
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 4 1 68712295
P 5000 1550
F 0 "U1" H 5050 1650 30  0000 C CNN
F 1 "PORT" H 5000 1550 30  0000 C CNN
F 2 "" H 5000 1550 60  0000 C CNN
F 3 "" H 5000 1550 60  0000 C CNN
	4    5000 1550
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 5 1 687122E8
P 5000 1750
F 0 "U1" H 5050 1850 30  0000 C CNN
F 1 "PORT" H 5000 1750 30  0000 C CNN
F 2 "" H 5000 1750 60  0000 C CNN
F 3 "" H 5000 1750 60  0000 C CNN
	5    5000 1750
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 6 1 68712317
P 7100 2200
F 0 "U1" H 7150 2300 30  0000 C CNN
F 1 "PORT" H 7100 2200 30  0000 C CNN
F 2 "" H 7100 2200 60  0000 C CNN
F 3 "" H 7100 2200 60  0000 C CNN
	6    7100 2200
	-1   0    0    1   
$EndComp
$Comp
L SKY130mode scmode1
U 1 1 68712384
P 8900 2800
F 0 "scmode1" H 8900 2950 98  0000 C CNB
F 1 "SKY130mode" H 8900 2700 118 0000 C CNB
F 2 "" H 8900 2950 60  0001 C CNN
F 3 "" H 8900 2950 60  0001 C CNN
	1    8900 2800
	1    0    0    -1  
$EndComp
$Comp
L CMOS_INVTR X1
U 1 1 6877C242
P 5700 1650
F 0 "X1" H 5700 1650 60  0000 C CNN
F 1 "CMOS_INVTR" H 5650 1450 60  0000 C CNN
F 2 "" H 5700 1650 60  0001 C CNN
F 3 "" H 5700 1650 60  0001 C CNN
	1    5700 1650
	1    0    0    -1  
$EndComp
$EndSCHEMATC
