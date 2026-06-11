# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['app_windows\\control_center_app.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\Python314\\tcl\\tcl8.6', '_tcl_data'), ('C:\\Python314\\tcl\\tk8.6', '_tk_data'), ('C:\\Python314\\tcl\\tcl8.6', 'tcl'), ('C:\\Python314\\tcl\\tk8.6', 'tk')],
    hiddenimports=[],
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
    name='AI-Bridge-Local-Control-Center',
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
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='AI-Bridge-Local-Control-Center',
)
