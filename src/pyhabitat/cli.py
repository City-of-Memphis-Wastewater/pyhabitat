# src/pyhabitat/cli.py
import argparse
from pathlib import Path

import pyhabitat
from pyhabitat.version_info import get_package_version
from pyhabitat.reporting import report

"""
from . import environment 
from .environment import * # to enable CLI --list
import pyhabitat # refers to the folder
"""
# Instead of wildcarding .environment, we pull the clean API from the package root
from pyhabitat import (
    environment, 
    __all__ as public_api
)


def run_cli():
    """Parse CLI arguments and run the pyhabitat environment report."""
    current_version = get_package_version()
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
        environment.clear_all_caches() # 
        print("All cached results cleared to allow for fresh checks.")
        return # avoid running the report
    
    if args.list:
        # Use the __all__ we imported from .
        for name in public_api:
            func = getattr(pyhabitat, name, None)
            if callable(func):
                print(name)
                if args.debug:
                    doc = func.__doc__ or "(no description)"
                    print(f"  {doc}")
        return
    
    """if args.list:
        for name in pyhabitat.__all__:
            func = getattr(pyhabitat, name, None)
            if callable(func):
                print(name)
                if args.debug:
                    doc = func.__doc__ or "(no description)"
                    print(f"{name}: {doc}")
        return"""
    '''
    if args.command:
        func = getattr(pyhabitat, args.command, None)
        if callable(func):
            print(func())
            return # Exit after running the subcommand
        else:
            print(f"Unknown function: {args.command}")
            return # Exit after reporting the unknown command
    '''    
    """if args.command:
        func = getattr(pyhabitat, args.command, None)
        if callable(func):
            kwargs = {}
            if args.path:
                kwargs['path'] = Path(args.path)
            if args.debug:
                kwargs['debug'] = args.debug
            print(func(**kwargs))
            return
        else:
            # necessary to avoid printing report if specific function matching the command is not found
            print(f"Function not callable. Check spelling: {args.command}")
            return"""
        
    if args.command:
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
            print(f"Function not found or not callable: {args.command}")
            return


    report(path=Path(args.path) if args.path else None, debug=args.debug)
