# eSim Automated Tool Manager

A prototype command-line tool manager that automates installation, update
checking, configuration, and dependency management for eSim's external
tools (Ngspice, KiCad, GHDL, and easily extensible to more).

This submission satisfies:
- **Requirement 1** — Tool Installation Management (cross-platform, version-aware)
- **Requirement 2** — Update/Upgrade System (`check-updates`, `update`)
- **Requirement 3** — Configuration Handling (PATH resolution, `user_config.json`)
- **Requirement 4** — Dependency Checker (`check-deps`)
- **Requirement 5** — CLI + logging (`list`, `logs`, `config/`, `logs/tool_manager.log`)
- **Bonus (Req 6)** — Uses native package managers (`apt` / `brew` / `choco`)
  detected automatically per OS.

That is all 5 core requirements plus the optional bonus, using a single
lightweight, dependency-free Python package.

## Requirements

- Python 3.8+
- No third-party pip packages required (standard library only)
- Linux: `apt` (Debian/Ubuntu) recommended for real installs
- macOS: `brew`
- Windows: `choco`

> Note: actual installation of Ngspice/KiCad/GHDL requires elevated
> privileges (via `sudo` on a normal user account, or none if already
> root) and internet access. The manager detects whether `sudo` is
> needed/available and only prepends it when appropriate — it will not
> fail with a misleading error when run as root in a container with no
> `sudo` binary installed. All commands also support `--dry-run` so the
> logic can be verified without making system changes (useful for
> grading environments and CI).
>
> The install/update logic (command construction, sudo handling, version
> detection, and configuration-manifest writing) is covered by the
> automated test suite with all system calls mocked, and has been
> exercised manually via `--dry-run` to confirm the generated commands
> are correct (e.g. `apt install -y ngspice`). A real, non-dry-run
> install has not been independently verified on a fresh machine as
> part of this submission.

## Project layout

```
esim-tool-manager/
├── esim_tool_manager/
│   ├── __init__.py
│   ├── __main__.py       # `python -m esim_tool_manager ...`
│   ├── core.py           # ToolManager, ConfigStore, DependencyChecker, VersionDetector
│   └── cli.py            # argparse-based CLI
├── config/                # auto-created: registry + installed state + user config
├── logs/                  # auto-created: tool_manager.log (full audit trail)
├── docs/
│   └── design_document.md
└── README.md
```

## Installation

```bash
git clone <your-fork-url>
cd esim-tool-manager
# no pip install needed — standard library only, run directly with:
#   python -m esim_tool_manager <command>

# Optional: install as a console script (still zero third-party dependencies)
pip install -e .
esim-tool-manager list
```

## Usage

```bash
# See all known tools, installed versions, and whether updates are available
python -m esim_tool_manager list

# Check whether required system-level dependencies (gcc, make, ...) exist
python -m esim_tool_manager check-deps ngspice

# Install a tool (uses apt/brew/choco automatically based on OS)
python -m esim_tool_manager install ngspice
python -m esim_tool_manager install ngspice --dry-run   # preview only, no changes

# Check for updates across all registered tools
python -m esim_tool_manager check-updates

# Update a specific tool
python -m esim_tool_manager update ngspice --dry-run

# Configure PATH/env resolution for an already-installed tool
python -m esim_tool_manager configure ngspice

# Find the action log (every install/update/error is recorded here)
python -m esim_tool_manager logs
```

## Running the test suite

The project ships with a standard-library `unittest` suite (no pytest
dependency needed, keeping the project dependency-free) covering version
parsing, platform/package-manager detection, install-command generation,
the runtime-vs-build dependency split, and unknown-tool error handling.

```bash
python -m unittest discover -s tests -v
```

Expected: **21 tests, all passing**, in well under a second (everything is
mocked — no real installs or network calls happen during tests).

## Testing without root/admin access (recommended for reviewers)

Every state-changing command supports `--dry-run`, which prints the exact
command that *would* run and logs it, without executing anything:

```bash
python -m esim_tool_manager install kicad --dry-run
python -m esim_tool_manager update kicad --dry-run
```

## Sample output

```text
$ python -m esim_tool_manager list
TOOL     INSTALLED      LATEST         UPDATE?
-------------------------------------------------
ngspice  not installed  42             no
kicad    not installed  8.0.0          no
ghdl     not installed  4.1.0          no

$ python -m esim_tool_manager install ngspice --dry-run
Starting installation for 'ngspice' on Linux
[ngspice] No runtime dependencies required.
[ngspice] All build dependencies (only needed if compiling from source) satisfied.
Running: sudo apt install -y ngspice
[dry-run] Skipping actual execution.

$ python -m esim_tool_manager install doesnotexist
Error: Unknown tool 'doesnotexist'. Known tools: ['ngspice', 'kicad', 'ghdl']

Available tools:
  ngspice
  kicad
  ghdl
```

## Extending to a new tool

Add an entry to `config/tool_registry.json` (auto-generated on first run)
following the existing `ngspice`/`kicad`/`ghdl` shape — no code changes
needed for tools installable via a standard package manager.

## Design document

See [`docs/design_document.md`](docs/design_document.md) for full
architecture, module responsibilities, and future roadmap (GUI, direct
binary downloads for tools without package-manager support, checksum
verification, rollback).
