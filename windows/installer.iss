; =============================================================================
; eSim Windows installer (Inno Setup 6).
;
; Compiled by build-windows.ps1, which passes:
;   /DAppVersion=<VERSION>   /DStageDir=<staged tree>   /DOutDir=<dist>
;
; Design notes (see PACKAGING.md for the full rationale):
;  * Install root defaults to C:\FOSSEE\eSim -- deliberately SPACE-FREE:
;    the optional MSYS2/mingw toolchain (NgVeri model builds) and ngspice
;    code-model paths break subtly under paths with spaces.
;  * Everything per-user (~/.esim, ~/.nghdl, KiCad sym-lib-table) is done by
;    windows\windows_bootstrap.py on every launch, NOT here -- so multi-user
;    machines and upgrades self-heal, and the logic is unit-tested.
;  * KiCad IS bundled, at tools\kicad: the official installer's payload,
;    pruned for eSim by build-windows.ps1's Stage-Kicad (no 3D models/demos/
;    translations). Private to eSim: esim.bat prepends tools\kicad\bin to
;    PATH; no registry entries, file associations or global env vars, so a
;    system-wide KiCad install coexists untouched. One exe = the whole tool.
; =============================================================================

#ifndef AppVersion
  #define AppVersion "0.0"
#endif
#ifndef StageDir
  #define StageDir "build\eSim"
#endif
#ifndef OutDir
  #define OutDir "dist"
#endif

