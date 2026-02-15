# src/pyhabitat/__init__.py
"""
pyhabitat: Lightweight introspection utilities for Python runtime, OS, build, and GUI environments.

Public API categories:
- Platform/OS detection: on_windows(), on_wsl(), on_termux(), ...
- Interactive/terminal checks: interactive_terminal_is_available(), is_likely_ci_or_non_interactive()
- GUI/backend availability: tkinter_is_available(), matplotlib_is_available_for_gui_plotting()
- Executable/file type checks: is_elf(), is_pyz(), is_pipx(), ...
- Launch helpers: edit_textfile(), show_system_explorer()
- High-level introspection: SystemInfo, report()
"""
from __future__ import annotations

from ._version import __version__

# Explicit public API — no star imports
# environment.py
from .environment import (
    on_termux,
    on_freebsd,
    on_linux,
    on_pydroid,
    on_android,
    on_windows,
    on_wsl,
    on_macos,
    on_ish_alpine,
    as_pyinstaller,
    as_frozen,
    is_msix,
    in_repl,
    interp_path,
    get_interp_shebang,
)

# console.py
from .console import (
    is_likely_ci_or_non_interactive,
    interactive_terminal_is_available,
    can_spawn_shell,
    user_darrin_deyoung,
    is_running_in_uvicorn,
    can_spawn_shell_lite,          # if you want it public (it's @cache'd helper)
)

# gui_elements.py
from .gui_elements import (
    matplotlib_is_available_for_gui_plotting,
    matplotlib_is_available_for_headless_image_export,
    tkinter_is_available,
    web_browser_is_available,
)

# file_character.py
from .file_character import (
    is_elf,
    is_pyz,
    is_windows_portable_executable,
    is_macos_executable,
    is_pipx,
    is_python_script,
    is_in_git_repo,
    read_magic_bytes,
    check_executable_path,
)

# system_info.py → assuming it exports SystemInfo
from .system_info import SystemInfo

# reporting.py → assuming it exports report
from .reporting import report

# launch.py
from .launch import (
    edit_textfile,
    show_system_explorer,
)

# Optional: lazy loading for heavier classes/functions (optional but nice)
def __getattr__(name: str):
    if name == "SystemInfo":
        from .system_info import SystemInfo
        globals()["SystemInfo"] = SystemInfo
        return SystemInfo
    if name == "report":
        from .reporting import report
        globals()["report"] = report
        return report
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

# Public API — exactly matches what we imported
__all__ = [
    "__version__",
    # environment
    "on_termux",
    "on_freebsd",
    "on_linux",
    "on_pydroid",
    "on_android",
    "on_windows",
    "on_wsl",
    "on_macos",
    "on_ish_alpine",
    "as_pyinstaller",
    "as_frozen",
    "is_msix",
    "in_repl",
    "interp_path",
    "get_interp_shebang",
    # console
    "is_likely_ci_or_non_interactive",
    "interactive_terminal_is_available",
    "can_spawn_shell",
    "user_darrin_deyoung",
    "is_running_in_uvicorn",
    "can_spawn_shell_lite",
    # gui_elements
    "matplotlib_is_available_for_gui_plotting",
    "matplotlib_is_available_for_headless_image_export",
    "tkinter_is_available",
    "web_browser_is_available",
    # file_character
    "is_elf",
    "is_pyz",
    "is_windows_portable_executable",
    "is_macos_executable",
    "is_pipx",
    "is_python_script",
    "is_in_git_repo",
    "read_magic_bytes",
    "check_executable_path",
    # system_info & reporting
    "SystemInfo",
    "report",
    # launch
    "edit_textfile",
    "show_system_explorer",
]
