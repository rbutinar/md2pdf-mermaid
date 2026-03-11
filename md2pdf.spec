# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for md2pdf-mermaid standalone executable.

Build with: pyinstaller md2pdf.spec --clean
"""

import sys
from PyInstaller.utils.hooks import collect_all, collect_submodules

block_cipher = None

# Collect all playwright data files (driver, node.js runtime)
playwright_datas, playwright_binaries, playwright_hiddenimports = collect_all('playwright')

# Collect markdown extensions
markdown_hiddenimports = collect_submodules('markdown')

a = Analysis(
    ['md2pdf/__main__.py'],
    pathex=[],
    binaries=playwright_binaries,
    datas=playwright_datas,
    hiddenimports=[
        'md2pdf',
        'md2pdf.cli',
        'md2pdf.converter',
        'md2pdf.html_renderer',
        'md2pdf.mermaid',
        'md2pdf.emoji_handler',
        'md2pdf.browser_manager',
        'reportlab',
        'reportlab.lib',
        'reportlab.lib.colors',
        'reportlab.lib.pagesizes',
        'reportlab.lib.units',
        'reportlab.lib.styles',
        'reportlab.platypus',
        'reportlab.pdfgen',
        'reportlab.pdfbase',
        'reportlab.pdfbase.ttfonts',
        'reportlab.pdfbase.pdfmetrics',
        'PIL',
        'PIL.Image',
    ] + markdown_hiddenimports + playwright_hiddenimports,
    hookspath=[],
    hooksconfig={},
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
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='md2pdf',
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
