"""Static guards for the Windows packaging inputs.

Nothing here builds or installs anything: these read installer.iss,
deps-manifest.json, requirements-windows.txt, build-windows.ps1 and
Ubuntu/install-eSim.sh as text and assert the properties a Windows rebuild
would otherwise have to catch by hand, on a VM, once per release.

Two of them are the point of the file:

  * the users-modify ACE stays scoped -- a future edit that puts it back
    on {app} re-opens write access to python\\, eSim.exe, tools\\kicad\\bin and
    tools\\msys64\\ for every local user of a shared machine;
  * the Windows and Ubuntu pin lists stay identical -- they are two
    files, they install the same four tools, and nothing but a test keeps a
    bump to one from silently skipping the other.

Pure stdlib + pytest, no Windows APIs, so this runs on Linux CI too.
"""

import json
import os
import re

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
WINDIR = os.path.dirname(HERE)
REPO = os.path.dirname(WINDIR)

ISS = os.path.join(WINDIR, 'installer.iss')
MANIFEST = os.path.join(WINDIR, 'deps-manifest.json')
REQS = os.path.join(WINDIR, 'requirements-windows.txt')
BUILD_PS1 = os.path.join(WINDIR, 'build-windows.ps1')
INSTALL_SH = os.path.join(REPO, 'Ubuntu', 'install-eSim.sh')
SKY130_PREPARE = os.path.join(
    REPO, 'src', 'configuration', 'Sky130Prepare.py')

# The dirs the running app writes inside the install tree. Keep in step with
# installer.iss's [Dirs] comment, which records what each one is written by.
WRITTEN_DIRS = ('{app}\\tools\\nghdl', '{app}\\library\\modelParamXML')

# Read-only at runtime; a users-modify ACE on any of these (or on a parent
# that would inherit down to them) would reopen a tamper vector.
MUST_NOT_BE_WRITABLE = (
    '{app}',
    '{app}\\python',
    '{app}\\tools\\kicad',
    '{app}\\tools\\msys64',
    '{app}\\src',
    '{app}\\library\\kicadLibrary',
)


def _read(path):
    with open(path, encoding='utf-8') as fh:
        return fh.read()


def _iss_section(text, name):
    """Lines of one .iss section, comments and blanks dropped."""
    out = []
    in_section = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith('[') and stripped.endswith(']'):
            in_section = stripped.lower() == '[%s]' % name.lower()
            continue
        if in_section and stripped and not stripped.startswith(';'):
            out.append(stripped)
    return out


def _dirs_with_permissions():
    """{dir name: permissions value} for every [Dirs] entry that sets one."""
    granted = {}
    for line in _iss_section(_read(ISS), 'Dirs'):
        m = re.search(r'Name:\s*"([^"]+)"', line)
        p = re.search(r'Permissions:\s*([^;]+)', line)
        if m and p:
            granted[m.group(1)] = p.group(1).strip()
    return granted


# --------------------------------------------------------------------------
# The users-modify grant is scoped to what the app writes
# --------------------------------------------------------------------------

def test_permissions_granted_only_on_runtime_written_dirs():
    granted = _dirs_with_permissions()
    assert set(granted) == set(WRITTEN_DIRS), (
        'installer.iss [Dirs] grants permissions on %s; expected exactly %s. '
        'Widening this needs a matching entry in the [Dirs] comment saying '
        'WHAT writes there at runtime.' % (sorted(granted), sorted(WRITTEN_DIRS)))
    for value in granted.values():
        assert value == 'users-modify', value


@pytest.mark.parametrize('path', MUST_NOT_BE_WRITABLE)
def test_no_users_modify_on_read_only_trees(path):
    """Neither the tree root nor any dir holding executables gets an ACE.

    {app} is the one that matters most: the ACE Inno writes is inheritable, so
    granting it there reaches python\\, eSim.exe and every bundled toolchain.
    """
    assert path not in _dirs_with_permissions()


def test_written_dirs_are_populated_by_files_not_just_created():
    """Both granted dirs must receive real content from [Files].

    The ACE is only useful if the paths the app writes INHERIT it, which they
    do because Inno runs [Dirs] before [Files]. If an exclude ever swept one of
    these out of the install, the [Dirs] entry would silently create a bare
    directory and the app would be writing somewhere else entirely."""
    text = _read(ISS)
    files = _iss_section(text, 'Files')
    assert any('DestDir: "{app}\\tools\\nghdl' in line for line in files), \
        'nothing installs into {app}\\tools\\nghdl'
    # modelParamXML rides the main StageDir\* -> {app} entry, so it just has to
    # survive that entry's (long) exclude list.
    for line in files:
        m = re.search(r'Excludes:\s*"([^"]*)"', line)
        if m:
            assert 'modelParamXML' not in m.group(1)


