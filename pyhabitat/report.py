import sys
import logging
from pathlib import Path

from .environment import *
def report(path=None, debug=False):
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
    if is_pyz(): # and is_repl(): 
        # Keep window open. This iteration is non rigorous.
        # To address use pf Python launcher from Windows Store to launch downoaded .pyz, which closed quickly
        try:
            input("Press Return to Continue...")
        except Exception as e:
            logging.debug("input() failed")
               