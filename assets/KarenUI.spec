# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files

datas = [('hey_karen_en.ppn', '.'), ('hey_karen_es.ppn', '.'), ('你好美丽_zh.ppn', '.'), ('karenCirclePic.png', '.'), ('karenPic.jpeg', '.'), ('porcupine_params_es.pv', '.'), ('porcupine_params_zh.pv', '.'), ('voice_indicator.png', '.')]
datas += collect_data_files('pvporcupine')


a = Analysis(
    ['karen_ui.py'],
    pathex=[],
    binaries=[],
    datas=datas,
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
    name='KarenUI',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
