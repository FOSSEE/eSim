# Automated Tool Manager for eSim

## 1. Overview

The Automated Tool Manager is a Python-based command-line utility developed as part of the eSim Semester Long Internship Task 5.

The purpose of the Tool Manager is to simplify the management of external tools required by eSim.

The manager provides a centralized interface for detecting, installing, checking, updating, upgrading, and monitoring the required EDA tools.

Supported tools:

- Ngspice
- Verilator
- GHDL
- KiCad

The implementation is designed for Ubuntu Linux systems using APT.

## 2. Objectives

The main objectives are:

1. Detect installed eSim dependencies.
2. Identify missing dependencies.
3. Install supported tools using APT.
4. Detect installed package versions.
5. Check whether newer package versions are available.
6. Upgrade supported packages.
7. Maintain configuration settings.
8. Record tool-management activities.
9. Provide a simple command-line interface.
10. Provide automated tests for core functionality.

## 3. Architecture

The Tool Manager consists of independent Python modules:

    cli.py
       |
       +-- detector.py
       +-- installer.py
       +-- dependency_checker.py
       +-- version_checker.py
       +-- update_checker.py
       +-- upgrade_manager.py
       +-- config.py
       +-- logger.py
       |
       +-- APT / dpkg
              |
              +-- Ngspice
              +-- Verilator
              +-- GHDL
              +-- KiCad

## 4. Modules

### detector.py

Detects whether supported tools are installed and retrieves their versions.

Supported tools:

- Ngspice
- Verilator
- GHDL
- KiCad

KiCad uses dpkg-query for version detection because it does not support the standard --version option.

### installer.py

Installs supported tools using APT.

Supported packages:

- ngspice
- verilator
- ghdl
- kicad

The installer verifies the installation after completion.

### dependency_checker.py

Checks whether all required eSim tools are installed.

The checker reports:

- Installed tools
- Missing tools
- Overall system status

### version_checker.py

Retrieves installed package versions and APT candidate versions.

### update_checker.py

Compares installed Debian package versions with the APT candidate versions using:

    dpkg --compare-versions

Possible states include:

- Up to date
- Update available
- Not installed
- Unable to check

### upgrade_manager.py

Upgrades individual packages using APT and verifies the installed package version afterward.

### config.py

Manages configuration using Python's configparser.

Configuration file:

    config/esim_manager.ini

### logger.py

Records Tool Manager operations in:

    logs/tool_manager.log

Generated logs are excluded from Git.

### cli.py

Provides the interactive menu:

    1. Scan Tools
    2. Install Tool
    3. Dependency Check
    4. System Information
    5. Check Updates
    6. Upgrade Tool
    7. Configuration
    8. View Logs
    9. Exit

### __main__.py

Provides the package entry point:

    python3 -m tools.esim_tool_manager

## 5. Configuration

The default configuration is:

    [system]
    package_manager = apt

    [esim]
    installation_path = /opt/esim

    [updates]
    auto_check = true

    [tools]
    ngspice = ngspice
    verilator = verilator
    ghdl = ghdl
    kicad = kicad

## 6. Testing

Tests are located in:

    tests/esim_tool_manager/

The project uses Python's built-in unittest framework.

Run:

    python3 -m unittest discover -s tests -v

Current tests cover:

- Installed tool detection
- Missing tool detection
- Supported tool validation
- Update comparison
- Up-to-date comparison
- Missing version handling

Current validation result:

    Ran 6 tests
    OK

## 7. System Requirements

The current implementation targets:

- Ubuntu Linux
- Python 3.x
- APT package manager
- dpkg

Supported tools:

- Ngspice
- Verilator
- GHDL
- KiCad

## 8. Security Considerations

Installation and upgrade operations use sudo because system package management requires administrative privileges.

The Tool Manager does not store passwords or authentication credentials.

Generated runtime logs are excluded from version control.

## 9. Future Improvements

Possible future improvements include:

- Graphical user interface
- Windows and macOS support
- Automatic rollback
- Remote package repository support
- Scheduled updates
- More comprehensive test coverage
- Additional eSim dependency support
- Integration with the existing eSim installation workflow
