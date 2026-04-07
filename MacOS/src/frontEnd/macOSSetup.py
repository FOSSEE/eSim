# src/frontEnd/macOSSetup.py
"""
macOS-specific setup for eSim KiCad library registration.
Runs on first eSim launch after KiCad has been initialized.
"""

import os
import sys
import logging

logger = logging.getLogger(__name__)

FLAG_FILE = os.path.expanduser("~/.esim/.macos_kicad_setup_done")
KICAD6_PREFS = os.path.expanduser("~/Library/Preferences/kicad/6.0")
SYM_LIB_TABLE = os.path.join(KICAD6_PREFS, "sym-lib-table")


def is_setup_done():
    return os.path.exists(FLAG_FILE)


def is_kicad_initialized():
    exists = os.path.exists(KICAD6_PREFS)
    logger.debug(f"KiCad prefs dir '{KICAD6_PREFS}' exists: {exists}")
    return exists


def get_esim_symbols_dir() -> str | None:
    """
    Resolve eSim symbols dir whether running from source or .app bundle.
    Returns absolute path or None if not found.
    """
    candidates = []

    # ── 1. Running inside PyInstaller .app bundle ──────────────────────
    if getattr(sys, 'frozen', False):
        # sys.executable = .../eSim.app/Contents/MacOS/eSim
        contents_dir = os.path.dirname(os.path.dirname(sys.executable))
        candidates.append(
            os.path.join(contents_dir, 'Resources',
                         'library', 'kicadLibrary', 'eSim-symbols')
        )
        # Also check _MEIPASS (PyInstaller extracted data root)
        candidates.append(
            os.path.join(sys._MEIPASS,
                         'library', 'kicadLibrary', 'eSim-symbols')
        )

    # ── 2. Running from source ─────────────────────────────────────────
    # This file is at src/frontEnd/macOSSetup.py
    # so esim_root = ../../
    this_file  = os.path.abspath(__file__)
    src_fe_dir = os.path.dirname(this_file)       # src/frontEnd/
    src_dir    = os.path.dirname(src_fe_dir)      # src/
    esim_root  = os.path.dirname(src_dir)         # eSim root
    candidates.append(
        os.path.join(esim_root, 'library', 'kicadLibrary', 'eSim-symbols')
    )

    # ── 3. Fallback: env var ───────────────────────────────────────────
    bundle_path = os.environ.get('ESIM_BUNDLE_PATH', '')
    if bundle_path:
        candidates.append(
            os.path.join(bundle_path, 'Contents', 'Resources',
                         'library', 'kicadLibrary', 'eSim-symbols')
        )

    for path in candidates:
        logger.debug(f"Checking symbols candidate: {path}")
        if os.path.exists(path):
            logger.info(f"Found eSim symbols at: {path}")
            return path

    logger.error(f"eSim symbols not found. Tried:\n" +
                 "\n".join(f"  {p}" for p in candidates))
    return None


def find_kicad_symbol_dir() -> str | None:
    """Find KiCad's own symbol directory (used only for verification)."""
    import json
    common_json = os.path.join(KICAD6_PREFS, "kicad_common.json")
    if os.path.exists(common_json):
        try:
            with open(common_json) as f:
                data = json.load(f)
            env = data.get("environment", {}).get("vars") or {}
            if "KICAD6_SYMBOL_DIR" in env:
                logger.debug(f"KICAD6_SYMBOL_DIR from json: {env['KICAD6_SYMBOL_DIR']}")
                return env["KICAD6_SYMBOL_DIR"]
        except Exception as e:
            logger.warning(f"Could not parse kicad_common.json: {e}")

    default = "/Applications/KiCad/KiCad.app/Contents/SharedSupport/symbols"
    if os.path.exists(default):
        return default

    logger.warning("KiCad symbol dir not found")
    return None


def ensure_sym_lib_table_exists():
    """
    Create a minimal sym-lib-table if KiCad hasn't created one yet.
    This can happen if KiCad was installed but never fully opened.
    """
    if os.path.exists(SYM_LIB_TABLE):
        return True

    logger.warning(f"sym-lib-table missing, creating minimal one at {SYM_LIB_TABLE}")
    os.makedirs(os.path.dirname(SYM_LIB_TABLE), exist_ok=True)
    with open(SYM_LIB_TABLE, 'w') as f:
        f.write('(sym_lib_table\n)\n')
    return True


