import argparse
from pathlib import Path
from pyhabitat.environment import main
from importlib.metadata import version, PackageNotFoundError

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
        version=f'%(prog)s {current_version}'
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
    args = parser.parse_args()
    main(path=Path(args.path) if args.path else None, debug=args.debug)


def get_version() -> str:
    """Retrieves the installed package version."""
    try:
        # The package name 'pyhabitat' must exactly match the name in your pyproject.toml
        return version('pyhabitat')
    except PackageNotFoundError:
        # This occurs if the script is run directly from the source directory
        # without being installed in editable mode, or if the package name is wrong.
        return "Not Installed (Local Development or Incorrect Name)"