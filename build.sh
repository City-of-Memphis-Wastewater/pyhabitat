#!/bin/bash
set -e

# Extract version from Python
VERSION=$(python -c "from utils import get_version; print(get_version())")

# Clean up old build
rm -rf pyhabitat-lite dist
mkdir -p pyhabitat-lite dist

# Copy only necessary files
cp __main__.py __init__.py cli.py environment.py utils.py pyproject.toml pyhabitat-lite/

# Build the .pyz
OUTPUT="dist/pyhabitat-${VERSION}.pyz"
python -m zipapp pyhabitat-lite -o "$OUTPUT" --python "/usr/bin/env python3"
chmod +x "$OUTPUT"

echo "✅ Built $OUTPUT"