# --------------------------------------------------------------------------
# Every downloaded artifact is hash-pinned
# --------------------------------------------------------------------------

def _manifest():
    data = json.loads(_read(MANIFEST))
    return {k: v for k, v in data.items() if not k.startswith('_')}


def test_every_manifest_entry_has_a_real_sha256():
    empty = [name for name, dep in _manifest().items() if not dep.get('sha256')]
    assert not empty, (
        'deps-manifest.json entries with a blank sha256: %s. A blank hash '
        'means the build either dies or trusts a first download.' % empty)


@pytest.mark.parametrize('name', sorted(_manifest()))
def test_manifest_hashes_are_well_formed(name):
    dep = _manifest()[name]
    assert re.fullmatch(r'[0-9a-f]{64}', dep['sha256']), dep['sha256']
    assert dep['url'].startswith('https://'), dep['url']
    assert dep['filename']


def test_iverilog_hash_records_its_provenance():
    """bleyer.org publishes no checksum, so this one hash cannot be
    cross-checked upstream. The note must say so -- otherwise the next
    maintainer assumes it was verified like the rest and re-accepts a changed
    artifact without a second look."""
    notes = _manifest()['iverilog']['notes']
    assert 'PROVENANCE' in notes.upper()
    assert 'trust-on-first-use' in notes


# --------------------------------------------------------------------------
# Pip specs are pinned, bounded, and identical on both OSes
# --------------------------------------------------------------------------

def _windows_pins():
    """The pinned tool block of requirements-windows.txt.

    Everything above it is the loose (>=) library set that tracks the system
    Qt/matplotlib story and is deliberately NOT bounded, so select on the two
    shapes the tool block uses: a URL, or a spec carrying an upper bound.
    """
    pins = []
    for raw in _read(REQS).splitlines():
        line = raw.strip()
        if not line or line.startswith('#'):
            continue
        if line.startswith('http') or '<' in line:
            pins.append(line)
    return pins


def _ubuntu_pins():
    """The PIP_PINS array from install-eSim.sh, comments stripped."""
    text = _read(INSTALL_SH)
    m = re.search(r'^PIP_PINS=\(\s*$(.*?)^\)\s*$', text, re.M | re.S)
    assert m, 'PIP_PINS array not found in Ubuntu/install-eSim.sh'
    ref = re.search(r'^PYHDLPARSER_REF="([0-9a-f]{40})"', text, re.M)
    assert ref, 'PYHDLPARSER_REF not found (or not a 40-hex commit)'
    pins = []
    for raw in m.group(1).splitlines():
        line = raw.strip()
        if not line or line.startswith('#'):
            continue
        line = re.sub(r'\s*#.*$', '', line)             # trailing comment
        value = line.strip().strip('"')
        pins.append(value.replace('$PYHDLPARSER_REF', ref.group(1)))
    return pins


def test_windows_and_ubuntu_install_the_same_pins():
    """The two lists are the same three tools plus watchdog. They drift the
    moment one is bumped alone, and the symptom is a bug that reproduces on
    exactly one OS."""
    win = set(_windows_pins())
    ubuntu = set(_ubuntu_pins())
    # watchdog is in the loose library block on Windows (it is imported, not
    # shelled out to) but must be installed by both.
    ubuntu.discard('watchdog>=3.0')
    assert 'watchdog>=3.0' in _read(REQS)
    assert win == ubuntu, (
        'Windows-only: %s | Ubuntu-only: %s'
        % (sorted(win - ubuntu), sorted(ubuntu - win)))


@pytest.mark.parametrize('pins_of', [_windows_pins, _ubuntu_pins],
                         ids=['windows', 'ubuntu'])
def test_pyhdlparser_is_pinned_to_a_commit_not_a_branch(pins_of):
    urls = [p for p in pins_of() if 'pyhdlparser' in p.lower()]
    assert len(urls) == 1, urls
    ref = urls[0].rsplit('/', 1)[-1]
    assert re.fullmatch(r'[0-9a-f]{40}', ref), (
        'pyhdlparser must be pinned to a commit; got %r. `master` is both a '
        'moving ref and a stale branch name (upstream renamed it to main).'
        % ref)


