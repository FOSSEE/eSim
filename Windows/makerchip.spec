# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['makerchip\\__main__.py'],
             pathex=[],
             binaries=[],
             datas=[('makerchip/asset', 'asset'), ('makerchip/_vendor/native_web_app-1.0.2.dist-info/LICENSE', 'native_web_app-1.0.2.dist-info'), ('LICENSE.md', '.')],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
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
          name='makerchip',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
