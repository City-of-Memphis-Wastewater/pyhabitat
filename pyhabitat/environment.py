'''
Title: environment.py
Author: Clayton Bennett
Created: 23 July 2024
'''
from __future__ import annotations # Delays annotation evaluation, allowing modern 3.10+ type syntax and forward references in older Python versions 3.8 and 3.9
import platform
import sys
import os
import webbrowser
import shutil
from pathlib import Path
import subprocess
import io
import zipfile
import logging

__all__ = [
    'matplotlib_is_available_for_gui_plotting',
    'matplotlib_is_available_for_headless_image_export',
    'tkinter_is_available',
    'on_termux',
    'on_freebsd',
    'on_linux',
    'on_pydroid',
    'on_android',
    'on_windows',
    'on_wsl',
    'on_apple',
    'on_ish_alpine',
    'as_pyinstaller',
    'as_frozen',
    'is_elf',
    'is_pyz',
    'is_windows_portable_executable',
    'is_macos_executable',
    'is_pipx',
    'interactive_terminal_is_available',
    'web_browser_is_available',
    'edit_textfile',
    'in_repl',
    'interp_path',
    'main',
]

# Global cache for tkinter and matplotlib (mpl) availability
_TKINTER_AVAILABILITY: bool | None = None
_MATPLOTLIB_EXPORT_AVAILABILITY: bool | None = None
_MATPLOTLIB_WINDOWED_AVAILABILITY: bool | None = None


# --- GUI CHECKS ---
def matplotlib_is_available_for_gui_plotting(termux_has_gui=False):
    """Check if Matplotlib is available AND can use a GUI backend for a popup window."""
    global _MATPLOTLIB_WINDOWED_AVAILABILITY

    if _MATPLOTLIB_WINDOWED_AVAILABILITY is not None:
        return _MATPLOTLIB_WINDOWED_AVAILABILITY

    # 1. Termux exclusion check (assume no X11/GUI)
    # Exclude Termux UNLESS the user explicitly provides termux_has_gui=True.
    if on_termux() and not termux_has_gui: 
        _MATPLOTLIB_WINDOWED_AVAILABILITY = False
        return False
    
    # 2. Tkinter check (The most definitive check for a working display environment)
    # If tkinter can't open a window, Matplotlib's TkAgg backend will fail.
    if not tkinter_is_available():
        _MATPLOTLIB_WINDOWED_AVAILABILITY = False
        return False

    # 3. Matplotlib + TkAgg check
    try:
        import matplotlib
        # Force the common GUI backend. At this point, we know tkinter is *available*.
        # # 'TkAgg' is often the most reliable cross-platform test.
        # 'TkAgg' != 'Agg'. The Agg backend is for non-gui image export. 
        if matplotlib.get_backend().lower() != 'tkagg':
            matplotlib.use('TkAgg', force=True)
        import matplotlib.pyplot as plt
        # A simple test call to ensure the backend initializes
        # This final test catches any edge cases where tkinter is present but 
        # Matplotlib's *integration* with it is broken
        plt.figure()
        plt.close()

        _MATPLOTLIB_WINDOWED_AVAILABILITY = True
        return True

    except Exception:
        # Catches Matplotlib ImportError or any runtime error from the plt.figure() call
        _MATPLOTLIB_WINDOWED_AVAILABILITY = False
        return False
    

def matplotlib_is_available_for_headless_image_export():
    """Check if Matplotlib is available AND can use the Agg backend for image export."""
    global _MATPLOTLIB_EXPORT_AVAILABILITY
    
    if _MATPLOTLIB_EXPORT_AVAILABILITY is not None:
        return _MATPLOTLIB_EXPORT_AVAILABILITY
    
    try:
        import matplotlib
        # The Agg backend (for PNG/JPEG export) is very basic and usually available 
        # if the core library is installed. We explicitly set it just in case.
        # 'Agg' != 'TkAgg'. The TkAgg backend is for interactive gui image display. 
        matplotlib.use('Agg', force=True) 
        import matplotlib.pyplot as plt
        
        # A simple test to ensure a figure can be generated
        plt.figure()
        # Ensure it can save to an in-memory buffer (to avoid disk access issues)
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        
        _MATPLOTLIB_EXPORT_AVAILABILITY = True
        return True
        
    except Exception:
        _MATPLOTLIB_EXPORT_AVAILABILITY = False
        return False
        
