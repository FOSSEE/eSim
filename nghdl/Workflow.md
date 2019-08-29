1.  When `nghdl` button clicked in `eSim` it calls the `ngspice_ghdl.py` from `nghdl` installed directory
- `ngspice_ghdl.py` defines the UI for nghdl, and the functionality of each button
- When `Upload` clicked, it calls `uploadModle` function from `ngspice_ghdl.py`
- Similarly functions called on each button click defined
- `uploadModle` inturn calls these 5 functions sequentially =>
- - createModelDirectory()
- - addingModelInModpath()
- - createModelFiles()
- - runMake()
- - runMakeInstall()

2. `createModelDirectory()`
- Create directory for the specified file name at `~/ngspice-nghdl/src/xspice/icm/ghdl/`
- The location where the directory is created in mentioned at `~/.nghdl/config.ini`, this config file is inside a hidden folder `.ngdhl`, created when nghdl is installed
- If a folder of the same name exists, it asks to overwrite, then removes earlier folder, and writes new one

3. `addingModelInModpath()`
- This adds the name of the new model created to `modpath.lst` file
- `modpath.lst` is located at `~/ngspice-nghdl/src/xspice/icm/ghdl`, this should contain name of all the models that the folder has
- Similarly you can look at `~/ngspice-nghdl/src/xspice/icm/digital` which also contains a `modpath.list` for all the models in that folder
- This `modpath.lst` is used in the `GNUMakefile` at `~/ngspice-nghdl/release/src/xspice/icm`
- This file used to keep a track of all components created
- If model already there it isn't added to the list

4. `createModelFiles()`
- Calls `model_generation.py` at the installed nghdl location under `src/model_generation.py`
- Moves the generated `cfunc.mode` and `ifspec.ifs` files to `~/ngspice-nghdl/src/xspice/icm/ghdl/modelName`
- Creates  `DUTghdl` folder at `~/ngspice-nghdl/src/xspice/icm/ghdl/modelName`
- Move `compile.sh`,`uthash.sh`,`ghdlserver.c`,`ghdlserver.h`,`Utility_Package.vhdl`,`Vhpi_Package.vhdl` to the `DUTghdl` folder
- Copy `modelName.vhdl` file from source location to `DUTghdl` folder
- Rum `compile.sh` which generates the object file for `ghdlserver.c`
- Give permission to `start_server.sh` and `sock_pkg_create.sh` to execute _chod a+x_
- Finally remove `compile.sh` and `ghdlserver.c`

5. `model_generation.py`
- Creates the following files =>
- - `connection_info.txt`
- - `cfunc.mod`
- - `ifspec.ifs`
- - `modelName_tb.vhdl` => testbench file for the model
- - `start_server.sh`
- - `sock_pkg_create.sh`
- The above files can be found either at `~/ngspice-nghdl/src/xspice/icm/ghdl/modelName` or `DUTghdl` folder inside it

6. `runMake()`
- Runs the `Makefile` at `~/ngspice-nghdl/release`
- Executing by running `make` command

7. `runMakeInstall()`
- Executes `make install`
- Finally calls `createSchematicLib()`

8. `createSchematicLib()`
- Connects with `createKicadLibrary.py` file at `~/nghdl/src` 
- Generates the `lib` file for the model, to be used by `KiCad`
- This is generated from a template stored at  `Appconfig.py`
- The generated `lib` is stored at `~/eSim_kicad.lib`
- Also creates `xml` file for the model, which is stored at eSim under `eSimLoc/src/modelParamXML/Nghdl

<br/>

Finally all the relevant files are generated, now while executing ngspice, we need to make sure to run the ngspice, which is located at -
- `~/ngspice-nghdl/install_dir/bin/ngspice` this has the binary for the ngspice,
- And also the script at `~/ngspice-nghdl/install_dir/share/ngspice/scripts/spinit`
= ` spinit` has the line `codemodel ...` mentioning a `cm` file to execute at runtime
- This has mention of `ghdl.cm` which makes sure that our `cfunc.c` file is executed at runtime
- You can see the `ghdl.cm` file is located at `~/ngspice-nghdl/release/src/xspice/icm/ghdl`
- Also the `cfunc.c` files, located at `~/ngspice-nghdl/release/src/xspice/icm/ghdl/modelName`
- These have mention of the `start_server.sh` file at `DUTghdl`, hence server is started and values passed as well
- Also you can look at `~/ngspice-nghdl/release/src/xspice/icm/digital` it has `digital.cm` and the folders inside have `cfunc.c`
- Also has `ifspec.c` which defines the interface

<br/>

- Note that, if you have ngspice currently installed remove it and genearate a softlink or command for the ngspice installed at -
`~/ngspice-nghdl/install_dir/bin/ngspice`
- `whereis ngspice`, run this to get the location from where `ngspice` is being executed currently
<br/>

- To generate softlink refer - [Creating softlink](https://askubuntu.com/questions/56339/how-to-create-a-soft-or-symbolic-link)i
- Exeecute `ln -s ~/ngspice-nghdl/install_dir/bin/ngspice /usr/bin/ngspice`


<br/>

- Also the installation script doesn't install ghdl, you will have to do it manually, either through a `.deb` package or build it from [source](https://github.com/ghdl/ghdl)
- Note that since we are using socket programming here, we require either the `llvm` architecture or `gcc`. Using `mcode` backend won't work here

<br/>

- To install ghdl from source, [this](https://github.com/ghdl/ghdl/issues/550) Github issue might be helpfu, the steps are -
- - `sudo ./configure --with-llvm-config`
- - sudo make
- - sudo make install
- Check [this](https://github.com/ghdl/ghdl/issues/166) Github issue for those building from `.deb` package
- To check current version and architecure of ghdl use -
- - `ghdl --version` command, it should have `llvm` code generator or `gcc`
<br/>

- Also once ghdl is installed, to check syntax of your vhdl files use -
`ghdl -s <vhdl file location>`
- Note that we need `std_vector_logic` as our ports here
