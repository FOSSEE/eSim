#!/bin/bash
#=============================================================================
# Focused unit test: KiCad 8.0 symbol-table copy logic
# Target: Ubuntu/install-eSim-scripts/install-eSim-25.04.sh (copyKicadLibrary)
#
# This test extracts and executes the actual production copyKicadLibrary()
# function directly from the installer script under an isolated sandbox.
#=============================================================================
set -euo pipefail

echo "============================================================"
echo "Running focused test for production copyKicadLibrary()..."
echo "============================================================"

# Resolve repository and installer script path
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALLER_SCRIPT="$(cd "$SCRIPT_DIR/../install-eSim-scripts" && pwd)/install-eSim-25.04.sh"

if [ ! -f "$INSTALLER_SCRIPT" ]; then
    echo "ERROR: Target installer script not found: $INSTALLER_SCRIPT" >&2
    exit 1
fi

echo "Target installer: $INSTALLER_SCRIPT"

# 1. Extract the actual production copyKicadLibrary function directly from installer
EXTRACTED_FUNC=$(sed -n '/^function copyKicadLibrary/,/^}/p' "$INSTALLER_SCRIPT")

if [ -z "$EXTRACTED_FUNC" ]; then
    echo "ERROR: Failed to extract copyKicadLibrary() from $INSTALLER_SCRIPT" >&2
    exit 1
fi

# Define error_exit stub to satisfy trap error_exit ERR inside production function
error_exit() {
    echo "ERROR: error_exit trap invoked during copyKicadLibrary execution" >&2
    exit 1
}

# Evaluate the production function into the current test shell
eval "$EXTRACTED_FUNC"

# 2. Set up isolated sandbox environment
TEST_SANDBOX=$(mktemp -d /tmp/esim_kicad8_test.XXXXXX)
trap 'rm -rf "$TEST_SANDBOX"' EXIT

TEST_HOME="$TEST_SANDBOX/mock_home"
mkdir -p "$TEST_HOME"

MOCK_SYSTEM_SYMBOLS="$TEST_SANDBOX/mock_usr_share_kicad_symbols"
mkdir -p "$MOCK_SYSTEM_SYMBOLS"

WORK_DIR="$TEST_SANDBOX/work"
mkdir -p "$WORK_DIR"

# Sample fixture data payloads
FIXTURE_SYM_CONTENT='(sym_lib_table
  (lib (name "eSim_Devices")(type "KiCad")(uri "${KICAD6_SYMBOL_DIR}/eSim_Devices.kicad_sym")(options "")(descr "eSim discrete devices"))
  (lib (name "eSim_Subckt")(type "KiCad")(uri "${KICAD6_SYMBOL_DIR}/eSim_Subckt.kicad_sym")(options "")(descr "eSim subcircuits"))
)'

FIXTURE_DEVICE_SYM='(kicad_symbol_lib (version 20231120) (generator eSim)
  (symbol "eSim_Diode" (in_bom yes) (on_board yes))
)'

# Helper function to create/recreate mock fixture files
create_fixtures() {
    mkdir -p "$WORK_DIR/kicadLibrary/template"
    mkdir -p "$WORK_DIR/kicadLibrary/eSim-symbols"
    echo "$FIXTURE_SYM_CONTENT" > "$WORK_DIR/kicadLibrary/template/sym-lib-table"
    echo "$FIXTURE_DEVICE_SYM" > "$WORK_DIR/kicadLibrary/eSim-symbols/eSim_Devices.kicad_sym"
}

# 3. Mock system commands so no system paths are modified

# Mock tar:
# Production function executes: tar -xJf library/kicadLibrary.tar.xz
# In this unit test, fixtures are provided directly in kicadLibrary/.
# Note: Binary archive extraction itself is not covered by this focused path test.
tar() {
    :
}

# Mock sudo:
# Intercepts /usr/share/kicad/symbols/ and redirects cp into mock system directory.
# Makes chown a harmless no-op.
sudo() {
    if [ "$1" = "cp" ]; then
        shift
        local args=()
        for arg in "$@"; do
            if [ "$arg" = "/usr/share/kicad/symbols/" ] || [ "$arg" = "/usr/share/kicad/symbols" ]; then
                args+=("$MOCK_SYSTEM_SYMBOLS/")
            else
                args+=("$arg")
            fi
        done
        command cp "${args[@]}"
    elif [ "$1" = "chown" ]; then
        :
    else
        command "$@"
    fi
}

# Export environment for isolated execution
ORIGINAL_HOME="$HOME"
export HOME="$TEST_HOME"
export USER="${USER:-testuser}"

