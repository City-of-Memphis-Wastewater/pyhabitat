import os
import sys
import shutil
import subprocess

# Define the source files to copy, matching the logic in build.ps1
# The key structure is (source_path, destination_dir_relative_to_build_root)
SOURCE_FILES = {
    # Root files
    "__main__.py": ".",
    "pyproject.toml": ".",
    # pyhabitat subdirectory files
    "pyhabitat/__init__.py": "pyhabitat",
    "pyhabitat/cli.py": "pyhabitat",
    "pyhabitat/environment.py": "pyhabitat",
    "pyhabitat/utils.py": "pyhabitat",
}

BUILD_ROOT = "pyhabitat-build"
DIST_DIR = "dist"


def run_build():
    """Executes the complete PYZ build process."""
    try:
        print("--- PyHabitat Cross-Platform Build ---")
        
        # --- 1. Extract version from pyhabitat.utils ---
        print("1. Extracting version...")
        # Use sys.executable for cross-platform Python interpreter
        result = subprocess.run(
            [sys.executable, '-c', 'from pyhabitat.utils import get_version; print(get_version())'],
            capture_output=True,
            text=True,
            check=True # Raise exception on error (equivalent to $ErrorActionPreference = "Stop")
        )
        VERSION = result.stdout.strip()
        print(f"   -> Detected version: {VERSION}")
        
        # --- 2. Clean up old build and create directories ---
        print("\n2. Cleaning and creating directories...")
        
        # Remove old build directories
        if os.path.exists(BUILD_ROOT):
            shutil.rmtree(BUILD_ROOT)
        #if os.path.exists(DIST_DIR):
        #    shutil.rmtree(DIST_DIR)
        # Remove only the specific PYZ output
        output_file = Path(DIST_DIR) / f"pyhabitat-{VERSION}.pyz"
        if output_file.exists():
            print(f"Removing old PYZ: {output_file}")
            output_file.unlink()
   
        # Create necessary directories
        os.makedirs(f"{BUILD_ROOT}/pyhabitat", exist_ok=True)
        os.makedirs(DIST_DIR, exist_ok=True)

        # --- 3. Copy only necessary files ---
        print("\n3. Copying source files...")
        for src, dest_dir in SOURCE_FILES.items():
            src_path = os.path.join(os.getcwd(), src)
            dest_path = os.path.join(BUILD_ROOT, dest_dir)
            
            if not os.path.exists(src_path):
                print(f"WARNING: Source file not found: {src}", file=sys.stderr)
                continue
                
            # shutil.copy2 is used to preserve metadata, similar to 'cp'
            shutil.copy2(src_path, dest_path)
            print(f"   -> Copied {src} to {dest_dir}/")

        # --- 4. Build the .pyz executable ---
        OUTPUT_FILENAME = f"pyhabitat-{VERSION}.pyz"
        OUTPUT_PATH = os.path.join(DIST_DIR, OUTPUT_FILENAME)
        
        print(f"\n4. Building {OUTPUT_PATH}...")
        
        # Build the .pyz using python -m zipapp
        subprocess.run(
            [
                sys.executable, 
                '-m', 
                'zipapp', 
                BUILD_ROOT, 
                '-o', 
                OUTPUT_PATH, 
                '--python', 
                '/usr/bin/env python3'
            ],
            check=True
        )

        # --- 5. Set executable permission (POSIX systems) ---
        # This step is harmless on Windows but necessary for Linux/macOS to run the PYZ directly.
        os.chmod(OUTPUT_PATH, 0o755)
        
        print(f"\n✅ Build successful! Output: {OUTPUT_PATH}")

    except subprocess.CalledProcessError as e:
        print(f"\nERROR: Subprocess failed with exit code {e.returncode}.", file=sys.stderr)
        print(f"Command: {' '.join(e.cmd)}", file=sys.stderr)
        print(f"Stderr: {e.stderr.strip()}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\nFATAL ERROR during build process: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    run_build()