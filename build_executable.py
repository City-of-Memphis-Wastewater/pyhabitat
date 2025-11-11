# build_executable.py
"""
Cross-platform PyHabitat EXE builder using PyInstaller.
- Extracts version from pyhabitat.utils
- Cleans old builds
- Builds single-file EXE
- Works on Windows, Linux, macOS
"""

import sys
import subprocess
import shutil
from pathlib import Path

# Constants
DIST_DIR = Path("dist")
BUILD_DIR = Path("build")
ENTRY_SCRIPT = Path("__main__.py")  # top-level entry
PYINSTALLER_NAME = "pyinstaller"  # should be in venv

def get_version() -> str:
    """Extract version from pyhabitat.utils"""
    try:
        result = subprocess.run(
            [sys.executable, "-c", "from pyhabitat.utils import get_version; print(get_version())"],
            capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return "0.0.0"

def clean_dirs():
    """Remove old build/dist directories."""
    for path in (DIST_DIR, BUILD_DIR):
        if path.exists():
            print(f"Removing {path}...")
            shutil.rmtree(path)

def build_executable():
    """Run PyInstaller to build single-file EXE."""
    version = get_version()
    output_name = f"pyhabitat-{version}-windows-amd64" if sys.platform.startswith("win") else f"pyhabitat-{version}"
    
    cmd = [
        sys.executable,
        "-m",
        PYINSTALLER_NAME,
        "--onefile",
        "--name", output_name,
        str(ENTRY_SCRIPT)
    ]
    
    print(f"Building EXE: {output_name}")
    subprocess.run(cmd, check=True)
    
    print(f"\n✅ Build complete! Find it in: {DIST_DIR}")

if __name__ == "__main__":
    print("--- PyHabitat EXE Builder ---")
    clean_dirs()
    build_executable()
