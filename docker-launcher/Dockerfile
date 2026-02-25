# eSim Docker Container
# Multi-stage build to keep the image smaller (~3.5GB vs ~5GB)
# FOSSEE IIT Bombay

# ============================================
# Stage 1: Build dependencies
# ============================================
FROM ubuntu:22.04 AS builder

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Kolkata

# Install build tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc g++ make cmake git \
    python3 python3-pip python3-dev python3-venv \
    autoconf automake libtool pkg-config bison flex gettext wget \
    libgtk-3-dev \
    && rm -rf /var/lib/apt/lists/*


# Setup Python venv with dependencies
# Note: setuptools<58 is needed for hdlparse which uses deprecated use_2to3
RUN python3 -m venv /build/venv \
    && /build/venv/bin/pip install --no-cache-dir "setuptools<58.0.0" wheel \
    && /build/venv/bin/pip install --no-cache-dir \
    matplotlib==3.7.5 numpy==1.24.4 scipy==1.10.1 \
    pillow==10.4.0 hdlparse==1.0.4 watchdog==4.0.2

# Build GAW3 (analog waveform viewer) from source
# gtkwave is digital only, gaw3 is what eSim actually uses
RUN git clone --depth 1 https://github.com/StefanSchippers/xschem-gaw.git /build/gaw3 \
    && cd /build/gaw3 \
    && aclocal && autoheader \
    && automake --add-missing --foreign 2>/dev/null || true \
    && autoconf \
    && sed -i 's/GETTEXT_MACRO_VERSION = 0.18/GETTEXT_MACRO_VERSION = 0.20/' po/Makefile.in.in \
    && ./configure --prefix=/usr/local \
    && make -j$(nproc) \
    && make DESTDIR=/build/gaw3-install install


# ============================================
# Stage 2: Runtime image
# ============================================
FROM ubuntu:22.04

LABEL maintainer="FOSSEE IIT Bombay"
LABEL description="eSim EDA Tool with GUI support"

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Kolkata
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
# Create user
ARG USERNAME=esim-user
ARG USER_UID=1000
ARG USER_GID=1000

ENV USERNAME=${USERNAME}



# VNC settings
ENV VNC_PORT=5901
ENV NOVNC_PORT=6080
ENV VNC_RESOLUTION=1920x1080
ENV VNC_DEPTH=24

# Desktop and font rendering settings
ENV GTK_THEME=Adwaita
ENV UBUNTU_MENUPROXY=0
ENV XDG_DATA_DIRS=/usr/share:/usr/local/share:/usr/share/icons
ENV QT_AUTO_SCREEN_SCALE_FACTOR=1
ENV GDK_SCALE=1
ENV FREETYPE_PROPERTIES="truetype:interpreter-version=40"

# Install runtime packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    kicad kicad-libraries gtkwave xterm \
    python3 python3-wxgtk4.0 python3-pyqt5\
    libx11-6 libxext6 libxrender1 libxfixes3 libxi6 libxrandr2 \
    libxcursor1 libxinerama1 libgl1 libgl1-mesa-glx libgl1-mesa-dri \
    libxcb1 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-randr0 \
    libxcb-render-util0 libxcb-shape0 libxcb-xfixes0 libxcb-xinerama0 \
    libxcb-xkb1 libxkbcommon0 libxkbcommon-x11-0 dbus-x11 \
    adwaita-icon-theme-full hicolor-icon-theme gnome-icon-theme \
    oxygen-icon-theme tango-icon-theme humanity-icon-theme \
    ca-certificates libgtk-3-0 libcanberra-gtk-module xdg-utils \
    libglib2.0-0 libfontconfig1 libfreetype6 \
    tigervnc-standalone-server tigervnc-common \
    xfce4 xfce4-terminal novnc websockify \
    xdotool wmctrl openbox tint2 \
    && rm -rf /var/lib/apt/lists/* && apt-get clean

# Copy built artifacts from builder stage
COPY --from=builder /build/gaw3-install/usr/local /usr/local/
# COPY --from=builder /build/esim ${ESIM_HOME}
COPY --from=builder /build/venv /opt/venv

# Install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    make \
    gnat \
    clang \
    llvm-11 \
    llvm-11-dev \
    llvm-11-runtime \
    llvm-11-tools \
    clang-11 \
    zlib1g-dev \
    autoconf \
    g++ \
    flex \
    bison \
    wget \
    unzip \
    xz-utils \
    libxaw7 \
    libxaw7-dev \
    libcanberra-gtk-module \
    libcanberra-gtk3-module \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /home/${USERNAME}/

# Download eSim source
RUN wget https://github.com/FOSSEE/eSim/archive/refs/tags/v2.5.zip

# Unzip
RUN unzip v2.5.zip

# Rename folder (optional)
RUN mv eSim-2.5 esim

# eSim paths
ENV ESIM_HOME=/home/${USERNAME}/esim
ENV PYTHONPATH="${ESIM_HOME}/src:/opt/venv/lib/python3.10/site-packages"

RUN groupadd --gid ${USER_GID} ${USERNAME} \
    && useradd --uid ${USER_UID} --gid ${USER_GID} -m ${USERNAME} \
    && mkdir -p /home/${USERNAME}/workspace \
    && chown -R ${USERNAME}:${USERNAME} /home/${USERNAME} \
    && chown -R ${USERNAME}:${USERNAME} ${ESIM_HOME}



WORKDIR /opt

########################################
# Install GHDL
########################################

RUN wget https://github.com/FOSSEE/nghdl/raw/installers/Ubuntu/ghdl-4.1.0.tar.gz \
    && tar -xzf ghdl-4.1.0.tar.gz \
    && cd ghdl-4.1.0 \
    && chmod +x configure \
    && ./configure --with-llvm-config=/usr/bin/llvm-config-11 \
    && make -j$(nproc) \
    && make install \
    && cd /opt \
    && rm -rf ghdl-4.1.0 ghdl-4.1.0.tar.gz


########################################
# Install Verilator
########################################

RUN wget https://github.com/verilator/verilator/archive/refs/tags/v4.210.tar.gz \
    && tar -xvf v4.210.tar.gz \
    && cd verilator-4.210 \
    && autoconf \
    && ./configure \
    && make -j$(nproc) \
    && make install \
    && cd /opt \
    && rm -rf verilator-4.210 v4.210.tar.gz

#########################################################
# Install NGHDL simulator
#########################################################



WORKDIR /tmp

RUN apt-get update && apt-get install -y \
    make gnat clang \
    zlib1g-dev autoconf g++ flex bison \
    libxaw7 libxaw7-dev \
    libcanberra-gtk-module libcanberra-gtk3-module \
    wget xz-utils git \
    && rm -rf /var/lib/apt/lists/*

# Clone NGHDL source
WORKDIR ${ESIM_HOME}/

RUN git clone --depth 1 https://github.com/FOSSEE/nghdl

# Create NGHDL symlink for eSim
RUN chmod 755 /home/esim-user/esim/nghdl/src/ngspice_ghdl.py \
    && rm -f /usr/local/bin/nghdl \
    && ln -s /home/esim-user/esim/nghdl/src/ngspice_ghdl.py /usr/local/bin/nghdl

# Download NGHDL simulator
WORKDIR /home/${USERNAME}
RUN wget https://github.com/FOSSEE/nghdl/raw/master/nghdl-simulator-source.tar.xz

# Extract NGHDL
RUN tar -xJf nghdl-simulator-source.tar.xz \
    && mv nghdl-simulator-source /home/${USERNAME}/nghdl-simulator \
    && mkdir -p /home/${USERNAME}/nghdl-simulator/release \
    && mkdir -p /home/${USERNAME}/nghdl-simulator/install_dir

RUN chown -R ${USERNAME}:${USERNAME} /home/${USERNAME}/nghdl-simulator \
    && chmod -R u+w /home/${USERNAME}/nghdl-simulator

WORKDIR /home/${USERNAME}/nghdl-simulator/release

# Ensure configure is executable
RUN chmod +x ../configure

RUN ../configure \
    --enable-xspice \
    --disable-debug \
    --prefix=/home/${USERNAME}/nghdl-simulator/install_dir \
    --exec-prefix=/home/${USERNAME}/nghdl-simulator/install_dir

RUN make -j$(nproc)
RUN make install

# Link ngspice
RUN ln -sf /home/${USERNAME}/nghdl-simulator/install_dir/bin/ngspice /usr/bin/ngspice

RUN chown -R ${USERNAME}:${USERNAME} /home/${USERNAME}/nghdl-simulator \
    && chmod -R u+w /home/${USERNAME}/nghdl-simulator


#########################################################



WORKDIR ${ESIM_HOME}/src/frontEnd

# Create eSim config
RUN mkdir -p /home/${USERNAME}/.esim \
 && printf '[DEFAULT]\n\
eSim_HOME = /home/%s/esim\n\
LICENSE = %%(eSim_HOME)s/LICENSE\n\
KicadLib = %%(eSim_HOME)s/library/kicadLibrary.zip\n\
IMAGES = %%(eSim_HOME)s/images\n\
VERSION = %%(eSim_HOME)s/VERSION\n\
MODELICA_MAP_JSON = %%(eSim_HOME)s/library/ngspicetoModelica/Mapping.json\n\
\n[eSim]\n\
workspace=/home/%s/eSim-Workspace\n\
kicad=/usr/bin\n\
ngspice=/usr/bin\n' \
${USERNAME} ${USERNAME} > /home/${USERNAME}/.esim/config.ini \
 && chown -R ${USERNAME}:${USERNAME} /home/${USERNAME}/.esim

# Create NGHDL config 
RUN mkdir -p /home/${USERNAME}/.nghdl \
 && printf "[NGHDL]\n\
NGHDL_HOME = /home/esim-user/nghdl-simulator\n\
DIGITAL_MODEL = %%(NGHDL_HOME)s/src/xspice/icm\n\
RELEASE = %%(NGHDL_HOME)s/release\n\
\n[SRC]\n\
SRC_HOME = /home/esim-user/esim/nghdl\n\
LICENSE = %%(SRC_HOME)s/LICENSE\n" \
> /home/${USERNAME}/.nghdl/config.ini \
 && chown -R ${USERNAME}:${USERNAME} /home/${USERNAME}/.nghdl

# Setup KiCad symbol libraries
RUN mkdir -p /home/${USERNAME}/.config/kicad/6.0 \
    && KICAD_CONFIG=/home/${USERNAME}/.config/kicad/6.0 \
    && ESIM_SYMLIB=/home/${USERNAME}/esim/library/kicadLibrary/eSim-symbols \
    && KICAD_SYMLIB=/usr/share/kicad/symbols \
    && echo '(sym_lib_table' > ${KICAD_CONFIG}/sym-lib-table \
    && for lib in eSim_Devices eSim_Sources eSim_Analog eSim_Digital eSim_Hybrid eSim_Power eSim_Subckt eSim_Miscellaneous eSim_Plot eSim_Nghdl eSim_Ngveri eSim_SKY130 eSim_SKY130_Subckts eSim_User; do \
    echo "  (lib (name \"$lib\")(type \"KiCad\")(uri \"${ESIM_SYMLIB}/${lib}.kicad_sym\")(options \"\")(descr \"\"))" >> ${KICAD_CONFIG}/sym-lib-table; \
    done \
    && for lib in Device power Simulation_SPICE Connector Analog Transistor_BJT Transistor_FET Diode Amplifier_Operational; do \
    echo "  (lib (name \"$lib\")(type \"KiCad\")(uri \"${KICAD_SYMLIB}/${lib}.kicad_sym\")(options \"\")(descr \"\"))" >> ${KICAD_CONFIG}/sym-lib-table; \
    done \
    && echo ')' >> ${KICAD_CONFIG}/sym-lib-table \
    && echo '(fp_lib_table)' > ${KICAD_CONFIG}/fp-lib-table \
    && chown -R ${USERNAME}:${USERNAME} /home/${USERNAME}/.config

# Copy eSim symbol libraries into KiCad system symbols
RUN cp -r ${ESIM_HOME}/library/kicadLibrary/eSim-symbols/* /usr/share/kicad/symbols/ \
    && chmod -R 755 /usr/share/kicad/symbols \
    && chown -R ${USERNAME}:${USERNAME} /usr/share/kicad/symbols

# Setup VNC with openbox + tint2 taskbar

RUN mkdir -p /home/${USERNAME}/.vnc \
    && printf '#!/bin/bash\nunset SESSION_MANAGER\nunset DBUS_SESSION_BUS_ADDRESS\nexport XDG_RUNTIME_DIR=/tmp/runtime-esim-user\nmkdir -p $XDG_RUNTIME_DIR && chmod 700 $XDG_RUNTIME_DIR\ntint2 &\nexec openbox-session\n' \
    > /home/${USERNAME}/.vnc/xstartup \
    && chmod +x /home/${USERNAME}/.vnc/xstartup \
    && printf '\x9f\x87\x18\xb4\x8e\x8f\x8a\x57' > /home/${USERNAME}/.vnc/passwd \
    && chmod 600 /home/${USERNAME}/.vnc/passwd \
    && chown -R ${USERNAME}:${USERNAME} /home/${USERNAME}/.vnc

# XFCE config to fix window focus issues
RUN mkdir -p /home/${USERNAME}/.config/xfce4/xfconf/xfce-perchannel-xml \
    && printf '<?xml version="1.0" encoding="UTF-8"?>\n<channel name="xfwm4" version="1.0">\n  <property name="general" type="empty">\n    <property name="focus_new" type="bool" value="true"/>\n    <property name="raise_on_focus" type="bool" value="true"/>\n    <property name="prevent_focus_stealing" type="bool" value="false"/>\n  </property>\n</channel>\n' \
    > /home/${USERNAME}/.config/xfce4/xfconf/xfce-perchannel-xml/xfwm4.xml \
    && chown -R ${USERNAME}:${USERNAME} /home/${USERNAME}/.config

# Font rendering config for better VNC quality
RUN mkdir -p /home/${USERNAME}/.config/fontconfig \
    && printf '<?xml version="1.0"?>\n<!DOCTYPE fontconfig SYSTEM "fonts.dtd">\n<fontconfig>\n  <match target="font"><edit name="antialias" mode="assign"><bool>true</bool></edit></match>\n  <match target="font"><edit name="hinting" mode="assign"><bool>true</bool></edit></match>\n  <match target="font"><edit name="hintstyle" mode="assign"><const>hintslight</const></edit></match>\n  <match target="font"><edit name="rgba" mode="assign"><const>rgb</const></edit></match>\n</fontconfig>\n' \
    > /home/${USERNAME}/.config/fontconfig/fonts.conf \
    && chown -R ${USERNAME}:${USERNAME} /home/${USERNAME}/.config/fontconfig

# Startup script
RUN printf '#!/bin/bash\nset -e\n\n# Ensure workspace exists\nmkdir -p /home/${USERNAME}/esim/eSim-Workspace\ncp -rn /home/${USERNAME}/esim/Examples/* /home/esim-user/eSim-Workspace/ 2>/dev/null || true\n\nif [ "$1" = "--vnc" ] || [ "$USE_VNC" = "1" ]; then\n    echo "Starting eSim in VNC mode"\n    vncserver -kill :1 2>/dev/null || true\n    export XDG_RUNTIME_DIR=/tmp/runtime-esim-user\n    mkdir -p $XDG_RUNTIME_DIR && chmod 700 $XDG_RUNTIME_DIR\n    vncserver :1 -geometry ${VNC_RESOLUTION:-1920x1080} -depth ${VNC_DEPTH:-24} -SecurityTypes None\n    sleep 3\n    websockify --web=/usr/share/novnc/ ${NOVNC_PORT:-6080} localhost:5901 &\n    echo "VNC ready at http://localhost:${NOVNC_PORT:-6080}/vnc.html"\n    export DISPLAY=:1\n    sleep 2\n    cd /home/${USERNAME}/esim/src/frontEnd\n    python3 Application.py\n    tail -f /dev/null\nelse\n    echo "Starting eSim in X11 mode"\n    cd /home/${USERNAME}/esim/src/frontEnd\n    exec python3 Application.py\nfi\n' \
    > /usr/local/bin/start-esim.sh \
    && chmod +x /usr/local/bin/start-esim.sh

RUN chown -R ${USERNAME}:${USERNAME} /home/${USERNAME} \
    && chmod -R u+rwX /home/${USERNAME}
USER ${USERNAME}

ENTRYPOINT ["/usr/local/bin/start-esim.sh"]
CMD []
