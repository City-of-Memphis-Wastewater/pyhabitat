from importlib.metadata import version, PackageNotFoundError
def get_version() -> str:
    """Retrieves the installed package version."""
    try:
        # The package name 'pyhabitat' must exactly match the name in your pyproject.toml
        return version('pyhabitat')
    except PackageNotFoundError:
        # This occurs if the script is run directly from the source directory
        # without being installed in editable mode, or if the package name is wrong.
        return "Not Installed (Local Development or Incorrect Name)"