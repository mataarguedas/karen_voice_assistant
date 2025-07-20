# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files

datas = [('assets/hey_karen_en.ppn', 'assets'), ('assets/hey_karen_es.ppn', 'assets'), ('assets/ni_hao_mei_li_zh.ppn', 'assets'), ('assets/karenCirclePic.png', 'assets'), ('assets/karenPic.jpeg', 'assets'), ('assets/porcupine_params_es.pv', 'assets'), ('assets/porcupine_params_zh.pv', 'assets'), ('assets/voice_indicator.png', '.')]
datas += collect_data_files('pvporcupine')


a = Analysis(
    ['main.py'],
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
    name='Karen',
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
