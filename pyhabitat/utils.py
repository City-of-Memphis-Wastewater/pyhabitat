# ./utils.py
from __future__ import annotations 
import re
from pathlib import Path
from importlib.metadata import version, PackageNotFoundError


def get_version_from_pyproject() -> str:
    """
    Read the version from pyproject.toml without external dependencies.
    Handles both Poetry and PEP-621 formats:
        version = "0.1.0"
        [project]
        version = "0.1.0"
    """
    pyproject = Path(__file__).parent.parent / "pyproject.toml"

    if not pyproject.exists():
        return "Unknown (pyproject.toml missing)"

    text = pyproject.read_text(encoding="utf-8")

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

