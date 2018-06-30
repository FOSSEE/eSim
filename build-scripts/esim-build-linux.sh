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

# ubuntu, debian, linux mint
fpm --output-type deb --input-type dir --force --package dist/esim.deb --name esim \
	--version 1.0 --license "GNU GPLv3" --vendor "FOSSEE, IIT Bombay" \
	--description "EDA and circuit simulation tools." --url "https://esim.fossee.in" \
	--category "Electronics" --depends "kicad = 4.0.7" --depends "ngpsice = 28" \
	--deb-dist "stable" --deb-no-default-config-files ./dist/esim=/opt \
	../esim-linux.desktop-template=/usr/share/applications/esim.desktop

# fedora, openSUSE, centOS
fpm --output-type rpm --input-type dir --force --package dist/esim.rpm --name esim \
	--version 1.0 --license "GNU GPLv3" --vendor "FOSSEE, IIT Bombay" \
	--description "EDA and circuit simulation tools." --url "https://esim.fossee.in" \
	--category "Electronics" --depends "kicad = 4.0.7" --depends "ngpsice = 28" \
	 ./dist/esim=/opt ../esim-linux.desktop-template=/usr/share/applications/esim.desktop

# arch linux (pacman)
fpm --output-type pacman --input-type dir --force --package dist/esim.pkg.tar.xz --name esim \
	--version 1.0 --license "GNU GPLv3" --vendor "FOSSEE, IIT Bombay" \
	--description "EDA and circuit simulation tools." --url "https://esim.fossee.in" \
	--category "Electronics" --depends "kicad = 4.0.7" --depends "ngpsice = 28" \
	 ./dist/esim=/opt ../esim-linux.desktop-template=/usr/share/applications/esim.desktop

# self extracting sh installer
fpm --output-type sh --input-type dir --force --package dist/esim.sh --name esim \
	--version 1.0 --license "GNU GPLv3" --vendor "FOSSEE, IIT Bombay" \
	--description "EDA and circuit simulation tools." --url "https://esim.fossee.in" \
	--category "Electronics" --depends "kicad = 4.0.7" --depends "ngpsice = 28" \
	 ./dist/esim=/opt ../esim-linux.desktop-template=/usr/share/applications/esim.desktop