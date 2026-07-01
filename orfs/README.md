# eSim-2.5 OpenROAD Flow Script Installation Guide

## **Platform :** Ubuntu 22.04 LTS

# 1. Clone the Repository

Open a terminal and run:

```bash
git clone https://github.com/FOSSEE/eSim.git
```
---

# 2. Move to the Project Directory

```bash
cd eSim
```

---

# 3. eSim-2.5 Installation and Uninstallation

## • Install eSim and Required Dependencies

Give execution permission to the installation script and run it:

```bash
chmod +x install-eSim.sh
./install-eSim.sh --install
```

This step installs:

- eSim
- OpenROAD dependencies
- Required tools and libraries

## • Uninstall eSim and All Components

```bash
./install-eSim.sh --uninstall
```

This removes eSim and all installed components from the system.

---

# 4. Build OpenROAD Flow Scripts 

## • Build orfs Locally

Run the following command:

```bash
python3 orfs-setup.py
```

This command builds the OpenROAD Flow Scripts required for RTL-to-GDSII generation.

## • Rebuild orfs (If Build Fails)

If the build process fails:

1. Delete the existing `OpenROAD-flow-scripts` folder.
2. Run the build command again:

```bash
python3 orfs-setup.py
```

---

# 5. Running the Tools

## • Run eSim

### 1. Using Terminal

```bash
esim
```

### 2. Using Desktop Shortcut

Double-click the **eSim** desktop icon.

## • Run OpenROAD GUI

```bash
cd ~ eSim/orfs/OpenROAD-flow-scripts/flow
openroad -gui
```

## • Run Yosys

```bash
yosys
```

## • Run KLayout

```bash
klayout
```

---

# 6. Viewing Layouts in OpenROAD GUI

Start the OpenROAD GUI:

```bash
cd ~ eSim/orfs/OpenROAD-flow-scripts/flow
openroad -gui
```

## • View Half Adder Layout TCL Commands

```tcl
read_lef platforms/sky130hd/lef/sky130_fd_sc_hd.tlef

read_lef platforms/sky130hd/lef/sky130_fd_sc_hd_merged.lef

read_def results/sky130hd/Half_Adder/base/6_final.def

gui::fit
```

## • View Full Adder Layout TCL Commands

```tcl
read_liberty platforms/sky130hd/lib/sky130_fd_sc_hd__tt_025C_1v80.lib   (Optional)

read_lef platforms/sky130hd/lef/sky130_fd_sc_hd.tlef

read_lef platforms/sky130hd/lef/sky130_fd_sc_hd_merged.lef

read_def results/sky130hd/FullAdder/base/6_final.def

gui::fit
```
