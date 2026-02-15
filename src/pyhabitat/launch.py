# src/pyhabitat/launch.py
from __future__ import annotations
import os
import sys
import subprocess
from pathlib import Path
import shutil
from typing import Optional

# On Windows, we need the msvcrt module for non-blocking I/O
try:
    import msvcrt
except ImportError:
    msvcrt = None

from .console import interactive_terminal_is_available
from .environment import (
    in_repl, on_windows, is_msix, on_termux, on_ish_alpine, on_linux, on_macos, on_wsl
)

__all__ = [
    'edit_textfile',
    'show_system_explorer',
]

# --- LAUNCH MECHANISMS BASED ON ENVIRONMENT ---

def edit_textfile(path: Path | str | None = None, background: Optional[bool] = None) -> None:
    """
    Opens a file with the environment's default application.
    
    Logic:
    - If background is None: 
        - Blocks (waits) if in REPL or Interactive Terminal (supports nano/vim).
        - Runs backgrounded if in a GUI/headless environment.
    - If background is True/False: Manual override.
    
    Ensures line-ending compatibility and dependency installation in 
    constrained environments (Termux, iSH).
    """
    

    if path is None:
        return
    
    path = Path(path).resolve()

    # --- 1. Intelligent Context Detection ---
    if background is None:
        # Detect if we have a TTY/REPL to determine if blocking is necessary
        if in_repl() or interactive_terminal_is_available():
            is_async = False  
        else:
            is_async = True   
    else:
        is_async = background

    # Choose runner: Popen for fire-and-forget, run for blocking
    launcher = subprocess.Popen if is_async else subprocess.run

    try:

        # --- Windows --- 
        if on_windows():

            # Force resolve to handle MSIX VFS redirection
            # Force resolve AND normalize slashes for the Windows API
            abs_path = os.path.normpath(str(Path(path).resolve()))
            #success = False

            # 0: Special case: MSIX files (Sandboxed, os.startfile() known to fail
            if is_msix(): # 

                try:
                    # Use the explicit path to System32 notepad to bypass environment issues
                    system_notepad = os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'System32', 'notepad.exe')
                    subprocess.Popen([system_notepad, abs_path])
                    return
                except Exception as e:
                    print(f"Notepad launch failed via MSIX package: {e}")

            # 1. Primary: System Default (Natively non-blocking/async)
            try:
                # os.startfile is natively non-blocking (async)
                os.startfile(abs_path)
                #success = True
                return
            except Exception as e:
                # This catches the "No program associated" or "Access denied" errors
                print(f"os.startfile() failed in pyhabitat.edit_textfile(): {e}")

            # 2. Secondary: Force Notepad (Guaranteed fallback)
            # Use Popen to ENSURE it never blocks the caller, regardless of REPL status.
            try:
                subprocess.Popen(['notepad.exe', abs_path])
                #success = True
                return
            except Exception as e: 
                print(f"notepad.exe failed in pyhabitat.edit_textfile(): {e}")

            print(f"\n[Error] Windows could not open the file: {abs_path}")

        # --- Termux (Android) ---
        elif on_termux():
            try:
                # Try to run directly assuming tools exist
                _run_dos2unix(path)
                subprocess.run(['nano', str(path)])
            except FileNotFoundError:
                # Fallback: Install missing tools
                # Using -y ensures the package manager doesn't hang waiting for a 'Yes'
                subprocess.run(['pkg', 'install', '-y', 'dos2unix', 'nano'], 
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                _run_dos2unix(path)
                subprocess.run(['nano', str(path)])
            
        # --- iSH (iOS Alpine) ---
        elif on_ish_alpine():
            try:
                _run_dos2unix(path)
                subprocess.run(['nano', str(path)])
            except FileNotFoundError:
                # Alpine uses 'apk add'
                subprocess.run(['apk', 'add', 'dos2unix', 'nano'], 
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                _run_dos2unix(path)
                subprocess.run(['nano', str(path)])

        # --- Standard Desktop Linux ---
        elif on_linux():
            _run_dos2unix(path)
            success = False
            
            # 1. Try System Default (xdg-open)
            # We use subprocess.run here to check if the OS actually knows how to handle the file.
            try:
                # capture_output=True keeps the 'no mailcap rules' error out of the user's console
                subprocess.run(['xdg-open', str(path)], check=True, capture_output=True)
                success = True
            except (subprocess.CalledProcessError, FileNotFoundError, Exception):
                # If xdg-open fails (like the JSON error you saw), we move to manual fallbacks
                pass

            if not success:
                # 2. Fallback Ladder: Common GUI Editors
                # These are safe to background (using the 'launcher' Popen/run logic)
                # Prioritize standalone editors over IDEs
                gui_editors = ['gedit', 'mousepad', 'kate', 'xed', 'code']
                for editor in gui_editors:
                    if shutil.which(editor):
                        # launcher will be Popen if we are in a GUI, or run if in a TTY
                        launcher([editor, str(path)])
                        success = True
                        break
            
            if not success:
                # 3. Final Fallback: Terminal Editor
                # This MUST be blocking (subprocess.run) to work in a TTY/REPL context.
                # We don't spawn a new window to avoid environmental/SSH crashes.
                if shutil.which('nano'):
                    # If we are in a GUI, the user might need to look at the terminal they launched from
                    if is_async: 
                        print(f"\n[Note] No GUI editor found. Opening {path.name} in nano within the terminal.")
                    
                    subprocess.run(['nano', str(path)])
                    success = True
                else:
                    # Absolute last resort
                    print(f"\n[Error] No suitable editor (GUI or Terminal) found. File saved at: {path}")
                
        # --- macOS ---
        elif on_macos():
            _run_dos2unix(path)
            # 'open' on Mac usually returns immediately for GUI apps anyway, 
            # but using our launcher keeps the Popen logic consistent.
            try:
                launcher(['open', str(path)])
            except Exception:
                # Terminal fallback for Mac if 'open' fails (very rare)
                if shutil.which('nano'):
                    subprocess.run(['nano', str(path)])
        else:
            print("Unsupported operating system.")
            
    except Exception as e:
        print(f"The file could not be opened: {e}")

# --- Helper Functions ---    
def _run_dos2unix(path: Path | str | None = None):
    """Attempt to run dos2unix, failing silently if not installed."""
    
    path = Path(path).resolve()

    try:
        # We rely on shutil.which not being needed, as this is a robust built-in utility on most targets
        # The command won't raise an exception unless the process itself fails, not just if the utility isn't found.
        # We also don't use check=True here to allow silent failure if the utility is missing (e.g., minimalist Linux).
        subprocess.run(['dos2unix', str(path)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        # This will be raised if 'dos2unix' is not on the system PATH
        pass 
    except Exception:
        # Catch other subprocess errors (e.g. permission issues)
        pass

def show_system_explorer(path: str | Path = None) -> None: 
    """
    Opens the system file explorer (File Explorer, Finder, or Nautilus/etc.)
    to the directory containing the exported reports.
    """
    # 1. Standardize to a Path object immediately
    if path is None:
        path = Path.cwd()
    else:
        path = Path(path)
    
    # 2. Smart Trim: If they pointed to a file, we want to open the folder it's in
    if path.is_file():
        path = path.parent
    
    # Ensure it exists before we try to open it (prevents shell crashes)
    if not path.exists():
        print(f"Error: Path does not exist: {path}")
        return
    
    # Ensure path is a string and expanded
    path = str(Path(path).expanduser().resolve())


    try:
        if on_wsl():
            win_path = subprocess.check_output(["wslpath", "-w", path]).decode().strip()
            subprocess.Popen(["explorer.exe", win_path])
        elif on_windows():
            # use os.startfile for the most native Windows experience
            os.startfile(path)
        elif sys.platform == "darwin":
            # macOS
            subprocess.Popen(["open", str(path)])

        #  Android (Termux)
        elif on_termux():
            # termux-open passes the intent to the Android system explorer
            subprocess.Popen(["termux-open", path])
            return
        
        else:
            # Linux/Other: pyhabitat or xdg-open fallback
            # Using xdg-open is the standard for Nautilus, Dolphin, Thunar, etc.
            subprocess.Popen(["xdg-open", path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"Could not open system explorer. Path: {path}. Error: {e}")
