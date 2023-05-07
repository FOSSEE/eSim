#!/bin/sh

echo "run 'flatpak-builder --force-clean build-dir org.flatpak.FOSSEE_Inst_test.yml' to build"
echo "run 'flatpak-builder --user --install --force-clean build-dir org.flatpak.FOSSEE_Inst_test.yml' to install"

echo "use 'flatpak run org.flatpak.FOSSEE_Inst_test to run app' to run app"
echo "use 'python3 flatpak-pip-generator --requirements-file='/home/suchinton/Repos/Test/req' --output pypi-dependencies --yaml
' to resolove pip dependencies"
