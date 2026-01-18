# -*- mode: python ; coding: utf-8 -*-

"""
PyInstaller spec file for building the macOS application bundle.

Run with:
  pyinstaller build/pyinstaller_mac.spec

The resulting bundle (Kabu-Kansoku.app) will be placed in the dist/
directory. Note that you must run this on macOS; cross‑compiling from
Windows or Linux to macOS is not supported by PyInstaller.
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
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

app = BUNDLE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Kabu-Kansoku',
    icon=None,
    bundle_identifier='com.example.kabukansoku',
)

coll = COLLECT(
    app,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name='Kabu-Kansoku'
)