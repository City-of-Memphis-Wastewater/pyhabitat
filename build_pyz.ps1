# build.ps1 - PowerShell script to build the Python .pyz executable
# NOTE: This script is intended to be run in a Windows PowerShell environment.

# Stop script execution on any command failure
$ErrorActionPreference = "Stop"

# --- 1. Extract version from pyhabitat.utils ---
# Executes Python command and captures the output into the $VERSION variable
$VERSION = python -c "from pyhabitat.utils import get_version; print(get_version())"

# --- 2. Clean up old build and create directories ---
Write-Host "Cleaning old build artifacts..."
# Remove old directories. -ErrorAction SilentlyContinue prevents failing if they don't exist.
Remove-Item -Path "pyhabitat-build", "dist" -Recurse -Force -ErrorAction SilentlyContinue

# Create necessary directories
New-Item -Path "pyhabitat-build", "dist" -ItemType Directory -Force
New-Item -Path "pyhabitat-build/pyhabitat" -ItemType Directory -Force

# --- 3. Copy only necessary files ---
Write-Host "Copying source files..."

# Copy files to the root of the temporary build directory
Copy-Item -Path "__main__.py", "pyproject.toml" -Destination "pyhabitat-build/"

# Copy files to the pyhabitat subdirectory
Copy-Item -Path "pyhabitat/__init__.py", "pyhabitat/cli.py", "pyhabitat/environment.py", "pyhabitat/utils.py" -Destination "pyhabitat-build/pyhabitat"

# --- 4. Build the .pyz executable ---
$OUTPUT = "dist/pyhabitat-${VERSION}.pyz"
Write-Host "Building $OUTPUT..."

# Use python -m zipapp to create the archive
# Note: '/usr/bin/env python3' is left as the shebang argument for cross-platform execution of the PYZ
python -m zipapp pyhabitat-build -o "$OUTPUT" --python "/usr/bin/env python3"

# --- 5. Output Success Message ---
# NOTE: The chmod +x command is POSIX-specific and has no direct equivalent needed for execution on Windows.
# The file will need to be executed on Linux/CI environments where the permissions are handled differently.

Write-Host "✅ Built $OUTPUT"