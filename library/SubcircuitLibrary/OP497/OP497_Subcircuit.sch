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
LIBS:OP497_Subcircuit-cache
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
L resistor R1
U 1 1 679F6A14
P 1680 3080
F 0 "R1" H 1730 3210 50  0000 C CNN
F 1 "2.5k" H 1730 3030 50  0000 C CNN
F 2 "" H 1730 3060 30  0000 C CNN
F 3 "" V 1730 3130 30  0000 C CNN
	1    1680 3080
	1    0    0    -1  
$EndComp
$Comp
L eSim_NPN Q1
U 1 1 679F6B29
P 2200 3240
F 0 "Q1" H 2100 3290 50  0000 R CNN
F 1 "eSim_NPN" H 2150 3390 50  0000 R CNN
F 2 "" H 2400 3340 29  0000 C CNN
F 3 "" H 2200 3240 60  0000 C CNN
	1    2200 3240
	0    1    1    0   
$EndComp
$Comp
L eSim_NPN Q2
U 1 1 679F6B86
P 2460 3680
F 0 "Q2" H 2360 3730 50  0000 R CNN
F 1 "eSim_NPN" H 2410 3830 50  0000 R CNN
F 2 "" H 2660 3780 29  0000 C CNN
F 3 "" H 2460 3680 60  0000 C CNN
	1    2460 3680
	0    1    -1   0   
$EndComp
$Comp
L eSim_NPN Q3
U 1 1 679F6C10
P 2970 3030
F 0 "Q3" H 2870 3080 50  0000 R CNN
F 1 "eSim_NPN" H 2920 3180 50  0000 R CNN
F 2 "" H 3170 3130 29  0000 C CNN
F 3 "" H 2970 3030 60  0000 C CNN
	1    2970 3030
	1    0    0    -1  
$EndComp
$Comp
L resistor R2
U 1 1 679F6C82
P 1700 3630
F 0 "R2" H 1750 3760 50  0000 C CNN
F 1 "2.5k" H 1750 3580 50  0000 C CNN
F 2 "" H 1750 3610 30  0000 C CNN
F 3 "" V 1750 3680 30  0000 C CNN
	1    1700 3630
	1    0    0    -1  
$EndComp
$Comp
L resistor R3
U 1 1 67A21583
P 2850 3470
F 0 "R3" H 2900 3600 50  0000 C CNN
F 1 "10k" H 2900 3420 50  0000 C CNN
F 2 "" H 2900 3450 30  0000 C CNN
F 3 "" V 2900 3520 30  0000 C CNN
	1    2850 3470
	1    0    0    -1  
$EndComp
$Comp
L eSim_NPN Q6
U 1 1 67A215FD
P 3850 3030
F 0 "Q6" H 3750 3080 50  0000 R CNN
F 1 "eSim_NPN" H 3800 3180 50  0000 R CNN
F 2 "" H 4050 3130 29  0000 C CNN
F 3 "" H 3850 3030 60  0000 C CNN
	1    3850 3030
	-1   0    0    -1  
$EndComp
$Comp
L eSim_NPN Q4
U 1 1 67A216BC
P 3170 2530
F 0 "Q4" H 3070 2580 50  0000 R CNN
F 1 "eSim_NPN" H 3120 2680 50  0000 R CNN
F 2 "" H 3370 2630 29  0000 C CNN
F 3 "" H 3170 2530 60  0000 C CNN
	1    3170 2530
	-1   0    0    -1  
$EndComp
$Comp
L eSim_NPN Q5
U 1 1 67A21748
P 3650 2530
F 0 "Q5" H 3550 2580 50  0000 R CNN
F 1 "eSim_NPN" H 3600 2680 50  0000 R CNN
F 2 "" H 3850 2630 29  0000 C CNN
F 3 "" H 3650 2530 60  0000 C CNN
	1    3650 2530
	1    0    0    -1  
$EndComp
$Comp
L resistor R4
U 1 1 67A21A6B
P 3020 1770
F 0 "R4" H 3070 1900 50  0000 C CNN
F 1 "10k" H 3070 1720 50  0000 C CNN
F 2 "" H 3070 1750 30  0000 C CNN
F 3 "" V 3070 1820 30  0000 C CNN
	1    3020 1770
	0    1    1    0   
