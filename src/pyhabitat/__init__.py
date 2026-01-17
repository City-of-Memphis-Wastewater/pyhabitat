# src/pyhabitat/__init__.py
from __future__ import annotations
from .version_info import get_package_version as version
from .system_info import SystemInfo
from .reporting import report
from .environment import *
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
    'version',
    'SystemInfo',
    'report',
] + environment.__all__

__version__ = version()
