<#
=============================================================================
          FILE: build-windows.ps1

         USAGE: pwsh -ExecutionPolicy Bypass -File windows\build-windows.ps1
                    [-SkipMsys] [-AcceptNewHashes] [-Clean]

                Needs PowerShell 7+ (pwsh), NOT Windows PowerShell 5.1.

   DESCRIPTION: Reproducible Windows packaging for eSim. Runs on a Windows
                build machine (or windows-latest CI runner). Produces:
                    windows\dist\eSim-<VERSION>-installer.exe   (Inno Setup,
                        single exe: eSim + toolchain + bundled pruned KiCad)
                    windows\dist\*.sha256

                Every third-party download is pinned in deps-manifest.json
                (URL + sha256). Nothing is fetched from a moving 'latest'.

                Pipeline:
                  1. verify build tools (7z; Inno Setup auto-installed)
                  2. download + hash-check every dep into windows\downloads\
                  3. stage windows\build\eSim\        (app tree, filtered like
                     make-release.sh, INCLUDING nghdl\src for VHDL co-sim)
                  4. stage private Python + pip install requirements-windows
                  5. stage tools\msys64 (MSYS2 + mingw64 gcc/make/verilator/
                     ghdl-llvm; the HDL-toolchain installer component AND the
                     build substrate for step 6)
                  6. Stage-SimToolchain: build the CUSTOM eSim ngspice
                     (nghdl-simulator: d_cosim + ivlng + ghdl.cm) from
                     nghdl\nghdl-simulator-source.tar.xz inside MSYS2 into
                     tools\nghdl\{src,release,install_dir}, and Icarus
                     Verilog from the pinned source WITH libvvp into
                     library\bin\iverilog -- both hard-verified (binaries
                     run, code models present, a trivial .cir simulates)
                  7. stage tools\ngspice (official build; the Compact
                     flavour's plain-simulation fallback)
                  8. Stage-Kicad: extract the pinned official KiCad installer
                     payload, PRUNED for eSim (no 3D models, demos or
                     translations -- see $KicadPrune), into tools\kicad --
                     the one KiCad eSim launches; nothing else to download
                  9. compile installer.iss with ISCC

        -SkipMsys        build without the HDL toolchain component (smaller
                         installer; NgVeri/NGHDL builds unavailable).
                         Implies -SkipSimBuild.
        -SkipSimBuild    skip the MSYS2 source builds (step 6): ngspice falls
                         back to the official zip shim and iverilog to the
                         Bleyer setup (NO libvvp -> d_cosim and VHDL co-sim
                         will not work). For quick packaging iterations only.
        -AcceptNewHashes record sha256 for manifest entries whose hash is
                         blank, rewriting deps-manifest.json. Verify recorded
                         hashes against upstream before committing!
        -Clean           delete build\ and dist\ first (downloads\ is kept;
                         it is content-addressed by the manifest hashes)

  ORGANIZATION: eSim Team, FOSSEE, IIT Bombay
=============================================================================
#>
[CmdletBinding()]
param(
    [switch]$SkipMsys,
    [switch]$SkipSimBuild,
    [switch]$AcceptNewHashes,
    [switch]$Clean
)
if ($SkipMsys) { $SkipSimBuild = $true }   # no MSYS2 -> nothing to build with

# PowerShell 7+, not the Windows PowerShell 5.1 that ships with Windows: this
# script uses PS7-only syntax (Get-Date -AsUTC, ${env:ProgramFiles(x86)}), and
# under 5.1 it dies with a parse error that reads like a bug in the script.
if ($PSVersionTable.PSVersion.Major -lt 7) {
    Write-Error ("This build needs PowerShell 7+ (running $($PSVersionTable.PSVersion)). " +
                 "Install it (winget install Microsoft.PowerShell), then re-run with pwsh:`n" +
                 "    pwsh -ExecutionPolicy Bypass -File windows\build-windows.ps1")
    exit 1
}

$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'   # 10x faster Invoke-WebRequest

$WinDir   = $PSScriptRoot
$RepoRoot = Split-Path $WinDir -Parent
$Downloads = Join-Path $WinDir 'downloads'
$Build     = Join-Path $WinDir 'build'
$Stage     = Join-Path $Build 'eSim'
$Dist      = Join-Path $WinDir 'dist'
$Version   = (Get-Content (Join-Path $RepoRoot 'VERSION') -Raw).Trim()

function Log([string]$msg) { Write-Host ">>> $msg" -ForegroundColor Cyan }
function Die([string]$msg) { Write-Error $msg; exit 1 }

# ---------------------------------------------------------------- tools ----
function Resolve-7z {
    foreach ($c in @('7z', "$env:ProgramFiles\7-Zip\7z.exe")) {
        if (Get-Command $c -ErrorAction SilentlyContinue) { return $c }
    }
    Die '7-Zip is required (winget install 7zip.7zip) - extracts .7z/.tar.xz/.nupkg'
}

function Resolve-Iscc {
    # NB: ${env:ProgramFiles(x86)} MUST be brace-wrapped -- "$env:ProgramFiles(x86)"
    # parses as $env:ProgramFiles + literal "(x86)" -> "C:\Program Files(x86)" (no
    # space), a path that never exists, so the check always failed.
    foreach ($c in @('iscc',
                     "${env:ProgramFiles(x86)}\Inno Setup 6\ISCC.exe",
                     "$env:LOCALAPPDATA\Programs\Inno Setup 6\ISCC.exe")) {
        if (Get-Command $c -ErrorAction SilentlyContinue) { return $c }
    }
    # Auto-install from the pinned manifest entry (build-machine tool only).
    Log 'Inno Setup not found - installing from pinned manifest entry'
    $setup = Get-Dep 'innosetup'
    & $setup /VERYSILENT /SUPPRESSMSGBOXES /NORESTART | Out-Null
    $c = "${env:ProgramFiles(x86)}\Inno Setup 6\ISCC.exe"
    if (-not (Test-Path $c)) { Die 'Inno Setup install failed' }
    return $c
}

# ------------------------------------------------------------- manifest ----
$ManifestPath = Join-Path $WinDir 'deps-manifest.json'
$Manifest = Get-Content $ManifestPath -Raw | ConvertFrom-Json

function Get-Dep([string]$name) {
    <# Download (once) + sha256-verify a manifest entry; returns local path. #>
    $e = $Manifest.$name
    if (-not $e) { Die "deps-manifest.json has no entry '$name'" }
    New-Item -ItemType Directory -Force -Path $Downloads | Out-Null
    $file = Join-Path $Downloads $e.filename
    if (-not (Test-Path $file)) {
        Log "Downloading $name $($e.version)"
        Invoke-WebRequest -Uri $e.url -OutFile $file -UserAgent 'eSim-build'
    }
    $hash = (Get-FileHash $file -Algorithm SHA256).Hash.ToLower()
    if ([string]::IsNullOrEmpty($e.sha256)) {
        if (-not $AcceptNewHashes) {
            Die "$name has no pinned sha256. Re-run with -AcceptNewHashes, then verify the recorded hash against upstream's published checksum before committing."
        }
        $e.sha256 = $hash
        $Manifest | ConvertTo-Json -Depth 5 | Set-Content $ManifestPath -Encoding UTF8
        Log "$name sha256 recorded: $hash  (VERIFY against upstream!)"
    }
    elseif ($hash -ne $e.sha256.ToLower()) {
        Die "$name hash mismatch!`n  expected $($e.sha256)`n  got      $hash`nDelete $file if upstream re-released, and re-verify."
    }
    return $file
}

# ---------------------------------------------------------------- stage ----
function Stage-App {
    Log 'Staging eSim tree (working-tree snapshot, filtered like make-release.sh)'
    New-Item -ItemType Directory -Force -Path $Stage | Out-Null
    # Same exclusion set as make-release.sh: VCS/build cruft + regeneratable
    # simulation outputs. robocopy /MIR keeps re-runs incremental. nghdl/ IS
    # staged (src/ = the VHDL co-sim python + ghdlserver sources that
    # ngspice_ghdl.py needs at runtime via [SRC] SRC_HOME, Example/ = test
    # designs); only its 11 MB simulator source tarball stays out -- the
    # BUILT tree ships at tools\nghdl instead (Stage-SimToolchain).
    # NOTE: library\SubcircuitLibrary IS staged (make-release.sh excludes it,
    # but the app needs it at runtime: the subcircuit browser opens there and
    # the netlister resolves X-instances against its .sub files -- without it
    # every schematic using a library IC fails to convert). Its bulk was sim
    # outputs; those are stripped by the /XF filters below instead.
    $xd = @('.git', 'dist', '__pycache__', '.pytest_cache', '.mypy_cache',
            'node_modules', 'Ubuntu',
            'windows', 'flatpak', 'snap', 'appimage', 'docker-launcher') |
          ForEach-Object { Join-Path $RepoRoot $_ }
    # Stage-side dirs the LATER stages create (private Python, built
    # toolchains): excluded so /MIR's purge pass cannot delete them on an
    # incremental re-run -- rebuilding the ngspice toolchain costs ~an hour.
    # NB 'library\bin' not 'library\bin\iverilog': the repo has no
    # library\bin, so /MIR sees the whole stage-side bin as one EXTRA dir and
    # deletes it recursively -- /XD on the CHILD never gets consulted, which
    # silently forced a ~15 min iverilog source rebuild on every re-run.
    $xd += @('python', 'tools', 'library\bin') |
           ForEach-Object { Join-Path $Stage $_ }
    # /XJ: do not follow junctions. A dev box often has repo-root python\ and
    # tools\ junctions pointing at an INSTALLED eSim (handy for running the
    # working tree against a real toolchain) -- without /XJ robocopy walks
    # straight through them and mirrors the installed tree's gigabytes back
    # into the stage, so the installer would repackage its own output.
    # A linked git worktree has a root .git FILE (pointing at the parent
    # repository), not the .git directory covered by /XD. Exclude the filename
    # too so an installer built from a worktree never leaks that absolute path.
    robocopy $RepoRoot $Stage /MIR /XJ /NFL /NDL /NJH /NJS /XD @xd `
        /XF '.git' '*.pyc' '*.pyo' '*.raw' 'plot_data_*.txt' '.DS_Store' `
            'fp-info-cache' `
            'nghdl-simulator-source.tar.xz' `
            'install-nghdl.sh' | Out-Null
    if ($LASTEXITCODE -ge 8) { Die "robocopy failed ($LASTEXITCODE)" }

    # Stage-side leftovers no pipeline stage owns (so /MIR never purges them:
    # they live under the /XD-protected tools\). nghdl.old is a hand-made
    # backup of an earlier simulator build that shipped in the last release.
    Remove-Item (Join-Path $Stage 'tools\nghdl.old') -Recurse -Force `
        -ErrorAction SilentlyContinue

    # kicadLibrary must be a real dir at runtime on Windows (symbols are
    # referenced in place); expand the tarball form if that's what the tree has.
    $lib = Join-Path $Stage 'library'
    if ((Test-Path "$lib\kicadLibrary.tar.xz") -and -not (Test-Path "$lib\kicadLibrary")) {
        & $7z x "$lib\kicadLibrary.tar.xz" "-o$lib" -y | Out-Null
        & $7z x "$lib\kicadLibrary.tar"    "-o$lib" -y | Out-Null
        Remove-Item "$lib\kicadLibrary.tar"
    }

    Set-Content (Join-Path $Stage 'RELEASE') @"
eSim release (Windows)
version    : $Version
built      : $(Get-Date -AsUTC -Format yyyy-MM-dd) (UTC)
installer  : Inno Setup (windows/installer.iss)
"@

    # The repo windows\ dir is excluded wholesale above (build cruft:
    # build-windows.ps1, installer.iss, downloads\, dist\). But two files in
    # it are RUNTIME launchers the shipped tree needs:
    #   * esim.bat            -> stage ROOT: its ESIM_HOME=%~dp0 must resolve to
    #                            the install root so %ESIM_HOME%\src, \python,
    #                            \tools, \windows\windows_bootstrap.py all hit.
    #   * windows_bootstrap.py -> stage windows\: esim.bat runs it every launch
    #                            for per-user setup (config.ini, sym-lib-table).
    # Stage them back explicitly so installer.iss (StageDir\* -> {app}) ships them.
    Copy-Item (Join-Path $WinDir 'esim.bat') (Join-Path $Stage 'esim.bat') -Force
    $stageWin = Join-Path $Stage 'windows'
    New-Item -ItemType Directory -Force -Path $stageWin | Out-Null
    Copy-Item (Join-Path $WinDir 'windows_bootstrap.py') (Join-Path $stageWin 'windows_bootstrap.py') -Force
    # installer.iss runs it on uninstall (only if present) to remove the
    # per-user config and KiCad library entries eSim added.
    Copy-Item (Join-Path $WinDir 'uninstall_cleanup.py') (Join-Path $stageWin 'uninstall_cleanup.py') -Force
}

function Stage-Python {
    Log 'Staging private Python + wheel set'
    $pkg = Get-Dep 'python'
    $pydir = Join-Path $Stage 'python'
    if (-not (Test-Path "$pydir\python.exe")) {
        $tmp = Join-Path $Build 'python-nupkg'
        & $7z x $pkg "-o$tmp" -y | Out-Null          # .nupkg is a zip
        New-Item -ItemType Directory -Force -Path $pydir | Out-Null
        Copy-Item "$tmp\tools\*" $pydir -Recurse -Force
        Remove-Item $tmp -Recurse -Force
    }
    & "$pydir\python.exe" -m pip install --upgrade pip --quiet
    & "$pydir\python.exe" -m pip install --quiet `
        -r (Join-Path $WinDir 'requirements-windows.txt')
    if ($LASTEXITCODE -ne 0) { Die 'pip install failed' }
    # Record the exact resolved set for the release notes / reproducibility.
    & "$pydir\python.exe" -m pip freeze |
        Set-Content (Join-Path $Stage 'python-wheels.lock')
    # Sanity: the GUI toolkit must import.
    & "$pydir\python.exe" -c 'import PyQt6.QtWidgets, PyQt6.Qsci'
    if ($LASTEXITCODE -ne 0) { Die 'PyQt6/Qsci import check failed' }
}

function Stage-Sky130 {
    <# The repository carries SKY130 as a compressed release payload.  The
       application, however, opens library\sky130_fd_pr\models directly, so
       Windows must ship the expanded tree -- never the tarball.  Repair the
       one malformed include in this pinned upstream snapshot through the
       same Python helper the Ubuntu installer uses, then delete both archive
       layers only after validation succeeds. #>
    Log 'Staging extracted and ngspice-ready SKY130 PDK'
    $lib = Join-Path $Stage 'library'
    $archive = Join-Path $lib 'sky130_fd_pr.tar.xz'
    $tar = Join-Path $lib 'sky130_fd_pr.tar'
    $pdk = Join-Path $lib 'sky130_fd_pr'

    if (Test-Path $archive) {
        # Stage-App mirrors the source tree on every build.  Re-expand the
        # archive rather than retaining an older incremental-stage directory.
        Remove-Item $pdk -Recurse -Force -ErrorAction SilentlyContinue
        & $7z x $archive "-o$lib" -y | Out-Null
        if ($LASTEXITCODE -ne 0 -or -not (Test-Path $tar)) {
            Die 'failed to decompress library\sky130_fd_pr.tar.xz'
        }
        & $7z x $tar "-o$lib" -y | Out-Null
        if ($LASTEXITCODE -ne 0) {
            Die 'failed to extract library\sky130_fd_pr.tar'
        }
    }
    if (-not (Test-Path $pdk)) {
        Die 'SKY130 PDK missing after staging (expected library\sky130_fd_pr)'
    }

    $prepare = Join-Path $Stage 'src\configuration\Sky130Prepare.py'
    & (Join-Path $Stage 'python\python.exe') $prepare $pdk
    if ($LASTEXITCODE -ne 0) { Die 'SKY130 PDK validation/repair failed' }

    Remove-Item $tar, $archive -Force -ErrorAction SilentlyContinue
    if ((Test-Path $tar) -or (Test-Path $archive)) {
        Die 'SKY130 archive remained in stage after successful extraction'
    }
}

function Stage-Ngspice {
    Log 'Staging ngspice (official Windows build; Compact-flavour fallback)'
    $arc = Get-Dep 'ngspice'
    $dst = Join-Path $Stage 'tools\ngspice'
    if (-not (Test-Path $dst)) {
        $tmp = Join-Path $Build 'ngspice-x'
        & $7z x $arc "-o$tmp" -y | Out-Null
        # Archive root is Spice64/: bin/ngspice.exe + lib/ngspice/*.cm
        $root = Get-ChildItem $tmp -Directory | Select-Object -First 1
        New-Item -ItemType Directory -Force -Path $dst | Out-Null
        Copy-Item "$($root.FullName)\*" $dst -Recurse -Force
        Remove-Item $tmp -Recurse -Force
    }
    if (-not (Test-Path "$dst\bin\ngspice.exe")) { Die 'ngspice.exe not staged' }
    if ($SkipSimBuild) {
        # No custom build: CosimConfig resolves
        # <NGHDL_HOME>\install_dir\bin\ngspice.exe and the bootstrap points
        # NGHDL_HOME at tools\nghdl, so shim the official build there. The
        # official build has NO ivlng/ghdl.cm -> d_cosim/VHDL co-sim stay off
        # (and the in-app doctor says so).
        $shim = Join-Path $Stage 'tools\nghdl\install_dir'
        if (-not (Test-Path $shim)) {
            New-Item -ItemType Directory -Force -Path (Split-Path $shim) | Out-Null
            Copy-Item $dst $shim -Recurse
        }
        # The zip's ngspice.exe is the GUI build and prints nothing on
        # stdout; eSim's batch runs and the SKY130 smoke test need the
        # console build, which the zip ships as ngspice_con.exe.
        Copy-Item "$shim\bin\ngspice_con.exe" "$shim\bin\ngspice.exe" -Force
    }
}

function Test-Sky130Simulation {
    <# Parse the complete tt corner and run a real CMOS inverter through the
       exact ngspice path eSim launches.  A file-existence check missed the
       upstream line that ngspice parsed as a current source; this catches the
       packaging boundary and model-deck boundary together. #>
    Log 'Verifying staged SKY130 PDK with a CMOS inverter simulation'
    $ngspice = Join-Path $Stage 'tools\nghdl\install_dir\bin\ngspice.exe'
    if (-not (Test-Path $ngspice)) { Die 'runtime ngspice missing for SKY130 smoke test' }
    $pdk = (Join-Path $Stage 'library\sky130_fd_pr') -replace '\\', '/'
    $smoke = Join-Path $Build 'sky130-smoke'
    New-Item -ItemType Directory -Force -Path $smoke | Out-Null
    Set-Content (Join-Path $smoke '.spiceinit') -Encoding ascii @'
set ngbehavior=hsa
set ng_nomodcheck
'@
    Set-Content (Join-Path $smoke 'inverter.cir') -Encoding ascii @"
* eSim staged SKY130 CMOS inverter smoke test
.include "$pdk/models/sky130_fd_pr__model__r+c.model.spice"
.include "$pdk/models/sky130_fd_pr__model__linear.model.spice"
.include "$pdk/models/sky130_fd_pr__model__diode_pw2nd_11v0.model.spice"
.include "$pdk/models/sky130_fd_pr__model__diode_pd2nw_11v0.model.spice"
.lib "$pdk/models/sky130.lib.spice" tt
.include "$pdk/models/sky130_fd_pr__model__inductors.model.spice"
.include "$pdk/models/sky130_fd_pr__model__pnp.model.spice"
VDD vdd 0 1.8
VIN in 0 PULSE(0 1.8 1n 50p 50p 2n 4n)
XMN out in 0 0 sky130_fd_pr__nfet_01v8 w=1 l=0.15
XMP out in vdd vdd sky130_fd_pr__pfet_01v8 w=2 l=0.15
CLOAD out 0 10f
.tran 10p 8n
.measure tran vout_low FIND v(out) AT=2n
.measure tran vout_high FIND v(out) AT=4n
.end
"@

    Push-Location $smoke
    try {
        $output = (& $ngspice -b 'inverter.cir' 2>&1 | Out-String)
        $rc = $LASTEXITCODE
    }
    finally { Pop-Location }
    if ($rc -ne 0) { Die "SKY130 inverter simulation failed (rc=$rc):`n$output" }

    $low = [regex]::Match($output, 'vout_low\s*=\s*([-+0-9.eE]+)')
    $high = [regex]::Match($output, 'vout_high\s*=\s*([-+0-9.eE]+)')
    if (-not $low.Success -or -not $high.Success) {
        Die "SKY130 inverter measurements missing:`n$output"
    }
    $lowValue = [double]::Parse($low.Groups[1].Value,
        [Globalization.CultureInfo]::InvariantCulture)
    $highValue = [double]::Parse($high.Groups[1].Value,
        [Globalization.CultureInfo]::InvariantCulture)
    if ([math]::Abs($lowValue) -ge 0.1 -or $highValue -le 1.7) {
        Die "SKY130 inverter response invalid (low=$lowValue, high=$highValue)"
    }
    Log "SKY130 inverter OK (low=$lowValue V, high=$highValue V)"
}

function Stage-Iverilog {
    <# -SkipSimBuild fallback only: Bleyer's prebuilt Icarus. It has NO
       libvvp, so the Verilog Verifier works but d_cosim cannot run. The
       real path is the libvvp source build in Stage-SimToolchain. #>
    if (-not $SkipSimBuild) { return }
    Log 'Staging Icarus Verilog (Bleyer fallback; NO libvvp -> no d_cosim)'
    $setup = Get-Dep 'iverilog'
    $dst = Join-Path $Stage 'library\bin\iverilog'
    if (-not (Test-Path $dst)) {
        $tmp = Join-Path $Build 'iverilog-x'
        # Bleyer's setup is Inno Setup 6.1, which 7-Zip cannot open. Install
        # it silently into a build dir (no tasks: no PATH change), copy the
        # tree, then run its uninstaller so the build machine keeps no trace.
        $p = Start-Process $setup -PassThru -ArgumentList '/VERYSILENT', '/SUPPRESSMSGBOXES',
            '/NORESTART', '/NOICONS', '/TASKS=""', "/DIR=`"$tmp`""
        $p.WaitForExit()
        if (-not (Test-Path "$tmp\bin\iverilog.exe")) { Die "Icarus Verilog setup failed (exit $($p.ExitCode))" }
        New-Item -ItemType Directory -Force -Path $dst | Out-Null
        Copy-Item "$tmp\*" $dst -Recurse -Force -Exclude 'unins000.*'
        $u = Start-Process "$tmp\unins000.exe" -PassThru -ArgumentList '/VERYSILENT', '/SUPPRESSMSGBOXES', '/NORESTART'
        $u.WaitForExit()
        Remove-Item $tmp -Recurse -Force -ErrorAction SilentlyContinue
    }
    if (-not (Test-Path "$dst\bin\iverilog.exe")) { Die 'iverilog.exe not staged' }
}

# MSYS2 package sets. mingw64: the toolchain the APP invokes at model-build
# time (ModelGeneration/nghdl: mingw32-make, gcc, verilator, ghdl) -- these
# SHIP in the 'hdl' installer component. msys: build-only utilities that
# Stage-SimToolchain needs to compile ngspice/iverilog from source; they ride
# along in the shipped tree (a few MB) and keep user-side model rebuilds
# self-sufficient.
$MingwPkgs = 'mingw-w64-x86_64-gcc mingw-w64-x86_64-make ' +
             'mingw-w64-x86_64-verilator mingw-w64-x86_64-ghdl-llvm ' +
             # dlfcn-win32 provides libdl (-ldl): the ngspice XSPICE code-model
             # link (src/xspice/icm/makedefs) hard-codes -ldl, a Linux-ism.
             # mingw has no libdl in its base -> spice2poly.cm et al. fail with
             # "cannot find -ldl". dlfcn-win32 is a Win32-API-backed libdl.
             'mingw-w64-x86_64-dlfcn ' +
             # readline: ngspice's configure REQUIRES it (`Checking for
             # readline: ... configure: error: Couldn't find GNU readline
             # headers`) -- it is not optional in the 45.2 tree, and nothing
             # else in this package set pulls it in, so a cold provision died
             # at configure. Brings mingw-w64-x86_64-termcap with it; both DLLs
             # are already expected by the runtime closure staged below.
             'mingw-w64-x86_64-readline'
$MsysPkgs  = 'make autoconf automake libtool bison flex gperf patch tar'

function Set-MsysEnv {
    <# Make every staged-MSYS2 bash call HERMETIC. The staged bash runs as a
       login shell (-l): it sources /etc/profile (good -- that puts /mingw64/bin
       and /usr/bin on PATH) but THEN ~/.bash_profile + ~/.bashrc. The stock
       nsswitch `db_home: cygwin desc` resolves HOME to the real Windows user
       profile, so a personal ~/.bashrc (e.g. one doing `export PATH=...:$PATH`
       that drops /usr/bin) silently wrecks the build -- cygpath/head/gcc vanish
       and commands fail with "cd: null directory". Point HOME at a clean
       build-local dir so NO user dotfiles are sourced; MSYS2 honors an
       inherited HOME. #>
    $env:MSYSTEM = 'MINGW64'
    $env:CHERE_INVOKED = '1'
    $env:HOME = Join-Path $Stage 'tools\msys64\home\builder'
    New-Item -ItemType Directory -Force -Path $env:HOME | Out-Null
}

function Invoke-MsysBash([string]$cmd, [string]$errmsg) {
    <# Run one command line in the staged MSYS2's bash as a MINGW64 login
       shell (login -> /etc/profile puts /mingw64/bin on PATH; CHERE_INVOKED
       keeps the caller's working directory). Dies with $errmsg on failure. #>
    $bash = Join-Path $Stage 'tools\msys64\usr\bin\bash.exe'
    if (-not (Test-Path $bash)) { Die "MSYS2 bash not staged ($bash)" }
    Set-MsysEnv
    & $bash -lc $cmd
    if ($LASTEXITCODE -ne 0) { Die "$errmsg (bash rc=$LASTEXITCODE)" }
}

function Stage-Msys {
    if ($SkipMsys) { Log 'Skipping MSYS2 toolchain (-SkipMsys)'; return }
    Log 'Staging MSYS2 + mingw gcc/make/verilator/ghdl-llvm (HDL toolchain)'
    $arc = Get-Dep 'msys2'
    $dst = Join-Path $Stage 'tools\msys64'
    # "Already staged?" is decided by the BINARY, never by the directory:
    # Set-MsysEnv points HOME at $dst\home\builder and CREATES it, so after the
    # very first Set-MsysEnv call $dst exists no matter what. A `Test-Path $dst`
    # guard therefore skipped extraction on a COLD build, leaving a msys64\
    # holding nothing but home\, and the run died at the mingw32-make check
    # below with no pacman output to explain it.
    $bash = Join-Path $dst 'usr\bin\bash.exe'
    if (-not (Test-Path $bash)) {
        # A half-made tree (only home\ from an aborted run, or a partial
        # extraction) cannot be merged into by Move-Item -- it would nest as
        # $dst\msys64. Nothing in such a tree is worth keeping; clear it.
        Remove-Item $dst -Recurse -Force -ErrorAction SilentlyContinue
        $tmp = Join-Path $Build 'msys-x'
        Remove-Item $tmp -Recurse -Force -ErrorAction SilentlyContinue
        & $7z x $arc "-o$tmp" -y | Out-Null            # .tar.xz -> .tar
        & $7z x (Get-ChildItem "$tmp\*.tar").FullName "-o$tmp" -y | Out-Null
        New-Item -ItemType Directory -Force -Path (Split-Path $dst) | Out-Null
        Move-Item "$tmp\msys64" $dst
        Remove-Item $tmp -Recurse -Force
        # Hermetic MINGW64 login env -- set only NOW: it creates HOME inside the
        # tree that has to exist first (see the guard above).
        Set-MsysEnv
        # First run initializes; then install the toolchain NgVeri/NGHDL
        # invoke (ModelGeneration: mingw64\bin\mingw32-make.exe, verilator,
        # VERILATOR_ROOT=<msys>\mingw64; ngspice_ghdl: gcc, ghdl) plus the
        # source-build utilities. ghdl-llvm EXPLICITLY: the plain ghdl
        # alternative can resolve to mcode, which cannot link the nghdl
        # socket server (see nghdl/install-nghdl-scripts/GHDL-BACKEND-26.04.md).
        # MSYS2 provisioning MUST be multi-pass, each in its OWN login shell.
        # A core-system `pacman -Syu` (pacman, bash, msys2-runtime, filesystem)
        # DELIBERATELY terminates every MSYS2 process when done -- the shell
        # dies with a nonzero code BY DESIGN, and this can happen on more than
        # one consecutive pass (runtime, then keyring/db settle). So:
        #   * chaining `pacman -Syu && pacman -S ...` never reaches the install;
        #   * gating `Die` on a -Syu exit code would abort a healthy machine.
        # Run -Syu repeatedly, IGNORING its exit code, until a pass makes no
        # changes (rc 0 with no self-terminate). The toolchain install itself
        # sits AFTER this block (it must also run on re-runs) and is the only
        # pacman step gated by Die, along with the binary/ghdl checks below.
        & $bash -lc 'true'                                    # trigger first-run init (keyring, post-install)
        for ($i = 1; $i -le 4; $i++) {                        # -Syu may self-terminate several times; rc ignored on purpose
            & $bash -lc 'pacman -Syu --noconfirm'
            if ($LASTEXITCODE -eq 0) { break }                # a clean pass (no core update left) => settled
        }
    }
    # Re-run path: the block above was skipped, but the toolchain install, the
    # ghdl backend check and `pacman -Q` below still need the hermetic login env
    # (without /usr/bin on PATH `head` and friends are missing and the checks
    # silently report nothing). Idempotent, so re-calling it after a fresh stage
    # is harmless.
    Set-MsysEnv
    # The toolchain install runs on EVERY build, not only on first provisioning:
    # it is `--needed` (a no-op costing seconds once satisfied), and it is the
    # only way a change to $MingwPkgs/$MsysPkgs reaches an ALREADY-staged
    # tools\msys64 -- otherwise adding a package (readline, say) silently has no
    # effect until someone deletes the whole staged MSYS2 by hand.
    & $bash -lc "pacman -S --noconfirm --needed $MingwPkgs $MsysPkgs"
    if ($LASTEXITCODE -ne 0) { Die 'MSYS2 toolchain provisioning failed' }
    & $bash -lc 'pacman -Scc --noconfirm'
    if (-not (Test-Path "$dst\mingw64\bin\mingw32-make.exe")) {
        Die 'mingw32-make.exe missing after MSYS2 provisioning'
    }
    # Prove the GHDL backend is NOT mcode before anything gets built with it.
    $ghdlver = & "$dst\usr\bin\bash.exe" -lc '/mingw64/bin/ghdl --version 2>&1 | head -n2'
    if ($ghdlver -match 'mcode') {
        Die "MSYS2 ghdl reports an mcode backend ($ghdlver). nghdl needs llvm/gcc; pin mingw-w64-x86_64-ghdl-llvm."
    }
    Log "ghdl: $($ghdlver -join ' ')"
    # Record the package set MSYS2 actually resolved. Everything else this
    # build downloads is hash-pinned in deps-manifest.json, but the base
    # tarball is only the STARTING point: the `pacman -Syu` + install above are
    # ROLLING, so two builds a week apart ship different gcc/verilator/ghdl
    # with nothing in the artifact recording which. Pinning package URLs
    # against repo.msys2.org's archive is the full fix; this makes a release
    # Traceable today -- the same role python-wheels.lock plays for the pip
    # set. It is written INSIDE the tree (unlike python-wheels.lock, which
    # installer.iss excludes) so a user's install can be identified after the
    # fact, from the installed files alone, when a model build misbehaves.
    # Written on every run, not just first provisioning, so a re-run after a
    # manual pacman in the stage refreshes rather than lies.
    $pkgList = & "$dst\usr\bin\bash.exe" -lc 'pacman -Q'
    if ($pkgList) {
        Set-Content (Join-Path $dst 'PACKAGES.lock') $pkgList
        Log "MSYS2 packages recorded: $(@($pkgList).Count) -> tools\msys64\PACKAGES.lock"
    } else {
        Log 'WARNING: `pacman -Q` produced no output; PACKAGES.lock not written'
    }
    Repair-VerilatorRuntimeMacros
}

function Repair-VerilatorRuntimeMacros {
    <# Silence the one warning EVERY NgVeri model build on Windows emits.

       verilator's own runtime source does this on MinGW:

           # define STDOUT_FILENO _fileno(stdout)
           # define STDERR_FILENO _fileno(stderr)

       unguarded, while mingw's stdio.h has already defined both (as 1 and 2).
       So every compile of verilated.cpp -- which is every model build, since
       the generated Makefile rebuilds ../verilated.o -- prints two
       `warning: 'STDOUT_FILENO' redefined` blocks, six lines each with the
       include chain. Nothing is wrong: the values agree. But it lands in the
       NgVeri terminal in the middle of a successful build and users read it
       as a crash. (ModelGeneration no longer paints stderr red wholesale, so
       it is amber now, not red -- this removes it outright.)

       `#undef` before the define, NOT `#ifndef` around it: that keeps
       verilator's own definition winning, so the object is byte-for-byte the
       semantics upstream intended and only the diagnostic goes away.

       Deliberately tolerant, because MSYS2's verilator is NOT hash-pinned --
       deps-manifest.json pins the msys2 BASE tarball, then `pacman -S` pulls
       whatever the rolling repo has that day (recorded after the fact in
       PACKAGES.lock; 5.050-1 at the time of writing). So this:
         * is idempotent -- a re-run over an already-patched stage is a no-op;
         * never Dies -- a verilator that fixed this upstream simply matches
           nothing, and the build carries on. It is a cosmetic patch; it must
           not be able to fail a release. #>
    $inc = Join-Path $Stage `
        'tools\msys64\mingw64\share\verilator\include\verilated.cpp'
    if (-not (Test-Path $inc)) {
        Log 'NOTE: verilated.cpp not found; skipping the STDOUT_FILENO patch'
        return
    }
    $src = Get-Content -Raw $inc
    if ($src -match '(?m)^\s*#\s*undef\s+STD(OUT|ERR)_FILENO') {
        Log 'verilator runtime: STDOUT_FILENO guard already present'
        return
    }
    # Keep the file's own `# define` spacing on the inserted `# undef` line.
    $patched = [regex]::Replace(
        $src,
        '(?m)^([ \t]*#[ \t]*)define([ \t]+)(STDOUT_FILENO|STDERR_FILENO)\b',
        "`${1}undef`${2}`${3}`n`${1}define`${2}`${3}")
    if ($patched -eq $src) {
        Log 'NOTE: verilator no longer redefines STD*_FILENO; nothing to patch'
        return
    }
    # LF, no BOM: this is a C++ source compiled by mingw g++, and the file it
    # replaces has Unix endings.
    [IO.File]::WriteAllText($inc, $patched, (New-Object Text.UTF8Encoding $false))
    Log 'verilator runtime: guarded the STDOUT/STDERR_FILENO redefinition'
}

function Stage-SimToolchain {
    <# The heart of Windows sim parity: build the CUSTOM eSim ngspice
       (nghdl-simulator -- ngspice + d_cosim + the ivlng Icarus bridge +
       ghdl.cm/Ngveri.cm) and a libvvp-enabled Icarus Verilog inside the
       staged MSYS2, mirroring what nghdl/install-nghdl.sh does on Ubuntu.

       Ships THREE trees, matching the Ubuntu $HOME/nghdl-simulator layout so
       every config key means the same thing on both OSes:
         tools\nghdl\src         ngspice sources (runtime model builds write
                                 new models into src\xspice\icm -- that is
                                 config DIGITAL_MODEL)
         tools\nghdl\release     the CONFIGURED build tree (runtime
                                 mingw32-make in release\src\xspice\icm
                                 rebuilds Ngveri.cm/ghdl.cm -- config RELEASE)
         tools\nghdl\install_dir the ngspice prefix (bin\ngspice.exe,
                                 lib\ngspice\*.cm -- what CosimConfig runs)
       Console build (no --with-wingui), exactly like Ubuntu: eSim drives
       ngspice through QProcess and parses stdout; the wingui build hijacks
       stdout into its own window. That console binary has no graphics device
       on Windows, so a second wingui-only exe is built alongside it purely for
       the interactive plot window (see below). #>
    if ($SkipSimBuild) {
        Log 'Skipping sim-toolchain source builds (-SkipSimBuild)'
        return
    }

    $nghdlDst  = Join-Path $Stage 'tools\nghdl'
    $ngspiceExe = Join-Path $nghdlDst 'install_dir\bin\ngspice.exe'
    $tarball = Join-Path $RepoRoot 'nghdl\nghdl-simulator-source.tar.xz'
    if (-not (Test-Path $tarball)) { Die "missing $tarball" }
    $toolsU = (Join-Path $Stage 'tools') -replace '\\', '/'
    $dllShU = (Join-Path $RepoRoot 'windows\msys-dll-closure.sh') -replace '\\', '/'

    # --- custom ngspice ----------------------------------------------------
    if (Test-Path $ngspiceExe) {
        Log 'Custom ngspice already staged (delete tools\nghdl to rebuild)'
    }
    else {
        Log 'Building custom eSim ngspice (nghdl-simulator, ngspice-45.2 base) in MSYS2 - this takes a while'
        $tarU   = $tarball -replace '\\', '/'
        # Fresh tree every time; configure a clean build dir. The tarball is the
        # eSim nghdl-simulator: ngspice-45.2 + the nghdl delta (ghdl/Ngveri icm
        # model dirs, outitf.c ghdlserver close hook, spinit/makedefs wiring,
        # Verilator-5 link rules) baked in.
        # ngspice >= 42 also brings d_cosim + the ivlng Icarus bridge, which the
        # old ngspice-35 tarball could never provide.
        #
        # One delta is deliberately NOT baked into the tarball: patches\0002
        # makes a d_cosim block evaluate at the operating point so it agrees
        # with an equivalent NgVeri model at t=0. It stays a readable diff for
        # review instead of an opaque change inside a binary tarball, and is
        # applied here to the freshly extracted tree. Ubuntu does the same in
        # nghdl/install-nghdl.sh (apply_esim_patches). The tree is extracted
        # fresh above, so a plain apply is enough -- no idempotence dance --
        # but a failure must stop the build rather than silently ship an
        # unpatched simulator, which is why this is inside the `set -e` chain.
        $patchU = (Join-Path $RepoRoot 'patches\ngspice') -replace '\\', '/'
        Invoke-MsysBash (
            "set -e; cd `"`$(cygpath -u '$toolsU')`" && " +
            "rm -rf nghdl nghdl-simulator-source && " +
            "tar -xJf `"`$(cygpath -u '$tarU')`" && " +
            "mv nghdl-simulator-source nghdl && cd nghdl && " +
            "for p in `"`$(cygpath -u '$patchU')`"/*.patch; do " +
            "[ -f `"`$p`" ] || continue; " +
            "echo `"applying `$(basename `"`$p`")`"; " +
            "patch -p1 < `"`$p`"; done && " +
            "rm -rf release && " +
            # Verilator runtime objects for Ngveri.cm: the icm makefile lists them
            # as link inputs but nothing compiles them (verilated_threads.o is a
            # Verilator-5 split). -DVL_TIME_CONTEXT drops the weak sc_time_stamp()
            # that a Windows DLL, unlike a Linux .so, will not leave undefined.
            "g++ -DVL_TIME_CONTEXT -I/mingw64/share/verilator/include -I/mingw64/share/verilator/include/vltstd -std=gnu++17 -O2 -fPIC -c /mingw64/share/verilator/include/verilated.cpp -o src/xspice/icm/Ngveri/verilated.o && " +
            "g++ -DVL_TIME_CONTEXT -I/mingw64/share/verilator/include -I/mingw64/share/verilator/include/vltstd -std=gnu++17 -O2 -fPIC -c /mingw64/share/verilator/include/verilated_threads.cpp -o src/xspice/icm/Ngveri/verilated_threads.o && " +
            "mkdir -p install_dir release && cd release && " +
            "../configure --enable-xspice --disable-debug " +
            "--prefix=`"`$(cygpath -am ../install_dir)`" " +
            "--exec-prefix=`"`$(cygpath -am ../install_dir)`" " +
            # -fno-strict-aliasing: kept from the ngspice-35 era (GCC-16 -O2
            # miscompiled its strcat paths); semantically safe on 45.2.
            # LIBS: ngspice gates Winsock behind --with-wingui (off in this console
            # build) but the nghdl socket client (frontend/outitf.c) needs ws2_32.
            "CFLAGS='-m64 -O2 -fno-strict-aliasing' LDFLAGS='-m64 -s' " +
            "LIBS='-lws2_32 -lpsapi -lshlwapi' && " +
            # -j2 NOT -j`$(nproc): MSYS2's fork() emulation collapses under heavy
            # parallel libtool/sh spawning (dofork: child died 0xC0000142, EAGAIN).
            # Even at -j2 it still trips occasionally: a compile dies with NO
            # diagnostic at all (`make: *** [rawfile.lo] Error 1` and nothing
            # else), and the same file then builds fine on its own. So retry the
            # whole make serially -- make resumes from the objects already built,
            # so the fallback costs only the handful left, and a genuine code
            # error still fails the second pass and kills the build.
            # ngspice.exe (and the .cm/ivlng DLLs it loads) depend on MinGW
            # runtime DLLs (gomp/readline/termcap/stdc++/gcc_s/winpthread);
            # their closure is staged by the always-run block below, which the
            # "already staged" fast path also goes through.
            "{ make -j2 || make -j1; } && make install"
        ) 'custom ngspice build failed'
    }
    if (-not (Test-Path $ngspiceExe)) { Die 'ngspice.exe missing after custom build' }

    <# --- wingui ngspice, for interactive plots only -------------------------
       The console build above has no graphics device at all (config.h:
       X_DISPLAY_MISSING, no HAS_WINGUI), so `plot` in it can only ever answer
       "Can't open viewport for graphics" -- on Ubuntu the same console build
       plots because it links X11. Build the source a second time with
       --with-wingui and keep just the exe: NgspiceWidget.open_ngspice_plots
       runs it for the plot session while the batch run keeps using the console
       twin, whose stdout it parses. On Windows ngspice finds its lib dir
       relative to the exe (src/misc/ivars.c: dirname(argv0)/../share/ngspice),
       so the exe copied into install_dir\bin picks up the console build's
       installed spinit and its absolute codemodel paths; no `make install`,
       so nothing in install_dir is overwritten. #>
    $ngspiceGuiExe = Join-Path $nghdlDst 'install_dir\bin\ngspice_gui.exe'
    if (Test-Path $ngspiceGuiExe) {
        Log 'wingui ngspice already staged (delete tools\nghdl to rebuild)'
    }
    else {
        Log 'Building wingui ngspice (interactive plot window) in MSYS2'
        Invoke-MsysBash (
            "set -e; cd `"`$(cygpath -u '$toolsU')/nghdl`" && " +
            "rm -rf release_gui && mkdir -p release_gui && cd release_gui && " +
            "../configure --with-wingui --enable-xspice --disable-debug " +
            "--prefix=`"`$(cygpath -am ../install_dir)`" " +
            "--exec-prefix=`"`$(cygpath -am ../install_dir)`" " +
            "CFLAGS='-m64 -O2 -fno-strict-aliasing' LDFLAGS='-m64 -s' " +
            "LIBS='-lws2_32 -lpsapi -lshlwapi' && " +
            # Serial retry, same reason as the console build above.
            "{ make -j2 || make -j1; } && " +
            "cp src/ngspice.exe ../install_dir/bin/ngspice_gui.exe && " +
            # The build tree is throwaway: only `release` is shipped (runtime
            # model rebuilds use it) and a second one would near-double it.
            "cd .. && rm -rf release_gui"
        ) 'wingui ngspice build failed'
    }
    if (-not (Test-Path $ngspiceGuiExe)) { Die 'ngspice_gui.exe missing after wingui build' }

    # Always ensure the MinGW runtime-DLL closure is present (idempotent, and
    # the "already staged" fast path must not skip it): without it the
    # verification below hard-hangs on Windows' missing-DLL error dialog.
    # (The iverilog .vpi modules are added as extra seeds for this same dir
    # further down, once the Icarus tree is staged -- ngspice's ivlng bridge
    # LoadLibrary's them at d_cosim simulation time, and their dependencies
    # resolve from ngspice.exe's OWN dir, never the .vpi's.)
    Invoke-MsysBash (
        "nb=`"`$(cygpath -u '$toolsU')/nghdl/install_dir`"; " +
        "sh `"`$(cygpath -u '$dllShU')`" `"`$nb/bin`" " +
        "`"`$nb`"/bin/*.exe `"`$nb`"/lib/ngspice/ivlng.dll `"`$nb`"/lib/ngspice/*.cm"
    ) 'runtime DLL closure staging failed'

    # Hard verification: version answers, the code models d_cosim/NGHDL need
    # exist, and a trivial transient actually simulates.
    $ver = & $ngspiceExe --version 2>&1 | Select-String 'ngspice' | Select-Object -First 1
    if (-not $ver) { Die 'staged ngspice does not answer --version' }
    Log "ngspice: $ver"
    $cmdir = Join-Path $nghdlDst 'install_dir\lib\ngspice'
    foreach ($cm in @('analog.cm', 'digital.cm', 'tlines.cm', 'ghdl.cm', 'Ngveri.cm')) {
        if (-not (Test-Path (Join-Path $cmdir $cm))) {
            Die "code model missing after build: $cmdir\$cm"
        }
    }
    # ngspice-45.2 ships the d_cosim code model (inside digital.cm's model set)
    # plus the ivlng Icarus bridge (ivlng.dll + ivlng.vpi, installed by
    # src/xspice/verilog). eSim's Icarus d_cosim flow and the toolchain doctor
    # both require it -- hard-fail if the build dropped it.
    foreach ($f in @('ivlng.dll', 'ivlng.vpi')) {
        if (-not (Test-Path (Join-Path $cmdir $f))) {
            Die "ivlng (Icarus d_cosim bridge) missing after build: $cmdir\$f"
        }
    }
    $smoke = Join-Path $Build 'smoke.cir'
    Set-Content $smoke "smoke test`nv1 1 0 dc 1`nr1 1 0 1k`n.op`n.end"
    & $ngspiceExe -b $smoke | Out-Null
    if ($LASTEXITCODE -ne 0) { Die "staged ngspice failed a trivial .cir run (rc=$LASTEXITCODE)" }
    Log 'ngspice smoke simulation OK'

    # --- Icarus Verilog with libvvp -----------------------------------------
    $ivDst = Join-Path $Stage 'library\bin\iverilog'
    $ivExe = Join-Path $ivDst 'bin\iverilog.exe'
    $haveLibvvp = @(Get-ChildItem "$ivDst\bin", "$ivDst\lib" -Filter 'libvvp*' `
                    -ErrorAction SilentlyContinue).Count -gt 0
    if ((Test-Path $ivExe) -and $haveLibvvp) {
        Log 'libvvp iverilog already staged (delete library\bin\iverilog to rebuild)'
    }
    else {
        Log 'Building Icarus Verilog with libvvp in MSYS2 (pinned source)'
        $src = Get-Dep 'iverilog_source'
        $srcU = $src -replace '\\', '/'
        $bldU = (Join-Path $Build 'iverilog-src') -replace '\\', '/'
        $dstU = $ivDst -replace '\\', '/'
        Invoke-MsysBash (
            "set -e; rm -rf `"`$(cygpath -u '$bldU')`" && mkdir -p `"`$(cygpath -u '$bldU')`" && " +
            "cd `"`$(cygpath -u '$bldU')`" && " +
            "tar -xzf `"`$(cygpath -u '$srcU')`" --strip-components=1 && " +
            "sh autoconf.sh && " +
            "./configure --prefix=`"`$(cygpath -m '$dstU')`" --enable-libvvp && " +
            # Serial retry: same MSYS2 parallel-spawn flakiness as the ngspice
            # builds, and -j$(nproc) exposes far more of it than their -j2.
            "{ make -j`$(nproc) || make -j1; } && make install"
        ) 'iverilog (libvvp) build failed'
    }
    if (-not (Test-Path $ivExe)) { Die 'iverilog.exe missing after build' }
    if (-not (Test-Path (Join-Path $ivDst 'bin\vvp.exe'))) { Die 'vvp.exe missing after build' }
    if (-not (Get-ChildItem "$ivDst\bin", "$ivDst\lib" -Filter 'libvvp*' -ErrorAction SilentlyContinue)) {
        Die "libvvp missing under $ivDst - the whole point of the source build. Check --enable-libvvp support at the pinned ref."
    }
    # ngspice's ivlng adapter does LoadLibrary("libvvp") -- the UNVERSIONED
    # name (eSim netlists pass no lib_args). The MinGW build emits only the
    # versioned libvvp-1.dll, so d_cosim dies with "Cannot open DLL libvvp"
    # unless a plain libvvp.dll sits beside it. Keep both.
    $vvpVersioned = Get-ChildItem "$ivDst\bin" -Filter 'libvvp-*.dll' -ErrorAction SilentlyContinue |
        Select-Object -First 1
    $vvpPlain = Join-Path $ivDst 'bin\libvvp.dll'
    if ($vvpVersioned -and -not (Test-Path $vvpPlain)) {
        Copy-Item $vvpVersioned.FullName $vvpPlain
        Log "staged libvvp.dll (copy of $($vvpVersioned.Name)) for ngspice ivlng"
    }
    if (-not (Test-Path $vvpPlain)) {
        Die "libvvp.dll (unversioned, dlopen-ed by ngspice ivlng) missing under $ivDst\bin"
    }

    # --- runtime-DLL closure for the Icarus tree -----------------------------
    # iverilog.exe itself imports only system DLLs, but everything under it
    # does not: ivl.exe/vhdlpp.exe link the MinGW runtime, and the .vpi
    # modules (system.vpi adds libbz2 + zlib1 on top) are LoadLibrary'd by
    # ivl.exe at COMPILE time (system-function discovery), by vvp.exe at sim
    # time, and by ngspice's ivlng bridge at d_cosim time. Windows resolves a
    # loaded module's dependencies from the loading EXE's dir + PATH -- never
    # from the module's own dir -- so the closure must sit in all three exe
    # dirs. Without it a fresh machine (no MinGW DLLs anywhere on PATH) dies
    # with "Failed to open ...system.vpi: The specified module could not be
    # found" -- and iverilog still exits 0, so the break used to surface only
    # at simulation time (now also caught in code by icarus.vpi_load_failed).
    $ivU = $ivDst -replace '\\', '/'
    Invoke-MsysBash (
        "iv=`"`$(cygpath -u '$ivU')`"; " +
        "nb=`"`$(cygpath -u '$toolsU')/nghdl/install_dir/bin`"; " +
        "cl=`"`$(cygpath -u '$dllShU')`"; " +
        "seeds=`"`$iv/bin/*.exe `$iv/bin/*.dll `$iv/lib/ivl/*.exe `$iv/lib/ivl/*.tgt `$iv/lib/ivl/*.vpi`"; " +
        "sh `"`$cl`" `"`$iv/bin`" `$seeds && " +
        "sh `"`$cl`" `"`$iv/lib/ivl`" `$seeds && " +
        "sh `"`$cl`" `"`$nb`" `$iv/lib/ivl/*.vpi `$iv/bin/libvvp-1.dll"
    ) 'iverilog runtime DLL closure staging failed'

    # Hard verification under a bare PATH (all a fresh user machine has):
    # compile AND vvp-run a module that uses a $-task, failing the build on
    # any VPI load error. `iverilog -V` cannot catch this class -- the driver
    # exe has no MinGW imports and never loads a .vpi.
    $vDir = Join-Path $Build 'iverilog-verify'
    New-Item -ItemType Directory -Force $vDir | Out-Null
    Set-Content (Join-Path $vDir 't.v') `
        "module t; initial begin `$display(""vpi-ok""); `$finish; end endmodule"
    $oldPath = $env:PATH
    try {
        $env:PATH = "$env:SystemRoot\System32;$env:SystemRoot"
        $cOut = & (Join-Path $ivDst 'bin\iverilog.exe') '-g2012' `
            '-o' (Join-Path $vDir 't.out') (Join-Path $vDir 't.v') 2>&1 | Out-String
        if ($LASTEXITCODE -ne 0 -or $cOut -match 'Failed to open') {
            Die "bare-PATH iverilog compile failed (rc=$LASTEXITCODE): $cOut"
        }
        $sOut = & (Join-Path $ivDst 'bin\vvp.exe') (Join-Path $vDir 't.out') 2>&1 | Out-String
        if ($LASTEXITCODE -ne 0 -or $sOut -notmatch 'vpi-ok') {
            Die "bare-PATH vvp run failed (rc=$LASTEXITCODE): $sOut"
        }
    }
    finally { $env:PATH = $oldPath }
    Log 'Icarus Verilog (with libvvp) staged; bare-PATH compile+sim verified'
}

# The official KiCad NSIS payload directories that do NOT ship inside the
# eSim installer. Everything is data KiCad loads lazily (or never, in eSim's
# flows); no binary in bin\ links against any of it. Compressed weight in the
# 9.0.3 exe, which is 1057 MB total:
#   share\kicad\3dmodels    784 MB  3D viewer STEP/WRL models (eSim: unused)
#   share\kicad\demos        55 MB  example projects
#   bin\Lib\site-packages\{numpy,PIL,pip,...}
#                            32 MB  plugin-ecosystem python extras; KiCad's
#                                   own pcbnew startup imports none of them
#                                   (wx and _pcbnew.pyd, which it does load,
#                                   are KEPT)
#   share\kicad\internat      6 MB  UI translations (English is built in)
#   bin\Lib\{test,ensurepip,idlelib,lib2to3,__pycache__}
#                             9 MB  python stdlib cruft
#   share\locale            ~ 2 MB  wxWidgets translations
# Keep: bin\ (all exes + DLLs + embedded python runtime), symbols, footprints,
# templates, resources, COPYRIGHT.txt (GPL notice). Verified functional after
# pruning: kicad-cli answers version and netlists an eSim example schematic
# (the smoke test below re-proves both on every build).
$KicadPrune = @(
    '$PLUGINSDIR',
    'share\kicad\3dmodels',
    'share\kicad\demos',
    'share\kicad\internat',
    'share\locale',
    'bin\Lib\test',
    'bin\Lib\ensurepip',
    'bin\Lib\idlelib',
    'bin\Lib\lib2to3',
    'bin\Lib\__pycache__',
    'bin\Lib\site-packages\numpy',
    'bin\Lib\site-packages\numpy.libs',
    'bin\Lib\site-packages\PIL',
    'bin\Lib\site-packages\pip',
    'bin\Lib\site-packages\setuptools',
    'bin\Lib\site-packages\wheel',
    'bin\Lib\site-packages\pkg_resources'
)

function Stage-Kicad {
    <# Bundle KiCad INSIDE the eSim installer: extract the pinned official
       KiCad NSIS installer's payload (7z reads it directly; per-file Deflate,
       not solid, so exclusions cost nothing), minus $KicadPrune, into
       tools\kicad. esim.bat puts tools\kicad\bin first on PATH, so the app's
       bare `eeschema`/`pcbnew` invocations resolve here -- a system-wide
       KiCad install, if any, is untouched and never fought with (no registry,
       no file associations, no KICAD9_* env vars).

       This deliberately supersedes the old ship-alongside design: one exe to
       download was the hard requirement, and the old objection ("a private
       KiCad copy rots") applied to a HAND-maintained repack. This one is
       reproducible: bump kicad_installer in deps-manifest.json and rebuild. #>
    Log 'Staging KiCad (official payload, pruned for eSim)'
    $setup = Get-Dep 'kicad_installer'
    $dst = Join-Path $Stage 'tools\kicad'
    $cli = Join-Path $dst 'bin\kicad-cli.exe'
    if (Test-Path $cli) {
        Log 'KiCad already staged (delete tools\kicad to re-stage)'
    }
    else {
        $xargs = $KicadPrune | ForEach-Object { "-x!$_" }
        # rc 1 = warnings only (NSIS exes carry a signature tail 7z reports as
        # "data after the end of archive"); rc >= 2 = real extraction failure.
        & $7z x -tNsis $setup "-o$dst" -y @xargs | Out-Null
        if ($LASTEXITCODE -ge 2) { Die "KiCad payload extraction failed (7z rc=$LASTEXITCODE)" }
        # Version stamp: windows_bootstrap.py derives the %APPDATA%\kicad\<N.M>
        # config dir from this so eSim's symbol libraries are registered
        # before KiCad's very first launch.
        Set-Content (Join-Path $dst 'KICAD-VERSION') $Manifest.kicad_installer.version
    }
    # Hard verification, mirroring the ngspice smoke test: the pruned tree
    # must still answer its version AND netlist a real eSim schematic.
    if (-not (Test-Path (Join-Path $dst 'bin\eeschema.exe'))) { Die 'eeschema.exe missing from staged KiCad' }
    $ver = (& $cli version 2>&1 | Select-Object -First 1)
    if ("$ver" -notmatch [regex]::Escape($Manifest.kicad_installer.version)) {
        Die "staged kicad-cli reports '$ver', expected $($Manifest.kicad_installer.version)"
    }
    foreach ($d in @('share\kicad\symbols', 'share\kicad\footprints', 'share\kicad\template')) {
        if (-not (Test-Path (Join-Path $dst $d))) { Die "staged KiCad is missing $d" }
    }
    # The bootstrap registers every row from KiCad's own template disabled by
    # default. Prove the template and symbol directory are a complete pair:
    # no referenced file was pruned, and no shipped library lacks a row users
    # can activate later in KiCad's Symbol Libraries dialog.
    $symbolDir = Join-Path $dst 'share\kicad\symbols'
    $templateFile = Join-Path $dst 'share\kicad\template\sym-lib-table'
    if (-not (Test-Path $templateFile)) { Die 'staged KiCad is missing its sym-lib-table template' }
    $templateText = Get-Content -Raw $templateFile
    $templateSymbols = @([regex]::Matches(
        $templateText, '[/\\]([^/\\"]+\.kicad_sym)"') |
        ForEach-Object { $_.Groups[1].Value } | Sort-Object -Unique)
    $stockSymbols = @(Get-ChildItem $symbolDir -Filter '*.kicad_sym' -File |
        ForEach-Object { $_.Name } | Sort-Object -Unique)
    $missingFiles = @($templateSymbols | Where-Object { $_ -notin $stockSymbols })
    $missingRows = @($stockSymbols | Where-Object { $_ -notin $templateSymbols })
    if ($stockSymbols.Count -eq 0 -or $missingFiles.Count -or $missingRows.Count) {
        Die "KiCad symbol/template mismatch: $($stockSymbols.Count) files, $($templateSymbols.Count) rows; missing files [$($missingFiles -join ', ')]; missing rows [$($missingRows -join ', ')]"
    }
    # The repo's Examples are legacy-format .sch (they predate KiCad 6);
    # kicad-cli imports that directly, which conveniently ALSO proves the
    # pruned tree still reads the legacy schematics eSim users have.
    $sch = Join-Path $Stage 'Examples\BasicGates\BasicGates.sch'
    $net = Join-Path $Build 'kicad-smoke.net'
    Remove-Item $net -ErrorAction SilentlyContinue
    & $cli sch export netlist --output $net $sch | Out-Null
    if (-not (Test-Path $net) -or (Get-Item $net).Length -eq 0) {
        Die 'staged KiCad failed to netlist Examples\BasicGates (smoke test)'
    }
    Log "KiCad $($Manifest.kicad_installer.version) staged (pruned), $($stockSymbols.Count) stock symbol libraries + netlist smoke OK"
}

function Stage-Launcher {
    <# Compile eSim.exe -- the native launcher the shortcuts point at (a .bat
       cannot carry an icon/version info and looks like a bare script in
       Windows search). Sources in windows\launcher; mirrors esim.bat's env
       setup. Runs every build: Stage-App's /MIR purge removes stage-root
       files that aren't in the repo, so the exe must be re-staged after it
       (same rule as esim.bat; the compile is ~1s). #>
    Log 'Compiling eSim.exe launcher'
    $src = Join-Path $WinDir 'launcher'
    $out = Join-Path $Stage 'eSim.exe'
    $gcc = Join-Path $Stage 'tools\msys64\mingw64\bin\gcc.exe'
    if (-not (Test-Path $gcc)) {
        $gcc = (Get-Command gcc -ErrorAction SilentlyContinue).Source
    }
    if (-not $gcc) {
        # -SkipMsys: no MSYS2 gcc. Use the pinned standalone mingw-w64 gcc
        # (build-machine tool only, nothing from it ships).
        $gccDir = Join-Path $Build 'mingw64'
        if (-not (Test-Path "$gccDir\bin\gcc.exe")) {
            & $7z x (Get-Dep 'mingw_gcc') "-o$Build" -y | Out-Null
        }
        $gcc = "$gccDir\bin\gcc.exe"
        if (-not (Test-Path $gcc)) { Die 'pinned mingw-w64 gcc did not unpack' }
    }
    $bindir = Split-Path $gcc
    $res = Join-Path $Build 'esim_launcher.res.o'
    # windres shells out to the C preprocessor; it must be able to find cpp.
    $oldPath = $env:PATH
    $env:PATH = "$bindir;$env:PATH"
    try {
        & (Join-Path $bindir 'windres.exe') `
            -I $src -I (Join-Path $RepoRoot 'images') `
            (Join-Path $src 'esim_launcher.rc') -O coff -o $res
        if ($LASTEXITCODE -ne 0) { Die 'windres failed on esim_launcher.rc' }
        & $gcc -municode -mwindows -O2 -Wall -Wextra `
            (Join-Path $src 'esim_launcher.c') $res -o $out
        if ($LASTEXITCODE -ne 0) { Die 'gcc failed on esim_launcher.c' }
    }
    finally { $env:PATH = $oldPath }
    if (-not (Test-Path $out)) { Die 'eSim.exe was not produced' }
}

function Optimize-Stage {
    <# Ship-size trims applied IN the stage, all behaviour-preserving and
       idempotent (safe on cache-hit re-runs). Trims that would break the
       stage's own build role (autotools, gnat, gdb feed source rebuilds
       here) live in installer.iss Excludes instead, so only the SHIPPED
       tree loses them.
       1) strip iverilog: the source build inherits autoconf's default
          CFLAGS (-g -O2), shipping ~100 MB of DWARF -- ivl.exe alone is
          57 MB and strips to 2.4 MB. Verified: stripped copies behave
          identically (PE, no .debug sections referenced at runtime).
       2) PyQt6: the wheel bundles the entire Qt runtime (Quick, Qml,
          Multimedia + ffmpeg, Designer, Pdf, 3D, ...). eSim imports only
          QtCore/QtGui/QtWidgets/QtPrintSupport(Qsci dep)/QtSvg + Qsci --
          dependency-walked with objdump: the kept .pyds and the
          platforms/styles/imageformats/iconengines plugins need exactly
          the kept DLL set plus the wheel's VC runtime. 214 -> ~60 MB.
       3) scipy: imported nowhere; gone from requirements-windows.txt, this
          purges stages provisioned before that change. #>
    Log 'Optimizing stage (strip iverilog, prune PyQt6, purge scipy)'

    # --- 1) strip the iverilog source build ---------------------------------
    $strip = Join-Path $Stage 'tools\msys64\mingw64\bin\strip.exe'
    $iv = Join-Path $Stage 'library\bin\iverilog'
    if ((Test-Path $strip) -and (Test-Path $iv)) {
        $targets = @(Get-ChildItem "$iv\bin", "$iv\lib\ivl" -File -ErrorAction SilentlyContinue |
            Where-Object { $_.Extension -in '.exe', '.dll', '.tgt', '.vpi' })
        $before = ($targets | Measure-Object Length -Sum).Sum
        foreach ($t in $targets) { & $strip --strip-unneeded $t.FullName }
        $after = (($targets | ForEach-Object { Get-Item $_.FullName }) |
            Measure-Object Length -Sum).Sum
        Log ('iverilog stripped: {0:N1} MB -> {1:N1} MB' -f ($before / 1MB), ($after / 1MB))
        & "$iv\bin\iverilog.exe" -V | Out-Null
        if ($LASTEXITCODE -ne 0) { Die 'stripped iverilog.exe no longer answers -V' }
        # Strip touched the runtime DLLs and .vpi modules too -- re-prove the
        # bare-PATH compile Stage-SimToolchain verified (VPI loads intact).
        $vSrc = Join-Path $Build 'iverilog-verify\t.v'
        if (Test-Path $vSrc) {
            $oldPath = $env:PATH
            try {
                $env:PATH = "$env:SystemRoot\System32;$env:SystemRoot"
                $cOut = & "$iv\bin\iverilog.exe" '-g2012' `
                    '-o' (Join-Path $Build 'iverilog-verify\t2.out') $vSrc 2>&1 | Out-String
                if ($LASTEXITCODE -ne 0 -or $cOut -match 'Failed to open') {
                    Die "stripped iverilog fails bare-PATH compile (rc=$LASTEXITCODE): $cOut"
                }
            }
            finally { $env:PATH = $oldPath }
        }
    }

    # --- 2) prune the PyQt6 wheel to the modules eSim imports ---------------
    $pyqt = Join-Path $Stage 'python\Lib\site-packages\PyQt6'
    if (Test-Path "$pyqt\Qt6\bin") {
        $keepMods = @('QtCore', 'QtGui', 'QtWidgets', 'QtPrintSupport', 'QtSvg', 'Qsci', 'sip')
        $keepDlls = @('Qt6Core.dll', 'Qt6Gui.dll', 'Qt6Widgets.dll', 'Qt6PrintSupport.dll',
                      'Qt6Svg.dll',
                      # VC runtime the wheel carries; every kept binary links it
                      'concrt140.dll', 'msvcp140.dll', 'msvcp140_1.dll', 'msvcp140_2.dll',
                      'msvcp140_atomic_wait.dll', 'msvcp140_codecvt_ids.dll', 'vccorlib140.dll',
                      'vcruntime140.dll', 'vcruntime140_1.dll', 'vcruntime140_threads.dll')
        $keepPlugins = @('platforms', 'styles', 'imageformats', 'iconengines', 'generic')
        Get-ChildItem "$pyqt\Qt6\bin" -File |
            Where-Object { $keepDlls -notcontains $_.Name } | Remove-Item -Force
        Get-ChildItem "$pyqt\Qt6\plugins" -Directory |
            Where-Object { $keepPlugins -notcontains $_.Name } | Remove-Item -Recurse -Force
        # qpdf imageformat links the deleted Qt6Pdf.dll
        Remove-Item "$pyqt\Qt6\plugins\imageformats\qpdf.dll" -Force -ErrorAction SilentlyContinue
        # qml runtime, Qt UI translations, .sip build files, lupdate tooling
        foreach ($d in @("$pyqt\Qt6\qml", "$pyqt\Qt6\translations", "$pyqt\bindings", "$pyqt\lupdate")) {
            Remove-Item $d -Recurse -Force -ErrorAction SilentlyContinue
        }
        # bindings (+stubs) for Qt modules eSim never imports
        Get-ChildItem $pyqt -File |
            Where-Object { $_.Extension -in '.pyd', '.pyi' } |
            Where-Object { $keepMods -notcontains ($_.BaseName -replace '\.cp\d.*$', '') } |
            Remove-Item -Force

        # The GUI stack must still come up on the pruned set (offscreen uses
        # the kept qoffscreen platform plugin; matplotlib exercises the Agg
        # canvas import chain).
        $pyexe = Join-Path $Stage 'python\python.exe'
        $env:QT_QPA_PLATFORM = 'offscreen'
        try {
            & $pyexe -c 'from PyQt6.QtWidgets import QApplication; import PyQt6.Qsci; from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg; QApplication([]); print("pyqt-prune-ok")'
            if ($LASTEXITCODE -ne 0) { Die 'PyQt6 prune broke the GUI stack (offscreen import check)' }
        }
        finally { Remove-Item Env:QT_QPA_PLATFORM -ErrorAction SilentlyContinue }
    }

    # --- 3) purge scipy from pre-existing stages -----------------------------
    Get-ChildItem (Join-Path $Stage 'python\Lib\site-packages') -Filter 'scipy*' -ErrorAction SilentlyContinue |
        Remove-Item -Recurse -Force
}

# Upstream demo models that are genuinely part of the distribution (they came
# with the sky130 PDK + analog IPs). Everything else under modelParamXML is a
# local user's model. Keep in sync with library\modelParamXML\Ngveri\.gitignore.
$script:ShippedModelXml = @('dvsd_8_bit_priority_encoder.xml', 'vsdserializer_v1.xml')

function Reset-StageModels {
    <# Return the staged tree to a FRESH-INSTALL model state.

       Stage-App mirrors the working tree with robocopy, and Stage-SimToolchain
       reuses an already-built tools\nghdl on re-runs. Both faithfully carry
       across whatever the packager's own eSim did on this box, and a model the
       packager added leaks into the release three ways at once:

         1. library\modelParamXML\{Ngveri,NgVeriCosim,Nghdl}\<model>.xml
            -- NgVeri._list_models reads these back, so a fresh install opens
            Remove Models already listing a stranger's models.
         2. tools\nghdl\{src,release}\src\xspice\icm\{Ngveri,ghdl}\<model>\
            -- the model's generated C + compiled objects, plus its line in
            modpath.lst (which is what cmpp builds the code model FROM).
         3. tools\nghdl\install_dir\lib\ngspice\{Ngveri.cm,ghdl.cm}
            -- worst of the three: the model is LINKED INTO the shipped code
            model, so it is loadable in the user's ngspice whether or not any
            of the files above survive.

       .gitignore cannot help here: robocopy mirrors the working tree, not the
       index. So scrub the stage itself, then relink the two code models from a
       model-free icm tree. Idempotent -- on a clean stage every step no-ops.

       Anything found is reported, not silently swallowed: a packager should
       see what their box was about to ship. #>
    Log 'Resetting staged models to fresh-install state'
    $script:RemovedModelNames = @()

    # --- 1) modelParamXML: drop everything not on the shipped whitelist ------
    foreach ($d in @('Ngveri', 'NgVeriCosim', 'Nghdl')) {
        $dir = Join-Path $Stage "library\modelParamXML\$d"
        if (-not (Test-Path $dir)) { continue }
        Get-ChildItem $dir -Filter '*.xml' -File -ErrorAction SilentlyContinue |
            Where-Object { $script:ShippedModelXml -notcontains $_.Name } |
            ForEach-Object {
                Log "  drop local model xml: $d\$($_.Name)"
                $script:RemovedModelNames += $_.BaseName
                Remove-Item $_.FullName -Force
            }
    }

    # --- 2) icm model dirs + modpath.lst ------------------------------------
    $nghdlDst = Join-Path $Stage 'tools\nghdl'
    $icmRoots = @("$nghdlDst\src\xspice\icm", "$nghdlDst\release\src\xspice\icm")
    $dirty = $false
    foreach ($root in $icmRoots) {
        foreach ($fam in @('Ngveri', 'ghdl')) {
            $famDir = Join-Path $root $fam
            if (-not (Test-Path $famDir)) { continue }
            # Every subdirectory here IS a model, bar automake's own .deps:
            # the family's build artifacts (Ngveri.cm, dlmain.o, verilated*.o,
            # cm*.h, objects.inc) are files, never directories.
            Get-ChildItem $famDir -Directory -ErrorAction SilentlyContinue |
                Where-Object { -not $_.Name.StartsWith('.') } |
                ForEach-Object {
                    Log "  drop compiled model: $fam\$($_.Name)"
                    $script:RemovedModelNames += $_.Name
                    Remove-Item $_.FullName -Recurse -Force
                    $dirty = $true
                }
            # modpath.lst is the model list cmpp compiles from; an entry with no
            # directory makes it abort, so the list must be emptied, not left.
            $mp = Join-Path $famDir 'modpath.lst'
            if ((Test-Path $mp) -and (Get-Item $mp).Length -gt 0) {
                $script:RemovedModelNames += (Get-Content $mp |
                    Where-Object { $_.Trim() })
                Clear-Content $mp
                $dirty = $true
            }
        }
    }
    $script:RemovedModelNames = @($script:RemovedModelNames |
        Where-Object { $_ } | ForEach-Object { $_.Trim() } | Sort-Object -Unique)

    # --- 4) relink the code models without them ------------------------------
    # Unconditional, not gated on $dirty. A model can be linked into Ngveri.cm
    # with no trace left in the icm tree -- eSim's d_cosim teardown removes the
    # model directory and its modpath.lst line but never relinks -- so "nothing
    # to delete" does not imply "nothing in the .cm". The relink is ~30 s.
    if (-not $dirty) { Log 'no model files staged; relinking anyway' }
    $relIcm = Join-Path $nghdlDst 'release\src\xspice\icm'
    $bash = Join-Path $Stage 'tools\msys64\usr\bin\bash.exe'
    if (-not ((Test-Path $relIcm) -and (Test-Path $bash))) {
        # No toolchain to rebuild with (-SkipMsys / -SkipSimBuild). Do NOT
        # pretend this is fine: the .cm files still carry the models, and
        # Assert-CleanStage will refuse to package them.
        Log 'WARNING: cannot relink code models (no staged MSYS2/release tree)'
        return
    }
    # Delete the built code models first: make compares timestamps, and the
    # existing .cm is newer than the sources whose object list just shrank, so
    # an incremental make would leave the model linked in.
    foreach ($fam in @('Ngveri', 'ghdl')) {
        Remove-Item (Join-Path $relIcm "$fam\$fam.cm") -Force -ErrorAction SilentlyContinue
    }
    $instU = ((Join-Path $nghdlDst 'install_dir') -replace '\\', '/')
    $icmU = ($relIcm -replace '\\', '/')
    # Same two commands the runtime model build runs (ModelGeneration.runMake /
    # runMakeInstall), including the pkglibdir/pkgdatadir override: the tree was
    # configured with the BUILD box's absolute prefix baked into makedefs, so a
    # stock `make install` would write the .cm somewhere outside this stage.
    Log 'Relinking Ngveri.cm/ghdl.cm without local models'
    # Strip afterwards rather than relinking with '-s': the icm makefile keeps
    # -shared (and the -lws2_32/-lpsapi closure) in LDFLAGS, so passing
    # LDFLAGS='-m64 -s' on the command line REPLACES all of it and the link
    # collapses into an exe link -- "undefined reference to `WinMain'". Without
    # a strip the relinked models come back ~2.6x the size the toolchain build
    # shipped, so strip the four copies (release tree + install_dir) instead.
    # --strip-unneeded keeps the export table these DLLs are dlopen'd for.
    Invoke-MsysBash (
        "set -e; cd `"`$(cygpath -u '$icmU')`" && " +
        "mingw32-make && " +
        "mingw32-make install pkglibdir='$instU/lib/ngspice' " +
        "pkgdatadir='$instU/share/ngspice' && " +
        "strip --strip-unneeded Ngveri/Ngveri.cm ghdl/ghdl.cm " +
        "'$instU/lib/ngspice/Ngveri.cm' '$instU/lib/ngspice/ghdl.cm'"
    ) 'code-model relink failed'

    # The relinked models must still load: ngspice reads spinit at startup and
    # `codemodel`s every .cm in lib\ngspice, so a broken one fails here.
    $ngspiceExe = Join-Path $nghdlDst 'install_dir\bin\ngspice.exe'
    if (Test-Path $ngspiceExe) {
        $smoke = Join-Path $Build 'cm-relink-smoke.cir'
        Set-Content $smoke "relink smoke`nv1 1 0 dc 1`nr1 1 0 1k`n.op`n.end"
        $out = & $ngspiceExe -b $smoke 2>&1 | Out-String
        if ($LASTEXITCODE -ne 0 -or $out -match 'could not be loaded|error') {
            Die "relinked code models broke ngspice (rc=$LASTEXITCODE): $out"
        }
        Log 'Relinked code models load and simulate OK'
    }
}

function Assert-CleanStage {
    <# Refuse to package a stage that carries anything from the packager's own
       machine. Reset-StageModels does the removing; this is the independent
       check that it worked, so a silent regression in the staging order (or a
       future -Skip flag that bypasses the reset) cannot ship a dirty tree.

       Fails the build rather than warning: a leak is only discoverable after
       the installer is in users' hands. #>
    Log 'Verifying release stage contents'
    $bad = @()

    # /XD handles an ordinary checkout's .git directory; /XF handles the .git
    # pointer file used by linked worktrees. Keep this independent guard so a
    # future staging rewrite still cannot publish repository metadata.
    if (Test-Path (Join-Path $Stage '.git')) {
        $bad += 'VCS metadata: .git'
    }

    foreach ($d in @('Ngveri', 'NgVeriCosim', 'Nghdl')) {
        $dir = Join-Path $Stage "library\modelParamXML\$d"
        if (-not (Test-Path $dir)) { continue }
        $bad += Get-ChildItem $dir -Filter '*.xml' -File -ErrorAction SilentlyContinue |
            Where-Object { $script:ShippedModelXml -notcontains $_.Name } |
            ForEach-Object { "local model xml: modelParamXML\$d\$($_.Name)" }
    }

    $nghdlDst = Join-Path $Stage 'tools\nghdl'
    foreach ($root in @("$nghdlDst\src\xspice\icm", "$nghdlDst\release\src\xspice\icm")) {
        foreach ($fam in @('Ngveri', 'ghdl')) {
            $famDir = Join-Path $root $fam
            if (-not (Test-Path $famDir)) { continue }
            $bad += Get-ChildItem $famDir -Directory -ErrorAction SilentlyContinue |
                Where-Object { -not $_.Name.StartsWith('.') } |
                ForEach-Object { "compiled model dir: $fam\$($_.Name)" }
            $mp = Join-Path $famDir 'modpath.lst'
            if (Test-Path $mp) {
                $bad += Get-Content $mp | Where-Object { $_.Trim() } |
                    ForEach-Object { "modpath.lst entry: $fam -> $_" }
            }
        }
    }

    # The decisive one. Files can be deleted after the fact; a model linked
    # into the code model can only be removed by relinking it, so scan the
    # shipped binaries for the names we pulled out. ASCII-decoding the bytes is
    # enough -- cmpp emits the model name as a plain C identifier/string.
    $cmdir = Join-Path $nghdlDst 'install_dir\lib\ngspice'
    foreach ($cm in @('Ngveri.cm', 'ghdl.cm')) {
        $f = Join-Path $cmdir $cm
        if (-not (Test-Path $f)) { continue }
        $text = [Text.Encoding]::ASCII.GetString([IO.File]::ReadAllBytes($f))
        foreach ($n in $script:RemovedModelNames) {
            if ($n -and $text.Contains($n)) { $bad += "$cm still links model '$n'" }
        }
    }

    # The generated symbol libs are seeds: eSim writes a user's model symbols to
    # %LOCALAPPDATA%-side kicad_symbols, never back into these, so any symbol
    # here came from the packager's box.
    foreach ($sym in @('eSim_NgVeri.kicad_sym', 'eSim_Nghdl.kicad_sym',
                       'eSim_NgVeriCosim.kicad_sym')) {
        $f = Join-Path $Stage "library\kicadLibrary\eSim-symbols\$sym"
        if (-not (Test-Path $f)) { continue }
        $n = @(Select-String -Path $f -Pattern '^\s*\(symbol "' -AllMatches).Count
        if ($n -gt 0) { $bad += "$sym carries $n pre-seeded symbol(s)" }
    }

    if ($bad.Count) {
        Die ("stage is not clean -- refusing to package:`n  " +
             ($bad -join "`n  "))
    }
    Log 'Stage clean: no VCS metadata or local models'
}

# ----------------------------------------------------------------- main ----
if ($Clean) { Remove-Item $Build, $Dist -Recurse -Force -ErrorAction SilentlyContinue }
$7z = Resolve-7z
New-Item -ItemType Directory -Force -Path $Build, $Dist | Out-Null

Stage-App
Stage-Python
Stage-Sky130        # archive -> validated runtime dir; archive never ships
Stage-Msys           # must precede Stage-SimToolchain (it builds inside MSYS2)
Stage-SimToolchain   # custom ngspice + libvvp iverilog (Full flavour)
Stage-Ngspice        # official build: Compact fallback (+ shim on -SkipSimBuild)
Test-Sky130Simulation # complete tt-corner parse + analog inverter response
Stage-Iverilog       # Bleyer fallback, only on -SkipSimBuild
Stage-Kicad          # pruned official KiCad payload -> tools\kicad (bundled)
Stage-Launcher       # eSim.exe (native shortcut target; after Stage-App's /MIR)
Optimize-Stage       # strip iverilog + prune PyQt6/scipy (idempotent, last)
Reset-StageModels    # fresh-install model state (relinks the code models)
Assert-CleanStage    # ...and refuse to package if anything local survived

Log 'Compiling installer (Inno Setup)'
$Iscc = Resolve-Iscc
& $Iscc /Qp "/DAppVersion=$Version" "/DStageDir=$Stage" "/DOutDir=$Dist" `
    (Join-Path $WinDir 'installer.iss')
if ($LASTEXITCODE -ne 0) { Die 'ISCC failed' }

Get-ChildItem $Dist -File | Where-Object Extension -ne '.sha256' | ForEach-Object {
    "$((Get-FileHash $_.FullName -Algorithm SHA256).Hash.ToLower())  $($_.Name)" |
        Set-Content "$($_.FullName).sha256"
}

Log "Done. Artifacts in $Dist"
Get-ChildItem $Dist | Format-Table Name, @{n='MB';e={[math]::Round($_.Length/1MB,1)}}
