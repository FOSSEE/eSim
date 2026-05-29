Installation
===========================

This guide will help you install eSim on Ubuntu (Linux), other Linux distributions via Flatpak, and Microsoft Windows.

**Table of Contents**

1. `eSim installation via Flatpak (All Linux) <#flatpak-installation>`_
2. `eSim installation on Ubuntu OS (Linux) <#ubuntu-installation>`_
3. `eSim installation on Microsoft Windows OS <#windows-installation>`_
4. `Support <#support>`_

.. _flatpak-installation:

eSim Installation via Flatpak (Fedora, Ubuntu, openSUSE, Arch, etc.)
--------------------------------------------------------------------

The Flatpak method works on **all major Linux distributions** including Fedora, Ubuntu, Debian, openSUSE, Arch Linux, and others.

**Step 1:** Install Flatpak if not already installed:

   On Fedora:       ``sudo dnf install flatpak``
   On Ubuntu:       ``sudo apt install flatpak``
   On openSUSE:     ``sudo zypper install flatpak``
   On Arch:         ``sudo pacman -S flatpak``

**Step 2:** Add the Flathub repository:

   ``flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo``

**Step 3:** Install eSim:

   When available on Flathub: ``flatpak install flathub org.fossee.eSim``

   Or build from source: ``flatpak-builder build flatpak/org.fossee.eSim.yml --install --user``

**Step 4 (Optional):** Install KiCad for schematic editing:

   ``flatpak install flathub org.kicad.KiCad``

**Run eSim:** ``flatpak run org.fossee.eSim`` or launch from your application menu.

**Flatpak limitations:**

- NGHDL and Makerchip are not included. For full NGHDL/Modelica support, use the Ubuntu native installer.
- SKY130 PDK is not bundled. Use the Ubuntu installer for mixed-signal design with SKY130.
- xterm and gaw are not included; external waveform viewer features may require xterm installed on the host system.
- NGHDL KiCad symbol creation (createkicad) may not work fully due to sandbox restrictions on writing to KiCad's symbol directory.

.. _ubuntu-installation:

eSim Installation on Ubuntu OS (Linux)
-----------------------------------------

**Step 1:** After downloading eSim, extract it using:

    ``$ unzip eSim-2.5.zip``

**Step 2:** Change directories into the top-level eSim directory (where this INSTALL file can be found).

**Step 3:** To install eSim and its dependencies, run:

    ``$ chmod +x install-eSim.sh``

    ``$ ./install-eSim.sh --install``

**Step 4:** To uninstall eSim and all of its components, run:

    ``$ ./install-eSim.sh --uninstall``


**How to Run eSim**

**A. Through Terminal**

    ``$ esim``

**B. Double-click the eSim desktop icon**

.. _windows-installation:

eSim Installation on Microsoft Windows OS
--------------------------------------------

**Step 1:** Download eSim for Windows from https://esim.fossee.in/.  
*Disable your antivirus (if any) before proceeding.*

**Step 2:** If MinGW and/or MSYS is already installed on your machine, remove it from the PATH environment variable as it may interfere with eSim.

**Step 3:** Double-click the eSim installer and follow the instructions to install eSim.

**Step 4:** After installation, download and add the following file to the eSim home directory (`FOSSEE\eSim\`):

    https://github.com/FOSSEE/eSim/blob/master/src/frontEnd/TerminalUi.ui#L6

**Step 5:** Download and add the following executable to the `nghdl` folder (`FOSSEE\eSim\nghdl\src`):

    https://drive.google.com/file/d/17MNCCq9cG6A7fnIH-4KMUMY-yb4rW9s4/view?usp=sharing

**Step 6:** Installation is now complete.

**Step 7:** To uninstall eSim and all of its components, run the uninstaller `uninst-eSim.exe` located in the top-level eSim directory.

.. _support:

Support
---------

If you encounter any issues or errors during installation, please report them at:  
https://github.com/FOSSEE/eSim
 
For any queries regarding eSim, please write to us at  
`contact-esim@fossee.in <mailto:contact-esim@fossee.in>`_

---
