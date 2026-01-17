#!/usr/bin/env python3
# ./build_executable.py
"""
build_executable.py
Builds the PyHabitat standalone EXE using PyInstaller.
"""
from __future__ import annotations
import shutil
import subprocess
import sys
from pathlib import Path

from pyhabitat.version_info import get_package_name, get_package_version, get_version_for_build, get_python_version, form_dynamic_binary_name
from pyhabitat.system_info import SystemInfo
from pyhabitat.environment import on_windows

# --- Config ---

MAIN_SCRIPT = "src/pyhabitat/__main__.py"
DIST_DIR = Path("dist") / "onefile"
BUILD_DIR= Path("build")
BUILD_ASSETS_DIR = Path("build_assets")
VERSION_FILE = BUILD_DIR/ "VERSION"  # Move the temp VERSION file into build/ folder

if BUILD_DIR.exists():
    print(f"Removing build folder: {BUILD_DIR}")
    shutil.rmtree(BUILD_DIR)
BUILD_DIR.mkdir(parents=True, exist_ok=True)
DIST_DIR.mkdir(parents=True, exist_ok=True) 
VERSION_FILE.write_text(get_version_for_build(), encoding="utf-8")

def clean_build_folder():
    """Remove build folder after completion"""
    if BUILD_DIR.exists():
        print(f"Removing build folder: {BUILD_DIR}")
        shutil.rmtree(BUILD_DIR)


def run_pyinstaller(exe_name):
    """Run PyInstaller to build the executable."""
    print(f"--- PyHabitat executable Builder --")
    
    print(f"Building executable: {exe_name}")

    pyinstaller_exe = Path(sys.executable).parent / ("pyinstaller.exe" if sys.platform.startswith("win") else "pyinstaller")

    if not pyinstaller_exe.exists():
        raise SystemExit(f"PyInstaller not found at {pyinstaller_exe}. Install it in venv.")

    # Define modules to exclude for smaller binary size.
    exclusions = [
        "tkinter",
        "matplotlib",
        # Add other standard library modules PyHabitat checks but doesn't need to run itself
    ]
    
    exclusion_flags = [f"--exclude-module={mod}" for mod in exclusions] # CHANGED <-------------------------

    # Use the --specpath argument to move the .spec file output to the build folder.
    specpath_flag = ["--specpath", str(BUILD_DIR)] # CHANGED <-------------------------

    # Ensure the build directory exists before PyInstaller is run and spec file is written.
    BUILD_DIR.mkdir(parents=True, exist_ok=True) # CHANGED <-------------------------

    cmd = [
        str(pyinstaller_exe),
        "--onefile",
        "--name",exe_name,
        "--distpath", str(DIST_DIR),  
        "--paths", "src",  # Critical: Tells PyInstaller to look in src/
        f"--add-data={VERSION_FILE.resolve()}:.",
        *specpath_flag,
        *exclusion_flags,
        MAIN_SCRIPT
    ]

    # 2. Windows-Specific Resource Logic
    if on_windows():

        rc_file = prepare_windows_version_info(get_version_for_build())
        if rc_file:
            # Tell PyInstaller to use this version info
            cmd += ["--version-file", str(rc_file)]
            
        # If you have an icon, you'd add it here
        icon_file = "assets/pyhabitat-ico-alpha_256x256.ico"
        if Path(icon_file).exists():
            cmd += ["--icon", icon_file]
        
        # If you want to use that .rc template to stamp the EXE:
        rc_path = BUILD_ASSETS_DIR / "version.rc.template"
        if rc_path.exists():
            # Note: You usually need to 'render' the template with the real version 
            # or use a tool like 'pyi-set-version' if you want it automated.
            # For now, we just ensure the path is correct if referenced.
            pass

    try:
        subprocess.run(cmd, check=True)
        print(f"Build complete! EXE is in {DIST_DIR}")
        print(f"Spec file is in: {BUILD_DIR}")
    except subprocess.CalledProcessError as e:
        print("Build failed!")
        print(e)
        raise
    

def prepare_windows_version_info(version_str):
    """
    Renders the version.rc.template with the actual version and 
    saves it to the build directory.
    """
    template_path = BUILD_ASSETS_DIR / "version.rc.template"
    if not template_path.exists():
        return None

    # Logic to split "1.1.9" into (1, 1, 9, 0) for Windows file versioning
    parts = version_str.split('.')
    while len(parts) < 4:
        parts.append('0')
    win_version = ", ".join(parts)

    content = template_path.read_text()
    # Assuming template has a placeholder like {{VERSION_TUPLE}}
    content = content.replace("{{VERSION_TUPLE}}", win_version)
    content = content.replace("{{VERSION_STR}}", version_str)

    out_rc = BUILD_DIR / "version.rc"
    out_rc.write_text(content)
    return out_rc

if __name__ == "__main__":
    package_name = get_package_name()
    package_version = get_version_for_build()
    py_version = get_python_version()

    sysinfo = SystemInfo()
    os_tag = sysinfo.get_os_tag()
    architecture = sysinfo.get_arch()
    executable_descriptor = form_dynamic_binary_name(package_name, package_version, py_version, os_tag, architecture)
    run_pyinstaller(exe_name = executable_descriptor)
    clean_build_folder()
