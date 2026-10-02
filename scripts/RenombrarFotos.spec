# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['renombrarfotos.py'],
    pathex=['src'],
    binaries=[],
    datas=[],
    hiddenimports=[
        'renombrar',
        'renombrar.main',
        'renombrar.core',
        'renombrar.core.file_utils',
        'renombrar.core.date_utils',
        'renombrar.core.extractor_metadatos',
        'renombrar.core.procesador_archivos',
        'renombrar.ui',
        'renombrar.ui.menu',
        'renombrar.ui.menu_criterio',
        'PIL',
        'pillow_heif',
        'mutagen',
        'hachoir'
    ],
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
    name='RenombrarFotos',
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
