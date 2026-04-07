#!/bin/sh
gcc -c ghdlserver.c
ghdl -a Utility_Package.vhdl && 
ghdl -a Vhpi_Package.vhdl 


