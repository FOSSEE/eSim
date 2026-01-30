## eSim 2.5 Installation Issues on Ubuntu 25.xx (Internship Task 4)

This document describes the issues encountered while installing **eSim 2.5** on **Ubuntu 25.xx** (VirtualBox) and the steps taken to analyze and resolve them.

---

### Issue 1: DNS Resolution Failure in VirtualBox

**Problem**
- Ubuntu 25.xx VM was unable to resolve domain names.
- Commands such as `ping google.com` and GitHub access failed.
- This blocked package installation and repository access.

**Root Cause**
- Ubuntu 25.xx uses `systemd-resolved`.
- `/etc/resolv.conf` is a stub resolver and does not contain real DNS entries.
- DNS was not automatically assigned in the VirtualBox NAT environment.

**Fix Applied**
- Configured DNS explicitly using `systemd-resolved`:
- Restarted the resolver service:

- Network connectivity was restored successfully.

**Result**
- Internet access started working.
- GitHub and package repositories became accessible.

---

### Issue 2: setup.py Installation Failure

**Problem**
- Running `python3 setup.py install` failed.
- Errors included:
- `setuptools` deprecation warnings
- Permission denied while writing to `/usr/local/lib`

**Analysis**
- Direct use of `setup.py install` is deprecated.
- System-wide installation requires elevated permissions.
- Modern Python packaging discourages this method.

**Resolution**
- The issue was documented instead of forcing installation.
- Deprecated installation method was avoided.
- Modern tools such as `pip` and `pyproject.toml`-based builds were recommended.

---

### Conclusion

This task involved identifying real compatibility and environment issues on Ubuntu 25.xx.
One major issue (DNS resolution) was fixed, and another critical issue (deprecated installation method) was analyzed and documented with proper technical reasoning.

![GitHub release (latest by date)](https://img.shields.io/github/v/release/fossee/esim?color=blueviolet)
![GitHub](https://img.shields.io/github/license/fossee/esim?color=blue)
![Python](https://img.shields.io/badge/python-v3.6+-blue.svg)
[![PEP8](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)
![Travis (.com)](https://img.shields.io/travis/com/Eyantra698Sumanto/eSim)
[![Documentation Status](https://readthedocs.org/projects/esim/badge/?version=latest)](https://esim.readthedocs.io/en/latest/?badge=latest)
[![GitHub forks](https://img.shields.io/github/forks/fossee/esim)](https://github.com/fossee/esim/network)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat)](https://github.com/fossee/esim)
![GitHub contributors](https://img.shields.io/github/contributors/fossee/esim)

## eSim

[eSim](https://esim.fossee.in/) is an open source EDA tool for circuit design, simulation, analysis and PCB design, developed by [FOSSEE Team](https://www.fossee.in/) at [IIT Bombay](https://www.iitb.ac.in/).
It is an integrated tool build using open source softwares such as KiCad, Ngspice and GHDL.

## Releases and Installation
eSim is released for the following distributions (operating systems):
* Ubuntu 22.04, 23.04, 24.04 LTS versions.
* Microsoft Windows 8, 10 and 11.

To use eSim on your machine having above distributions, please refer to link [here](https://esim.fossee.in/downloads) for installation and other guidelines.

> Note for other distributions: You can refer [`installers`](https://github.com/fossee/eSim/tree/installers) branch for documentation on packaging (for above mentioned distributions) to build installers for your operating system in a similar way. For providing your build, please check the `Contribution` section mentioned below.

## Features
* An open-source EDA tool.
* Perform Circuit Design.
* Perform Simulation.
* Perform Layout Design.
* Model and Subcircuit builder.
* Support for Mixed-Signal Simulations including Microcontrollers.
* eSim has been successfully ported to low cost FOSSEE [laptop](https://laptop.fossee.in/)

## Open-Source Softwares Used
* [Python](https://www.python.org/)
* [KiCad](https://www.kicad.org/)
* [NGHDL](https://github.com/fossee/nghdl/)
* [Makerchip](https://www.makerchip.com/)
* [SkyWater SKY130 PDK](https://skywater-pdk.rtfd.io/)

## eSim Manual
To know everything about eSim, how it works and it's feature please download the manual from [here](https://static.fossee.in/esim/manuals/eSim_Manual_2.5.pdf)

## Contact
For any queries regarding eSim please write us on at this [email address](mailto:contact-esim@fossee.in).

Other Contact Details are available [here](https://esim.fossee.in/contact-us).

## Contribution
Please refer [here](https://github.com/FOSSEE/eSim/blob/master/CONTRIBUTION.md) for further details.

## License
It is developed by FOSSEE Team at IIT Bombay and is released under GNU GPL License.
