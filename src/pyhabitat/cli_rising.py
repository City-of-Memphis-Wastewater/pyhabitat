# src/pyhabitat/cli_rising.py
from __future__ import annotations
import argparse
import inspect
import logging
from pathlib import Path
import sys

import pyhabitat
from ._version import __version__

logger = logging.getLogger(__name__)


def run_cli() -> None:
    """Parse CLI arguments using subparsers for an elegant, scalable tool."""
    current_version = __version__
    
    # Root parser
    parser = argparse.ArgumentParser(
        description="PyHabitat: Python environment and build introspection"
    )
    parser.add_argument(
        '-v', '--version',
        action='version',
        version=f'PyHabitat {current_version}'
    )
    parser.add_argument(
        "--clear-cache",
        action='store_true',
        help="Force fresh environment checks with cached results.",
    )

    # Subparsers for independent commands
    subparsers = parser.add_subparsers(
        dest="command",
        metavar="command",
        help="Target function or routine to run"
    )

    # 1. Register a dedicated subparser for the default full system report
    report_parser = subparsers.add_parser("report", help="Run the full pyhabitat environment report (default)")
    report_parser.add_argument("--path", type=str, default=None, help="Path to inspect (defaults to sys.argv[0])")
    #report_parser.add_argument("--debug", action="store_true", help="Enable verbose debug output")

    # 2. Dynamically loop through __all__ and map functions to CLI sub-commands
    for name in pyhabitat.__all__:
        if name in ("__version__", "report", "safe_notify"):
            continue
            
        func = getattr(pyhabitat, name, None)
        if not callable(func):
            continue

        # Create a subcommand matching the exact function name
        doc = func.__doc__ or f"Run pyhabitat.{name}()"
        first_line_doc = doc.strip().split("\n")[0]
        cmd_parser = subparsers.add_parser(name, help=first_line_doc)

        # Inspect the function signature to add targeted parameters automatically
        try:
            sig = inspect.signature(func)
            params = sig.parameters
        except (ValueError, TypeError):
            params = {}

        # Adapt path/exec_path parameter signatures seamlessly to standard --path flags
        if "path" in params or "exec_path" in params:
            cmd_parser.add_argument(
                "--path", 
                type=str, 
                default=None, 
                help="Path to check/evaluate"
            )
            
        #if "debug" in params:
        #    cmd_parser.add_argument(
        #        "--debug", 
        #        action="store_true", 
        #        help="Enable verbose function debug output"
        #    )

    # Intercept --clear-cache before parsing so it bypasses required subcommands
    if "--clear-cache" in sys.argv:
        if hasattr(pyhabitat, "clear_mpl_cache"):
            pyhabitat.clear_mpl_cache()
        if hasattr(pyhabitat, "clear_shell_cache"):
            pyhabitat.clear_shell_cache()
        pyhabitat.safe_notify("All cached results cleared to allow for fresh checks.")
        return

    # Handle the empty arguments edge-case by falling back to the standard report
    if len(sys.argv) == 1:
        pyhabitat.report(path=None, debug=False)
        return

    args = parser.parse_args()

    # Execution logic branch
    if args.command == "report":
        report_path = Path(args.path) if args.path else None
        pyhabitat.report(path=report_path, debug=args.debug)
        return

    if args.command:
        func = getattr(pyhabitat, args.command)
        kwargs = {}
        
        # Build kwargs based on what the parsed subcommand provides
        try:
            sig = inspect.signature(func)
            params = sig.parameters
        except (ValueError, TypeError):
            params = {}

        if hasattr(args, "path") and args.path:
            resolved_path = Path(args.path)
            if "path" in params:
                kwargs["path"] = resolved_path
            elif "exec_path" in params:
                kwargs["exec_path"] = resolved_path

        if hasattr(args, "debug") and args.debug and "debug" in params:
            kwargs["debug"] = True

        try:
            result = func(**kwargs)
            if result is not None:
                print(result)
        except Exception as e:
            pyhabitat.safe_notify(f"Error executing '{args.command}': {e}")
            sys.exit(1)
