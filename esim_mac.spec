# -*- mode: python ; coding: utf-8 -*-

import os
import sys

block_cipher = None

# Base path of the repository
base_dir = os.path.abspath(os.getcwd())

a = Analysis(
    ['src/frontEnd/Application.py'],
    pathex=[os.path.join(base_dir, 'src')],
    binaries=[],
    datas=[
        ('library', 'library'),
        ('images', 'images'),
        ('VERSION', '.'),
    ],
    hiddenimports=[
        'frontEnd',
        'frontEnd.pathmagic',
        'frontEnd.ProjectExplorer',
        'frontEnd.Workspace',
        'frontEnd.DockArea',
        'projManagement',
        'projManagement.openProject',
        'projManagement.newProject',
        'projManagement.Kicad',
        'projManagement.Validation',
        'projManagement.Worker',
        'kicadtoNgspice',
        'kicadtoNgspice.DeviceModel',
        'kicadtoNgspice.Processing',
        'kicadtoNgspice.SubcircuitTab',
        'maker',
        'maker.Maker',
        'maker.ModelGeneration',
        'maker.NgVeri',
        'ngspiceSimulation',
        'ngspiceSimulation.NgspiceWidget',
        'browser',
        'browser.Welcome',
        'browser.UserManual',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

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
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='eSim',
)

app = BUNDLE(
    coll,
    name='eSim.app',
    icon=os.path.join(base_dir, 'images', 'logo.icns'),
    bundle_identifier='org.fossee.esim',
    info_plist={
        'NSPrincipalClass': 'NSApplication',
        'NSAppleScriptEnabled': False,
        'CFBundleDocumentTypes': [],
    },
)