$EndComp
$Comp
L resistor R5
U 1 1 67A21AD4
P 3700 1770
F 0 "R5" H 3750 1900 50  0000 C CNN
F 1 "10k" H 3750 1720 50  0000 C CNN
F 2 "" H 3750 1750 30  0000 C CNN
F 3 "" V 3750 1820 30  0000 C CNN
	1    3700 1770
	0    1    1    0   
$EndComp
$Comp
L eSim_NPN Q8
U 1 1 67A21C5A
P 4260 2530
F 0 "Q8" H 4160 2580 50  0000 R CNN
F 1 "eSim_NPN" H 4210 2680 50  0000 R CNN
F 2 "" H 4460 2630 29  0000 C CNN
F 3 "" H 4260 2530 60  0000 C CNN
	1    4260 2530
	1    0    0    -1  
$EndComp
$Comp
L eSim_PNP Q7
U 1 1 67A21DA2
P 3970 4290
F 0 "Q7" H 3870 4340 50  0000 R CNN
F 1 "eSim_PNP" H 3920 4440 50  0000 R CNN
F 2 "" H 4170 4390 29  0000 C CNN
F 3 "" H 3970 4290 60  0000 C CNN
	1    3970 4290
	1    0    0    1   
$EndComp
$Comp
L eSim_NPN Q9
U 1 1 67A21DFE
P 4490 4100
F 0 "Q9" H 4390 4150 50  0000 R CNN
F 1 "eSim_NPN" H 4440 4250 50  0000 R CNN
F 2 "" H 4690 4200 29  0000 C CNN
F 3 "" H 4490 4100 60  0000 C CNN
	1    4490 4100
	-1   0    0    -1  
$EndComp
$Comp
L eSim_PNP Q10
U 1 1 67A220BA
P 4950 3400
F 0 "Q10" H 4850 3450 50  0000 R CNN
F 1 "eSim_PNP" H 4900 3550 50  0000 R CNN
F 2 "" H 5150 3500 29  0000 C CNN
F 3 "" H 4950 3400 60  0000 C CNN
	1    4950 3400
	-1   0    0    1   
$EndComp
$Comp
L eSim_PNP Q12
U 1 1 67A221C2
P 5380 3390
F 0 "Q12" H 5280 3440 50  0000 R CNN
F 1 "eSim_PNP" H 5330 3540 50  0000 R CNN
F 2 "" H 5580 3490 29  0000 C CNN
F 3 "" H 5380 3390 60  0000 C CNN
	1    5380 3390
	-1   0    0    1   
$EndComp
$Comp
L eSim_PNP Q14
U 1 1 67A22250
P 5810 3380
F 0 "Q14" H 5710 3430 50  0000 R CNN
F 1 "eSim_PNP" H 5760 3530 50  0000 R CNN
F 2 "" H 6010 3480 29  0000 C CNN
F 3 "" H 5810 3380 60  0000 C CNN
	1    5810 3380
	-1   0    0    1   
$EndComp
$Comp
L eSim_PNP Q11
U 1 1 67A2261A
P 5370 2750
F 0 "Q11" H 5270 2800 50  0000 R CNN
F 1 "eSim_PNP" H 5320 2900 50  0000 R CNN
F 2 "" H 5570 2850 29  0000 C CNN
F 3 "" H 5370 2750 60  0000 C CNN
	1    5370 2750
	-1   0    0    1   
$EndComp
$Comp
L eSim_PNP Q13
U 1 1 67A22620
P 5800 2740
F 0 "Q13" H 5700 2790 50  0000 R CNN
F 1 "eSim_PNP" H 5750 2890 50  0000 R CNN
F 2 "" H 6000 2840 29  0000 C CNN
F 3 "" H 5800 2740 60  0000 C CNN
	1    5800 2740
	-1   0    0    1   
$EndComp
$Comp
L capacitor C1
U 1 1 67A2272A
P 5430 1840
F 0 "C1" H 5455 1940 50  0000 L CNN
F 1 "10nF" H 5455 1740 50  0000 L CNN
F 2 "" H 5468 1690 30  0000 C CNN
F 3 "" H 5430 1840 60  0000 C CNN
	1    5430 1840
	1    0    0    -1  
