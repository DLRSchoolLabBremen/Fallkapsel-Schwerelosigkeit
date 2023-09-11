# -*- mode: python ; coding: utf-8 -*-
import subprocess
import re
from io import StringIO

command = "pip show customtkinter"
process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
output, error = process.communicate()
ctk_location = re.search(r'Location:\s+(.*)', str(output.decode("utf-8"))).group(1)

block_cipher = None


a = Analysis(
    ['__main__'],
    pathex=[],
    binaries=[],
    datas=[(ctk_location + '\\customtkinter', 'customtkinter\\')],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Fallkapselserver',
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
