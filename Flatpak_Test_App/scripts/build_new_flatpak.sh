#!/bin/sh

echo "Reference Commands:"
echo "========================================================================="
echo "To build, run command:"
echo "  $ flatpak-builder --force-clean build-dir org.flatpak.FOSSEE_Inst_test.yml"
echo "========================================================================="
echo "To install the app, run command:"
echo "  $ flatpak-builder --user --install --force-clean build-dir org.flatpak.FOSSEE_Inst_test.ym"
echo "========================================================================="
echo "To run application, run command:"
echo '  $ flatpak run org.flatpak.FOSSEE_Inst_test to run app'
echo "========================================================================="
echo "To resolove new pip dependencies, run command:"
echo '  $ python3 flatpak-pip-generator --requirements-file='$HOME/Repos/Test/req' --output pypi-dependencies --yaml'
echo "========================================================================="
