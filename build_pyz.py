#!/usr/bin/env python3
# ./build_pyz.py
from __future__ import annotations
import os
import sys
import subprocess
import shutil
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))
import pyhabitat

from pyhabitat.version_info import get_version_from_pyproject
from pyhabitat.environment import on_termux

# --- Configuration ---
PROJECT_NAME = "pyhabitat"
DIST_DIR = Path("dist") / "zipapp"
BUILD_ROOT = Path("pyhabitat-build")

def run_command(cmd, env=None):
    """Run command with printing and environment support."""
    print(f"\n$ {' '.join(cmd)}")
    # If no env provided, default to current os.environ
    final_env = env if env is not None else os.environ.copy()
    subprocess.run(cmd, check=True, env=final_env)

def get_custom_env():
    """Handles Fdroid Termux sandboxing by redirecting TMPDIR."""
    custom_env = os.environ.copy()
    if on_termux():
        termux_tmp = Path.home() / ".tmp"
        termux_tmp.mkdir(exist_ok=True)
        custom_env["TMPDIR"] = str(termux_tmp)
        print(f"Termux detected: Redirecting TMPDIR to {termux_tmp}")
    return custom_env

def run_build():
    print(f"--- PYZ Build (uv-powered) ---")
    
    # 1. Setup Directories
    if BUILD_ROOT.exists():
        shutil.rmtree(BUILD_ROOT)
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    
    custom_env = get_custom_env()

    # 2. Build the Wheel using uv
    # This automatically uses the pyproject.toml logic
    print("\n1. Building Project Wheel...")
    run_command(["uv", "build", "--wheel", "--out-dir", str(DIST_DIR)], env=custom_env)

    # 3. Find the wheel (using your existing find_latest logic style)
    wheels = sorted(DIST_DIR.glob(f"{PROJECT_NAME}-*.whl"), key=lambda f: f.stat().st_mtime, reverse=True)
    if not wheels:
        raise FileNotFoundError("No wheel found after build.")
    wheel_path = wheels[0]

    # 4. Stage the files into BUILD_ROOT
    # uv pip install --target is the fastest way to expand a wheel for zipapp
    print(f"\n2. Staging wheel: {wheel_path.name}")
    run_command([
        "uv", "pip", "install", 
        str(wheel_path), 
        "--target", str(BUILD_ROOT),
        "--no-deps"
    ], env=custom_env)

    # 5. Build the PYZ
    # We use the standard zipapp module
    output_pyz = DIST_DIR / f"{wheel_path.stem}.pyz"
    print(f"\n3. Packaging ZipApp: {output_pyz.name}")

    # 1. Get the version from the source TOML
    version = get_version_from_pyproject()

    internal_pkg_dir = BUILD_ROOT / "pyhabitat"
    internal_pkg_dir.mkdir(parents=True, exist_ok=True) # Defensive check

    # 2. "Stamp" the build directory so the PYZ carries its identity
    version_file = internal_pkg_dir / "VERSION"
    version_file.write_text(version, encoding="utf-8")
    
    run_command([
        sys.executable, "-m", "zipapp",
        str(BUILD_ROOT),
        "-o", str(output_pyz),
        "-m", "pyhabitat.cli:run_cli", # Matches [project.scripts]
        "-p", "/usr/bin/env python3"
    ])

    # 6. Finalize
    output_pyz.chmod(0o755)
    # Optional: Keep build_root for debugging or delete it
    shutil.rmtree(BUILD_ROOT)
    
    print(f"\n✅ Build successful! Portable PYZ: {output_pyz.resolve()}")

if __name__ == "__main__":
    run_build()