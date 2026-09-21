# src/pyhabitat/webcheck.py
from __future__ import annotations
import os
import webbrowser
import shutil
from .environment import (
    on_termux, 
    on_linux,
    on_windows,
    on_macos,
    on_wsl,
)
def web_browser_is_available() -> bool:
    """Check if a web browser can be launched in the current environment."""
    # 1. Termux on Android
    if on_termux() and shutil.which("termux-open-url"):
        return True

    # 2. WSL / Windows Edge bridge
    if on_wsl() and (shutil.which("microsoft-edge") or shutil.which("wslview")):
        return True

    # 3. Linux Desktop GUI launcher
    if on_linux() and shutil.which("xdg-open"):
        return True

    # 4. macOS launcher
    if on_macos() and shutil.which("open"):
        return True

    # 5. Windows native launcher
    if on_windows() and shutil.which("cmd"):
        return True

    # 6. Fallback to standard Python webbrowser registry
    try:
        browser = webbrowser.get()
        return browser is not None
    except (webbrowser.Error, Exception):
        return False