def register_esim_libraries(sym_lib_table_path: str, symbols_src: str) -> bool:
    """
    Register eSim symbol libraries in KiCad's sym-lib-table.
    Uses absolute paths from eSim's bundled/installed location.
    """
    esim_libs = [
        ("eSim_Analog",        "eSim_Analog.kicad_sym"),
        ("eSim_Devices",       "eSim_Devices.kicad_sym"),
        ("eSim_Digital",       "eSim_Digital.kicad_sym"),
        ("eSim_Hybrid",        "eSim_Hybrid.kicad_sym"),
        ("eSim_Miscellaneous", "eSim_Miscellaneous.kicad_sym"),
        ("eSim_Nghdl",         "eSim_Nghdl.kicad_sym"),
        ("eSim_Ngveri",        "eSim_Ngveri.kicad_sym"),
        ("eSim_Plot",          "eSim_Plot.kicad_sym"),
        ("eSim_Power",         "eSim_Power.kicad_sym"),
        ("eSim_Sources",       "eSim_Sources.kicad_sym"),
        ("eSim_Subckt",        "eSim_Subckt.kicad_sym"),
        ("eSim_User",          "eSim_User.kicad_sym"),
        ("eSim_SKY130",        "eSim_SKY130.kicad_sym"),
        ("eSim_IHP",           "eSim_IHP.kicad_sym"),
    ]

    # Verify symbol files actually exist before registering
    missing = []
    for name, filename in esim_libs:
        full_path = os.path.join(symbols_src, filename)
        if not os.path.exists(full_path):
            missing.append(full_path)
    if missing:
        logger.warning(f"Some symbol files missing (will skip):\n" +
                       "\n".join(f"  {p}" for p in missing))

    try:
        with open(sym_lib_table_path, 'r') as f:
            content = f.read()
    except Exception as e:
        logger.error(f"Cannot read sym-lib-table: {e}")
        return False

    new_entries = []
    for name, filename in esim_libs:
        uri = os.path.join(symbols_src, filename)
        if name not in content and os.path.exists(uri):
            entry = (
                f'  (lib (name "{name}")'
                f'(type "KiCad")'
                f'(uri "{uri}")'
                f'(options "")'
                f'(descr "eSim Library"))'
            )
            new_entries.append(entry)
            logger.debug(f"Will register: {name} → {uri}")

    if not new_entries:
        logger.info("All eSim libraries already registered in sym-lib-table")
        return True

    # Safely insert before the closing ')'
    new_content = content.rstrip()
    if new_content.endswith(')'):
        new_content = new_content[:-1].rstrip()
        new_content += '\n' + '\n'.join(new_entries) + '\n)\n'
    else:
        # Malformed table — append and close
        logger.warning("sym-lib-table missing closing ')' — repairing")
        new_content += '\n' + '\n'.join(new_entries) + '\n)\n'

    try:
        with open(sym_lib_table_path, 'w') as f:
            f.write(new_content)
        logger.info(f"Registered {len(new_entries)} eSim libraries")
        return True
    except Exception as e:
        logger.error(f"Cannot write sym-lib-table: {e}")
        return False


def reset_setup_flag():
    """Call this to force re-registration on next launch (for debugging)."""
    if os.path.exists(FLAG_FILE):
        os.remove(FLAG_FILE)
        logger.info("Setup flag cleared — will re-run on next launch")


def mark_setup_done():
    os.makedirs(os.path.dirname(FLAG_FILE), exist_ok=True)
    with open(FLAG_FILE, 'w') as f:
        # Record the symbols path used, so we can detect stale installs
        symbols_src = get_esim_symbols_dir() or "unknown"
        f.write(f"eSim macOS KiCad setup completed\nsymbols_src={symbols_src}\n")


def run_macos_kicad_setup(show_ui=True) -> bool:
    if sys.platform != 'darwin':
        return True

    # ── Debug: log key paths on every run ─────────────────────────────
    logger.info(f"sys.frozen={getattr(sys, 'frozen', False)}")
    logger.info(f"sys.executable={sys.executable}")
    if getattr(sys, 'frozen', False):
        logger.info(f"sys._MEIPASS={sys._MEIPASS}")

    if is_setup_done():
        # Re-validate that the registered paths still exist
        symbols_src = get_esim_symbols_dir()
        if symbols_src:
            logger.info("macOS KiCad setup already done and symbols still present")
            return True
        else:
            # Bundle was moved or paths changed — redo registration
            logger.warning("Setup was done but symbols no longer found — re-registering")
            reset_setup_flag()

    if not is_kicad_initialized():
        logger.warning("KiCad preferences directory not found")
        if show_ui:
            from PyQt5 import QtWidgets
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("KiCad Setup Required")
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText(
                "eSim libraries need to be registered with KiCad.\n\n"
                "Please open KiCad once to complete its initial setup,\n"
                "then restart eSim to register eSim libraries automatically."
            )
            msg.exec_()
        return False

    symbols_src = get_esim_symbols_dir()
    if not symbols_src:
        if show_ui:
            from PyQt5 import QtWidgets
            QtWidgets.QMessageBox.critical(
                None, "eSim Setup Error",
                "Could not locate eSim symbol libraries.\n"
                "Please reinstall eSim."
            )
        return False

    ensure_sym_lib_table_exists()

    if not register_esim_libraries(SYM_LIB_TABLE, symbols_src):
        if show_ui:
            from PyQt5 import QtWidgets
            QtWidgets.QMessageBox.critical(
                None, "eSim Setup Error",
                f"Failed to register eSim libraries in KiCad.\n"
                f"Check that KiCad has been opened at least once.\n\n"
                f"sym-lib-table: {SYM_LIB_TABLE}"
            )
        return False

    mark_setup_done()
    logger.info("macOS KiCad setup completed successfully")

    if show_ui:
        from PyQt5 import QtWidgets
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("eSim Setup Complete")
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText(
            "eSim libraries have been successfully registered with KiCad.\n"
            "You can now use eSim components in your schematics."
        )
        msg.exec_()

    return True