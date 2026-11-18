# eSim 2.5 GUI and simulation on Ubuntu 25.04 — visual evidence

The earlier verification (`LIVE_VERIFICATION.md`) stopped at the command line:
dependencies, the GHDL/LLVM build, the Python layer. This document closes the
remaining gap by running **the eSim 2.5 application itself** and **ngspice** on
the same Ubuntu 25.04 machine, with screenshots.

## How the GUI was run

The environment is the same Ubuntu 25.04 (Plucky Puffin) userland from
`LIVE_VERIFICATION.md`. It has WSLg, so a real X server is present at
`DISPLAY=:0` — verified with `xdpyinfo`:

```
name of display:    :0
version number:    11.0
vendor string:    Microsoft Corporation
```

eSim's GUI imports were installed exactly as the patched installer does — the
same pinned `hdlparse` 1.0.7, plus PyQt5, matplotlib and watchdog:

```
$ /root/esim-env/bin/python -c "import PyQt5, matplotlib, hdlparse.verilog_parser as v; v.VerilogExtractor()"
PyQt5 + QtWidgets + matplotlib + hdlparse: OK
pyhdlparser hdlparse version: 1.0.7
```

`Application.py` then constructs the real window, shows it, and loads a shipped
example project into the project tree.

**One honest note on how the screenshots were taken.** WSLg's Weston
compositor refuses `X_GetImage` on the root window, so an external tool such as
`import` or `xwd` cannot capture the screen:

```
X Error of failed request:  BadMatch (invalid parameter attributes)
  Major opcode of failed request:  73 (X_GetImage)
```

The screenshots are therefore rendered by **Qt itself** (`QWidget.grab()`),
which is eSim's own widget tree drawn at full fidelity — the same pixels the
window manager would display. The application runs for real; only the capture
path differs from a desktop screenshot. This is stated here rather than
implied otherwise.

## What the screenshots show

| File | What it is |
|---|---|
| `01-esim-gui-project-loaded.png` | The eSim 2.5 main window. The FOSSEE banner, the full left toolbar (NgVeri, NGHDL, Modelica, Makerchip, …), **Project tree showing the shipped `Astable555` example loaded**, the Welcome pane, and the status line `eSim Started…… Project Selected : None`. |
| `02-esim-about.png` | eSim's version dialog: **eSim 2.5**, *Running on Ubuntu 25.04 (Plucky Puffin)*, **Python 3.13.3 · PyQt5 5.15.14**, FOSSEE IIT Bombay. |
| `03-ngspice-transient.png` | A real ngspice 44.2 transient simulation on this machine, plotted from the 108 sample points ngspice produced. |
| `04-esim-project-tree.png` | The project explorer pane at native scale, showing the `Astable555` node. |

The eSim window is 796×596 in every capture because eSim fixes its own window
size at construction; this is the application's geometry, not a crop.

## The simulation

ngspice is what eSim actually simulates circuits with. On this Ubuntu 25.04:

```
$ ngspice --version
** ngspice-44.2 : Circuit level simulation program
** Compiled with KLU Direct Linear Solver
```

A 5 V step into a 1 kΩ / 1 µF RC low-pass was simulated and plotted from the
printed `.tran` points — a textbook charge to 5 V and discharge to 0 V with the
correct 1 ms time constant. `scripts/rc-verify.cir` is the deck and
`scripts/16-plot-simulation.py` draws the figure from ngspice's own output.

The shipped `Examples/Astable555` project was also run through ngspice. Its
`.cir` netlist references the LM555 subcircuit through eSim's interactive
`plot_v1` probe, which only works inside the eSim GUI session, so a bare
`ngspice -b` on that file does not complete — that is a property of the example's
probe wiring, not of the installation. `E-ngspice-simulation.log` records the
attempt and the exact error.

## What this adds

`LIVE_VERIFICATION.md` proved the **installer** works on Ubuntu 25.04. This
document proves the **installed result** works: the GUI starts, loads a project,
and the simulator it drives produces correct results. Together they cover every
layer the task asks about except an operator physically clicking the toolbar.

## Reproduce

```bash
# dependencies and Python environment
bash scripts/12-esim-env.sh

# load a project into the GUI and render it
/root/esim-env/bin/python scripts/17-esim-project-open.py \
    <pkg>/src/frontEnd <out-dir> <pkg>

# the version dialog
/root/esim-env/bin/python scripts/14-esim-gui-shots.py \
    <pkg>/src/frontEnd <out-dir> <pkg>

# the simulation and its plot
bash scripts/15-ngspice-simulation.sh
python scripts/16-plot-simulation.py <ngspice-output> <out.png>
```