[Setup]
AppId={{7E63A0F2-2C6B-4D3B-9E3E-ESIM0000FOSS}
AppName=eSim
AppVersion={#AppVersion}
AppPublisher=FOSSEE, IIT Bombay
AppPublisherURL=https://esim.fossee.in/
DefaultDirName={sd}\FOSSEE\eSim
DisableProgramGroupPage=yes
UninstallFilesDir={app}
UninstallDisplayIcon={app}\eSim.exe
OutputDir={#OutDir}
OutputBaseFilename=eSim-{#AppVersion}-installer
Compression=lzma2/max
SolidCompression=yes
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
PrivilegesRequired=admin
WizardStyle=modern

; License agreement page. eSim is GPLv3; the repo's root LICENSE is the same
; text shipped in the install tree. Pointing LicenseFile at it makes Inno add
; the standard "License Agreement" page (accept/decline) before folder select,
; matching the old NSIS installer's first step. Path is relative to this .iss.
; Inno reads it as plain text (no .txt extension needed; RTF is auto-detected).
LicenseFile=..\LICENSE

; Branding. One identity end to end: the setup exe carries the SAME icon as
; eSim.exe, the Start-menu/desktop shortcuts and the uninstall entry, so the
; downloaded file is recognisable in Explorer and the download bar before it
; is ever run. The wizard panels (eSim mark + FOSSEE logo) are generated from
; the repo's own logo assets by branding\make-wizard-images.py -- one file per
; DPI scaling step (100/125/150/200%); Inno picks the closest match, which is
; why they are listed rather than wildcarded (a wildcard would also sweep the
; small images into the big-panel slot).
SetupIconFile=..\images\esim.ico
WizardImageFile=branding\wizard-164x314.bmp,branding\wizard-205x393.bmp,branding\wizard-246x471.bmp,branding\wizard-328x628.bmp
WizardSmallImageFile=branding\wizard-small-55x58.bmp,branding\wizard-small-69x73.bmp,branding\wizard-small-83x87.bmp,branding\wizard-small-110x116.bmp

[Types]
Name: "full";    Description: "Full (HDL toolchain: NgVeri, d_cosim, NGHDL/GHDL VHDL co-sim)"
Name: "compact"; Description: "Compact (analog simulation only; no HDL model builds)"
Name: "custom";  Description: "Custom"; Flags: iscustom

[Components]
Name: "core"; Description: "eSim application, ngspice, Icarus Verilog"; \
    Types: full compact custom; Flags: fixed
Name: "hdl";  Description: "HDL toolchain: MSYS2 mingw gcc/make/verilator/GHDL (NgVeri code-model builds + NGHDL VHDL co-simulation)"; \
    Types: full

[Tasks]
; The AI Assistant's Python packages ship in the bundled interpreter; what
; this task adds is too big to bundle: the Ollama runtime (pinned in
; deps-manifest.json, sha256-checked) and ~2.2 GB of local models. Opt-in,
; since it is a multi-GB download; without it eSim shows the assistant with a
; prompt to install Ollama.
Name: "aiassistant"; Description: "Install the eSim AI Assistant (downloads Ollama, 1.5 GB, and ~2.2 GB of local AI models)"; \
    Flags: unchecked

[Dirs]
; eSim's HDL model builds WRITE inside the install tree by design -- exactly
; like the Ubuntu install owns $HOME/nghdl-simulator. Setup runs as admin but
; eSim runs as the user, so the written dirs carry a users-modify ACE, which
; NTFS inheritance then extends to everything [Files] installs into them
; (Inno processes [Dirs] before [Files]).
;
; The grant used to sit on {app} itself. That also handed every local user
; write access to python\, eSim.exe, tools\kicad\bin and tools\msys64\ -- i.e.
; the ability to swap a binary the NEXT user of the machine runs. On the
; shared lab machines eSim targets that is a local tamper vector, so the ACE
; is scoped to the two trees the running app genuinely writes:
;
;   tools\nghdl            new model sources land in src\xspice\icm, the .cm
;                          rebuild runs in release\, `make install` writes
;                          install_dir\, and windows_bootstrap.fix_spinit
;                          rewrites install_dir\share\ngspice\scripts\spinit
;                          on first launch (it ships with build-machine paths
;                          baked into its codemodel lines).
;   library\modelParamXML  createkicad / createkicadCosim / NgVeri /
;                          model_teardown add and remove <model>.xml under
;                          Ngveri, NgVeriCosim and Nghdl.
;
; Read-only at runtime -- verified against the source, deliberately NOT
; granted (if a future change starts writing to one of these, widen the list
; here rather than moving the ACE back up to {app}):
;   library\kicadLibrary   static symbol libs are referenced in place; the
;                          libs eSim REWRITES moved to ~\.esim\kicad_symbols
;                          (kicad_symlib.generated_symlib_path) long ago, and
;                          the install path survives only as a legacy READ
;                          probe for migrating older installs.
;   library\bin\iverilog   ensure_unversioned_libvvp() copies libvvp.dll only
;                          when the build did not -- and Stage-SimToolchain
;                          stages it (the Bleyer fallback has no libvvp to
;                          copy at all, so the write never happens either way).
;   tools\msys64           used purely as a toolchain: mingw32-make, gcc,
;                          verilator and ghdl are invoked by full path with
;                          cwd= the model dir, and the generated cfunc's
;                          scratch file goes to %LOCALAPPDATA%\Temp.
;   src, windows, python   bytecode is precompiled by [Run] below, as admin.
;
; KNOWN RESIDUAL -- this scoping removes eSim's OWN over-broad grant, and on
; its own it does NOT finish the job at the default install root. Windows
; ships C:\ with `NT AUTHORITY\Authenticated Users:(OI)(CI)(IO)(M)`, an
; inherit-only Modify that propagates into every folder created under it, so a
; tree at {sd}\FOSSEE\eSim inherits user-writable ACLs from the drive root no
; matter what this section says. Verified on a real install:
;   C:\FOSSEE\eSim\python -> BUILTIN\Users:(I)(OI)(CI)(M)      [this section]
;                            NT AUTHORITY\Authenticated Users:(I)(M)  [from C:\]
; Closing it needs the install root's INHERITANCE broken as well, e.g. a [Run]
; step after the files land:
;   icacls "{app}" /inheritance:r ^
;     /grant *S-1-5-32-544:(OI)(CI)F /grant *S-1-5-18:(OI)(CI)F ^
;     /grant *S-1-5-32-545:(OI)(CI)RX
; (well-known SIDs, not names -- localized Windows renames these groups). That
; is a bigger behavioural change than a permissions narrowing: it must be
; validated by a Full install followed by an NgVeri + d_cosim + NGHDL model
; build from a SECOND, standard-user account, since getting it wrong leaves a
; tree the user can neither build in nor delete. Deliberately left for that
; test rather than shipped unverified.
Name: "{app}\tools\nghdl";           Permissions: users-modify
Name: "{app}\library\modelParamXML"; Permissions: users-modify

[Files]
; Core = everything except the HDL build toolchain. NOTE tools\nghdl\
; install_dir (the custom eSim ngspice runtime: d_cosim + ivlng + ghdl.cm,
; plus ngspice_gui.exe, the wingui twin that draws the interactive plots)
; IS core -- every flavour simulates with it; only the trees used to BUILD
; new HDL models (MSYS2, ngspice sources, configured build tree) are the
; optional 'hdl' component. release_gui is a throwaway build dir; the build
; script deletes it, and this excludes an interrupted build's leftovers.
; tools\nghdl.old: a hand-made backup of an earlier simulator tree that
; survives in the stage across incremental builds (nothing in the pipeline
; creates or purges it) and rode into the last release as 127 MB of dead
; weight. Belt and braces -- the build script now deletes it as well.
;
; Ship-size excludes (the stage keeps all of this -- source rebuilds there
; need the full toolchain; only the SHIPPED tree is trimmed):
;  * tools\nghdl\{examples,tests,autom4te.cache,visualc,man}: ngspice source
;    tarball baggage; runtime model builds touch only src\ headers, release\
;    and install_dir\.
;  * tools\ngspice\{examples,docs}: official-zip baggage, ~26 MB.
;  * pip/pytest and friends: installed into the stage python for build-time
;    testing; the app imports none of them. NOTE the installed tree therefore
;    has no pip/pytest -- run the suite against an install with the STAGE
;    python (same version, same wheel set).
;  * scipy: nothing in the tree imports it (also gone from
;    requirements-windows.txt; this catches stages provisioned before that).
;  * developer/repo files a user install has no use for (leading backslash =
;    rooted at {app}, so e.g. \scripts does NOT touch python\Scripts, and
;    \docs does not shadow anything deeper):
;      - build/porting notes + packaging docs (WINDOWS-*.md, PACKAGING.md,
;        MAINTAINERS-PACKAGING.md), contributor/repo docs (CONTRIBUTION.md,
;        SECURITY.md, INSTALL -- Ubuntu instructions), Sphinx sources
;        (\code, \conf.py, \index.rst), Linux-only trees (\ihp, \patches,
;        \scripts, \docs, make-release.sh), and pip metadata for the bundled
;        interpreter (setup.py, requirements.txt, python-wheels.lock).
;      - unrooted `tests`: every dir named tests outside msys64 is dev-only
;        (src\*\tests, site-packages numpy/matplotlib/colorama tests, kicad
;        stdlib tests) -- verified by find before adding. `test` likewise
;        (kicad stdlib ctypes/tkinter/unittest test dirs). msys64 and the
;        nghdl src/release trees have their OWN [Files] entries, so these
;        unrooted patterns cannot reach the toolchain.
;    windows\windows_bootstrap.py STAYS: launcher_windows imports it on
;    every launch. README.md, LICENSE, VERSION, RELEASE stay (user-facing).
Source: "{#StageDir}\*"; DestDir: "{app}"; Components: core; \
    Excludes: "tools\msys64\*,tools\nghdl\src\*,tools\nghdl\release\*,tools\nghdl\release_gui\*,tools\nghdl.old\*,tools\nghdl\examples,tools\nghdl\tests,tools\nghdl\autom4te.cache,tools\nghdl\visualc,tools\nghdl\man,tools\ngspice\examples,tools\ngspice\docs,python\Lib\site-packages\pip,python\Lib\site-packages\pip-*,python\Lib\site-packages\pytest,python\Lib\site-packages\_pytest,python\Lib\site-packages\pytest-*,python\Lib\site-packages\pytest_timeout*,python\Lib\site-packages\iniconfig*,python\Lib\site-packages\pluggy*,python\Lib\site-packages\scipy,python\Lib\site-packages\scipy.libs,python\Lib\site-packages\scipy-*,python\Scripts\pip.exe,python\Scripts\pip3.exe,python\Scripts\pip3.12.exe,python\Scripts\pytest.exe,python\Scripts\py.test.exe,python\Scripts\f2py.exe,python\Scripts\numpy-config.exe,\PACKAGING.md,\MAINTAINERS-PACKAGING.md,\CONTRIBUTION.md,\SECURITY.md,\INSTALL,\make-release.sh,\setup.py,\conf.py,\index.rst,\requirements.txt,\python-wheels.lock,\code,\docs,\ihp,\patches,\scripts,\src\conftest.py,tests,test"; \
    Flags: recursesubdirs createallsubdirs ignoreversion
; MSYS2 ship-size excludes, verified against what runtime model builds use:
;  * pacman download cache (var\cache) and locale/man/doc/info trees.
;  * gdb (debugger; nothing in a user install debugs). NOTE: this exclusion
;    used to be paired with "mingw64's python3.14 deliberately STAYS despite
;    arriving as gdb's scripting dep", because verilator's verilated.mk
;    hardcodes `PYTHON3 = python3` and every NgVeri model make runs
;    $(PYTHON3) verilator_includer -- pruning it broke NgVeri with "Error
;    127". That reasoning silently depended on gdb being INSTALLED, and gdb
;    has never been in $MingwPkgs: it was only ever present in a
;    hand-provisioned build tree ("Install Reason: Explicitly installed"),
;    so the python it dragged in vanished the moment anyone built from
;    scratch -- and NgVeri died with `python3: command not found` again.
;    ModelGeneration now passes eSim's OWN bundled interpreter as a make
;    command-line variable (_python_for_make), so no MSYS2 python is needed
;    on any path and nothing here has to be kept alive for it. Do not
;    "restore" mingw-w64-x86_64-python to fix a python3 error; check that
;    override instead.
;  * gnat*.exe + adainclude: the Ada COMPILER that built ghdl. ghdl.exe is
;    statically linked (imports only system DLLs) and never compiles Ada at
;    runtime. adalib STAYS: lib\ghdl\grt.lst passes -L...\adalib\ at VHDL
;    elaboration, so NGHDL links against it on user machines.
;  * autotools (autoconf x6, automake x8, aclocal): configure ran at package
;    time; runtime model builds only ever run make. perl STAYS -- the
;    verilator driver is a perl script.
;  * verilator debug twins (only `verilator --debug` loads them).
Source: "{#StageDir}\tools\msys64\*"; DestDir: "{app}\tools\msys64"; Components: hdl; \
    Excludes: "var\cache,usr\share\locale,usr\share\man,usr\share\doc,usr\share\info,usr\share\bash-completion,mingw64\share\man,mingw64\share\doc,mingw64\share\info,mingw64\share\locale,mingw64\share\gtk-doc,mingw64\share\gdb,gdb.exe,gdbserver.exe,gdb-add-index,gnat*.exe,adainclude,verilator_bin_dbg.exe,verilator_coverage_bin_dbg.exe,usr\bin\autoconf*,usr\bin\autoheader*,usr\bin\autom4te*,usr\bin\automake*,usr\bin\autoreconf*,usr\bin\autoscan*,usr\bin\autoupdate*,usr\bin\autopoint,usr\bin\aclocal*,usr\bin\ifnames,usr\share\autoconf*,usr\share\automake*,usr\share\aclocal*"; \
    Flags: recursesubdirs createallsubdirs ignoreversion skipifsourcedoesntexist
Source: "{#StageDir}\tools\nghdl\src\*"; DestDir: "{app}\tools\nghdl\src"; Components: hdl; \
    Flags: recursesubdirs createallsubdirs ignoreversion skipifsourcedoesntexist
Source: "{#StageDir}\tools\nghdl\release\*"; DestDir: "{app}\tools\nghdl\release"; Components: hdl; \
    Flags: recursesubdirs createallsubdirs ignoreversion skipifsourcedoesntexist

[Icons]
; eSim.exe is a real GUI executable (windows\launcher) with the icon and
; version info embedded: proper identity in Windows search and the taskbar.
; By default it spawns eSim under python.exe in its own log console (the
; stdout/stderr stream, Linux-like); pass --no-console for the silent pythonw
; launch. esim.bat remains in {app} for terminal use (--no-console, --doctor).
; AppUserModelID matches SetCurrentProcessExplicitAppUserModelID in
; Application.py: the running python windows group under this shortcut, so
; the taskbar shows the eSim icon (and pinning works) instead of a blank
; python entry.
Name: "{autoprograms}\eSim"; Filename: "{app}\eSim.exe"; WorkingDir: "{app}"; AppUserModelID: "FOSSEE.eSim.2.5"
Name: "{autodesktop}\eSim";  Filename: "{app}\eSim.exe"; WorkingDir: "{app}"; AppUserModelID: "FOSSEE.eSim.2.5"

[Run]
; Precompile bytecode at install time so the first cold launch doesn't compile
; every .py on import (and Defender doesn't scan each freshly written .pyc).
Filename: "{app}\python\python.exe"; \
    Parameters: "-m compileall -q -j 0 ""{app}\src"" ""{app}\windows"""; \
    WorkingDir: "{app}"; StatusMsg: "Precompiling eSim modules..."; \
    Flags: runhidden
; NOTE: no Defender exclusion here, deliberately. An installer that whitelists
; its own directory from the system antivirus is indistinguishable from
; malware behaviour and erodes user trust, whatever the cold-start win.
; Cold-start cost is addressed the legitimate ways instead: precompiled
; bytecode (above) and background import prewarm in the app.
; AI Assistant runtime (task above). runasoriginaluser: Ollama installs per
; user, so an elevated run would install it into the admin's profile, not the
; user's. Visible console: the download takes minutes and prints progress.
Filename: "{app}\python\python.exe"; \
    Parameters: """{app}\windows\install_ai_assistant.py"""; \
    WorkingDir: "{app}"; StatusMsg: "Installing the eSim AI Assistant (large download)..."; \
    Tasks: aiassistant; Flags: runasoriginaluser waituntilterminated
; runasoriginaluser: the installer is elevated but eSim must run as the real
; user -- an elevated first run would write root-owned files into ~/.esim and
; the workspace that later non-elevated launches cannot touch.
Filename: "{app}\eSim.exe"; Description: "Launch eSim"; \
    Flags: postinstall nowait skipifsilent runasoriginaluser

[UninstallRun]
; NOTE: the per-user cleanup (KiCad sym-lib-table, ~\.esim, ~\.nghdl) is NOT
; here. It needs the user's answer to a prompt, and it must run as a specific
; account -- neither of which this section can do: `runasoriginaluser` is a
; [Run]-only flag ("Parameter Flags includes a flag that is not supported in
; this section"), and its [Code] twin refuses too ("Internal error: Cannot
; call EXECASORIGINALUSER function during Uninstall"). Both verified against
; Inno 6.3.3. See RunUserCleanup in [Code].
;
; Clean up the exclusion earlier installer versions added (current installer
; adds none). Harmless no-op when absent.
Filename: "powershell.exe"; RunOnceId: "RemoveEsimDefenderExclusion"; \
    Parameters: "-NoProfile -ExecutionPolicy Bypass -Command ""Remove-MpPreference -ExclusionPath '{app}' -ErrorAction SilentlyContinue"""; \
    Flags: runhidden

[UninstallDelete]
; Belt and braces for the biggest runtime-written trees. The [Code] sweep
; below removes ALL of {app}; these entries stay because they cost nothing and
; still fire on a tree the sweep declines to touch (marker files missing, e.g.
; someone deleted eSim.exe by hand before uninstalling).
;
; Compiled artifacts the app writes inside its own tree at runtime.
Type: filesandordirs; Name: "{app}\library\modelParamXML\Ngveri"
Type: filesandordirs; Name: "{app}\library\modelParamXML\NgVeriCosim"
Type: filesandordirs; Name: "{app}\library\modelParamXML\Nghdl"
; The nghdl tree accumulates user-built model sources and build objects
; (src\xspice\icm\{Ngveri,ghdl}\<model>, release tree .o) on top of the
; installed files; sweep the whole thing so an uninstall is clean.
Type: filesandordirs; Name: "{app}\tools\nghdl"
; Bundled KiCad writes caches inside its own tree at runtime (fp-info-cache,
; regenerated .pyc under bin\Lib); sweep it too.
Type: filesandordirs; Name: "{app}\tools\kicad"

; =============================================================================
; [Code] -- what the uninstall log alone cannot clean.
;
; Inno removes exactly what it installed. eSim adds to that tree AFTER the
; install log is written, so a plain uninstall used to leave the install
; folder standing with hundreds of files in it:
;
;   * __pycache__: the [Run] compileall above, plus every later launch,
;     writes .pyc for modules whose stage counterpart had none (windows\,
;     parts of python\Lib) -- unlogged, so never deleted.
;   * Examples\: simulating a bundled example writes beside it --
;     <name>.cir.out, analysis, plot_data_*.txt, *.raw, *_Previous_Values.xml,
;     <name>-cache.lib, -rescue.lib.
;   * library\SubcircuitLibrary, library\deviceModelLibrary: subcircuits and
;     device models the user adds land in the install tree.
;   * tools\nghdl, tools\kicad, library\modelParamXML: covered above.
;
; and per-user state the installer never created and cannot see:
;
;   * ~\.esim, ~\.nghdl (windows_bootstrap.py writes these on every launch)
;   * %APPDATA%\kicad\<ver>\sym-lib-table rows whose uri points INTO the tree
;     being deleted -- left behind, KiCad reports a missing library on every
;     schematic the user opens afterwards.
;
; So the uninstall gains two steps:
;   usUninstall     -- ask about the user's own data, then run
;                      windows\uninstall_cleanup.py while the bundled python
;                      is still on disk (nothing has been deleted yet).
;   usPostUninstall -- SweepDir removes whatever the log playback left, i.e.
;                      every file eSim wrote after installation, and a
;                      detached cmd takes the emptied folders afterwards.
;
; Safety: the sweep is a recursive delete of a user-chosen directory, so it
; runs only when {app} still carries an eSim marker file AND is not a system
; directory or a drive root AND this user's workspace is not inside it (a
; workspace under the install tree cancels the sweep outright -- leftover
; files are a nuisance, deleted schematics are not recoverable). Directory
; reparse points (junctions/symlinks) are unlinked, never followed. If
; anything is refused (eSim or KiCad still running, files open in a terminal)
; the user is told which folder to remove by hand rather than being left to
; discover it.
; =============================================================================
[Code]
var
  SweepWanted: Boolean;
  PurgeUserData: Boolean;

function NormDir(const Dir: String): String;
begin
  Result := Lowercase(RemoveBackslashUnlessRoot(Trim(Dir)));
end;

// True for anything a recursive delete must never be pointed at: a drive root
// and the well-known shared/system directories. Someone who installs eSim into
// a folder they also keep other things in still loses only that folder -- the
// marker check below is what guards against that, and the [Setup] default
// (SystemDrive\FOSSEE\eSim) is a dedicated one.
function IsProtectedDir(const Dir: String): Boolean;
var
  D: String;
  Guards: TArrayOfString;
  I: Integer;
begin
  D := NormDir(Dir);
  Result := True;
  if Length(D) <= 3 then Exit;                      // 'c:' / 'c:\'
  SetArrayLength(Guards, 10);
  Guards[0] := ExpandConstant('{win}');
  Guards[1] := ExpandConstant('{sys}');
  Guards[2] := ExpandConstant('{pf}');
  Guards[3] := ExpandConstant('{pf32}');
  Guards[4] := ExpandConstant('{commonpf}');
  Guards[5] := ExpandConstant('{commonappdata}');
  Guards[6] := ExpandConstant('{userappdata}');
  Guards[7] := ExpandConstant('{localappdata}');
  Guards[8] := ExpandConstant('{userdocs}');
  Guards[9] := ExpandConstant('{%USERPROFILE}');
  for I := 0 to GetArrayLength(Guards) - 1 do
    if (Guards[I] <> '') and (NormDir(Guards[I]) = D) then Exit;
  Result := False;
end;

// Is this really an eSim install root? Checked while the files are still
// there, i.e. at the start of usUninstall. unins000.dat counts: the running
// uninstaller lives in the app dir (UninstallFilesDir), so its presence means
// this directory is one Setup created.
function LooksLikeEsimInstall(const Dir: String): Boolean;
var
  D: String;
begin
  D := AddBackslash(Dir);
  Result := FileExists(D + 'eSim.exe') or FileExists(D + 'esim.bat') or
            FileExists(D + 'VERSION') or FileExists(D + 'unins000.dat');
end;

// eSim's workspace defaults to ~\eSim-Workspace, well outside the install
// tree -- but the picker lets the user put it anywhere, including inside the
// install folder. Sweeping then takes their schematics with it. Read the
// workspace this user chose (~\.esim\workspace.txt, "<check> <path>") and, if
// it is under the tree, refuse to sweep at all: leaving files behind is a
// nuisance, deleting someone's projects is not recoverable.
function WorkspaceInsideApp(const AppDir: String): Boolean;
var
  Raw: AnsiString;
  Line, WS: String;
  P: Integer;
begin
  Result := False;
  if not LoadStringFromFile(ExpandConstant('{%USERPROFILE}') +
                            '\.esim\workspace.txt', Raw) then Exit;
  Line := Trim(String(Raw));
  P := Pos(' ', Line);
  if P = 0 then Exit;
  WS := Trim(Copy(Line, P + 1, Length(Line)));
  if WS = '' then Exit;
  Result := CompareText(NormDir(Copy(WS, 1, Length(AppDir))),
                        NormDir(AppDir)) = 0;
end;

function AskPurgeUserData(): Boolean;
var
  Home: String;
begin
  if UninstallSilent then begin
    Result := False;                      { silent uninstall keeps user data }
    Exit;
  end;
  Home := ExpandConstant('{%USERPROFILE}');
  Result := MsgBox(
    'Remove eSim''s settings and saved models too?' #13#10 #13#10 +
    'Uninstalling removes the program, but eSim also keeps a little' #13#10 +
    'data in your user folder:' #13#10 #13#10 +
    '    - your preferences and workspace location' #13#10 +
    '    - any models you built yourself with NgVeri or NGHDL' #13#10 #13#10 +
    'Keep them  (No, recommended)' #13#10 +
    '    A few MB. If you ever install eSim again, it comes back set' #13#10 +
    '    up exactly as you left it.' #13#10 #13#10 +
    'Delete them  (Yes)' #13#10 +
    '    Choose this only if you want no trace of eSim left behind.' #13#10 +
    '    Models you built will be gone for good.' #13#10 #13#10 +
    'Your projects and your eSim workspace folder are NOT deleted' #13#10 +
    'either way.' #13#10 #13#10 +
    'The folders in question are ' + Home + '\.esim and ' + Home + '\.nghdl',
    mbConfirmation, MB_YESNO or MB_DEFBUTTON2) = IDYES;
end;

// The per-user half: unregister eSim's rows from the KiCad sym-lib-table
// (always -- they point into the tree that is about to go, and KiCad reports a
// missing library on every schematic opened afterwards if they stay), and
// delete ~\.esim + ~\.nghdl when the user said yes.
//
// This runs as the account performing the uninstall. Inno offers no way to be
// anyone else here: `runasoriginaluser` is a [Run]-only flag and
// ExecAsOriginalUser refuses during uninstall (both verified on 6.3.3). That
// account IS the user in the normal case (they elevate their own uninstall),
// and it is exactly the profile the prompt named. On a shared machine
// uninstalled by a DIFFERENT admin, every other user's ~\.esim and KiCad table
// are simply left alone -- untouched, never half-cleaned.
//
// Best effort -- an uninstall must not fail because a config file was
// read-only; the script itself never returns non-zero without --strict.
procedure RunUserCleanup(const AppDir: String);
var
  Py, Script, Params: String;
  ResultCode: Integer;
begin
  Py := AddBackslash(AppDir) + 'python\pythonw.exe';
  Script := AddBackslash(AppDir) + 'windows\uninstall_cleanup.py';
  if not (FileExists(Py) and FileExists(Script)) then Exit;
  Params := '"' + Script + '" --esim-root "' +
            RemoveBackslashUnlessRoot(AppDir) + '"';
  if PurgeUserData then Params := Params + ' --purge-user-data';
  Exec(Py, Params, AppDir, SW_HIDE, ewWaitUntilTerminated, ResultCode);
end;

// Delete everything in Dir except the running uninstaller. Returns the number
// of entries that refused to go.
function SweepDir(const Dir: String): Integer;
var
  FR: TFindRec;
  Base, P: String;
  IsDir, IsLink: Boolean;
begin
  Result := 0;
  Base := AddBackslash(Dir);
  if not FindFirst(Base + '*', FR) then Exit;
  try
    repeat
      if (FR.Name <> '.') and (FR.Name <> '..') and
         (Pos('unins', Lowercase(FR.Name)) <> 1) then begin
        P := Base + FR.Name;
        IsDir := (FR.Attributes and FILE_ATTRIBUTE_DIRECTORY) <> 0;
        IsLink := (FR.Attributes and FILE_ATTRIBUTE_REPARSE_POINT) <> 0;
        if IsDir and IsLink then begin
          // A junction/symlink: unlink it, NEVER recurse -- the target is
          // somewhere else on the disk and is not ours to delete.
          if not RemoveDir(P) then Result := Result + 1;
        end else if IsDir then begin
          if not DelTree(P, True, True, True) then Result := Result + 1;
        end else begin
          if not DeleteFile(P) then Result := Result + 1;
        end;
      end;
    until not FindNext(FR);
  finally
    FindClose(FR);
  end;
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
var
  AppDir, Parent, Params: String;
  Failures, ResultCode: Integer;
begin
  // Before anything is removed: decide (while the marker files still exist)
  // whether the tree may be swept, ask about the user's own data, and act on
  // that answer while the bundled python is still there.
  if CurUninstallStep = usUninstall then begin
    AppDir := RemoveBackslashUnlessRoot(ExpandConstant('{app}'));
    SweepWanted := DirExists(AppDir) and LooksLikeEsimInstall(AppDir) and
                   not IsProtectedDir(AppDir);
    if SweepWanted and WorkspaceInsideApp(AppDir) then begin
      SweepWanted := False;
      if not UninstallSilent then
        MsgBox('Your eSim workspace is inside' #13#10 #13#10 +
               AppDir + #13#10 #13#10 +
               'so the leftover files in that folder are NOT being removed --' #13#10 +
               'your projects are in there. Move them somewhere else, then' #13#10 +
               'delete the folder.', mbInformation, MB_OK);
    end;
    PurgeUserData := AskPurgeUserData();
    RunUserCleanup(AppDir);
  end;

  // After Inno has run the [UninstallRun] entries and deleted everything it
  // logged: whatever is left in the tree is what eSim wrote after install --
  // .pyc, simulation output beside the bundled Examples, subcircuits and
  // device models the user added, HDL build objects. Sweep it.
  if CurUninstallStep = usPostUninstall then begin
    if SweepWanted then begin
      AppDir := RemoveBackslashUnlessRoot(ExpandConstant('{app}'));
      Failures := SweepDir(AppDir);
      if (Failures > 0) and not UninstallSilent then
        MsgBox('Some files could not be removed from' #13#10 #13#10 +
               AppDir + #13#10 #13#10 +
               'They are most likely still open -- close eSim, KiCad and any' #13#10 +
               'terminal or Explorer window in that folder, then delete it.',
               mbInformation, MB_OK);
    end;
    // The app dir now holds only unins000.*, which Inno deletes as it exits --
    // after this code has run, so the empty folder (and the empty
    // SystemDrive\FOSSEE parent the default install created) would otherwise
    // stay. Hand both to a detached cmd that waits for the uninstaller to
    // finish and then rmdir's them. rmdir WITHOUT /s removes empty directories
    // only, so this can never take anything with it.
    if SweepWanted then begin
      AppDir := RemoveBackslashUnlessRoot(ExpandConstant('{app}'));
      Parent := ExtractFileDir(AppDir);
      Params := '/C ping -n 3 127.0.0.1 >nul & rmdir "' + AppDir + '"' +
                ' & ping -n 3 127.0.0.1 >nul & rmdir "' + AppDir + '"';
      if not IsProtectedDir(Parent) then
        Params := Params + ' & rmdir "' + Parent + '"';
      Exec(ExpandConstant('{cmd}'), Params, '', SW_HIDE, ewNoWait, ResultCode);
    end;
  end;
end;

// No KiCad detection anymore: KiCad ships inside this installer at
// tools\kicad (see the design notes at the top), so there is nothing to
// detect, offer or download after this exe finishes.
