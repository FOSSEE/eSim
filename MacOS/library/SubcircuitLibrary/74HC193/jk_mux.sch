EESchema Schematic File Version 2
LIBS:jk_mux-rescue
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
LIBS:jk_mux-cache
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
L d_jkff U3
U 1 1 67CB1FFF
P 5550 3400
F 0 "U3" H 5550 3400 60  0000 C CNN
F 1 "d_jkff" H 5550 3250 60  0000 C CNN
F 2 "" H 5550 3400 60  0000 C CNN
F 3 "" H 5550 3400 60  0000 C CNN
	1    5550 3400
	1    0    0    -1  
$EndComp
Wire Wire Line
	4200 2750 4950 2750
Wire Wire Line
	4950 2750 4950 3150
Wire Wire Line
	4200 4000 4950 4000
Wire Wire Line
	4950 4000 4950 3750
$Comp
L PORT U1
U 4 1 67CB24B8
P 3800 4850
F 0 "U1" H 3850 4950 30  0000 C CNN
F 1 "PORT" H 3800 4850 30  0000 C CNN
F 2 "" H 3800 4850 60  0000 C CNN
F 3 "" H 3800 4850 60  0000 C CNN
	4    3800 4850
	0    -1   -1   0   
$EndComp
Wire Wire Line
	3800 4600 3800 4500
Wire Wire Line
	3800 3250 3150 3250
Wire Wire Line
	3150 3250 3150 4550
Wire Wire Line
	3150 4550 3800 4550
Connection ~ 3800 4550
$Comp
L PORT U1
U 1 1 67CB252E
P 2600 2600
F 0 "U1" H 2650 2700 30  0000 C CNN
F 1 "PORT" H 2600 2600 30  0000 C CNN
F 2 "" H 2600 2600 60  0000 C CNN
F 3 "" H 2600 2600 60  0000 C CNN
	1    2600 2600
	1    0    0    -1  
$EndComp
Wire Wire Line
	2850 2600 3400 2600
$Comp
L d_inverter U2
U 1 1 67CB259F
P 2950 3850
F 0 "U2" H 2950 3750 60  0000 C CNN
F 1 "d_inverter" H 2950 4000 60  0000 C CNN
F 2 "" H 3000 3800 60  0000 C CNN
F 3 "" H 3000 3800 60  0000 C CNN
	1    2950 3850
	1    0    0    -1  
$EndComp
Wire Wire Line
	3250 3850 3400 3850
Wire Wire Line
	2650 3850 2650 3050
Wire Wire Line
	2650 3050 2950 3050
Wire Wire Line
	2950 3050 2950 2600
Connection ~ 2950 2600
$Comp
L PORT U1
U 3 1 67CB2601
P 3100 2950
F 0 "U1" H 3150 3050 30  0000 C CNN
F 1 "PORT" H 3100 2950 30  0000 C CNN
F 2 "" H 3100 2950 60  0000 C CNN
F 3 "" H 3100 2950 60  0000 C CNN
	3    3100 2950
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 2 1 67CB265C
P 2850 4200
F 0 "U1" H 2900 4300 30  0000 C CNN
F 1 "PORT" H 2850 4200 30  0000 C CNN
F 2 "" H 2850 4200 60  0000 C CNN
F 3 "" H 2850 4200 60  0000 C CNN
	2    2850 4200
	1    0    0    -1  
$EndComp
Wire Wire Line
	3350 2950 3400 2950
Wire Wire Line
	3100 4200 3400 4200
$Comp
L PORT U1
U 5 1 67CB26E6
P 4450 4650
F 0 "U1" H 4500 4750 30  0000 C CNN
F 1 "PORT" H 4450 4650 30  0000 C CNN
F 2 "" H 4450 4650 60  0000 C CNN
F 3 "" H 4450 4650 60  0000 C CNN
	5    4450 4650
	1    0    0    -1  
$EndComp
Wire Wire Line
	4700 4650 4700 3450
Wire Wire Line
	4700 3450 4950 3450
$Comp
L PORT U1
U 6 1 67CB2755
P 5550 2400
F 0 "U1" H 5600 2500 30  0000 C CNN
F 1 "PORT" H 5550 2400 30  0000 C CNN
F 2 "" H 5550 2400 60  0000 C CNN
F 3 "" H 5550 2400 60  0000 C CNN
	6    5550 2400
	0    1    1    0   
$EndComp
$Comp
L PORT U1
U 7 1 67CB27B8
P 5550 4500
F 0 "U1" H 5600 4600 30  0000 C CNN
F 1 "PORT" H 5550 4500 30  0000 C CNN
F 2 "" H 5550 4500 60  0000 C CNN
F 3 "" H 5550 4500 60  0000 C CNN
	7    5550 4500
	0    -1   -1   0   
$EndComp
$Comp
L PORT U1
U 8 1 67CB2803
P 6550 3150
F 0 "U1" H 6600 3250 30  0000 C CNN
F 1 "PORT" H 6550 3150 30  0000 C CNN
F 2 "" H 6550 3150 60  0000 C CNN
F 3 "" H 6550 3150 60  0000 C CNN
	8    6550 3150
	-1   0    0    1   
$EndComp
$Comp
L PORT U1
U 9 1 67CB2872
P 6550 3750
F 0 "U1" H 6600 3850 30  0000 C CNN
F 1 "PORT" H 6550 3750 30  0000 C CNN
F 2 "" H 6550 3750 60  0000 C CNN
F 3 "" H 6550 3750 60  0000 C CNN
	9    6550 3750
	-1   0    0    1   
$EndComp
Wire Wire Line
	5550 2650 5550 2850
Wire Wire Line
	5550 4100 5550 4250
Wire Wire Line
	6100 3150 6300 3150
Wire Wire Line
	6100 3750 6300 3750
$Comp
L mux X1
U 1 1 67CB272E
P 3800 2800
F 0 "X1" H 3800 2800 60  0000 C CNN
F 1 "mux" H 3800 2950 60  0000 C CNN
F 2 "" H 3800 2800 60  0001 C CNN
F 3 "" H 3800 2800 60  0001 C CNN
	1    3800 2800
	1    0    0    -1  
$EndComp
$Comp
L mux X2
U 1 1 67CB276D
P 3800 4050
F 0 "X2" H 3800 4050 60  0000 C CNN
F 1 "mux" H 3800 4200 60  0000 C CNN
F 2 "" H 3800 4050 60  0001 C CNN
F 3 "" H 3800 4050 60  0001 C CNN
	1    3800 4050
	1    0    0    -1  
$EndComp
$EndSCHEMATC
