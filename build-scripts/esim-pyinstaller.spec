a = Analysis(['../src/frontEnd/Application.py'],
             pathex = [ '../src' ],
             binaries = None,
             datas = [ ('../Examples', 'Examples'),
                       ('../kicadSchematicLibrary', 'kicadSchematicLibrary'),
                       ('../res', 'res'),
                       ('../LICENSE', '.') ],
             hiddenimports = ['packaging.requirements', 'packaging.specifiers'],
             hookspath = None,
             runtime_hooks = None,
             excludes = [],
             cipher = None)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='esim',
          debug=False,
          strip=False,
          upx=True,
          console=True )

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='esim')
