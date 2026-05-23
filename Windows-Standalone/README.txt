Overview

The eSim Standalone System is a powerful Windows-based graphical package management and dependency automation platform developed for the eSim ecosystem. The project is designed to simplify the installation, configuration, updating, and maintenance of all essential tools and dependencies required for electronic circuit simulation, VLSI workflows, embedded system design, and HDL-based development environments.

The standalone system provides a complete GUI-driven experience where users can install and manage important engineering tools without manually executing terminal commands. The platform automates package installation, dependency handling, version tracking, update verification, logging, and environment configuration through an integrated and user-friendly interface.

This system is especially useful for students, researchers, developers, educators, and electronics engineers who want a simplified setup process for the eSim environment on Windows systems.

Project Objectives

The major objectives of the eSim Standalone System are:

To automate the installation of essential eSim tools and packages.
To eliminate complex manual dependency configurations.
To provide a centralized GUI for package management.
To simplify version tracking and software updates.
To maintain installation logs and package records.
To improve the user experience for Windows-based eSim setup.
To provide a scalable architecture for future tool integrations.
To support package installation, updates, and status monitoring in real time.
To create a modular and maintainable package management framework.
Key Features
1. Graphical User Interface (GUI)

The system is built using PyQt5, providing a clean and interactive graphical interface for users. The GUI enables:

One-click installation
Package status monitoring
Version checking
Update notifications
Dependency management
User-friendly dialogs and alerts
Real-time installation feedback
2. Automatic Package Installation

The standalone system automates the installation of required packages using:

Chocolatey package manager
GitHub release downloads
ZIP extraction
Custom installation scripts
Dependency automation

This removes the need for users to manually install tools individually.

3. Package Management System

The system maintains complete package information including:

Installed package name
Current version
Installation status
Installation date
Installation directory
Update availability

All package details are stored in a centralized JSON database.

4. Dependency Management

The standalone system automatically installs required dependencies for tools and applications. Dependencies are loaded dynamically from configuration files and installed through automated scripts.

Supported dependency operations include:

Dependency detection
Dependency installation
Error handling
Logging
Status updating
5. Chocolatey Integration

The project integrates with Chocolatey to manage Windows packages efficiently. The system can:

Detect Chocolatey installation
Install Chocolatey automatically
Update Chocolatey
Verify installed version
Maintain installation records

The Chocolatey manager also updates package installation details into the JSON database automatically.

Supported Packages and Tools

The standalone system currently supports installation and management of several major tools required for the eSim ecosystem.

Supported Tools Include
KiCad
LLVM
GHDL
Ngspice
Python packages
System dependencies
Chocolatey packages
KiCad Package Manager

The KiCad package manager module provides:

Latest version fetching
Version selection
Installation automation
Update management
Installed version detection
Outdated version notification
Installation status monitoring

The module automatically checks if the installed version is outdated and notifies the user accordingly.

KiCad Features
GUI-based installer
Version dropdown selection
Automatic update support
Chocolatey integration
JSON-based package tracking
Installation directory management
Error handling and logging
GHDL Package Manager

The GHDL package manager automates HDL tool installation directly from GitHub releases. The module:

Fetches latest releases using GitHub API
Downloads Windows-compatible binaries
Extracts ZIP packages
Configures environment paths
Updates installation records

The system automatically handles GHDL installation and update workflows without manual intervention.

GHDL Features
GitHub API integration
Automatic binary download
ZIP extraction automation
PATH configuration
GUI-based installation
Version tracking
Update support
LLVM Management

The standalone system also supports LLVM installation and version management. The LLVM module helps users:

Install LLVM automatically
Track installed versions
Check latest versions
Verify installation status
Manage installation directories

This ensures proper support for HDL compilation and simulation workflows.

Dependency Automation

The dependency management system installs required libraries and system components automatically using Chocolatey and command-line operations.

Dependencies include:

make
gnat
clang
llvm
zlib
GTK modules
X11 libraries

The dependency manager also updates package status information into the installation database after successful installation.

Installation Tracking System

The project maintains a centralized package database using install_details.json.

The JSON file stores:

Package names
Installed versions
Installation status
Installation timestamps
Installation directories
Python package lists
Dependency lists

This allows the standalone system to maintain persistent installation records across sessions.

Logging System

The standalone system includes a complete logging mechanism for:

Installation activities
Errors
Warnings
Update operations
Dependency installation
Package verification

The logging system improves debugging and helps users monitor system activities effectively.

Error Handling

The project implements robust exception handling mechanisms to ensure stable operation during:

Package downloads
Installation failures
JSON parsing
Dependency installation
Version fetching
API requests
PATH configuration

This improves reliability and minimizes unexpected crashes.

User Interface Design

The graphical interface is designed with:

Modern button styling
Interactive layouts
Responsive design
Status indicators
Installation dialogs
Version labels
Update notifications

The UI simplifies complex package management tasks into easy one-click operations.

Technologies Used
Programming Language
Python
GUI Framework
PyQt5
Package Management
Chocolatey
Data Storage
JSON
APIs Used
GitHub Releases API
System Utilities
subprocess
os
shutil
requests
zipfile
Project Architecture

The standalone system follows a modular architecture where each package manager operates independently.

Core Modules
Dependency Manager
Chocolatey Manager
KiCad Package Manager
GHDL Package Manager
LLVM Package Manager
Logging System
JSON Status Manager

This modular approach improves maintainability and scalability.

Workflow of the Standalone System
Step 1

Launch the GUI application.

Step 2

Check package installation status.

Step 3

Fetch latest package versions.

Step 4

Install missing dependencies.

Step 5

Install selected packages.

Step 6

Update installation database.

Step 7

Maintain logs and status reports.

Step 8

Allow updates and future package management.

Advantages of the Standalone System
Simplifies eSim setup process
Reduces manual configuration errors
Provides centralized package management
Improves installation reliability
Supports automatic updates
User-friendly graphical interface
Real-time installation monitoring
Scalable architecture
Efficient dependency management
Better maintainability
Future Enhancements

Future improvements planned for the standalone system include:

Integrated online update server
Multi-platform support
Advanced package analytics
Dark mode UI
Parallel package installation
Backup and restore functionality
Auto-repair mechanisms
Cloud synchronization
Plugin architecture
Real-time progress monitoring
Integrated terminal console
Download manager
Portable package support
Offline installation mode
Use Cases

The eSim Standalone System can be used in:

Engineering colleges
Research laboratories
Electronics projects
Embedded systems development
VLSI workflows
FPGA development
HDL simulation environments
Educational workshops
Student training programs
Open-source electronics platforms
Conclusion

The eSim Standalone System is a comprehensive GUI-driven package and dependency management solution designed to simplify the setup and maintenance of the eSim environment on Windows systems. By automating installations, updates, dependency handling, and version management, the project significantly reduces configuration complexity and improves user productivity.

Its modular architecture, graphical interface, automated workflows, and centralized management system make it a scalable and efficient solution for students, developers, educators, and electronics engineers working in simulation and hardware design environments.

The project serves as a strong foundation for future expansion into a fully integrated and intelligent tool management ecosystem for electronic design automation and simulation platforms.