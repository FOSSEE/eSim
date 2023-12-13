# eSim_PSpice_to_KiCad_Python_Parser

This code is written by Suryavamsi Tenetti, FOSSEE, IIT Bombay and modified by Sumanto Kar and Gloria Nandihal, FOSSEE, IIT Bombay.

This program converts PSpice schematic files (.sch) to KiCad schematic files (.sch)

This program converts PSpice library files (.slb) to KiCad library files (.lib)

USAGE:

-----------------------------------------------
**Make sure the python 3 compiler is installed in the PC**

Run the following command in the terminal in order to install it.

$ sudo apt install python3.7

-----------------------------------------------
**To download the eSim_PSpice_to_KiCad_Python_Parser**

Clone or Download the *eSim_PSpice_to_KiCad_Python_Parser* from the Git in the Home folder(or any other folder) of the local computer.

-----------------------------------------------
**To convert the PSpice library(.slb) files to KiCad library(.lib) files**

Set the path where the *libparser.py* file is located. It is located at */eSim_PSpice_to_KiCad_Python_Parser/lib/PythonLib*

$ python3 libParser.py <path to the pspice lib file(slb)> <output_library_name_without_extension> 

Example:
$ python3 libParser.py ~/Home/eSim_PSpice_to_KiCad_Python_Parser/libray/analog.slb analog

This will create analog.lib file and save it in the path </Home/eSim_PSpice_to_KiCad_Python_Parser/libray/>

-----------------------------------------------
**To convert the PSpice schematic files to KiCad schematic files**

Set the path where the *parser.py* file is located. It is located at */eSim_PSpice_to_KiCad_Python_Parser/lib/PythonLib*

$ python3 parser.py <path/to/pspice-schematic.sch> <path/to/output-project-name-without-extension>

Example:
$ python3 parser.py ~/Desktop/pspice/rc.sch ~/Desktop/convert/rc

This will create a folder rc at the location /Desktop/convert/. The directory will have  rc.sch, rc.proj and rc.pro.
The directory will have read only access. You need to use chmod command to change the access.

--------------------------------------------------------
**To change the access of the file and folder**

Use this command to change access to the files:

chmod <options> <permissions> <file name>
Example:
chmod u=rwx,g=rx,o=r myfile

You can also use: 

sudo chmod 777 filename.

Example: sudo chmod 777 ~/Desktop/convert/rc

-----------------------------------------------
**To open the KiCad schematic file in eSim** 

1. Open eSim.
2. Create a *new project*.
3. Open the schematic using *open schematic* option.
4. Make sure all the libraries are loaded (9k+) using *Place component* option in eeschema.
5. Append the schematic using *Append Schematic* option from the file menu
6. Go to the directory where your files are converted.
7. Select the KiCad coverted schematic file (.sch). Click on Open.
8. To simulate, follow the instructions available on the eSim webpage
    https://esim.fossee.in/pspice-to-kicad
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
**To add libraries in the parser.py**

Open the *parser.py* python file. It is located at */eSim_PSpice_to_KiCad_Python_Parser/lib/PythonLib*
Type and add the libraries in the variables *"descr"* and *"prodescr"*

-----------------------------------------------
**WARNING**

1. Filenames should NOT contain whitespaces or tabs.
2. All required libraries SHOULD be added.
3. Use proper file format.
4. DO NOT TRY TO CONVERT library file as schematic file or vice versa.
5. Try adding libraries in the parser.py while getting error.
6. DO NOT CHANGE any of the files unless and until needed.