def tkinter_is_available() -> bool:
    """Check if tkinter is available and can successfully connect to a display."""
    global _TKINTER_AVAILABILITY
    
    # 1. Return cached result if already calculated
    if _TKINTER_AVAILABILITY is not None:
        return _TKINTER_AVAILABILITY

    # 2. Perform the full, definitive check
    try:
        import tkinter as tk
        
        # Perform the actual GUI backend test for absolute certainty.
        # This only runs once per script execution.
        root = tk.Tk()
        root.withdraw()
        root.update()
        root.destroy()
        
        _TKINTER_AVAILABILITY = True
        return True
    except Exception:
        # Fails if: tkinter module is missing OR the display backend is unavailable
        _TKINTER_AVAILABILITY = False
        return False

# --- ENVIRONMENT AND OPERATING SYSTEM CHECKS ---
def on_termux() -> bool:
    """Detect if running in Termux environment on Android, based on Termux-specific environmental variables."""
    
    if platform.system() != 'Linux':
        return False
    
    termux_path_prefix = '/data/data/com.termux'
    
    # Termux-specific environment variable ($PREFIX)
    # The actual prefix is /data/data/com.termux/files/usr
    if os.environ.get('PREFIX', default='').startswith(termux_path_prefix + '/usr'):
        return True
    
    # Termux-specific environment variable ($HOME)
    # The actual home is /data/data/com.termux/files/home
    if os.environ.get('HOME', default='').startswith(termux_path_prefix + '/home'):
        return True

    # Code insight: The os.environ.get command returns the supplied default if the key is not found. 
    #   None is retured if a default is not speficied.
    
    # Termux-specific environment variable ($TERMUX_VERSION)
    if 'TERMUX_VERSION' in os.environ:
        return True
    
    return False

def on_freebsd() -> bool:
    """Detect if running on FreeBSD."""
    return platform.system() == 'FreeBSD'

def on_linux():
    """Detect if running on Linux."""
    return platform.system() == 'Linux' 

def on_android() -> bool:
    """
    Detect if running on Android.
    
    Note: The on_termux() function is more robust and safe for Termux.
    Checking for Termux with on_termux() does not require checking for Android with on_android().

    on_android() will be True on:   
        - Sandboxed IDE's:
            - Pydroid3
            - QPython
        - `proot`-reliant user-space containers:
            - Termux
            - Andronix
            - UserLand
            - AnLinux

    on_android() will be False on:
        - Full Virtual Machines:
            - VirtualBox
            - VMware
            - QEMU      
    """
    # Explicitly check for Linux kernel name first
    if platform.system() != 'Linux':
        return False
    return "android" in platform.platform().lower()


def on_wsl():
    """Return True if running inside Windows Subsystem for Linux (WSL or WSL2)."""
    # Must look like Linux, not Windows
    if platform.system() != "Linux":
        return False

     
    # --- Check environment variables for WSL2 ---
    # False negative risk: 
    # Environment variables may be absent in older WSL1 installs.
    # False negative likelihood: low.
    if "WSL_DISTRO_NAME" in os.environ or "WSL_INTEROP" in os.environ:
        return True

    # --- Check kernel info for 'microsoft' or 'wsl' string (Fallback) ---
    # False negative risk: 
    # Custom kernels, future Windows versions, or minimal WSL distros may omit 'microsoft' in strings.
    # False negative likelihood: Very low to moderate.
    try:
        with open("/proc/version") as f:
            version_info = f.read().lower() 
            if "microsoft" in version_info or "wsl" in version_info:
                return True
    except (IOError, OSError):
        # This block would catch the PermissionError!
        # It would simply 'pass' and move on.
        pass


    # Check for WSL-specific mounts (fallback)
    """
    /proc/sys/kernel/osrelease
    Purpose: Contains the kernel release string. In WSL, it usually contains "microsoft" (WSL2) or "microsoft-standard" (WSL1).
    Very reliable for detecting WSL1 and WSL2 unless someone compiled a custom kernel and removed the microsoft string.
    
    False negative risk: 
    If /proc/sys/kernel/osrelease cannot be read due to permissions, a containerized WSL distro, or some sandboxed environment.
    # False negative likelihood: Very low.
    """
    try:
        with open("/proc/sys/kernel/osrelease") as f:
            osrelease = f.read().lower()
            if "microsoft" in osrelease:
                return True
    except (IOError, OSError):
    # This block would catch the PermissionError, an FileNotFound
        pass
    return False

