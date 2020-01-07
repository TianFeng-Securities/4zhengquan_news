# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['get_news.py'],
             pathex=['C:\\Users\\Think\\Documents\\Python_test\\天风证券\\四大证券报项目\\zhengquan_news'],
             binaries=[],
             datas=[('resource','.')],
             hiddenimports=[],
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
          name='get_news',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True , icon='test.ico')
