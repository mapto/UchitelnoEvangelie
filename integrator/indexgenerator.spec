# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['indexgenerator.py'],
             pathex=[],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=['pandas', 'matplotlib', 'lib2to3', 'numpy', 'scipy', 'PIL', 'PyQt5'],
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
          name='indexgenerator',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          runtime_tmpdir=None,
          console=True, icon='indexgenerator.ico' )
