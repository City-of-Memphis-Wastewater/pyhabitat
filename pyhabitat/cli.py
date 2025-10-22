import argparse
from pathlib import Path
from pyhabitat.environment import main

def run_cli():
    """Parse CLI arguments and run the pyhabitat environment report."""
    parser = argparse.ArgumentParser(
        description="PyHabitat: Python environment and build introspection"
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
    args = parser.parse_args()
    main(path=Path(args.path) if args.path else None, debug=args.debug)
