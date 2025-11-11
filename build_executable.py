#!/usr/bin/env python3
"""
build_executable.py
Builds the PyHabitat standalone EXE using PyInstaller.
"""

import shutil
import subprocess
import sys
from pathlib import Path

# Config
exe_name = "pyhabitat-1.0.36-windows-amd64"
main_script = "__main__.py"
dist_dir = Path("dist")
build_dir = Path("build")

def clean():
    """Remove only the specific output EXE if it exists."""
    output_file = dist_dir / f"{exe_name}.exe"
    if output_file.exists():
        print(f"Removing old EXE: {output_file}")
        output_file.unlink()
    # Optionally remove the PyInstaller build folder, since it's temp
    if build_dir.exists():
        print(f"Removing build folder: {build_dir}")
        shutil.rmtree(build_dir)


def build_executable():
    """Run PyInstaller to build the EXE."""
    print(f"--- PyHabitat EXE Builder ---")
    clean()
    print(f"Building EXE: {exe_name}")

    pyinstaller_exe = Path(sys.executable).parent / "pyinstaller.exe"
    if not pyinstaller_exe.exists():
        raise SystemExit(f"PyInstaller not found at {pyinstaller_exe}. Install it in your venv.")

    cmd = [
        str(pyinstaller_exe),
        "--onefile",
        "--name",
        exe_name,
        main_script
    ]

    try:
        subprocess.run(cmd, check=True)
        print(f"Build complete! EXE is in {dist_dir}")
    except subprocess.CalledProcessError as e:
        print("Build failed!")
        print(e)
        raise

if __name__ == "__main__":
    build_executable()
