# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['karen.py'],
    pathex=[],
    binaries=[],
    datas=[('Hey_Karen_EN.ppn', '.'), ('Hey_Karen_ES.ppn', '.'), ('porcupine_params_es.pv', '.'), ('venv\\Lib\\site-packages\\pvporcupine\\resources', 'pvporcupine\\resources'), ('venv\\Lib\\site-packages\\pvporcupine\\lib', 'pvporcupine\\lib')],
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
    a.binaries,
    a.datas,
    [],
    name='karen',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
