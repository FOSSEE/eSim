# LTSpice To KiCad Converter by eSim Team

This code is referred from the following repository: https://github.com/laurentc2/LTspice2Kicad

This code is authored by Sumanto Kar, FOSSEE, IIT Bombay and the team members.

The repository contains program to convert LTSpice Schematics to KiCad Schematics.

The repository also contains program to convert LTSpice symbol files(.asy) to KiCad symbol files(.lib).

The code is supported by both Windows and Ubuntu(and flavors) Operating System.


## Cloning the repo:

To start with, please clone the repository:</br>
	```
	git clone https://github.com/FOSSEE/LTSpiceToKiCadConverter
	```

## Windows OS

### To Convert the Schematic file

1. Make sure python3 is installed and added to the path
2. Switch to src/Windows directory
3. Paste the LTspice file(.asc format) to be converted here
4. Double Click on the ```Sch_CreateBat.bat``` script
5. The LTspice schematic is converted to eSim(KiCad) schematic and project files
6. The files are saved in the src/Windows in a folder created with name ```LTspice_<schematic_name>```

-----------------------------------------------
### To Convert the .asy file to .lib file

1. Make sure python3 is installed and added to the path
2. Switch to src/Windows directory
3. Run the following command to convert the .asy files contained in a single folder to a .lib file:
	```
	python3 lib_LTspice2Kicad.py <Path to the folder containing the .asy files">
	```
	Example:
	```
	python3 lib_LTspice2Kicad.py "C:\Program Files\LTC\LTspiceXVII\lib\sym\DAC"
	```
	The .asy files will be converted a single .lib file with name LTspice_<folder_name>.lib. 
	For example: LTspice_DAC.lib</br>
4. To convert many folders containg .asy files:</br>
	- Edit the path in the ```lib_LTspice2Kicad.bat``` file using a text editor</br>
	- Save and close it</br>
	- Double click on the Batch files</br>
	- All the converted .lib files will be saved in the src/Windows


## Ubuntu OS

### To Convert the Schematic file

1. Make sure python3 is installed and added to the path
2. Switch to src/Ubuntu directory
3. Run the following command to convert the LTspice(.asc) files to KiCad Schematic(.sch, .pro and .proj) files:
    ```
    python3 sch_LTspice2Kicad.py <Path to the .asc file">
    ```
    For Example:
    ```
    python3 sch_LTspice2Kicad.py "/home/sumanto/Downloads/ltspice/ltspice/27C.asc"
    ```
4. The files are saved in a folder(in the same path where the original .asc file exists) created with name ```LTspice_<schematic_name>```

-----------------------------------------------
### To Convert the .asy file to .lib file

1. Make sure python3 is installed and added to the path
2. Switch to src/Ubuntu directory
3. Run the following command to convert the .asy files contained in a single folder to a .lib file:
	```
	python3 lib_LTspice2Kicad.py <Path to the folder containing the .asy files">
	```
	Example:
	```
	python3 lib_LTspice2Kicad.py "python3 lib_LTspice2Kicad.py /home/sumanto/Downloads/ltspice/libs/DAC"
	```
	The .asy files will be converted and save in src/Ubuntu to a single .lib file with name LTspice_<folder_name>.lib. 
	For example: LTspice_DAC.lib

-----------------------------------------------
### Example LTspice Schematics(.asc) and Symbol libraries(.asy)
The Example LTspice Schematics(.asc) and Symbol Libraries(.asy) are available in the LTspice software.

Please download the software from the official website.

## Converted KiCad Schematics(.sch, .pro, .proj)
The converted examples are available [here](https://github.com/FOSSEE/LTSpiceToKiCadConverter/tree/main/Examples/ConvertedKiCad_Schematics_no_eSim_Plots).


## Converted KiCad Schematics with eSim Simulation Plots
The Converted KiCad Schematics with eSim Simulation Plots are available [here](https://github.com/FOSSEE/LTSpiceToKiCadConverter/tree/main/Examples/ConvertedKiCadSchematics_witheSimPlots).

## Converted KiCad Symbol Library files(.lib)
The converted KiCad Symbol Library files are available [here](https://github.com/FOSSEE/LTSpiceToKiCadConverter/tree/main/Examples/ConvertedLibraries).


## Important Notes/Commands
**To change the access of the file and folder**

Use this command to change access to the files:</br>
	```
		chmod <options> <permissions> <file name>
	```</br> 
Example:</br>
	```
		chmod u=rwx,g=rx,o=r myfile
	```</br> 
You can also use:</br> 
	```	
		sudo chmod 777 filename.
	```</br> 
Example:</br>
	```
	sudo chmod 777 ~/Desktop/convert/rc
	```</br> 

-----------------------------------------------
**To open the KiCad schematic file in [eSim](https://esim.fossee.in/home)** 

1. Open eSim.
2. Create a *new project*.
3. Open the schematic using *open schematic* option.
4. Make sure all the libraries are loaded (9k+) using *Place component* option in eeschema.
5. Append the schematic using *Append Schematic* option from the file menu
6. Go to the directory where your files are converted.
7. Select the KiCad coverted schematic file (.sch). Click on Open.
8. To simulate, follow the instructions available on the eSim webpage.
-----------------------------------------------
**To load the KiCad libraries**

If all the libraries in eeschema are not loaded, follow these steps:
1. In eeschema, select *Preferences* option.
2. Click on the *Component Libraries* in the drop down list.
3. A dialog box appears, click on the *Add* option.
4. Go to the path where your library to be added is saved.
5. Select the library to be added and click on *Open* button.
6. Close the dialog box.
-----------------------------------------------

## Warning!
- All required libraries SHOULD be added.
- Use proper file format.
- DO NOT TRY TO CONVERT library file as schematic file or vice versa.
- Try adding libraries in the parser.py while getting error.
- DO NOT CHANGE any of the files unless and until needed.

## eSim Manual
To know everything about eSim, how it works and it's feature please download the manual from [here](https://static.fossee.in/esim/manuals/eSim_Manual_2.3.pdf)

## Contact
For any queries regarding eSim please write us on at this [email address](mailto:contact-esim@fossee.in).

## Contribution
Please refer [here](https://github.com/FOSSEE/eSim/blob/master/CONTRIBUTION.md) for further details.

# License
It is developed by FOSSEE Team at IIT Bombay and is released under GNU GPL License.

