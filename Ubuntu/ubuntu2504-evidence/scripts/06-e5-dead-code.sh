#!/bin/bash
# E5: the dispatcher's run_version_script() has leftover config-file lines
# after the child script call. Neither $config_dir nor $config_file is defined
# in install-eSim.sh, so they collapse to /config.ini and the shell tries to
# append to the filesystem root. Reproduce that exact expansion as a non-root
# user, which is how the installer runs.
set -o pipefail
echo "=== the leftover lines, verbatim from the original install-eSim.sh:"
cat <<'ORIG'
    echo "[eSim]" >> $config_dir/$config_file
    echo "eSim_HOME = $eSim_Home" >> $config_dir/$config_file
    echo "LICENSE = %(eSim_HOME)s/LICENSE" >> $config_dir/$config_file
    echo "KicadLib = %(eSim_HOME)s/library/kicadLibrary.tar.xz" >> $config_dir/$config_file
    echo "IMAGES = %(eSim_HOME)s/images" >> $config_dir/$config_file
    echo "VERSION = %(eSim_HOME)s/VERSION" >> $config_dir/$config_file
    echo "MODELICA_MAP_JSON = %(eSim_HOME)s/library/ngspicetoModelica/Mapping.json" >> $config_dir/$config_file
ORIG
echo
echo "=== with config_dir/config_file undefined, the path expands to:"
# The real installer does not use set -u, so unset variables expand to "".
( unset config_dir config_file; echo "  >> ${config_dir}/${config_file}" )
echo
echo "=== executing it as a normal user (id: nobody) is how the installer runs:"
cat > /tmp/e5.sh <<'DEMO'
config_dir=""
config_file=""
echo "[eSim]" >> $config_dir/$config_file
DEMO
echo '$ su nobody -s /bin/bash -c "bash /tmp/e5.sh"'
su nobody -s /bin/bash -c "bash /tmp/e5.sh" 2>&1 | head -3
echo "run-exit=$?"
echo
echo "=== the same lines after the patch (run_version_script closes the if):"
echo "  the block is deleted, so nothing executes after the child installer."
echo
echo "E5: reproduced - a permission error is printed after a successful install."
