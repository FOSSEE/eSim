# Evidence index — eSim 2.5 on Ubuntu 25.04

All logs below were produced on a real Ubuntu 25.04 (Plucky Puffin) userland
(kernel `6.6.87.2-microsoft-standard-WSL2`, Python 3.13.3, apt 3.0.0) against
the live plucky archive, the unmodified eSim 2.5 package, and a real GHDL 4.1.0
build. Nothing is mocked. `LIVE_VERIFICATION.md` tells the story;
`scripts/` reproduces every log below.

| Log | Finding | Bytes | SHA-256 (first 16) | What it shows |
|---|---|---:|---|---|
| `E-shipped-installer-25.04.log` | E6 / entry gate | 844 | `aa06cead3be9f535` | The unmodified eSim 2.5 package on Ubuntu 25.04 exits with `Unsupported Ubuntu version: 25.04` — the package ships no 25.04 script. |
| `E-fixed-dispatcher.log` | E6 fix | 676 | `29877ea65d072ce3` | Same machine, fixed dispatcher: detects 25.04 and routes to `install-eSim-25.04.sh` instead of exiting. |
| `E3-hdlparse-reproduction.log` | E3 | 1105 | `59a30fec2096e30f` | `pip install hdlparse` fails on 25.04 / Python 3.13: `use_2to3 is invalid`. |
| `E3-hdlparse-fix.log` | E3 fix | 452 | `c9a4d06d3588fe08` | Pinned `pyhdlparser` installs `hdlparse 1.0.7`; `VerilogExtractor` — the class eSim imports — instantiates. |
| `E4-venv-isolation.log` | E4 | 984 | `815423feeff52128` | System-wide PyQt5/matplotlib/psutil install fine but are invisible inside the venv the installer creates. |
| `E5-dead-code.log` | E5 | 1052 | `aa4946876537a261` | The dispatcher's leftover config lines expand to `/` and fail with `Is a directory`. |
| `E6-kicad-pin.log` | E6 / installKicad | 949 | `ff26f6fdf9f83300` | `kicad=8.0.8+dfsg-1` resolves exactly on plucky; the unpinned fallback is shown too. |
| `claims-verification.log` | E1, E2, N4 | 1911 | `192c47fc6c5e92c0` | `unzip` absent then installed by the fix; the `exit 0` demo; the undefined `llvm_version` expansion; installed-package state. |
| `N1-libcanberra.log` | N1 | 649 | `0ad48e82e2371ed7` | `libcanberra-gtk-module` has no installation candidate; `libcanberra-gtk3-module` installs fine. |
| `N2-llvm18-install.log` | N2 | 558 | `ce9f58cbda5c2207` | Unversioned `llvm` is 20.0; `llvm-18`/`llvm-18-dev`/`clang-18` install as 18.1.8; `llvm-config-18` present. |
| `N3-ghdl-configure.log` | N3 | 1044 | `29952063cb9d5ee6` | GHDL 4.1.0 configure against `/usr/bin/llvm-config-18`: `Debugging is enabled with llvm 18.1.8`. |
| `N3-ghdl-build.log` | N3 | 11156 | `58dee7633b2c21c3` | Full GHDL 4.1.0 build in the `/mnt` tree: builds, installs, links `libLLVM-18.so.18.1`, reports `llvm 18.1.8 code generator`. |
| `N3-ghdl-simulation.log` | N3 end-to-end | 862 | `d096f28721472661` | A real VHDL counter simulated with that build: analyse, elaborate, run, counts 0-8, PASS assertion. |
| `N3-ghdl-source.log` | N3 setup | 165 | `8fa3880e275cf5b1` | GHDL 4.1.0 source acquisition. |
| `N-finding-clangxx.log` | new finding | 497 | `bfd350966722b3fd` | `clang-18` ships `/usr/bin/clang++-18` (`dpkg -L`); the unversioned `/usr/bin/clang++` belongs to LLVM 20. |
| `N-new-clangxx-fix-verify.log` | new finding + fix | 784 | `53177d85843edcb6` | Clean-room build. **Control:** plain `make` invokes the unversioned `clang++` (LLVM 20). **Fix:** `make CXX=clang++-18` builds exit 0 and links `libLLVM-18.so.18.1`. |
| `N-shipped-nghdl.log` | N1-N4 on shipped package | 1586 | `931f36c6cbd24b63` | The `nghdl.zip` dispatcher also refuses 25.04; its 24.04 dependency step's four bugs are executed directly on 25.04. |
| `E-ngspice-simulation.log` | installed-result check | 943 | `9201ed66c2dfa6cb` | ngspice 44.2 runs a real transient simulation; the shipped Astable555 example's probe wiring is also shown. |

## Screenshots (eSim GUI and simulation)

See `GUI_VERIFICATION.md` for method and caveats. These are rendered by Qt from
eSim's own widget tree because WSLg's Weston refuses `X_GetImage`; the
application runs for real.

| File | Bytes | SHA-256 (first 16) | What it shows |
|---|---:|---|---|
| `screenshots/01-esim-gui-project-loaded.png` | 51830 | `11107c74e014ff53` | eSim 2.5 main window with the Astable555 example in the project tree, full toolbar, FOSSEE banner. |
| `screenshots/02-esim-about.png` | 22558 | `1039c88ea24f8e86` | Version dialog: eSim 2.5, Ubuntu 25.04 (Plucky Puffin), Python 3.13.3, PyQt5 5.15.14. |
| `screenshots/03-ngspice-transient.png` | 46747 | `87e549969bc820cb` | ngspice 44.2 RC transient plotted from its own 108 samples. |
| `screenshots/04-esim-project-tree.png` | 7303 | `fa14aeec2545e6ea` | The project explorer pane at native scale. |

## Headline result

The shipped eSim 2.5 package refuses to install on Ubuntu 25.04 at all: its
dispatcher only knows 22.04, 23.04 and 24.04. The fixed dispatcher detects
25.04 and proceeds. That difference is the two `E-*dispatcher*` logs.

## New defect not in the original report

GHDL's LLVM backend is compiled with a C++ driver, and the script never pins
which one. Plain `make` uses the unversioned `clang++`, whose target is
`/usr/lib/llvm-20/bin/clang` — LLVM 20's front end against LLVM 18's libraries.
The fix is one flag, `CXX=clang++-${llvm_version}` on the `make` line, proven by
the control/fix pair in `N-new-clangxx-fix-verify.log`.