cd "$WORK_DIR"

# ------------------------------------------------------------
# Test Phase 1: First Run (Clean environment)
# ------------------------------------------------------------
echo ""
echo "[Test 1] Executing extracted copyKicadLibrary() on fresh environment..."
create_fixtures

# Run the actual extracted production function in a subshell to isolate shell traps/options
(copyKicadLibrary)

# Verification 1.1: Target directory ~/.config/kicad/8.0/ exists
if [ -d "$HOME/.config/kicad/8.0" ]; then
    echo "  [PASS] Target directory ~/.config/kicad/8.0/ was created."
else
    echo "  [FAIL] Target directory ~/.config/kicad/8.0/ was NOT created!" >&2
    exit 1
fi

# Verification 1.2: Target sym-lib-table exists and contents match fixture
TARGET_SYM_TABLE="$HOME/.config/kicad/8.0/sym-lib-table"
if [ -f "$TARGET_SYM_TABLE" ]; then
    echo "  [PASS] Target sym-lib-table exists at: $TARGET_SYM_TABLE"
else
    echo "  [FAIL] Target sym-lib-table was NOT created: $TARGET_SYM_TABLE" >&2
    exit 1
fi

COPIED_CONTENT=$(cat "$TARGET_SYM_TABLE")
if [ "$COPIED_CONTENT" = "$FIXTURE_SYM_CONTENT" ]; then
    echo "  [PASS] sym-lib-table contents match fixture exactly."
else
    echo "  [FAIL] sym-lib-table contents do NOT match fixture!" >&2
    exit 1
fi

# Verification 1.3: Legacy ~/.config/kicad/6.0/ was NOT created
if [ ! -d "$HOME/.config/kicad/6.0" ]; then
    echo "  [PASS] Legacy directory ~/.config/kicad/6.0/ was NOT created."
else
    echo "  [FAIL] Legacy directory ~/.config/kicad/6.0/ was incorrectly created!" >&2
    exit 1
fi

# Verification 1.4: Symbol file copied into mock system directory
COPIED_SYMBOL="$MOCK_SYSTEM_SYMBOLS/eSim_Devices.kicad_sym"
if [ -f "$COPIED_SYMBOL" ]; then
    echo "  [PASS] Symbol copied to system directory: $COPIED_SYMBOL"
else
    echo "  [FAIL] Symbol was NOT copied to system directory: $COPIED_SYMBOL" >&2
    exit 1
fi

# Verification 1.5: Production cleanup of kicadLibrary working directory
if [ ! -d "$WORK_DIR/kicadLibrary" ]; then
    echo "  [PASS] Temporary kicadLibrary/ directory was cleaned up by function."
else
    echo "  [FAIL] Temporary kicadLibrary/ was NOT cleaned up!" >&2
    exit 1
fi

# ------------------------------------------------------------
# Test Phase 2: Second Run (Idempotency check)
# ------------------------------------------------------------
echo ""
echo "[Test 2] Executing extracted copyKicadLibrary() second time (idempotency check)..."

# Recreate fixture (since production function cleans it up at end of run)
create_fixtures

# Execute extracted function second time and capture output
OUTPUT_RUN2=$(copyKicadLibrary)
echo "$OUTPUT_RUN2"

# Verification 2.1: Detected existing KiCad 8.0 directory
if echo "$OUTPUT_RUN2" | grep -q "kicad config folder already exists"; then
    echo "  [PASS] Detected existing config directory on rerun."
else
    echo "  [FAIL] Did not detect existing config directory on rerun!" >&2
    exit 1
fi

# Verification 2.2: sym-lib-table remained intact and uncorrupted
COPIED_CONTENT_RUN2=$(cat "$TARGET_SYM_TABLE")
if [ "$COPIED_CONTENT_RUN2" = "$FIXTURE_SYM_CONTENT" ]; then
    echo "  [PASS] sym-lib-table remains valid and identical after rerun."
else
    echo "  [FAIL] sym-lib-table corrupted after rerun!" >&2
    exit 1
fi

# Verification 2.3: Legacy 6.0 still does not exist
if [ ! -d "$HOME/.config/kicad/6.0" ]; then
    echo "  [PASS] Legacy directory ~/.config/kicad/6.0/ still does NOT exist."
else
    echo "  [FAIL] Legacy directory ~/.config/kicad/6.0/ was created on rerun!" >&2
    exit 1
fi

export HOME="$ORIGINAL_HOME"
echo ""
echo "============================================================"
echo "ALL TESTS PASSED: Extracted production function verified."
echo "============================================================"
exit 0
