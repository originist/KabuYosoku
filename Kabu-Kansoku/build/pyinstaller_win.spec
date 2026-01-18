# -*- mode: python ; coding: utf-8 -*-

"""
PyInstaller spec file for building the Windows executable.

Run with:
  pyinstaller build/pyinstaller_win.spec

This spec assumes that the entry point is src/main.py and includes
all application packages under the src/ directory. The generated
executable will be named "Kabu-Kansoku.exe" and placed in the
dist/ directory.
"""

import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root / "src"))

block_cipher = None

a = Analysis(
    [str(project_root / "src" / "main.py")],
    pathex=[str(project_root / "src")],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Kabu-Kansoku',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name='Kabu-Kansoku'
)