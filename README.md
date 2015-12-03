##eSim

eSim is an open source EDA tool for circuit design, simulation, analysis and PCB design, developed by FOSSEE team at IIT Bombay. 
It is an integrated tool build using open source software such as Kicad (http://www.kicad-pcd.org), Ngspice (http://ngspice.sourcefouge.net/) 
It is released under GNU GPL License. It runs on Ubuntu Linux, Windows XP and Windows.

eSim has been successfully ported to low cost FOSSEE laptop (http://laptop.fossee.in)

##Pre-requisites
1. Python 2.7
2. PyQt4
3. Matplotlib
4. NgSpice 
5. Kicad (Latest Version build on July-14)

## eSim Installation Ubuntu
Refer INSTALL file for eSim installation on Ubuntu.

## How to get the openModelica and Pspice to Kicad converter changes in windows.
This changes is not available in the current windows installer. However you can get those changes manually after replacing eSim folder with new folder eSim folder which contains the changes.
Please follow the steps
1. Download and install eSim on windows from eSim website.
2. Download the latest eSim code from https://github.com/FOSSEE/eSim/archive/develop.zip
3. Extract the zip and copy only the src and images directory
4. Now go to the location where eSim on windows is installed (By default it is in C:) And then just replace src and image directory with the one you just copied.



