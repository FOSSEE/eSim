# Flatpak_Test_App (FOSSEE_Installer_Test) WIP :warning:


## Documentation to package demo installer using Flatpak.

### To get stared, we need to first install the runtimes required for packing our Qt5 application

```
  flatpak install org.kde.Sdk//5.15-22.08

  flatpak install com.riverbankcomputing.PyQt.BaseApp//5.15-22.08
```
---

### To build the flatpak application we require flatpak-builder

Ubuntu:
```
  sudo apt install flatpak-builder -y
```
Fedora:
```
  sudo dnf install flatpak-builder -y
```

### Install the dependencies mentioned below on the host system

Ubuntu:
```
  sudo apt install make flex g++ ccache bison -y
```
Fedora:
```
  sudo dnf install make flex g++ ccache bison -y
```
Other Linux Distributions: Use equivalent commands to install the necesarry packages

### To see all available commands for building, installing, accessing runtime through shell and more...
```bash
  # execute the listed commands in ./flatpak/ dir
  bash scripts/build_new_flatpak.sh
```

## Screenshots:
![image](https://user-images.githubusercontent.com/75079303/236667264-3d77cd7a-9bf0-405b-a0fc-32cde1f2f9be.png)

![image](https://user-images.githubusercontent.com/75079303/236667291-1467a423-d1d1-479d-b2f2-3fd49e195926.png)


