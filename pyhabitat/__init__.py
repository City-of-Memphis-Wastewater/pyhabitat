# pyhabitat/__init__.py

from .environment import (
    is_termux, 
    is_windows, 
    is_pipx,
    matplotlib_is_available_for_gui_plotting,
    # Add all key functions here
)

# Optional: Set __all__ for explicit imports
__all__ = [
    'is_termux',
    'is_windows',
    'is_pipx',
    'matplotlib_is_available_for_gui_plotting',
]