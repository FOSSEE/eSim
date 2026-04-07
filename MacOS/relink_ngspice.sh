#!/bin/bash
# relink_ngspice.sh

BIN_DIR="dist/eSim.app/Contents/Resources/bin"
# Note: if PyInstaller puts it in MacOS/ instead, adjust:
# BIN_DIR="dist/eSim.app/Contents/MacOS/bin"

X11_LIBS=(
    libXaw.7.dylib
    libXmu.6.dylib
    libXt.6.dylib
    libXext.6.dylib
    libX11.6.dylib
    libXft.2.dylib
    libfontconfig.1.dylib
    libXrender.1.dylib
    libfreetype.6.dylib
    libSM.6.dylib
    libICE.6.dylib
    libXau.6.dylib
    libxcb.1.dylib
    libXpm.4.dylib
)

# ── 1. Fix ngspice → point each X11 dep to @loader_path ──────────────
echo "Relinking ngspice..."
for lib in "${X11_LIBS[@]}"; do
    install_name_tool \
        -change "/opt/X11/lib/${lib}" \
                "@loader_path/${lib}" \
        "${BIN_DIR}/ngspice"
done

# ── 2. Fix each dylib's own id + its internal cross-references ────────
echo "Fixing dylib ids and internal links..."
for lib in "${X11_LIBS[@]}"; do
    LIB_PATH="${BIN_DIR}/${lib}"

    # Set the dylib's own install name
    install_name_tool -id "@loader_path/${lib}" "${LIB_PATH}"

    # Relink each dylib's references to other X11 dylibs
    for dep in "${X11_LIBS[@]}"; do
        install_name_tool \
            -change "/opt/X11/lib/${dep}" \
                    "@loader_path/${dep}" \
            "${LIB_PATH}" 2>/dev/null
    done
done

# ── 3. Fix permissions ────────────────────────────────────────────────
chmod +x "${BIN_DIR}/ngspice"
chmod 755 "${BIN_DIR}"/*.dylib

# ── 4. Ad-hoc sign (required on Apple Silicon) ───────────────────────
echo "Signing..."
for lib in "${X11_LIBS[@]}"; do
    codesign --force --sign - "${BIN_DIR}/${lib}"
done
codesign --force --sign - "${BIN_DIR}/ngspice"

echo "Done. Verifying..."
otool -L "${BIN_DIR}/ngspice"