$EndComp
$Comp
L eSim_PNP Q15
U 1 1 67A22875
P 6960 2230
F 0 "Q15" H 6860 2280 50  0000 R CNN
F 1 "eSim_PNP" H 6910 2380 50  0000 R CNN
F 2 "" H 7160 2330 29  0000 C CNN
F 3 "" H 6960 2230 60  0000 C CNN
	1    6960 2230
	1    0    0    1   
$EndComp
$Comp
L eSim_PNP Q18
U 1 1 67A22B87
P 7930 2230
F 0 "Q18" H 7830 2280 50  0000 R CNN
F 1 "eSim_PNP" H 7880 2380 50  0000 R CNN
F 2 "" H 8130 2330 29  0000 C CNN
F 3 "" H 7930 2230 60  0000 C CNN
	1    7930 2230
	-1   0    0    1   
$EndComp
$Comp
L capacitor C2
U 1 1 67A22C9D
P 7460 2650
F 0 "C2" H 7485 2750 50  0000 L CNN
F 1 "10pF" H 7485 2550 50  0000 L CNN
F 2 "" H 7498 2500 30  0000 C CNN
F 3 "" H 7460 2650 60  0000 C CNN
	1    7460 2650
	1    0    0    -1  
$EndComp
$Comp
L resistor R6
U 1 1 67A22D3A
P 7410 3080
F 0 "R6" H 7460 3210 50  0000 C CNN
F 1 "10k" H 7460 3030 50  0000 C CNN
F 2 "" H 7460 3060 30  0000 C CNN
F 3 "" V 7460 3130 30  0000 C CNN
	1    7410 3080
	0    1    1    0   
$EndComp
$Comp
L eSim_Diode D1
U 1 1 67A23102
P 6490 2720
F 0 "D1" H 6490 2820 50  0000 C CNN
F 1 "eSim_Diode" H 6490 2620 50  0000 C CNN
F 2 "" H 6490 2720 60  0000 C CNN
F 3 "" H 6490 2720 60  0000 C CNN
	1    6490 2720
	0    1    1    0   
$EndComp
$Comp
L eSim_Diode D2
U 1 1 67A232E0
P 6490 3080
F 0 "D2" H 6490 3180 50  0000 C CNN
F 1 "eSim_Diode" H 6490 2980 50  0000 C CNN
F 2 "" H 6490 3080 60  0000 C CNN
F 3 "" H 6490 3080 60  0000 C CNN
	1    6490 3080
	0    1    1    0   
$EndComp
$Comp
L eSim_NPN Q16
U 1 1 67A23B3C
P 7160 3870
F 0 "Q16" H 7060 3920 50  0000 R CNN
F 1 "eSim_NPN" H 7110 4020 50  0000 R CNN
F 2 "" H 7360 3970 29  0000 C CNN
F 3 "" H 7160 3870 60  0000 C CNN
	1    7160 3870
	-1   0    0    -1  
$EndComp
$Comp
L eSim_NPN Q17
U 1 1 67A23DFE
P 7660 3870
F 0 "Q17" H 7560 3920 50  0000 R CNN
F 1 "eSim_NPN" H 7610 4020 50  0000 R CNN
F 2 "" H 7860 3970 29  0000 C CNN
F 3 "" H 7660 3870 60  0000 C CNN
	1    7660 3870
	1    0    0    -1  
$EndComp
$Comp
L capacitor C3
U 1 1 67A23EC8
P 8160 4370
F 0 "C3" H 8185 4470 50  0000 L CNN
F 1 "10nF" H 8185 4270 50  0000 L CNN
F 2 "" H 8198 4220 30  0000 C CNN
F 3 "" H 8160 4370 60  0000 C CNN
	1    8160 4370
	1    0    0    -1  
$EndComp
$Comp
L eSim_NPN Q19
U 1 1 67A24065
P 8510 3310
F 0 "Q19" H 8410 3360 50  0000 R CNN
F 1 "eSim_NPN" H 8460 3460 50  0000 R CNN
F 2 "" H 8710 3410 29  0000 C CNN
F 3 "" H 8510 3310 60  0000 C CNN
	1    8510 3310
	1    0    0    -1  
