#!/bin/bash

root_dir=$(pwd)

function installDependency {

    set +e          # Temporary disable exit on error
    trap "" ERR     # Do not trap on error of any command

    set -e          # Re-enable exit on error
    trap error_exit ERR
   
    echo "Creating virtual environment to isolate packages "
    python3 -m venv esim-env
    
    echo "Starting the virtual env..................."
    source esim-env/bin/activate

    echo "Upgrading Pip.............................."
    pip install --upgrade pip

    echo "Installing Required Dependencies..........."
    pip install PyQt5
    pip install numpy
    pip install matplotlib
    pip install scipy
    pip install watchdog
    pip install psutil
    pip install pyinstaller
    pip install makerchip-app
    pip install sandpiper-saas
    pip install setuptools
    pip install xterm
    pip install --upgrade https://github.com/hdl/pyhdlparser/tarball/master #python3 compatible hdlparse fork

    pip install pyinstaller #for app bundling
}

function unzipFiles {
    echo "Unzipping esim symbols folder..........................."
    tar -xzf library/kicadLibrary.tar.xz -C library/
}

function buildVerilator
{   
    
    echo "Installing $verilator......................."
    tar -xvf $verilator.tar.xz
    echo "$verilator successfully extracted"
    echo "Changing directory to $verilator installation"
    cd $verilator
    echo "Configuring $verilator build as per requirements"
    chmod +x configure
    ./configure
    make -j$(sysctl -n hw.ncpu)
    sudo make install
    echo "Removing the unessential verilator files........"
    rm -r docs
    rm -r examples
    rm -r include
    rm -r test_regress
    rm -r bin
    ls -1 | grep -E -v 'config.status|configure.ac|Makefile.in|verilator.1|configure|Makefile|src|verilator.pc' | xargs rm -f
    #sudo rm -v -r'!("config.status"|"configure.ac"|"Makefile.in"|"verilator.1"|"configure"|"Makefile"|"src"|"verilator.pc")'

    echo "Verilator installed successfully"
    cd ../

}

function buildNgspice {
    unzip nghdl.zip
    cd nghdl
    tar -xJf nghdl-simulator-source.tar.xz
    mv nghdl-simulator-source ~/nghdl-simulator

    cd ~/nghdl-simulator

    mkdir -p release
    cd release

    ../configure \
        --enable-xspice \
        --enable-cider \
        --disable-openmp \
        --disable-debug \
        --without-readline \
        --without-x \
        --enable-relpath \
        --prefix=/usr/local \
        --exec-prefix=/usr/local \
        CFLAGS="-m64 -O2 -std=gnu99 -Wno-error" \
        CXXFLAGS="-m64 -O2 -Wno-error" \
        LDFLAGS="-m64"

    # Compile verilated.o
    g++ -m64 -O2 -fPIC -fvisibility=hidden \
        -I/usr/local/share/verilator/include \
        -c /usr/local/share/verilator/include/verilated.cpp \
        -o ~/nghdl-simulator/src/xspice/icm/Ngveri/verilated.o

    make -j$(sysctl -n hw.ncpu) 2>&1 | tee make.log
    if [ $? -ne 0 ]; then
    grep "error:" make.log | head -20
    fi

    sudo make install
    echo "Done"

    cd $root_dir
}

unzipFiles
installDependency
buildVerilator
buildNgspice