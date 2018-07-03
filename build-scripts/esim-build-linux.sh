#!/bin/sh

##################################################
########## Requires pyinstaller and fpm ##########
###### https://pypi.org/project/PyInstaller ######
###### https://github.com/jordansissel/fpm #######
##################################################

# build eSim executable using pyinstaller
pyinstaller --clean -y esim-pyinstaller.spec


#################################################
# build distribution specific packages

# Package meta-data
NAME="esim"
VERSION="1.2.0"
LICENSE="GNU GPLv3"
VENDOR="FOSSEE, IIT Bombay"
DESCRIPTION="An open source EDA tool for circuit design, simulation, and analysis"
URL="https://esim.fossee.in"

# ubuntu, debian, linux mint
fpm --output-type deb --input-type dir --force --package "dist/$NAME.deb" --name "$NAME" \
	--version "$VERSION" --license "$LICENSE" --vendor "$VENDOR" \
	--description "$DESCRIPTION" --url "$URL" --depends "kicad=4.0" --depends "ngspice" \
	--deb-dist "stable" --deb-no-default-config-files ./dist/esim=/opt \
	linux-extras/esim-linux.desktop-template=/usr/share/applications/esim.desktop \
	linux-extras/esim-launcher.sh=/usr/local/bin/esim

# fedora, openSUSE, centOS
fpm --output-type rpm --input-type dir --force --package "dist/$NAME.rpm" --name "$NAME" \
	--version "$VERSION" --license "$LICENSE" --vendor "$VENDOR" \
	--description "$DESCRIPTION" --url "$URL" --depends "kicad-4.0" --depends "ngspice" \
	 ./dist/esim=/opt linux-extras/esim-linux.desktop-template=/usr/share/applications/esim.desktop \
	 linux-extras/esim-launcher.sh=/usr/local/bin/esim

# arch linux (pacman)
# Warning: Arch is a rolling release so pacman only supports installing latest versions of packages.
# Therefore it will force user to download Kicad 5 upon its release.
fpm --output-type pacman --input-type dir --force --package "dist/$NAME.pkg.tar.xz" --name "$NAME" \
	--version "$VERSION" --license "$LICENSE" --vendor "$VENDOR" \
	--description "$DESCRIPTION" --url "$URL" --depends "kicad" --depends "ngspice" \
	 ./dist/esim=/opt linux-extras/esim-linux.desktop-template=/usr/share/applications/esim.desktop \
	 linux-extras/esim-launcher.sh=/usr/local/bin/esim

# self extracting sh installer
# user will need to manually download kicad and ngspice
fpm --output-type sh --input-type dir --force --package "dist/$NAME.sh" --name "$NAME" \
	--version "$VERSION" --license "$LICENSE" --vendor "$VENDOR" \
	--description "$DESCRIPTION" --url "$URL" --depends "kicad" --depends "ngspice" \
	 ./dist/esim=/opt linux-extras/esim-linux.desktop-template=/usr/share/applications/esim.desktop \
	 linux-extras/esim-launcher.sh=/usr/local/bin/esim
	 