#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "========================================================="
echo "       Starting eSim Standalone macOS Packaging          "
echo "========================================================="

# 1. Dependency Checks: PyInstaller
if ! python3 -c "import PyInstaller" &> /dev/null; then
    echo "Installing PyInstaller..."
    pip3 install pyinstaller
else
    echo "PyInstaller is already installed."
fi

# 2. Dependency Checks: create-dmg (Homebrew)
if ! which create-dmg &> /dev/null; then
    echo "Installing create-dmg via Homebrew..."
    if which brew &> /dev/null; then
        brew install create-dmg
    else
        echo "Error: Homebrew is not installed. Please install Homebrew or install 'create-dmg' manually."
        exit 1
    fi
else
    echo "create-dmg is already installed."
fi

# 3. Create macOS .icns file dynamically from logo.png
echo "Generating macOS .icns application icon..."
if [ -f "images/logo.png" ]; then
    mkdir -p logo.iconset
    sips -z 16 16     images/logo.png --out logo.iconset/icon_16x16.png
    sips -z 32 32     images/logo.png --out logo.iconset/icon_16x16@2x.png
    sips -z 32 32     images/logo.png --out logo.iconset/icon_32x32.png
    sips -z 64 64     images/logo.png --out logo.iconset/icon_32x32@2x.png
    sips -z 128 128   images/logo.png --out logo.iconset/icon_128x128.png
    sips -z 256 256   images/logo.png --out logo.iconset/icon_128x128@2x.png
    sips -z 256 256   images/logo.png --out logo.iconset/icon_256x256.png
    sips -z 512 512   images/logo.png --out logo.iconset/icon_256x256@2x.png
    sips -z 512 512   images/logo.png --out logo.iconset/icon_512x512.png
    sips -z 1024 1024 images/logo.png --out logo.iconset/icon_512x512@2x.png
    iconutil -c icns logo.iconset
    mv logo.icns images/logo.icns
    rm -rf logo.iconset
    echo "Application icon successfully created at images/logo.icns."
else
    echo "Warning: images/logo.png not found. Bundling without custom icon."
fi

# 4. Compile Standalone macOS Application Bundle (.app)
echo "Compiling Standalone eSim.app..."
rm -rf dist/eSim dist/eSim.app build/esim_mac
pyinstaller --clean -y esim_mac.spec

# 5. Build Drag-and-Drop .dmg Installer Disk Image
echo "Packaging Standalone eSim.dmg installer..."
if [ -f "dist/eSim.dmg" ]; then
    rm "dist/eSim.dmg"
fi

create-dmg \
  --volname "eSim Installer" \
  --volicon "images/logo.icns" \
  --window-pos 200 120 \
  --window-size 600 400 \
  --icon-size 100 \
  --icon "eSim.app" 175 190 \
  --hide-extension "eSim.app" \
  --app-drop-link 425 190 \
  "dist/eSim.dmg" \
  "dist/"

echo "========================================================="
echo "   🎉 Success! eSim Standalone DMG built at: dist/eSim.dmg"
echo "========================================================="
