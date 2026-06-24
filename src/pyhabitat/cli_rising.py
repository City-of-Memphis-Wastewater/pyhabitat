# src/pyhabitat/cli.py
from __future__ import annotations
import argparse
import logging
from pathlib import Path
import sys

import pyhabitat
from ._version import __version__

logger = logging.getLogger(__name__)

public_api = pyhabitat.__all__


def run_cli() -> None:
    """Parse CLI arguments and run the pyhabitat environment report or utilities."""
    current_version = __version__
    parser = argparse.ArgumentParser(
        description="PyHabitat: Python environment and build introspection"
    )
    
    parser.add_argument(
        '-v', '--version',
        action='version',
        version=f'PyHabitat {current_version}'
    )
    
    parser.add_argument(
        "--path",
        type=str,
        default=None,
        help="Path to a script or binary to inspect (defaults to sys.argv[0])",
    )
    
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
    
    parser.add_argument(
        "--clear-cache",
        action='store_true',
        help="Force fresh environment checks with cached results.",
    )

    parser.add_argument(
        "command",
        nargs="?",
        help="Function name to run (or use --list)",
    )

    args = parser.parse_args()

    # 1. Handle Cache Clearing
    if args.clear_cache:
        # Check for existence of cache clearing routines safely
        if hasattr(pyhabitat, "clear_mpl_cache"):
            pyhabitat.clear_mpl_cache()
        if hasattr(pyhabitat, "clear_shell_cache"):
            pyhabitat.clear_shell_cache()
        pyhabitat.safe_notify("All cached results cleared to allow for fresh checks.")
        return

    # 2. Handle Listing Public APIs
    if args.list:
        for name in public_api:
            if name == "__version__":
                continue
            func = getattr(pyhabitat, name, None)
            if callable(func):
                pyhabitat.safe_notify(name)
                if args.debug:
                    doc = func.__doc__ or "(no description)"
                    pyhabitat.safe_notify(f"  {doc}")
        return

    # 3. Handle Running a Specific Function
    if args.command:
        # Prevent calling safe_notify directly via CLI as it requires mandatory args
        if args.command == "safe_notify":
            pyhabitat.safe_notify("Error: 'safe_notify' is a utility and cannot be called via CLI.")
            sys.exit(1)
            
        func = getattr(pyhabitat, args.command, None)
        
        if func is None or not callable(func):
            pyhabitat.safe_notify(f"Function not found or not callable: {args.command}")
            sys.exit(1)

        # Build execution kwargs dynamically matching target signature options
        kwargs = {}
        
        # Check what arguments the target function actually supports
        import inspect
        try:
            sig = inspect.signature(func)
            params = sig.parameters
        except (ValueError, TypeError):
            params = {}

        # Safely assign 'path' or alternative keyword variable variants
        if args.path:
            resolved_path = Path(args.path)
            if "path" in params:
                kwargs['path'] = resolved_path
            elif "exec_path" in params:
                kwargs['exec_path'] = resolved_path
            else:
                pyhabitat.safe_notify(f"Warning: Function '{args.command}' does not accept a path argument.")
                sys.exit(1)

        # Safely pass debug flag if supported
        if args.debug and "debug" in params:
            kwargs['debug'] = True

        # Run the targeted API function
        try:
            result = func(**kwargs)
            if result is not None:
                print(result)
        except Exception as e:
            pyhabitat.safe_notify(f"Error executing '{args.command}': {e}")
            if args.debug:
                raise
            sys.exit(1)
        return

    # 4. Default Fallback Behavior: Run the Report
    report_path = Path(args.path) if args.path else None
    pyhabitat.report(path=report_path, debug=args.debug)
