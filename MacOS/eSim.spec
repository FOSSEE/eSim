# -*- mode: python ; coding: utf-8 -*-
a = Analysis(
    ['src/frontEnd/Application.py'],
    pathex=['src/frontEnd'],                    # ← ADD: lets PyInstaller find macOSSetup
    binaries=[
        ('/usr/local/bin/ngspice', 'bin'),
        ('bundled_libs/libXaw.7.dylib',       'bin'),
        ('bundled_libs/libXmu.6.dylib',       'bin'),
        ('bundled_libs/libXt.6.dylib',        'bin'),
        ('bundled_libs/libXext.6.dylib',      'bin'),
        ('bundled_libs/libX11.6.dylib',       'bin'),
        ('bundled_libs/libXft.2.dylib',       'bin'),
        ('bundled_libs/libfontconfig.1.dylib','bin'),
        ('bundled_libs/libXrender.1.dylib',   'bin'),
        ('bundled_libs/libfreetype.6.dylib',  'bin'),
        ('bundled_libs/libSM.6.dylib',        'bin'),
        ('bundled_libs/libICE.6.dylib',       'bin'),
        ('bundled_libs/libXau.6.dylib',       'bin'),
        ('bundled_libs/libxcb.1.dylib',       'bin'),
        ('bundled_libs/libXpm.4.dylib',       'bin')
    ],
    datas=[
        ('images', 'images'),
        ('library', 'library'),
        ('Examples', 'Examples'),
        ('src', 'src'),
        ('nghdl', 'nghdl'),
        ('/usr/local/share/ngspice', 'share/ngspice'),
        ('/usr/local/lib/ngspice',   'lib/ngspice'),
        ('src/frontEnd/TerminalUi.ui', 'frontEnd'),
    ],
    hiddenimports=['macOSSetup', 'PyQt5.sip'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='eSim',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['eSimIcon.icns'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='eSim',
)
app = BUNDLE(
    coll,
    name='eSim.app',
    icon='eSimIcon.icns',
    bundle_identifier=None,
)