@pytest.mark.parametrize('pins_of', [_windows_pins, _ubuntu_pins],
                         ids=['windows', 'ubuntu'])
def test_named_tools_carry_both_a_floor_and_a_ceiling(pins_of):
    named = [p for p in pins_of() if not p.startswith('http')
             and not p.startswith('watchdog')]
    assert {p.split('>')[0] for p in named} == {
        'sandpiper-saas', 'volare'}
    for spec in named:
        assert '>=' in spec, spec
        assert re.search(r'<\s*\d', spec), (
            '%s has no upper bound: a new major of a tool the maker flows '
            'shell out to would land on an installer nobody rebuilt.' % spec)


def test_no_moving_refs_left_in_either_installer():
    """Comments may still discuss the old ref (they explain the pin); no
    executable line may install from one."""
    for path, comment in ((REQS, '#'), (INSTALL_SH, '#')):
        for lineno, raw in enumerate(_read(path).splitlines(), 1):
            line = raw.strip()
            if not line or line.startswith(comment):
                continue
            for moving in ('tarball/master', 'tarball/main'):
                assert moving not in line, '%s:%d %s' % (path, lineno, line)


def test_ubuntu_pip_loop_warns_on_every_failure():
    """Each pin is optional at runtime, so a failure must warn rather than
    abort -- and must not be silent, which is what the unguarded
    `pip install watchdog` used to be under `set +e`."""
    text = _read(INSTALL_SH)
    m = re.search(r'for spec in "\$\{PIP_PINS\[@\]\}"; do\s*\n(.*?)\n\s*done',
                  text, re.S)
    assert m, 'installPythonDeps no longer loops over PIP_PINS'
    body = m.group(1)
    assert 'pip install "$spec"' in body
    assert '|| warn' in body
    # No third-party package may be installed outside the loop. `pip install
    # --upgrade pip` is the one legitimate exception (it bootstraps the venv's
    # own pip and is not a pin).
    stray = [line.strip() for line in text.splitlines()
             if re.match(r'^\s*pip install ', line)
             and 'pip install "$spec"' not in line
             and not re.match(r'^\s*pip install --upgrade pip\s*$', line)]
    assert not stray, (
        'package installed outside the PIP_PINS loop (so unpinned and, under '
        '`set +e`, silent on failure): %s' % stray)


# --------------------------------------------------------------------------
# The rolling MSYS2 package set is recorded
# --------------------------------------------------------------------------

def test_build_records_msys2_package_lock():
    text = _read(BUILD_PS1)
    assert "pacman -Q" in text
    assert 'PACKAGES.lock' in text
    # Written after provisioning, i.e. inside Stage-Msys and after the
    # toolchain install -- not somewhere it could run against a bare tarball.
    stage = text.split('function Stage-Msys', 1)[1].split('\nfunction ', 1)[0]
    assert 'PACKAGES.lock' in stage
    assert stage.index('pacman -S --noconfirm') < stage.index('PACKAGES.lock')


def test_packages_lock_is_shipped_not_excluded():
    """PACKAGES.lock only earns its keep if it reaches the user's machine:
    identifying which gcc/verilator/ghdl a report came from is the whole
    point. It rides the tools\\msys64 entry, so no exclude may sweep it."""
    for line in _iss_section(_read(ISS), 'Files'):
        if 'tools\\msys64' not in line:
            continue
        m = re.search(r'Excludes:\s*"([^"]*)"', line)
        if not m:
            continue
        for pattern in m.group(1).split(','):
            assert 'PACKAGES.lock' not in pattern
            assert pattern.strip() != '*'


def test_linked_worktree_git_pointer_is_excluded_and_rejected():
    """A linked worktree uses a root .git file, so /XD alone is insufficient."""
    text = _read(BUILD_PS1)
    stage = text.split('function Stage-App', 1)[1].split(
        '\nfunction ', 1)[0]
    clean = text.split('function Assert-CleanStage', 1)[1].split(
        '\nfunction ', 1)[0]
    assert "/XF '.git'" in stage
    assert "Join-Path $Stage '.git'" in clean
    assert 'VCS metadata: .git' in clean


# --------------------------------------------------------------------------
# SKY130 -- expanded, repaired, and electrically smoke-tested before shipping
# --------------------------------------------------------------------------

