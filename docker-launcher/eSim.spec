# PyInstaller spec file for eSim Docker Launcher
# Build: pyinstaller eSim.spec

block_cipher = None

a = Analysis(
    ['run_esim_docker.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['socket', 'webbrowser', 'threading', 'tempfile', 'argparse'],
    hookspath=[],
    runtime_hooks=[],
    excludes=['tkinter', 'matplotlib', 'numpy', 'scipy', 'PIL', 'pandas', 'pytest'],
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='eSim-Launcher',
    debug=False,
    strip=False,
    upx=True,
    console=True,  # Keep console for menu
    icon='esim_logo.png' if __import__('os').path.exists('esim_logo.png') else None,
)