def on_pydroid():
    """Return True if running under Pydroid 3 (Android app)."""
    if not on_android():
        return False

    exe = (sys.executable or "").lower()
    if "pydroid" in exe or "ru.iiec.pydroid3" in exe:
        return True

    return any("pydroid" in p.lower() for p in sys.path)

def on_windows() -> bool:
    """Detect if running on Windows."""
    return platform.system() == 'Windows'

def on_apple() -> bool:
    """Detect if running on Apple."""
    return platform.system() == 'Darwin'

def on_ish_alpine() -> bool:
    """Detect if running in iSH Alpine environment on iOS."""
    # platform.system() usually returns 'Linux' in iSH

    # iSH runs on iOS but reports 'Linux' via platform.system()
    if platform.system() != 'Linux':
        return False
    
    # On iSH, /etc/apk/ will exist. However, this is not unique to iSH as standard Alpine Linux also has this directory.
    # Therefore, we need an additional check to differentiate iSH from standard Alpine.
    # HIGHLY SPECIFIC iSH CHECK: Look for the unique /proc/ish/ directory.
    # This directory is created by the iSH pseudo-kernel and does not exist 
    # on standard Alpine or other Linux distributions.
    if os.path.isdir('/etc/apk/') and os.path.isdir('/proc/ish'):
        # This combination is highly specific to iSH Alpine.
        return True
    
    return False

def in_repl() -> bool:
    """
    Detects if the code is running in the Python interactive REPL (e.g., when 'python' is typed in a console).

    This function specifically checks for the Python REPL by verifying the presence of the interactive
    prompt (`sys.ps1`). It returns False for other interactive terminal scenarios, such as running a
    PyInstaller binary in a console.

    Returns:
        bool: True if running in the Python REPL; False otherwise.
    """
    return hasattr(sys, 'ps1')


# --- BUILD AND EXECUTABLE CHECKS ---
    
def as_pyinstaller():
    """Detects if the Python script is running as a 'frozen' in the course of generating a PyInstaller binary executable."""
    # If the app is frozen AND has the PyInstaller-specific temporary folder path
    return as_frozen() and hasattr(sys, '_MEIPASS')

# The standard way to check for a frozen state:
def as_frozen():
    """
    Detects if the Python script is running as a 'frozen' (standalone) 
    executable created by a tool like PyInstaller, cx_Freeze, or Nuitka.

    This check is crucial for handling file paths, finding resources, 
    and general environment assumptions, as a frozen executable's 
    structure differs significantly from a standard script execution 
    or a virtual environment.

    The check is based on examining the 'frozen' attribute of the sys module.

    Returns:
        bool: True if the application is running as a frozen executable; 
              False otherwise.
    """
    return getattr(sys, 'frozen', False)

