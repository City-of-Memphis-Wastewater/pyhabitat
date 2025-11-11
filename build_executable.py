#!/usr/bin/env python3
"""
build_executable.py
Builds the PyHabitat standalone EXE using PyInstaller.
"""

import shutil
import subprocess
import sys
from pathlib import Path

from pyhabitat.utils import get_version
from pyhabitat.version_info import get_package_name, get_package_version, get_python_version, form_dynamic_binary_name
from pyhabitat.system_info import SystemInfo

# Config

VERSION = get_version()


main_script = "__main__.py"
dist_dir = Path("dist")
build_dir = Path("build")

def clean(exe_name):
    """Remove only the specific output executable if it exists."""
    output_file = dist_dir / exe_name

    if output_file.exists():
        print(f"Removing old executable: {output_file}")
        output_file.unlink()
    # Optionally remove the PyInstaller build folder, since it's temp
    if build_dir.exists():
        print(f"Removing build folder: {build_dir}")
        shutil.rmtree(build_dir)


def run_pyinstaller(exe_name):
    """Run PyInstaller to build the executable."""
    print(f"--- PyHabitat executable Builder --")
    clean(exe_name = exe_name)
    print(f"Building executable: {exe_name}")

    pyinstaller_exe = Path(sys.executable).parent / ("pyinstaller.exe" if sys.platform.startswith("win") else "pyinstaller")

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
    package_name = get_package_name()
    package_version = get_package_version()
    py_version = get_python_version()

    sysinfo = SystemInfo()
    os_tag = sysinfo.get_os_tag()
    architecture = sysinfo.get_arch()
    executable_descriptor = form_dynamic_binary_name(package_name, package_version, py_version, os_tag, architecture)
    run_pyinstaller(exe_name = executable_descriptor)
