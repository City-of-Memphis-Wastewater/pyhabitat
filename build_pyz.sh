#!/bin/bash
set -e

# Extract version from Python
VERSION=$(python -c "from pyhabitat.utils import get_version; print(get_version())")

# Clean up old build
rm -rf pyhabitat-build dist
mkdir -p pyhabitat-build dist
mkdir -p pyhabitat-build/pyhabitat

# Copy only necessary files
cp __main__.py pyproject.toml pyhabitat-build/
cp pyhabitat/__init__.py pyhabitat/cli.py pyhabitat/environment.py pyhabitat/utils.py  pyhabitat-build/pyhabitat

# Build the .pyz
OUTPUT="dist/pyhabitat-${VERSION}.pyz"
python -m zipapp pyhabitat-build -o "$OUTPUT" --python "/usr/bin/env python3"
chmod +x "$OUTPUT"

echo "✅ Built $OUTPUT"

