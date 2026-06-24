# src/pyhabitat/__init__.py

from __future__ import annotations

from ._version import __version__

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
    "on_chromeos_crostini",
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
    "safe_notify",

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

    # system_info
    "SystemInfo",

    # reporting
    "report",

    # launch
    "edit_textfile",
    "show_system_explorer",
    "serve_directory",
]


_ENVIRONMENT_EXPORTS = {
    "on_termux",
    "on_freebsd",
    "on_linux",
    "on_pydroid",
    "on_android",
    "on_windows",
    "on_wsl",
    "on_macos",
    "on_chromeos_crostini",
    "on_ish_alpine",
    "as_pyinstaller",
    "as_frozen",
    "is_msix",
    "in_repl",
    "interp_path",
    "get_interp_shebang",
}

_CONSOLE_EXPORTS = {
    "is_likely_ci_or_non_interactive",
    "interactive_terminal_is_available",
    "can_spawn_shell",
    "user_darrin_deyoung",
    "is_running_in_uvicorn",
    "can_spawn_shell_lite",
    "safe_notify",
}

_GUI_EXPORTS = {
    "matplotlib_is_available_for_gui_plotting",
    "matplotlib_is_available_for_headless_image_export",
    "tkinter_is_available",
    "web_browser_is_available",
}

_FILE_CHARACTER_EXPORTS = {
    "is_elf",
    "is_pyz",
    "is_windows_portable_executable",
    "is_macos_executable",
    "is_pipx",
    "is_python_script",
    "is_in_git_repo",
    "read_magic_bytes",
    "check_executable_path",
}

_LAUNCH_EXPORTS = {
    "edit_textfile",
    "show_system_explorer",
    "serve_directory",
}


def __getattr__(name: str):

    if name in _ENVIRONMENT_EXPORTS:
        from . import environment
        value = getattr(environment, name)

    elif name in _CONSOLE_EXPORTS:
        from . import console
        value = getattr(console, name)

    elif name in _GUI_EXPORTS:
        from . import gui_elements
        value = getattr(gui_elements, name)

    elif name in _FILE_CHARACTER_EXPORTS:
        from . import file_character
        value = getattr(file_character, name)

    elif name == "SystemInfo":
        from .system_info import SystemInfo
        value = SystemInfo

    elif name == "report":
        from .reporting import report
        value = report

    elif name in _LAUNCH_EXPORTS:
        from . import launch
        value = getattr(launch, name)

    else:
        raise AttributeError(
            f"module {__name__!r} has no attribute {name!r}"
        )

    # Cache resolved attribute for future lookups
    globals()[name] = value

    return value


def __dir__():
    return sorted(
        __all__ + [
            "__all__",
            "__builtins__",
            "__cached__",
            "__doc__",
            "__file__",
            "__getattr__",
            "__loader__",
            "__name__",
            "__package__",
            "__path__",
            "__spec__",
        ]
    )
