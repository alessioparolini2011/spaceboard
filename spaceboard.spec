# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['src/spaceboard/main.py'],
    pathex=[],
    binaries=[],
    datas=[('src/spaceboard/tcss/', 'spaceboard/tcss')], 
    hiddenimports=['textual', 'httpx'], 
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='spaceboard',
    console=True,          
    icon='assets/spaceboard.ico'        
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    name='spaceboard', 
)