$EndComp
$Comp
L eSim_PNP Q21
U 1 1 67A242DB
P 9270 4120
F 0 "Q21" H 9170 4170 50  0000 R CNN
F 1 "eSim_PNP" H 9220 4270 50  0000 R CNN
F 2 "" H 9470 4220 29  0000 C CNN
F 3 "" H 9270 4120 60  0000 C CNN
	1    9270 4120
	1    0    0    1   
$EndComp
$Comp
L eSim_PNP Q23
U 1 1 67A243EE
P 9750 4120
F 0 "Q23" H 9650 4170 50  0000 R CNN
F 1 "eSim_PNP" H 9700 4270 50  0000 R CNN
F 2 "" H 9950 4220 29  0000 C CNN
F 3 "" H 9750 4120 60  0000 C CNN
	1    9750 4120
	1    0    0    1   
$EndComp
$Comp
L eSim_Diode D3
U 1 1 67A244FA
P 9370 3310
F 0 "D3" H 9370 3410 50  0000 C CNN
F 1 "eSim_Diode" H 9370 3210 50  0000 C CNN
F 2 "" H 9370 3310 60  0000 C CNN
F 3 "" H 9370 3310 60  0000 C CNN
	1    9370 3310
	0    1    1    0   
$EndComp
$Comp
L eSim_NPN Q20
U 1 1 67A247E0
P 9170 2560
F 0 "Q20" H 9070 2610 50  0000 R CNN
F 1 "eSim_NPN" H 9120 2710 50  0000 R CNN
F 2 "" H 9370 2660 29  0000 C CNN
F 3 "" H 9170 2560 60  0000 C CNN
	1    9170 2560
	-1   0    0    -1  
$EndComp
$Comp
L eSim_NPN Q22
U 1 1 67A24B4B
P 9570 2210
F 0 "Q22" H 9470 2260 50  0000 R CNN
F 1 "eSim_NPN" H 9520 2360 50  0000 R CNN
F 2 "" H 9770 2310 29  0000 C CNN
F 3 "" H 9570 2210 60  0000 C CNN
	1    9570 2210
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 1 1 67A24ED7
P 1050 3030
F 0 "U1" H 1100 3130 30  0000 C CNN
F 1 "PORT" H 1050 3030 30  0000 C CNN
F 2 "" H 1050 3030 60  0000 C CNN
F 3 "" H 1050 3030 60  0000 C CNN
	1    1050 3030
	1    0    0    -1  
$EndComp
$Comp
L PORT U1
U 2 1 67A2506E
P 1050 3580
F 0 "U1" H 1100 3680 30  0000 C CNN
F 1 "PORT" H 1050 3580 30  0000 C CNN
F 2 "" H 1050 3580 60  0000 C CNN
F 3 "" H 1050 3580 60  0000 C CNN
	2    1050 3580
	1    0    0    -1  
$EndComp
Wire Wire Line
	1580 3030 1300 3030
Wire Wire Line
	1600 3580 1300 3580
Wire Wire Line
	2770 3030 1880 3030
Connection ~ 2200 3030
Wire Wire Line
	2000 3340 2000 3880
Wire Wire Line
	2000 3580 1900 3580
Wire Wire Line
	2000 3880 2830 3880
Connection ~ 2000 3580
Wire Wire Line
	2200 3580 2260 3580
Wire Wire Line
	2200 3580 2200 3030
Wire Wire Line
	2660 3580 2660 3340
Wire Wire Line
	2660 3340 2400 3340
Wire Wire Line
	2750 3420 2660 3420
Connection ~ 2660 3420
Wire Wire Line
	3750 3230 3070 3230
Wire Wire Line
	3070 2830 3070 2730
Wire Wire Line
	3750 2830 3750 2730
Wire Wire Line
	3370 2530 3450 2530
Wire Wire Line
	3070 2330 3070 1970
Wire Wire Line
	3750 2330 3750 1970
Wire Wire Line
	4060 2530 4060 2500
Wire Wire Line
	4060 2500 3410 2500
Wire Wire Line
	3410 2500 3410 2530
Connection ~ 3410 2530
Wire Wire Line
	7060 2030 7060 2010
Wire Wire Line
	7060 2010 7830 2010
Wire Wire Line
	7830 2010 7830 2030
Wire Wire Line
	5270 2550 5270 2510
