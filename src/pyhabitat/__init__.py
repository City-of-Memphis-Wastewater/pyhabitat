# src/pyhabitat/__init__.py
from __future__ import annotations
from .version_info import get_package_version as version
from .system_info import SystemInfo
from .reporting import report
from .environment import (
    matplotlib_is_available_for_gui_plotting,
    matplotlib_is_available_for_headless_image_export,
    tkinter_is_available,
    in_repl,
    on_freebsd,
    on_linux,
    on_android,
    on_windows,
    on_wsl,
    on_apple,
    on_termux,
    on_pydroid,
    on_ish_alpine,
    as_pyinstaller,
    as_frozen,
    is_elf,
    is_pyz,
    is_windows_portable_executable,
    is_msix,
    is_macos_executable,
    is_pipx,
    is_python_script,
    interactive_terminal_is_available,
    web_browser_is_available,
    edit_textfile,
    show_system_explorer,
    interp_path,
    main,
    user_darrin_deyoung,
    can_spawn_shell,
    is_ascii,
    is_binary,
    is_running_in_uvicorn
)
"""
Detect whether Python is running inside WSL, Docker, CI, or mobile environments.
"""
from .platform import *
from .runtime import *
from .packaging import *

__all__ = []
for module in (
    globals()['platform'], 
    globals()['runtime'], 
    globals()['packaging']):
    __all__.extend(module.__all__)

# Dynamically re-export everything environment declares in its __all__
__all__ = [
    'version',
    'SystemInfo',
    'report',
] + environment.__all__

__version__ = version()
