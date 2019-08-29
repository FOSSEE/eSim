#!/bin/sh
gcc -c ghdlserver.c
ghdl -a Utility_Package.vhdl && 
ghdl -a Vhpi_Package.vhdl &&
ghdl -a inverter.vhdl &&
ghdl -a inverter_tb.vhdl  &&

ghdl -e -Wl,ghdlserver.o inverter_tb &&
./inverter_tb 

