EESchema Schematic File Version 2
LIBS:Integrator_LM_741-rescue
LIBS:power
LIBS:eSim_Analog
LIBS:eSim_Devices
LIBS:eSim_Digital
LIBS:eSim_Hybrid
LIBS:eSim_Miscellaneous
LIBS:eSim_Plot
LIBS:eSim_Power
LIBS:eSim_Sources
LIBS:eSim_User
LIBS:eSim_Subckt
LIBS:74xgxx
LIBS:74xx
LIBS:ac-dc
LIBS:actel
LIBS:adc-dac
LIBS:Altera
LIBS:analog_devices
LIBS:analog_switches
LIBS:atmel
LIBS:audio
LIBS:brooktre
LIBS:cmos_ieee
LIBS:cmos4000
LIBS:conn
LIBS:contrib
LIBS:cypress
LIBS:dc-dc
LIBS:digital-audio
LIBS:diode
LIBS:display
LIBS:dsp
LIBS:elec-unifil
LIBS:ESD_Protection
LIBS:ftdi
LIBS:gennum
LIBS:hc11
LIBS:intel
LIBS:interface
LIBS:ir
LIBS:Lattice
LIBS:maxim
LIBS:memory
LIBS:microchip
LIBS:microchip_dspic33dsc
LIBS:microchip_pic10mcu
LIBS:microchip_pic12mcu
LIBS:microchip_pic16mcu
LIBS:microchip_pic18mcu
LIBS:microchip_pic32mcu
LIBS:microcontrollers
LIBS:motor_drivers
LIBS:motorola
LIBS:msp430
LIBS:nordicsemi
LIBS:nxp_armmcu
LIBS:onsemi
LIBS:opto
LIBS:Oscillators
LIBS:philips
LIBS:Power_Management
LIBS:powerint
LIBS:pspice
LIBS:references
LIBS:regul
LIBS:relays
LIBS:rfcom
LIBS:sensors
LIBS:silabs
LIBS:siliconi
LIBS:stm8
LIBS:stm32
LIBS:supertex
LIBS:switches
LIBS:texas
LIBS:transf
LIBS:transistors
LIBS:ttl_ieee
LIBS:valves
LIBS:video
LIBS:Xicor
LIBS:xilinx
LIBS:Zilog
LIBS:Integrator_LM_741-cache
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
L eSim_R R1
U 1 1 5CE9074D
P 5650 3100
F 0 "R1" H 5700 3230 50  0000 C CNN
F 1 "10k" H 5700 3150 50  0000 C CNN
F 2 "" H 5700 3080 30  0000 C CNN
F 3 "" V 5700 3150 30  0000 C CNN
	1    5650 3100
	1    0    0    -1  
$EndComp
$Comp
L eSim_C C1
U 1 1 5CE9074E
P 6950 2300
F 0 "C1" H 6975 2400 50  0000 L CNN
F 1 "0.47u" H 6975 2200 50  0000 L CNN
F 2 "" H 6988 2150 30  0000 C CNN
F 3 "" H 6950 2300 60  0000 C CNN
	1    6950 2300
	0    1    1    0   
$EndComp
$Comp
L eSim_GND #PWR01
U 1 1 5CE9074F
P 5000 3950
F 0 "#PWR01" H 5000 3700 50  0001 C CNN
F 1 "eSim_GND" H 5000 3800 50  0000 C CNN
F 2 "" H 5000 3950 50  0001 C CNN
F 3 "" H 5000 3950 50  0001 C CNN
	1    5000 3950
	1    0    0    -1  
$EndComp
$Comp
L DC-RESCUE-Integrator_LM_741 v3
U 1 1 5CE90750
P 6050 4250
F 0 "v3" H 5850 4350 60  0000 C CNN
F 1 "-15" H 5850 4200 60  0000 C CNN
F 2 "R1" H 5750 4250 60  0000 C CNN
F 3 "" H 6050 4250 60  0000 C CNN
	1    6050 4250
	0    1    1    0   
$EndComp
$Comp
L DC-RESCUE-Integrator_LM_741 v2
U 1 1 5CE90751
P 6050 1950
F 0 "v2" H 5850 2050 60  0000 C CNN
F 1 "+15" H 5850 1900 60  0000 C CNN
F 2 "R1" H 5750 1950 60  0000 C CNN
F 3 "" H 6050 1950 60  0000 C CNN
	1    6050 1950
	0    1    1    0   
$EndComp
$Comp
L PWR_FLAG #FLG02
U 1 1 5CE90752
P 4300 3650
F 0 "#FLG02" H 4300 3745 50  0001 C CNN
F 1 "PWR_FLAG" H 4300 3830 50  0000 C CNN
F 2 "" H 4300 3650 50  0000 C CNN
F 3 "" H 4300 3650 50  0000 C CNN
	1    4300 3650
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U1
U 1 1 5CE90753
P 5250 2950
F 0 "U1" H 5250 3450 60  0000 C CNN
F 1 "plot_v1" H 5450 3300 60  0000 C CNN
F 2 "" H 5250 2950 60  0000 C CNN
F 3 "" H 5250 2950 60  0000 C CNN
	1    5250 2950
	1    0    0    -1  
