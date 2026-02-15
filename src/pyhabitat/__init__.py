# src/pyhabitat/__init__.py
from __future__ import annotations
from ._version import __version__ 
from .system_info import SystemInfo
from .reporting import report
from .environment import *
from .console import *

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
__all__ = [
    '__version__',
    'SystemInfo',
    'report',
] + environment.__all__ + console.__all__

