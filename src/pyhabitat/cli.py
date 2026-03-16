# src/pyhabitat/cli.py
from __future__ import annotations
import argparse
from pathlib import Path
import sys

import pyhabitat
from ._version import get_version
from .reporting import report
from .console import safe_notify
# Instead of wildcarding .environment, we pull the clean API from the package root

from pyhabitat import (
    environment, 
    console,
    __all__ as public_api
)


def run_cli():
    """Parse CLI arguments and run the pyhabitat environment report."""
    current_version = get_version()
    parser = argparse.ArgumentParser(
        description="PyHabitat: Python environment and build introspection"
    )
    # Add the version argument
    parser.add_argument(
        '-v', '--version', 
        action='version', 
        version=f'PyHabitat {current_version}'
    )
    # Add the path argument
    parser.add_argument(
        "--path",
        type=str,
        default=None,
        help="Path to a script or binary to inspect (defaults to sys.argv[0])",
    )
    # Add the debug argument
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable verbose debug output",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available callable functions in pyhabitat"
    )
    # Add the path argument
    parser.add_argument(
        "--clear-cache",
        action = 'store_true',
        help="Force fresh environment checks with cached results.",
    )
    #parser.add_argument(
    #    "--verbose",
    #    action="store_true",
    #    help="List available callable functions in pyhabitat"
    #)
                
    parser.add_argument(
        "command",
        nargs="?",
        help="Function name to run (or use --list)",
    )

                
    args = parser.parse_args()

    if args.clear_cache:
        environment.clear_mpl_cache()
        console.clear_shell_cache() # 
        safe_notify("All cached results cleared to allow for fresh checks.")
        return # avoid running the report
    
    if args.list:
        # Use the __all__ we imported from .
        for name in public_api:
            func = getattr(pyhabitat, name, None)
            if callable(func):
                safe_notify(name)
                if args.debug:
                    doc = func.__doc__ or "(no description)"
                    safe_notify(f"  {doc}")
        return

    if False:
        safe_notify(args.safe_notify) # 
        safe_notify("All cached results cleared to allow for fresh checks.")
        return 

        
    if args.command:
        # 1. Prevent functions with arguments from being called via CLI
        if args.command == "safe_notify":
            safe_notify(f"Error: 'safe_notify' is a utility and cannot be called via CLI.")
            sys.exit(1)
        func = getattr(pyhabitat, args.command, None)
        if callable(func):
            kwargs = {}
            if args.path:
                kwargs['path'] = Path(args.path)
            if args.debug:
                kwargs['debug'] = args.debug
            
            # Run the specific requested function
            print(func(**kwargs))
            return
        else:
            safe_notify(f"Function not found or not callable: {args.command}")
            sys.exit(1)


    report(path=Path(args.path) if args.path else None, debug=args.debug)
