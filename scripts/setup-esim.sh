#!/usr/bin/bash
config_dir_esim="$HOME/.esim"
config_dir_nghdl="$HOME/.nghdl"

config_file="config.ini"
eSim_HOME="$SNAP/eSim"
NGHDL_HOME="$SNAP/nghdl-simulator"

# Setup KiCad 6.0 eSim libraries
TARGET="$HOME/.local/kicad/6.0"
FLAG="$TARGET/.esim_kicad_setup_done"


# eSim Configuration

if [ ! -d "$config_dir_esim/.setup_done" ]; then
    mkdir -p $config_dir_esim

    echo "[eSim]" > $config_dir_esim/$config_file
    echo "eSim_HOME = $eSim_Home" >> $config_dir_esim/$config_file
    echo "LICENSE = %(eSim_HOME)s/LICENSE" >> $config_dir_esim/$config_file
    echo "KicadLib = %(eSim_HOME)s/library/kicadLibrary.tar.xz" >> $config_dir_esim/$config_file
    echo "IMAGES = %(eSim_HOME)s/images" >> $config_dir_esim/$config_file
    echo "VERSION = %(eSim_HOME)s/VERSION" >> $config_dir_esim/$config_file
    echo "MODELICA_MAP_JSON = %(eSim_HOME)s/library/ngspicetoModelica/Mapping.json" >> $config_dir_esim/$config_file
    
    touch "$config_dir_esim/.setup_done"

fi


# nghdl configuration 

if [ ! -d $config_dir_nghdl/.setup_done ]; then
    mkdir -p $config_dir_nghdl

    echo "[NGHDL]" > $config_dir_nghdl/$config_file
    echo "NGHDL_HOME = $NGHDL_HOME" >> $config_dir_nghdl/$config_file
    echo "DIGITAL_MODEL = %(NGHDL_HOME)s/src/xspice/icm" >> $config_dir_nghdl/$config_file
    echo "RELEASE = %(NGHDL_HOME)s/release" >> $config_dir_nghdl/$config_file
    echo "[SRC]" >> $config_dir_nghdl/$config_file
    echo "SRC_HOME = $NGHDL_HOME" >> $config_dir_nghdl/$config_file
    echo "LICENSE = %(SRC_HOME)s/LICENSE" >> $config_dir_nghdl/$config_file

    touch $config_dir_nghdl/.setup_done

fi

if [ ! -f "$FLAG" ]; then
    echo "Setting up eSim libraries for the first time..."

#    install -d "$TARGET/symbols"
    install -d "$TARGET/template"

#    cp -r "$SNAP/3rdparty/symbols/." "$TARGET/symbols/"
    cp "$SNAP/3rdparty/template/sym-lib-table" "$TARGET/template/"

    touch "$FLAG"
    echo "eSim libraries setup completed."
else
    echo "eSim libraries already set up."
fi
