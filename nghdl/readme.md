Ngspice Ghdl Interfacing Documentation 
====

It contains all the documenation for Ngspice and Ghdl related work.

Note: This project is still in alpha version and has been tested for basic digital components.
====

## What exactly interfacing of ngspice ghdl do?
Ngspice support mixed mode simulation. It can simulate both digital and analog component. 

Ngspice has something called model which define the functionality of your circuit,which can be used in the netlist. For example you can create adder model in ngspice and use it in any circuit netlist of ngspice.

Now the question is if we already have digital model in ngspice why this interfacing ?
Well in ngspice it is little tediouse to write your digital model. But many people are familiar with ghdl and can easily write the vhdl code.
So the idea of interfacing is just to write ghdl code for a model and install it as dummy model in ngspice. So whenever ngspice look 
for that model it will actually call the ghdl to get the result.


##Pre-requisites
1. Ubuntu 12.04 (You can try it on other version and let us know)
2. Python 2.7
3. PyQt4


##How to install?
1. Clone this repository.
2. Run `./install-nghdl.sh` It will install ngspice from source code and put it in $HOME.
3. Set ngspice path in `.bashrc` file. Add `export PATH=/home/{your-username}/ngspice-26/install_dir/bin:$PATH` line in .bashrc

##Few words about installed code structure.
1. Ngspice will be installed in home directory $HOME. If you already have ngspice-26 directory there it will take its backup.
2. Source code for all other file will be present in ~/.esim-nghdl
3. symlink nghdl is stored in /usr/local/bin

##How to use?
1. Run nghdl in command terminal.
2. Upload your vhdl file.
3. Model will be created with name of your vhdl file. It can be seen under (~ngspice-26/src/xspice/icm/ghdl/)
4. You can use this model in your netlist.

##LIMITATION:
1. You can use only one output port in your file.
2. All the port should be std_logic_vector only.
3. We can use only one instance of code model in netlist.

##FUTURE WORK
1. Make changes to have more than one output.
2. Making changes to include use of more than one instance of code models.
3. Interfacing it with eSim formely known as Oscad so that we can use it in our schematic.

