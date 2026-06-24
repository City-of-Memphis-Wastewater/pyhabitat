#!/usr/bin/env python3
"""Script to inspect and print signatures of all public pyhabitat functions."""

from __future__ import annotations
import inspect
import sys
from pathlib import Path

# Ensure the local src directory is in the path for resolution
src_path = Path(__file__).parent / "src"
if src_path.exists():
    sys.path.insert(0, str(src_path))

import pyhabitat


def main() -> None:
    print(f"--- PyHabitat {pyhabitat.__version__} Function Signatures ---")
    
    # Iterate over the explicit public API list defined in __init__.py
    for name in pyhabitat.__all__:
        if name == "__version__":
            continue
            
        try:
            # Trigger your dynamic __getattr__ module loading
            obj = getattr(pyhabitat, name)
            
            if inspect.isclass(obj):
                print(f"\nClass: {name}")
                # Print class initializer signature if it's a class (like SystemInfo)
                try:
                    sig = inspect.signature(obj.__init__)
                    print(f"  __init__{sig}")
                except (ValueError, TypeError):
                    print("  __init__(no signature available)")
                    
            elif callable(obj):
                try:
                    sig = inspect.signature(obj)
                    print(f"func {name}{sig}")
                except ValueError:
                    print(f"func {name}(...)  # Signature not accessible")
            else:
                print(f"Constant/Other: {name} = {obj}")
                
        except AttributeError as e:
            print(f"Error resolving {name}: {e}")


if __name__ == "__main__":
    main()