Wire Wire Line
	5130 2510 5700 2510
Wire Wire Line
	5700 2510 5700 2540
Wire Wire Line
	9670 2010 9670 1590
Wire Wire Line
	3070 1590 3070 1670
Wire Wire Line
	3750 1670 3750 1590
Connection ~ 3750 1590
Wire Wire Line
	4360 2330 4360 1590
Connection ~ 4360 1590
Wire Wire Line
	5430 1690 5430 1590
Connection ~ 5430 1590
Wire Wire Line
	6760 2230 3070 2230
Connection ~ 3070 2230
Wire Wire Line
	5430 1990 5430 2230
Connection ~ 5430 2230
Wire Wire Line
	8130 2230 8240 2230
Wire Wire Line
	8240 2230 8240 2460
Wire Wire Line
	8240 2460 5860 2460
Wire Wire Line
	5860 2460 5860 2290
Wire Wire Line
	5860 2290 3750 2290
Connection ~ 3750 2290
Wire Wire Line
	4360 2310 3940 2310
Wire Wire Line
	3940 2310 3940 2730
Connection ~ 3940 2500
Connection ~ 4360 2310
Wire Wire Line
	4070 4090 4070 3580
Wire Wire Line
	4070 3580 4360 3580
Wire Wire Line
	4360 3580 4360 2730
Wire Wire Line
	5710 3180 5710 3140
Wire Wire Line
	5710 3140 4850 3140
Wire Wire Line
	4850 3140 4850 3200
Wire Wire Line
	5280 3090 5280 3190
Connection ~ 5280 3140
Wire Wire Line
	5270 2950 5270 3090
Wire Wire Line
	5270 3090 5280 3090
Wire Wire Line
	5270 3050 4480 3050
Wire Wire Line
	4480 3050 4480 3870
Wire Wire Line
	4480 3870 4390 3870
Wire Wire Line
	4390 3870 4390 3900
Connection ~ 5270 3050
Wire Wire Line
	2830 3600 4850 3600
Wire Wire Line
	2830 3880 2830 3600
Connection ~ 2460 3880
Wire Wire Line
	5280 3800 5280 3590
Wire Wire Line
	2710 3800 5280 3800
Wire Wire Line
	2710 3800 2710 3030
Connection ~ 2710 3030
Wire Wire Line
	5710 3580 5710 4100
Wire Wire Line
	5710 4100 4690 4100
Wire Wire Line
	9850 4320 9850 4980
Wire Wire Line
	3400 4980 3400 3230
Connection ~ 3400 3230
Wire Wire Line
	3770 4290 3400 4290
Connection ~ 3400 4290
Wire Wire Line
	4390 4300 3660 4300
Wire Wire Line
	3660 4300 3660 4290
Connection ~ 3660 4290
Wire Wire Line
	4070 4490 4070 4980
Connection ~ 4070 4980
Wire Wire Line
	6000 2740 6100 2740
Wire Wire Line
	6100 2740 6100 4980
Connection ~ 6100 4980
Wire Wire Line
	5570 2750 5570 2990
Wire Wire Line
	5570 2990 6030 2990
Wire Wire Line
	6030 2990 6030 2740
Connection ~ 6030 2740
Wire Wire Line
	5700 2940 5700 3070
Wire Wire Line
	5700 3070 6100 3070
Connection ~ 6100 3070
Wire Wire Line
	5150 3400 5150 3710
Wire Wire Line
	5150 3710 6080 3710
Wire Wire Line
	6080 3710 6080 3380
Wire Wire Line
	6010 3380 6490 3380
Wire Wire Line
	5580 3390 5580 3650
Wire Wire Line
	5580 3650 6040 3650
Wire Wire Line
	6040 3650 6040 3380
Connection ~ 6040 3380
Wire Wire Line
	6490 2870 6490 2930
Wire Wire Line
	6490 2570 5780 2570
Wire Wire Line
	5780 2570 5780 2430
Wire Wire Line
	5780 2430 4910 2430
Wire Wire Line
	5130 2430 5130 2510
Connection ~ 5270 2510
Wire Wire Line
	4910 2430 4910 2730
Wire Wire Line
	4910 2730 3940 2730
