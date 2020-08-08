# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(['eSim-2.0/src/frontEnd/Application.py'],
             pathex=['/home/rahul/Music'],
             binaries=[],
             datas=[],
             hiddenimports=['PyQt4.sip'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='eSim',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True,
          version='eSim-2.0/VERSION',
          icon='eSim-2.0/images/logo.png')
