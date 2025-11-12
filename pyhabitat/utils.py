# ./utils.py
from importlib.metadata import version, PackageNotFoundError
def get_version_defunct() -> str:
    """Retrieves the installed package version."""
    try:
        # The package name 'pyhabitat' must exactly match the name in your pyproject.toml
        return version('pyhabitat')
    except PackageNotFoundError:
        # This occurs if the script is run directly from the source directory
        # without being installed in editable mode, or if the package name is wrong.
        return "Not Installed (Local Development or Incorrect Name)"
import re
from pathlib import Path

def get_version():
    try:
        pyproject = Path(__file__).parent.parent / "pyproject.toml"
        content = pyproject.read_text(encoding="utf-8")
        match = re.search(r'^version\s*=\s*["\']([^"\']+)["\']', content, re.MULTILINE)
        if match:
            return match.group(1)
    except Exception:
        pass
    return "Not Installed (Local Development or Incorrect Name)"