Connection ~ 5130 2430
Wire Wire Line
	6490 3230 6490 4980
Connection ~ 6490 4980
Connection ~ 6490 3380
Connection ~ 6080 3380
Wire Wire Line
	7060 2430 7060 3670
Wire Wire Line
	7460 3870 7360 3870
Wire Wire Line
	7410 3870 7410 3610
Wire Wire Line
	7410 3610 7060 3610
Connection ~ 7060 3610
Connection ~ 7410 3870
Wire Wire Line
	7060 4070 7060 4980
Connection ~ 7060 4980
Wire Wire Line
	7760 4070 7760 4140
Wire Wire Line
	7060 4140 7800 4140
Connection ~ 7060 4140
Wire Wire Line
	9070 4120 7800 4120
Wire Wire Line
	7800 4120 7800 4140
Connection ~ 7760 4140
Wire Wire Line
	8610 3510 8610 4490
Connection ~ 8610 4120
Wire Wire Line
	7460 3310 8310 3310
Wire Wire Line
	7760 3310 7760 3670
Wire Wire Line
	7460 3280 7460 3310
Connection ~ 7760 3310
Wire Wire Line
	8160 4220 8160 3310
Connection ~ 8160 3310
Wire Wire Line
	7830 2430 7830 3040
Wire Wire Line
	7830 3040 7950 3040
Wire Wire Line
	7950 3040 7950 3310
Connection ~ 7950 3310
Wire Wire Line
	7460 2980 7460 2800
Wire Wire Line
	7460 2500 7460 2460
Connection ~ 7460 2460
Wire Wire Line
	7430 2010 7430 1590
Connection ~ 7430 1590
Connection ~ 7430 2010
Wire Wire Line
	9070 2760 9070 2900
Wire Wire Line
	9070 2900 8610 2900
Wire Wire Line
	8610 2900 8610 3110
Wire Wire Line
	9070 2360 9070 1590
Connection ~ 9070 1590
Wire Wire Line
	9370 1590 9370 3160
Connection ~ 9370 1590
Connection ~ 9370 2210
Connection ~ 9370 2560
Wire Wire Line
	9370 3920 9370 3460
Wire Wire Line
	8160 4520 8160 4980
Connection ~ 8160 4980
Wire Wire Line
	9370 4320 9370 4980
Connection ~ 9370 4980
Wire Wire Line
	9550 4120 9550 4490
Wire Wire Line
	9550 4490 8610 4490
Wire Wire Line
	9670 2410 9850 2410
Wire Wire Line
	9850 2410 9850 3920
Wire Wire Line
	10470 3140 9850 3140
Connection ~ 9850 3140
Connection ~ 9670 1590
Connection ~ 9850 4980
Wire Wire Line
	3050 3420 4360 3420
Connection ~ 4360 3420
Wire Wire Line
	4050 3030 4260 3030
Wire Wire Line
	4260 3030 4260 3600
Connection ~ 4260 3600
Wire Wire Line
	3070 1590 9970 1590
Wire Wire Line
	3400 4980 10080 4980
$Comp
L PORT U1
U 3 1 67A3C939
P 10720 3140
F 0 "U1" H 10770 3240 30  0000 C CNN
F 1 "PORT" H 10720 3140 30  0000 C CNN
F 2 "" H 10720 3140 60  0000 C CNN
F 3 "" H 10720 3140 60  0000 C CNN
	3    10720 3140
	-1   0    0    1   
$EndComp
$Comp
L PORT U1
U 4 1 67A3DAF1
P 10220 1590
F 0 "U1" H 10270 1690 30  0000 C CNN
F 1 "PORT" H 10220 1590 30  0000 C CNN
F 2 "" H 10220 1590 60  0000 C CNN
F 3 "" H 10220 1590 60  0000 C CNN
	4    10220 1590
	-1   0    0    1   
$EndComp
$Comp
L PORT U1
U 5 1 67A3DE72
P 10330 4980
F 0 "U1" H 10380 5080 30  0000 C CNN
F 1 "PORT" H 10330 4980 30  0000 C CNN
F 2 "" H 10330 4980 60  0000 C CNN
F 3 "" H 10330 4980 60  0000 C CNN
	5    10330 4980
	-1   0    0    1   
$EndComp
$EndSCHEMATC