# --- Binary Characteristic Checks ---
def is_elf(exec_path: Path | str | None = None, debug: bool = False, suppress_debug: bool =False) -> bool:
    """Checks if the currently running executable (sys.argv[0]) is a standalone PyInstaller-built ELF binary."""
    # If it's a pipx installation, it is not the monolithic binary we are concerned with here.
    exec_path, is_valid = _check_executable_path(exec_path, debug and not suppress_debug)
    if not is_valid:
        return False
    
    try:
        # Check the magic number: The first four bytes of an ELF file are 0x7f, 'E', 'L', 'F' (b'\x7fELF').
        # This is the most reliable way to determine if the executable is a native binary wrapper (like PyInstaller's).
        magic_bytes = read_magic_bytes(exec_path, 4, debug and not suppress_debug)

        return magic_bytes == b'\x7fELF'
    except Exception:
        if debug:
            logging.debug("False (Exception during file check)")
        return False
    
def is_pyz(exec_path: Path | str | None = None, debug: bool = False, suppress_debug: bool =False) -> bool:
    """Checks if the currently running executable (sys.argv[0]) is a PYZ zipapp ."""

    # If it's a pipx installation, it is not the monolithic binary we are concerned with here.
    exec_path, is_valid = _check_executable_path(exec_path, debug and not suppress_debug)
    if not is_valid:
        return False
    
    # Check if the extension is PYZ
    if not str(exec_path).endswith(".pyz"):
        if debug:
            logging.debug("False (Not a .pyz file)")
        return False

    if not _check_if_zip(exec_path):
        if debug:
            logging.debug("False (Not a valid ZIP file)")
        return False

    return True


def is_windows_portable_executable(exec_path: Path | str | None = None, debug: bool = False, suppress_debug: bool =False) -> bool:
    """
    Checks if the specified path or sys.argv[0] is a Windows Portable Executable (PE) binary.
    Windows Portable Executables include .exe, .dll, and other binaries.
    The standard way to check for a PE is to look for the MZ magic number at the very beginning of the file.
    """
    exec_path, is_valid = _check_executable_path(exec_path, debug and not suppress_debug)
    if not is_valid:
        return False
    magic_bytes = read_magic_bytes(exec_path, 2, debug and not suppress_debug)
    result = magic_bytes.startswith(b"MZ")

    return result
    
def is_macos_executable(exec_path: Path | str | None = None, debug: bool = False, suppress_debug: bool =False) -> bool:
    """
    Checks if the currently running executable is a macOS/Darwin Mach-O binary, 
    and explicitly excludes pipx-managed environments.
    """
    exec_path, is_valid = _check_executable_path(exec_path, debug and not suppress_debug)
    if not is_valid:
        return False
        
    try:
        # Check the magic number: Mach-O binaries start with specific 4-byte headers.
        # Common ones are: b'\xfe\xed\xfa\xce' (32-bit) or b'\xfe\xed\xfa\xcf' (64-bit)
        
        magic_bytes = read_magic_bytes(exec_path, 4, debug and not suppress_debug)

        # Common Mach-O magic numbers (including their reversed-byte counterparts)
        MACHO_MAGIC = {
            b'\xfe\xed\xfa\xce',  # MH_MAGIC
            b'\xce\xfa\xed\xfe',  # MH_CIGAM (byte-swapped)
            b'\xfe\xed\xfa\xcf',  # MH_MAGIC_64
            b'\xcf\xfa\xed\xfe',  # MH_CIGAM_64 (byte-swapped)
        }
        
        is_macho = magic_bytes in MACHO_MAGIC
        
            
        return is_macho
        
    except Exception:
        if debug:
            logging.debug("False (Exception during file check)")
        return False
    
