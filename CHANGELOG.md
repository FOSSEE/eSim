# Changelog
All notable changes to the eSim project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Created `/tests/test_security_p0.py` verifying all 26 edge cases for AST-based expression evaluation and subprocess sandboxing.
- Implemented Phase 1 DevOps automation pipeline (`.github/workflows/esim-ci.yml`), establishing Ruff, Pyright, and headless pytest-qt runner rules.
- Set up local pre-commit hooks configuration (`.pre-commit-config.yaml`) and central tool settings (`pyproject.toml`).

### Changed
- **PR #506 Conflict Resolution**: Restored our advanced, regex-based placeholder expression evaluator inside `plot_function` to safely compute traces containing parentheses (such as `v(out)`).

### Fixed
- **VULN-01 (P0 - Critical)**: Eliminated arbitrary code execution by replacing raw `eval()` in `plot_window.py` with a robust, whitelisted AST expression parser supporting standard mathematical operations (`np.sin`, `np.cos`, `np.log`, etc.).
- **VULN-02 (P0 - Critical)**: Eliminated shell injection in `pspiceToKicad.py` by converting `subprocess.run(shell=True)` to standard list-of-arguments process calling via `sys.executable`.
- **VULN-03 (P1 - High)**: Hardened `ngspice_ghdl.py` by converting vulnerable `subprocess.call(..., shell=True)` invocations to use safe list-of-arguments process execution and `shutil.rmtree`.
