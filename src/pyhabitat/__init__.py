# src/pyhabitat/__init__.py
from __future__ import annotations

from ._version import __version__
 

__all__ = [
    '__version__',
    'SystemInfo',
    'report',
]
def __getattr__(name):
    if name == "report":
        from .reporting import report
        return report
    
    if name == "SystemInfo":
        from .system_info import SystemInfo
        return SystemInfo
    

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

from .environment import *
from .console import *
from .launch import *
from .file_character import *
from .gui_elements import *


"""
Detect whether Python is running inside WSL, Docker, CI, or mobile environments.
"""

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
"""
# Dynamically re-export everything environment declares in its __all__
__all__ = __all__ + environment.__all__ + console.__all__ + file_character.__all__ + gui_elements.__all__

def __dir__():
    return sorted(__all__ + [
        "__all__", "__builtins__", "__cached__", "__doc__", "__file__",
        "__getattr__", "__loader__", "__name__", "__package__", "__path__", "__spec__"
    ])

