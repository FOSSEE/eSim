# Live Verification on Ubuntu 25.04 (Plucky Puffin)

This document records the on-machine verification that the original Task 4
report listed as outstanding. Everything below was executed on a real Ubuntu
25.04 userland (`PRETTY_NAME="Ubuntu 25.04"`, Python 3.13.3, apt 3.0.0) against
the live plucky archive, the unmodified eSim 2.5 package, and a real GHDL 4.1.0
build. Nothing is mocked. Raw logs are in `logs/`; `EVIDENCE_INDEX.md` maps each
log to the finding it proves.

## How the environment was created

Ubuntu 25.04 is an interim release and is no longer offered by `wsl --install`.
The official image `ubuntu-25.04-wsl-amd64.wsl` is still published on
`old-releases.ubuntu.com`; it was downloaded, verified against the published
`SHA256SUMS`, and imported as a separate distro (`Ubuntu2504`) so the host's
existing Ubuntu 24.04 stayed untouched.

```
sha256sum ubuntu-25.04-wsl-amd64.wsl
91f3e836698719846191821300bd21f321811abcef6f448bf8d7d8f8517b2743   (matches SHA256SUMS)
```

The plucky archive still resolves, so `apt-get update` and every package
operation below ran against the real Ubuntu 25.04 repositories.

## Headline result: the shipped package does not install at all

Running the unmodified eSim 2.5 package on Ubuntu 25.04:

```
$ cd eSim-2.5 && ./install-eSim.sh --install
Detected Ubuntu Version:
Unsupported Ubuntu version: 25.04 ()
```

The package ships `install-eSim-22.04.sh`, `install-eSim-23.04.sh` and
`install-eSim-24.04.sh` — **there is no 25.04 script**. The dispatcher's
`case $VERSION_ID` has no 25.04 arm, so it falls to `*)` and exits 1. The same
wall exists inside `nghdl.zip`: its dispatcher only knows 22.04/23.04/24.04.

This reframes E6. The finding is not only "25.10 and 26.04 are unrouted"; on a
stock Ubuntu 25.04 machine the installer never starts. The report's E6 fix —
routing 25.04 to a real 25.04 script, plus 25.10/26.04 in compatibility mode —
is exactly what turns the first line above into a working run.

With the fixed dispatcher, on the same machine:

```
Detected Ubuntu Version: 25.04
Running script: .../install-eSim-scripts/install-eSim-25.04.sh --install
  >>> ROUTED to install-eSim-25.04.sh, argument=--install
```

## Findings reproduced live

### E3 — hdlparse `use_2to3` (Python 3.13)

```
$ python3 -m venv venv && venv/bin/pip install hdlparse
error in hdlparse setup command: use_2to3 is invalid.
```

The fix installs and satisfies eSim's exact import:

```
$ venv/bin/pip install --upgrade "git+https://github.com/hdl/pyhdlparser.git@e1153ace..."
Successfully installed hdlparse-1.0.7
$ venv/bin/python -c "import hdlparse.verilog_parser as v; v.VerilogExtractor()"
VerilogExtractor OK
```

### E4 — the venv cannot see the system packages

The original `installDependency()` apt-installs PyQt5 / matplotlib / psutil
system-wide, then creates a venv without `--system-site-packages`. Verified:

```
system python3: PyQt5 + matplotlib + psutil OK
venv python:   ModuleNotFoundError: No module named 'PyQt5'
               ModuleNotFoundError: No module named 'matplotlib'
               ModuleNotFoundError: No module named 'psutil'
```

The system installs are dead weight; the venv needs its own pip installs, which
the patched script keeps.

### E5 — the dispatcher writes to the filesystem root

With `config_dir` and `config_file` undefined (as they are in
`install-eSim.sh`), the leftover lines expand to `/`:

```
$ bash e5-demo.sh
/: Is a directory
```

The patched dispatcher deletes those lines and closes the `if` block.

### E2 — unzip is genuinely absent on a fresh 25.04

```
$ which unzip
NOT FOUND
$ apt-get install -y unzip xz-utils    # the fix
$ which unzip
/usr/bin/unzip
```

### E6 — the KiCad pin resolves exactly on 25.04

```
$ apt-get install --simulate -y kicad=8.0.8+dfsg-1
Conf kicad (8.0.8+dfsg-1 Ubuntu:25.04/plucky [amd64])
$ apt-cache show kicad | grep ^Version
Version: 8.0.8+dfsg-1
```

### N1 — libcanberra-gtk-module has no candidate

```
$ apt-get install -y libcanberra-gtk-module libcanberra-gtk3-module
E: Package 'libcanberra-gtk-module' has no installation candidate
$ apt-get install -y libcanberra-gtk3-module       # the fix
Setting up libcanberra-gtk3-module:amd64 (0.30-17ubuntu2)
```

### N2 — the unversioned llvm is LLVM 20

```
$ apt-cache policy llvm | grep Candidate
  Candidate: 1:20.0-63ubuntu1
$ apt-get install -y llvm-18 llvm-18-dev clang-18
$ /usr/bin/llvm-config-18 --version
18.1.8
```

### N3 — GHDL 4.1.0 actually builds and simulates against LLVM 18

This is the claim the original report left as static analysis. It was executed:

```
$ ./configure --with-llvm-config=/usr/bin/llvm-config-18
Debugging is enabled with llvm 18.1.8
$ make -j28 CXX=clang++-18
make-exit=0  elapsed=1156s
$ make install
$ ghdl --version
GHDL 4.1.0 (tarball) [Dunoon edition]
 llvm 18.1.8 code generator
$ ldd ghdl1-llvm | grep llvm
libLLVM-18.so.18.1 => /lib/x86_64-linux-gnu/libLLVM-18.so.18.1
```

A real VHDL counter was then simulated end to end with that build:

```
$ ghdl -a --std=08 counter.vhdl counter_tb.vhdl
$ ghdl -e --std=08 counter_tb
$ ghdl -r --std=08 counter_tb --stop-time=200ns
count = 0 ... count = 8
PASS: counter reached 8 with the LLVM 18 backend
```

### N4 — the uninstall path purges empty package names

With `llvm_version` unset, as in the shipped script:

```
apt-get purge -y llvm-${llvm_version} llvm-${llvm_version}-dev
  ->  apt-get purge -y llvm- llvm--dev
```

## A new defect found during live verification

The build exposed a bug the original report did not list. GHDL's LLVM backend
is compiled with a **C++** driver, and the script never tells the build which
one to use. The unversioned `/usr/bin/clang++` belongs to the system LLVM 20:

```
$ readlink -f $(command -v clang++)
/usr/lib/llvm-20/bin/clang
```

So a plain `make` links LLVM 20's C++ front end against LLVM 18's libraries.
In practice this shows up as a hard failure (`clang++: not found` when only
`clang-18` is present and no unversioned `clang++` exists) or as a toolchain
mismatch. The fix — now in the shipped script and patch — builds with
`CXX=clang++-${llvm_version}`, mirroring the existing
`--with-llvm-config=/usr/bin/llvm-config-${llvm_version}` discipline. Note that
`clang-18` already ships `/usr/bin/clang++-18`, verified with `dpkg -L`; no
additional package is required, only the `CXX=` override on the `make` line.

## What remains out of scope

The GUI itself — launching `esim` on an X display and clicking through the
schematic editor — was not exercised. That needs a desktop session, not a
headless userland. Everything the task asks for at the installer level
(dependency resolution, version pinning, the GHDL/LLVM build, the Python
package layer) was executed and is recorded here.
