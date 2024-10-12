# -*- mode: python ; coding: utf-8 -*-
import sys
import os

block_cipher = None


spec_dir = os.path.dirname(os.path.abspath(SPEC))
models_dir = os.path.join(spec_dir, 'exo', 'inference', 'mlx', 'models')
model_files = []

# Automatically look through exo/inference/models/* for the dynamically imported inference engines
for root, dirs, files in os.walk(models_dir):
    for file in files:
        if file.endswith('.py') and file not in ['__init__.py', 'base.py']:
            model_files.append(os.path.join(root, file))

model_imports = [
    f"exo.inference.mlx.models.{os.path.basename(f)[:-3]}"
    for f in model_files
    if '__pycache__' not in f
]

print("Model imports:", model_imports)

a = Analysis(
    ['exo/main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('exo/tinychat', 'exo/tinychat'),
        ('exo', 'exo'),
    ],
    hiddenimports=[
        'transformers',
        'safetensors',
        'exo',
    ] + model_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Add mlx for macOS
if sys.platform.startswith('darwin'):
    a.datas += Tree('venv/lib/python3.12/site-packages/mlx', prefix='mlx')
    a.hiddenimports.extend(['mlx', 'mlx.core', 'mlx.nn', 'mlx._reprlib_fix'])

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='exo',
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
