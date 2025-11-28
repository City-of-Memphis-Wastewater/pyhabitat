import argparse
from pathlib import Path
from .report import report
from . import environment 
from .environment import * # to enable CLI --list
from .utils import get_version
#import __init__ as pyhabitat # works if everything is in root, v1.0.28
import pyhabitat # refers to the folder

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
        environment.clear_all_caches() # 
        print("All cached results cleared to allow for fresh checks.")

    if args.list:
        for name in pyhabitat.__all__:
            func = getattr(pyhabitat, name, None)
            if callable(func):
                print(name)
                if args.debug:
                    doc = func.__doc__ or "(no description)"
                    print(f"{name}: {doc}")
        return
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
    if args.command:
        func = getattr(pyhabitat, args.command, None)
        if callable(func):
            kwargs = {}
            if args.path:
                kwargs['path'] = Path(args.path)
            if args.debug:
                kwargs['debug'] = args.debug
            print(func(**kwargs))
            return


    report(path=Path(args.path) if args.path else None, debug=args.debug)