$EndComp
$Comp
L plot_v1 U2
U 1 1 5CE90754
P 7800 2900
F 0 "U2" H 7800 3400 60  0000 C CNN
F 1 "plot_v1" H 8000 3250 60  0000 C CNN
F 2 "" H 7800 2900 60  0000 C CNN
F 3 "" H 7800 2900 60  0000 C CNN
	1    7800 2900
	0    1    1    0   
$EndComp
Text GLabel 5100 2850 0    60   Input ~ 0
in
Text GLabel 7800 2700 1    60   Output ~ 0
out
$Comp
L eSim_R R2
U 1 1 5CE90755
P 7800 3250
F 0 "R2" H 7850 3380 50  0000 C CNN
F 1 "100" H 7850 3300 50  0000 C CNN
F 2 "" H 7850 3230 30  0000 C CNN
F 3 "" V 7850 3300 30  0000 C CNN
	1    7800 3250
	1    0    0    -1  
$EndComp
$Comp
L eSim_GND #PWR03
U 1 1 5CE90756
P 8100 4150
F 0 "#PWR03" H 8100 3900 50  0001 C CNN
F 1 "eSim_GND" H 8100 4000 50  0000 C CNN
F 2 "" H 8100 4150 50  0001 C CNN
F 3 "" H 8100 4150 50  0001 C CNN
	1    8100 4150
	1    0    0    -1  
$EndComp
$Comp
L sine v1
U 1 1 5CE93FC2
P 4550 3050
F 0 "v1" H 4350 3150 60  0000 C CNN
F 1 "sine" H 4350 3000 60  0000 C CNN
F 2 "R1" H 4250 3050 60  0000 C CNN
F 3 "" H 4550 3050 60  0000 C CNN
	1    4550 3050
	0    1    1    0   
$EndComp
Wire Wire Line
	5850 3050 6100 3050
Wire Wire Line
	5000 3050 5550 3050
Wire Wire Line
	5900 2300 5900 3050
Wire Wire Line
	5900 2300 6800 2300
Connection ~ 5900 3050
Wire Wire Line
	7100 2300 7600 2300
Wire Wire Line
	7600 2300 7600 3200
Wire Wire Line
	7200 3200 7700 3200
Wire Wire Line
	6500 1950 6500 2750
Wire Wire Line
	6500 4250 6500 3650
Wire Wire Line
	5600 3800 5600 4250
Wire Wire Line
	3400 3800 5600 3800
Wire Wire Line
	5000 3800 5000 3950
Wire Wire Line
	5600 1950 3400 1950
Wire Wire Line
	3400 1950 3400 3800
Connection ~ 5000 3800
Wire Wire Line
	4100 3050 3400 3050
Connection ~ 3400 3050
Wire Wire Line
	4300 3650 4300 3800
Connection ~ 4300 3800
Wire Wire Line
	5250 2750 5250 3050
Connection ~ 5250 3050
Wire Wire Line
	7600 2900 8000 2900
Connection ~ 7600 2900
Wire Wire Line
	7800 2900 7800 2700
Connection ~ 7800 2900
Wire Wire Line
	5100 2850 5250 2850
Connection ~ 5250 2850
Wire Wire Line
	6100 3300 5250 3300
Connection ~ 7600 3200
Wire Wire Line
	8000 3200 8100 3200
Wire Wire Line
	8100 3200 8100 4150
Connection ~ 5250 3800
Wire Wire Line
	5250 3300 5250 3800
$Comp
L eSim_R R3
U 1 1 5CECFFC5
P 6750 2700
F 0 "R3" H 6800 2830 50  0000 C CNN
F 1 "1k" H 6800 2750 50  0000 C CNN
F 2 "" H 6800 2680 30  0000 C CNN
F 3 "" V 6800 2750 30  0000 C CNN
	1    6750 2700
	1    0    0    -1  
$EndComp
$Comp
L eSim_R R4
U 1 1 5CED0012
P 7250 2700
F 0 "R4" H 7300 2830 50  0000 C CNN
F 1 "1.8533k" H 7300 2750 50  0000 C CNN
F 2 "" H 7300 2680 30  0000 C CNN
F 3 "" V 7300 2750 30  0000 C CNN
	1    7250 2700
	1    0    0    -1  
$EndComp
Wire Wire Line
	7450 2650 7550 2650
Wire Wire Line
	7550 2650 7550 2850
Wire Wire Line
	7550 2850 6700 2850
Wire Wire Line
	6950 2650 7150 2650
Wire Wire Line
	6650 2650 6600 2650
Wire Wire Line
	6600 2650 6600 2800
Wire Wire Line
	7050 2650 7050 4150
Wire Wire Line
	7050 4150 6500 4150
Connection ~ 6500 4150
Connection ~ 7050 2650
$Comp
L lm_741 X1
U 1 1 5CFB4761
P 6650 3200
F 0 "X1" H 6450 3200 60  0000 C CNN
F 1 "lm_741" H 6550 2950 60  0000 C CNN
F 2 "" H 6650 3200 60  0000 C CNN
F 3 "" H 6650 3200 60  0000 C CNN
	1    6650 3200
	1    0    0    -1  
$EndComp
$EndSCHEMATC