def test_windows_stage_expands_sky130_and_drops_both_archive_layers():
    text = _read(BUILD_PS1)
    stage = text.split('function Stage-Sky130', 1)[1].split(
        '\nfunction ', 1)[0]
    assert 'sky130_fd_pr.tar.xz' in stage
    assert 'sky130_fd_pr.tar' in stage
    assert 'Sky130Prepare.py' in stage
    assert 'Remove-Item $tar, $archive' in stage
    assert "Test-Path $archive" in stage
    assert "Test-Path $pdk" in stage

    main = text.rsplit('# ----------------------------------------------------------------- main ----',
                       1)[1]
    assert main.index('Stage-Python') < main.index('Stage-Sky130')
    assert main.index('Stage-Sky130') < main.index('Stage-SimToolchain')


def test_windows_build_runs_real_sky130_inverter_smoke():
    text = _read(BUILD_PS1)
    smoke = text.split('function Test-Sky130Simulation', 1)[1].split(
        '\nfunction ', 1)[0]
    assert 'sky130.lib.spice' in smoke
    assert 'sky130_fd_pr__nfet_01v8' in smoke
    assert 'sky130_fd_pr__pfet_01v8' in smoke
    assert '.measure tran vout_low' in smoke
    assert '.measure tran vout_high' in smoke
    assert 'ngbehavior=hsa' in smoke

    main = text.rsplit('# ----------------------------------------------------------------- main ----',
                       1)[1]
    assert main.index('Stage-Ngspice') < main.index('Test-Sky130Simulation')


def test_both_installers_use_the_same_sky130_repair_helper():
    assert os.path.isfile(SKY130_PREPARE)
    helper = _read(SKY130_PREPARE)
    assert 'BROKEN_INCLUDE' in helper
    assert 'FIXED_INCLUDE' in helper
    assert 'unknown PDK revision' in helper
    assert 'Sky130Prepare.py' in _read(BUILD_PS1)
    assert 'Sky130Prepare.py' in _read(INSTALL_SH)


# ── Windows build: files and tools a real build needs ───────────────────────

def _ps1_function(name):
    return _read(BUILD_PS1).split('function %s' % name, 1)[1].split('\nfunction ', 1)[0]


def _manifest_json():
    with open(MANIFEST, encoding='utf-8') as fh:
        return json.load(fh)


def test_every_windows_script_the_installer_runs_is_staged():
    # Stage-App drops the repo windows/ dir and copies runtime files back one
    # by one. installer.iss only runs a script if it exists, so a missing one
    # fails silently (the uninstall cleanup was skipped on every uninstall).
    scripts = sorted(set(re.findall(r"windows\\([A-Za-z0-9_]+\.py)", _read(ISS))))
    assert 'uninstall_cleanup.py' in scripts
    copies = [l for l in _ps1_function('Stage-App').splitlines()
              if l.strip().startswith('Copy-Item') and '$stageWin' in l]
    missing = [s for s in scripts if not any("'%s'" % s in l for l in copies)]
    assert missing == []


def test_skipsimbuild_ngspice_shim_is_the_console_build():
    # The official zip's ngspice.exe is the GUI build and prints nothing on
    # stdout, so the SKY130 smoke test (and eSim's batch runs) read no output.
    shim = _ps1_function('Stage-Ngspice').split('if ($SkipSimBuild)', 1)[1]
    assert re.search(r"ngspice_con\.exe.*ngspice\.exe", shim)


def test_bleyer_iverilog_setup_is_run_not_7z_extracted():
    # Bleyer's setup is an Inno Setup 6.1 installer, which 7-Zip cannot open
    # ("Cannot open the file as archive").
    body = _ps1_function('Stage-Iverilog')
    assert '$7z' not in body
    assert '/VERYSILENT' in body and '/DIR=' in body
    assert 'unins000.exe' in body, 'the temporary install must be removed again'


def test_kicad_installer_comes_from_kicads_github_release():
    # downloads.kicad.org ended the 1.1 GB download early on every attempt;
    # KiCad publishes the identical file (same sha256) on its GitHub release.
    url = _manifest_json()['kicad_installer']['url']
    assert url.startswith('https://github.com/KiCad/kicad-source-mirror/releases/download/')


def test_launcher_gets_a_pinned_gcc_when_msys2_is_skipped():
    gcc = _manifest_json()['mingw_gcc']
    assert gcc['url'].startswith('https://github.com/brechtsanders/winlibs_mingw/releases/download/')
    assert re.fullmatch(r'[0-9a-f]{64}', gcc['sha256'])
    assert "Get-Dep 'mingw_gcc'" in _ps1_function('Stage-Launcher')
