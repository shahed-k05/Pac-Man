# PyInstaller build specification for Pacman.
# Build from the project root with: pyinstaller pacman.spec

from pathlib import Path
from PyInstaller.utils.hooks import collect_all, collect_submodules

ROOT = Path(SPECPATH)

# Keep the existing relative paths used by the game.
datas = [
    (str(ROOT / "src" / "Graphics"), "src/Graphics"),
    (str(ROOT / "src" / "main"), "src/main"),
    (str(ROOT / "config.json"), "."),
    (str(ROOT / "highscore.json"), "."),
]

# Include the external A-Maze-ing package installed from the supplied wheel.
maze_datas, maze_binaries, maze_hiddenimports = collect_all("mazegenerator")
datas += maze_datas

hiddenimports = collect_submodules("mazegenerator")
hiddenimports += maze_hiddenimports

# Pygame discovers some of its modules dynamically.
hiddenimports += collect_submodules("pygame")

block_cipher = None

a = Analysis(
    [str(ROOT / "pac-man.py")],
    pathex=[str(ROOT)],
    binaries=maze_binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="Pacman",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
)
