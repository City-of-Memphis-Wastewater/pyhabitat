# pyhabitat.version_info.py
from __future__ import annotations # Delays annotation evaluation, allowing modern 3.10+ type syntax and forward references in older Python versions 3.8 and 3.9
import sys
from importlib.metadata import version, PackageNotFoundError
from pathlib import Path  

from .utils import get_version
from .system_info import SystemInfo

# -- Versioning --
PIP_PACKAGE_NAME = "pyhabitat"


def get_package_name() -> str:
    try:
        pyproject = Path(__file__).parent.parent / "pyproject.toml"
        content = pyproject.read_text(encoding="utf-8")
        match = re.search(r'^\s*name\s*=\s*["\']([^"\']+)["\']', content, re.MULTILINE)
        if match:
            return match.group(1)
    except Exception:
        pass
    return "pyhabitat"
    

try:
    __version__ = version(PIP_PACKAGE_NAME)

except PackageNotFoundError:
    # fallback if running from source
    try:
            with open(Path(__file__).parent / "VERSION") as f:
                __version__ = f.read().strip()
    except FileNotFoundError:
        __version__ = "dev" 

# --- Version Retrieval ---
def get_package_version() -> str:
    version = get_version()
        
    #print(f"Detected project version: {version}")
    return version


def get_python_version():
    py_major = sys.version_info.major
    py_minor = sys.version_info.minor
    py_version = f"py{py_major}{py_minor}"
    return py_version

def form_dynamic_binary_name(package_name: str, package_version: str, py_version: str, os_tag: str, arch: str) -> str:    
    # Use hyphens for the CLI/EXE/ELF name
    return f"{package_name}-{package_version}-{py_version}-{os_tag}-{arch}"

if __name__ == "__main__":
    package_name = get_package_name()
    package_version = get_package_version()
    py_version = get_python_version()
    
    sysinfo = SystemInfo()
    os_tag = sysinfo.get_os_tag()
    architecture = sysinfo.get_arch()

    bin_name = form_dynamic_binary_name(package_name, package_version, py_version, os_tag, architecture)
    print(f"bin_name = {bin_name}")