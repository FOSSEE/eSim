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

##Installing and setting PATH for eSim
1. Clone this repository or download it as zip file.
2. set PYTHONPATH
    - For Linux :
        Open .bashrc file and add this line.

        `export PYTHONPATH=$PYTHONPATH:/path-to-your-downloaded-folder/eSim/src`

    - For Window :
        set environment variable `PYHTONPATH` with complete path to your eSim/src


##How to run eSim ?
1. Using command line or terminal go to location eSim/src/frontEnd
2. Type below command to open eSim
    - `python Application.py`


##How to install latest version of kicad in Ubuntu ?
1. `sudo add-apt-repository ppa:js-reynaud/ppa-kicad`

2. `sudo apt-get update`

3. `sudo apt-get install kicad`


##How to install ngspice in Ubuntu?

    `sudo apt-get install ngspice`