def is_pipx(exec_path: Path | str | None = None, debug: bool = False, suppress_debug: bool = True) -> bool:
    """Checks if the executable is running from a pipx managed environment."""
    exec_path, is_valid = _check_executable_path(exec_path, debug and not suppress_debug, check_pipx=False)
    # check_pipx arg should be false when calling from inside of is_pipx() to avoid recursion error
    # For safety, _check_executable_path() guards against this.
    if not is_valid:
        return False
        
    try:
        interpreter_path = Path(sys.executable).resolve()
        pipx_bin_path, pipx_venv_base_path = _get_pipx_paths()

        # Normalize paths for comparison
        norm_exec_path = str(exec_path).lower()
        norm_interp_path = str(interpreter_path).lower()
        pipx_venv_base_str = str(pipx_venv_base_path).lower()

        if debug:
            logging.debug(f"EXEC_PATH: {exec_path}")
            logging.debug(f"INTERP_PATH: {interpreter_path}")
            logging.debug(f"PIPX_BIN_PATH: {pipx_bin_path}")
            logging.debug(f"PIPX_VENV_BASE: {pipx_venv_base_path}")
            is_in_pipx_venv_base = norm_interp_path.startswith(pipx_venv_base_str)
            logging.debug(f"Interpreter path resides somewhere within the pipx venv base hierarchy: {is_in_pipx_venv_base}")
            logging.debug(
                f"This determines whether the current interpreter is managed by pipx: {is_in_pipx_venv_base}"
            )
        if "pipx/venvs" in norm_exec_path or "pipx/venvs" in norm_interp_path:
            if debug:
                logging.debug("is_pipx() is True // Signature Check")
            return True

        if norm_interp_path.startswith(pipx_venv_base_str):
            if debug:
                logging.debug("is_pipx() is True // Interpreter Base Check")
            return True

        if norm_exec_path.startswith(pipx_venv_base_str):
            if debug:
                logging.debug("is_pipx() is True // Executable Base Check")
            return True

        if debug:
            logging.debug("is_pipx() is False")
        return False

    except Exception:
        if debug:
            logging.debug("False (Exception during pipx check)")
    
def is_python_script(path: Path | str | None = None, debug: bool = False, suppress_debug: bool =False) -> bool:
    """
    Checks if the specified path or running script is a Python source file (.py).

    By default, checks the running script (`sys.argv[0]`). If a specific `path` is
    provided, checks that path instead. Uses `Path.resolve()` for stable path handling.

    Args:
        path: Optional; path to the file to check (str or Path). If None, defaults to `sys.argv[0]`.
        debug: If True, prints the path being checked.

    Returns:
        bool: True if the specified or default path is a Python source file (.py); False otherwise.
    """
    exec_path, is_valid = _check_executable_path(path, debug and not suppress_debug, check_pipx=False)
    if not is_valid:
        return False
    return exec_path.suffix.lower() == '.py'    

# --- Interpreter Check ---

def interp_path(debug: bool = False) -> str:
    """
    Returns the path to the Python interpreter binary and optionally prints it.

    This function wraps `sys.executable` to provide the path to the interpreter
    (e.g., '/data/data/com.termux/files/usr/bin/python3' in Termux or the embedded
    interpreter in a frozen executable). If the path is empty (e.g., in some embedded
    or sandboxed environments), an empty string is returned.

    Args:
        print_path: If True, prints the interpreter path to stdout.

    Returns:
        str: The path to the Python interpreter binary, or an empty string if unavailable.
    """
    path = sys.executable
    if debug:
        logging.debug(f"Python interpreter path: {path}")
    return path

# --- TTY Check ---
def interactive_terminal_is_available():
    """
    Check if the script is running in an interactive terminal. 
    Assumpton: 
        If interactive_terminal_is_available() returns True, 
        then typer.prompt() or input() will work reliably,
        without getting lost in a log or lost entirely.
    
    """
    # Check if a tty is attached to stdin
    return sys.stdin.isatty() and sys.stdout.isatty()

    
# --- Browser Check ---
def web_browser_is_available() -> bool:
    """ Check if a web browser can be launched in the current environment."""
    try:
        # 1. Standard Python check
        webbrowser.get()
        return True
    except webbrowser.Error:
        # Fallback needed. Check for external launchers.
        # 2. Termux specific check
        if on_termux() and shutil.which("termux-open-url"):
            return True
        # 3. General Linux check
        if shutil.which("xdg-open"):
            return True
        return False
    
