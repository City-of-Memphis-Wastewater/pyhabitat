# pyhabitat.version_info.py
from __future__ import annotations # Delays annotation evaluation, allowing modern 3.10+ type syntax and forward references in older Python versions 3.8 and 3.9
import sys
from importlib.metadata import version, PackageNotFoundError
from pathlib import Path  
import re

from .system_info import SystemInfo

# -- Versioning --
PIP_PACKAGE_NAME = "pyhabitat"
# Auto-detected at build time (fallback)
FALLBACK_VERSION = "dev"


def _running_inside_pyinstaller() -> bool:
    return hasattr(sys, "_MEIPASS")

def _read_embedded_version() -> str | None:
    # Check PyInstaller runtime
    if _running_inside_pyinstaller():
        base = Path(sys._MEIPASS)  # temp folder where PyInstaller unpacks files
    else:
        base = Path(__file__).parent

    try:
        return (base / "VERSION").read_text().strip()
    except Exception:
        return None


def find_pyproject(start: Path) -> Path | None:
    for p in start.resolve().parents:
        candidate = p / "pyproject.toml"
        if candidate.exists():
            return candidate
    return None

def get_package_name() -> str:
    try:
        pyproject = find_pyproject(Path(__file__))
        content = pyproject.read_text(encoding="utf-8")
        match = re.search(r'^\s*name\s*=\s*["\']([^"\']+)["\']', content, re.MULTILINE)
        if match:
            return match.group(1)
    except Exception:
        pass
    return "pyhabitat"


def get_version_for_build() -> str:
    return get_version_from_pyproject()

def get_version_from_pyproject() -> str:
    """
    Read the version from pyproject.toml without external dependencies.
    Handles both Poetry and PEP-621 formats:
        version = "0.1.0"
        [project]
        version = "0.1.0"
    """
    pyproject = find_pyproject(Path(__file__))
    

    if not pyproject or not pyproject.exists():
        return "Unknown (pyproject.toml missing)"

    text = pyproject.read_text(encoding="utf-8")
    #print(text)
    # 1. Match PEP 621 style:
    #    version = "0.1.0" inside a [project] table
    project_section = re.search(
        r"\[project\](.*?)(?:\n\[|$)",
        text,
        re.DOTALL | re.IGNORECASE,
    )
    if project_section:
        match = re.search(
            r'version\s*=\s*["\']([^"\']+)["\']',
            project_section.group(1),
        )
        if match:
            return match.group(1)

    # 2. Match Poetry style:
    #    [tool.poetry]
    #    version = "0.1.0"
    poetry_section = re.search(
        r"\[tool\.poetry\](.*?)(?:\n\[|$)",
        text,
        re.DOTALL | re.IGNORECASE,
    )
    if poetry_section:
        match = re.search(
            r'version\s*=\s*["\']([^"\']+)["\']',
            poetry_section.group(1),
        )
        if match:
            return match.group(1)

    # fallback
    return "Unknown (version not found)"

def get_package_version() -> str:
    """
    Correct priority:
    
    1. embedded VERSION file (inside .pyz)
    2. pyproject.toml (local source)
    3. installed package metadata (pip)
    4. fallback
    """

     # 1. Running inside a binary / .pyz
    v = _read_embedded_version()
    if v:
        return v

    # 2. Local source tree → pyproject.toml
    v = get_version_from_pyproject()
    if v and not v.startswith("Unknown"):
        return v

    # 3. Installed package
    try:
        return version(PIP_PACKAGE_NAME)
    except PackageNotFoundError:
        pass

    # 4. Default
    return FALLBACK_VERSION


def get_python_version():
    py_major = sys.version_info.major
    py_minor = sys.version_info.minor
    py_version = f"py{py_major}{py_minor}"
    return py_version

def form_dynamic_binary_name(package_name: str, package_version: str, py_version: str, os_tag: str, arch: str) -> str:    
    # Use hyphens for the CLI/EXE/ELF name
    return f"{package_name}-{package_version}-{py_version}-{os_tag}-{arch}"

__version__ = get_package_version()

if __name__ == "__main__":
    package_name = get_package_name()
    package_version = get_package_version()
    py_version = get_python_version()
    
    sysinfo = SystemInfo()
    os_tag = sysinfo.get_os_tag()
    architecture = sysinfo.get_arch()

    bin_name = form_dynamic_binary_name(package_name, package_version, py_version, os_tag, architecture)
    print(f"bin_name = {bin_name}")