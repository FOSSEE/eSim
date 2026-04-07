![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/fossee/nghdl?color=blueviolet)
![Python](https://img.shields.io/badge/python-v3.6+-blue.svg)
[![PEP8](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)
[![GitHub forks](https://img.shields.io/github/forks/fossee/nghdl)](https://github.com/fossee/nghdl/network)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat)](https://github.com/fossee/nghdl)
![GitHub contributors](https://img.shields.io/github/contributors/fossee/nghdl)


Ngspice Ghdl Interfacing Documentation 
====

It contains all the documentation for Ngspice and GHDL related work.


## How is Ngspice interfaced with GHDL?
Ngspice supports mixed-signal simulation. It can simulate both digital and analog components.

Ngspice has something called code-model which defines the behavior of your component and can be used in the netlist. For example you can create a full-adder's code-model in Ngspice and use it in any circuit netlist of Ngspice.

Now the question is if we already have digital model creation in Ngspice, then why this interfacing?

Well, in Ngspice, it is difficult to write your own digital code-models. Though, many people are familiar with GHDL and can easily write the VHDL code.
So the idea of interfacing is just to write VHDL code for a model and use it as a dummy model in Ngspice. Thus, whenever Ngspice looks for that model, it will actually call GHDL to get the results.
GHDL's foreign language interface is used for this inter-process communication.


## Releases
* Ubuntu 18.04 and 20.04 LTS versions.
* Microsoft Windows 7, 8 and 10.

    > Note for other distributions: You can refer [`installers`](https://github.com/fossee/nghdl/tree/installers) branch for documentation on packaging (for above mentioned distributions) to build installers for your operating system in a similar way. For providing your build, please check the `Contribution` section mentioned below.


## Features
* Support for nearly 500 VHDL digital models.
* Support for VHDL digital models upto 64 output ports/pins.
* Support for Verilog digital models.


## Pre-requisites
* [GHDL (LLVM - v0.37)](http://ghdl.free.fr/)
* [Verilator (v4.210)](https://www.veripool.org/verilator/)
* [Ngspice (v35+)](https://ngspice.sourceforge.io/)


## How to install?
This module is made available with eSim (Electronic Circuit Simulation). 
Refer https://esim.fossee.in/ for more information.


## How to use the Examples provided with NGHDL?
1. Launch eSim --> Click on "NGHDL" icon from the left toolbar --> Click on "Browse" button --> Go to `nghdl/Example/`
2. Locate the example you wish to simulate, find the VHDL file within that example and click on "Open" button at the bottom of "Open File" window.
3. Click on "Upload" button in the NGHDL window. File will be processed in the backend for few seconds. Now exit the NGHDL window.
4. Open the desired example under `eSim/Examples/Mixed_Signal/` using the "Open Project" button, double click on the project when the project is loaded in the "Projects" window.
5. Click on the "Simulation" button on eSim Main window.


## Contribution
Please refer [here](https://github.com/FOSSEE/nghdl/blob/master/CONTRIBUTION.md) for further details.