# --- LAUNCH MECHANISMS BASED ON ENVIRONMENT ---
def edit_textfile(path: Path | str | None = None) -> None:
#def open_text_file_for_editing(path): # defunct function name as of 1.0.16
    """
    Opens a file with the environment's default application (Windows, Linux, macOS)
    or a guaranteed console editor (nano) in constrained environments (Termux, iSH).
    Ensures line-ending compatibility where possible.

    This function is known to fail on PyDroid3, where on_linus() is True but xdg-open 
    is not available.
    """
    if path is None:
        return
    
    path = Path(path).resolve()

    try:
        if on_windows():
            os.startfile(path)
        elif on_termux():
    	    # Install dependencies if missing (Termux pkg returns non-zero if already installed, so no check=True)
            subprocess.run(['pkg','install', 'dos2unix', 'nano'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            _run_dos2unix(path)
            subprocess.run(['nano', str(path)])
        elif on_ish_alpine():
            # Install dependencies if missing (apk returns 0 if already installed, so check=True is safe)
            subprocess.run(['apk','add', 'dos2unix'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            subprocess.run(['apk','add', 'nano'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            _run_dos2unix(path)
            subprocess.run(['nano', str(path)])
    	# --- Standard Unix-like Systems (Conversion + Default App) ---
        elif on_linux():
            _run_dos2unix(path) # Safety conversion for user-defined console apps
            subprocess.run(['xdg-open', str(path)])
        elif on_apple():
            _run_dos2unix(path) # Safety conversion for user-defined console apps
            subprocess.run(['open', str(path)])
        else:
            print("Unsupported operating system.")
    except Exception as e:
        print("The file could not be opened for editing in the current environment: {e}")
    """
    Why Not Use check=True on Termux:
    The pkg utility in Termux is a wrapper around Debian's apt. When you run pkg install <package>, if the package is already installed, the utility often returns an exit code of 100 (or another non-zero value) to indicate that no changes were made because the package was already present.
    """

# --- Helper Functions ---    
def _run_dos2unix(path: Path | str | None = None):
    """Attempt to run dos2unix, failing silently if not installed."""
    
    path = Path(path).resolve()

    try:
        # We rely on shutil.which not being needed, as this is a robust built-in utility on most targets
        # The command won't raise an exception unless the process itself fails, not just if the utility isn't found.
        # We also don't use check=True here to allow silent failure if the utility is missing (e.g., minimalist Linux).
        subprocess.run(['dos2unix', path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        # This will be raised if 'dos2unix' is not on the system PATH
        pass 
    except Exception:
        # Catch other subprocess errors (e.g. permission issues)
        pass
    
def read_magic_bytes(path: str, length: int = 4, debug: bool = False) -> bytes | None:
    """Return the first few bytes of a file for type detection.
    Returns None if the file cannot be read or does not exist.
    """
    try:
        with open(path, "rb") as f:
            magic = f.read(length)
        if debug:
            logging.debug(f"Magic bytes: {magic!r}")
        return magic
    except Exception as e:
        if debug:
            logging.debug(f"False (Error during file check: {e})")
        #return False # not typesafe
        #return b'' # could be misunderstood as what was found
        return None # no way to conflate that this was a legitimate error
    
def _get_pipx_paths():
    """
    Returns the configured/default pipx binary and home directories.
    Assumes you indeed have a pipx dir.
    """
    # 1. PIPX_BIN_DIR (where the symlinks live, e.g., ~/.local/bin)
    pipx_bin_dir_str = os.environ.get('PIPX_BIN_DIR')
    if pipx_bin_dir_str:
        pipx_bin_path = Path(pipx_bin_dir_str).resolve()
    else:
        # Default binary path (common across platforms for user installs)
        pipx_bin_path = Path.home() / '.local' / 'bin'

    # 2. PIPX_HOME (where the isolated venvs live, e.g., ~/.local/pipx/venvs)
    pipx_home_str = os.environ.get('PIPX_HOME')
    if pipx_home_str:
        # PIPX_HOME is the base, venvs are in PIPX_HOME/venvs
        pipx_venv_base = Path(pipx_home_str).resolve() / 'venvs'
    else:
        # Fallback to the modern default for PIPX_HOME (XDG standard)
        # Note: pipx is smart and may check the older ~/.local/pipx too
        # but the XDG one is the current standard.
        pipx_venv_base = Path.home() / '.local' / 'share' / 'pipx' / 'venvs'

    return pipx_bin_path, pipx_venv_base.resolve()


def _check_if_zip(path: Path | str | None) -> bool:
    """Checks if the file at the given path is a valid ZIP archive."""
    if path is None:
        return False
    path = Path(path).resolve()

    try:
        return zipfile.is_zipfile(path)
    except Exception:
        # Handle cases where the path might be invalid, or other unexpected errors
        return False

def _check_executable_path(exec_path: Path | str | None, 
                           debug: bool = False, 
                           check_pipx: bool = True
) -> tuple[Path | None, bool]: #compensate with __future__, may cause type checker issues
    """
    Helper function to resolve an executable path and perform common checks.

    Returns:
        tuple[Path | None, bool]: (Resolved path, is_valid)
        - Path: The resolved Path object, or None if invalid
        - bool: Whether the path should be considered valid for subsequent checks
    """
    # 1. Determine path
    if exec_path is None:
        exec_path = Path(sys.argv[0]).resolve() if sys.argv[0] and sys.argv[0] != '-c' else None
    else:
        exec_path = Path(exec_path).resolve()

    if debug:
        logging.debug(f"Checking executable path: {exec_path}")

    # 2. Handle missing path
    if exec_path is None:
        if debug:
            logging.debug("_check_executable_path() returns (None, False) // exec_path is None")
        return None, False
    
    # 3. Ensure path actually exists and is a file
    if not exec_path.is_file(): 
        if debug:
            logging.debug("_check_executable_path() returns (exec_path, False) // exec_path is not a file")
        return exec_path, False

    # 4. Avoid recursive pipx check loops
    # This guard ensures we don’t recursively call _check_executable_path()
    # via is_pipx() -> _check_executable_path() -> is_pipx() -> ...
    if check_pipx:
        caller = sys._getframe(1).f_code.co_name
        if caller != "is_pipx":
            if is_pipx(exec_path, debug):
                if debug:
                    logging.debug("_check_executable_path() returns (exec_path, False) // is_pipx(exec_path) is True")
                return exec_path, False

    return exec_path, True       
 

# --- Main Function for report and CLI compatibility ---

def main(path=None, debug=False):
    """Print a comprehensive environment report.

    Args:
        path (Path | str | None): Path to inspect (defaults to sys.argv[0]).
        debug (bool): Enable verbose debug output.
    """
    if debug:
        logging.basicConfig(level=logging.DEBUG)
        logging.getLogger('matplotlib').setLevel(logging.WARNING)  # Suppress matplotlib debug logs
    print("================================")
    print("======= PyHabitat Report =======")
    print("================================")
    print("\nCurrent Build Checks ")
    print("# // Based on hasattr(sys,..) and getattr(sys,..)")
    print("------------------------------")
    print(f"in_repl(): {in_repl()}")
    print(f"as_frozen(): {as_frozen()}")
    print(f"as_pyinstaller(): {as_pyinstaller()}")
    print("\nOperating System Checks")
    print("# // Based on platform.system()")
    print("------------------------------")
    print(f"on_windows(): {on_windows()}")
    print(f"on_apple(): {on_apple()}")
    print(f"on_linux(): {on_linux()}")
    print(f"on_wsl(): {on_wsl()}")
    print(f"on_android(): {on_android()}")
    print(f"on_termux(): {on_termux()}")
    print(f"on_pydroid(): {on_pydroid()}")
    print(f"on_ish_alpine(): {on_ish_alpine()}")
    print(f"on_freebsd(): {on_freebsd()}")
    print("\nCapability Checks")
    print("-------------------------")
    print(f"tkinter_is_available(): {tkinter_is_available()}")
    print(f"matplotlib_is_available_for_gui_plotting(): {matplotlib_is_available_for_gui_plotting()}")
    print(f"matplotlib_is_available_for_headless_image_export(): {matplotlib_is_available_for_headless_image_export()}")
    print(f"web_browser_is_available(): {web_browser_is_available()}")
    print(f"interactive_terminal_is_available(): {interactive_terminal_is_available()}")
    print("\nInterpreter Checks")
    print("# // Based on sys.executable()")
    print("-----------------------------")
    print(f"interp_path(): {interp_path()}")
    if debug:
        # Do these debug prints once to avoid redundant prints
        # Supress redundant prints explicity using suppress_debug=True, 
        # so that only unique information gets printed for each check, 
        # even when more than one use the same functions which include debugging logs.
        #print(f"_check_executable_path(interp_path(), debug=True)")
        _check_executable_path(interp_path(), debug=debug)    
        #print(f"read_magic_bites(interp_path(), debug=True)")
        read_magic_bytes(interp_path(), debug=debug)
    print(f"is_elf(interp_path()): {is_elf(interp_path(), debug=debug, suppress_debug=True)}")
    print(f"is_windows_portable_executable(interp_path()): {is_windows_portable_executable(interp_path(), debug=debug, suppress_debug=True)}")
    print(f"is_macos_executable(interp_path()): {is_macos_executable(interp_path(), debug=debug, suppress_debug=True)}")
    print(f"is_pyz(interp_path()): {is_pyz(interp_path(), debug=debug, suppress_debug=True)}")
    print(f"is_pipx(interp_path()): {is_pipx(interp_path(), debug=debug, suppress_debug=True)}")
    print(f"is_python_script(interp_path()): {is_python_script(interp_path(), debug=debug, suppress_debug=True)}")
    print("\nCurrent Environment Check")
    print("# // Based on sys.argv[0]")
    print("-----------------------------")
    inspect_path = path if path is not None else (None if sys.argv[0] == '-c' else sys.argv[0])
    logging.debug(f"Inspecting path: {inspect_path}")
    # Early validation of path
    if path is not None:
        path_obj = Path(path)
        if not path_obj.is_file():
            print(f"Error: '{path}' is not a valid file or does not exist.")
            if debug:
                logging.error(f"Invalid path: '{path}' is not a file or does not exist.")
            raise SystemExit(1)
    script_path = None
    if path or (sys.argv[0] and sys.argv[0] != '-c'):
        script_path = Path(path or sys.argv[0]).resolve()
    print(f"sys.argv[0] = {str(sys.argv[0])}")
    if script_path is not None:
        print(f"script_path = {script_path}")
        if debug:
            # Do these debug prints once to avoid redundant prints
            # Supress redundant prints explicity using suppress_debug=True, 
            # so that only unique information gets printed for each check, 
            # even when more than one use the same functions which include debugging logs.
            #print(f"_check_executable_path(script_path, debug=True)")
            _check_executable_path(script_path, debug=debug)
            #print(f"read_magic_bites(script_path, debug=True)")
            read_magic_bytes(script_path, debug=debug)
        print(f"is_elf(): {is_elf(script_path, debug=debug, suppress_debug=True)}")
        print(f"is_windows_portable_executable(): {is_windows_portable_executable(script_path, debug=debug, suppress_debug=True)}")
        print(f"is_macos_executable(): {is_macos_executable(script_path, debug=debug, suppress_debug=True)}")
        print(f"is_pyz(): {is_pyz(script_path, debug=debug, suppress_debug=True)}")
        print(f"is_pipx(): {is_pipx(script_path, debug=debug, suppress_debug=True)}")
        print(f"is_python_script(): {is_python_script(script_path, debug=debug, suppress_debug=True)}")
    else:
        print("Skipping: ") 
        print("    is_elf(), ")
        print("    is_windows_portable_executable(), ")
        print("    is_macos_executable(), ")
        print("    is_pyz(), ")
        print("    is_pipx(), ") 
        print("    is_python_script(), ")
        print("All False, script_path is None.")
    print("")
    print("=================================")
    print("=== PyHabitat Report Complete ===")
    print("=================================")
    print("")

if __name__ == "__main__": 
    main(debug=True)