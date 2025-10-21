#from .cli import run_cli

from .environment import (
    in_repl,
    on_termux,
    on_windows,
    on_apple,
    on_linux,
    on_ish_alpine,
    on_android,
    on_freebsd,
    is_elf,
    is_windows_portable_executable,
    is_macos_executable,
    is_pyz,
    is_pipx,
    is_python_script,
    as_frozen,
    as_pyinstaller,
    interp_path,
    tkinter_is_available,
    matplotlib_is_available_for_gui_plotting,
    matplotlib_is_available_for_headless_image_export,
    web_browser_is_available,
    interactive_terminal_is_available
)

def main():
    print("PyHabitat Environment Report")
    print("===========================")
    print("\nInterpreter Checks // Based on sys.executable()")
    print("-----------------------------")
    print(f"interp_path(): {interp_path()}")
    print(f"is_elf(interp_path()): {is_elf(interp_path())}")
    print(f"is_windows_portable_executable(interp_path()): {is_windows_portable_executable(interp_path())}")
    print(f"is_macos_executable(interp_path()): {is_macos_executable(interp_path())}")
    print(f"is_pyz(interp_path()): {is_pyz(interp_path())}")
    print(f"is_pipx(interp_path()): {is_pipx(interp_path())}")
    print(f"is_python_script(interp_path()): {is_python_script(interp_path())}")
    print("\nCurrent Environment Check // Based on sys.argv[0]")
    print("-----------------------------")
    print(f"is_elf(): {is_elf()}")
    print(f"is_windows_portable_executable(): {is_windows_portable_executable()}")
    print(f"is_macos_executable(): {is_macos_executable()}")
    print(f"is_pyz(): {is_pyz()}")
    print(f"is_pipx(): {is_pipx()}")
    print(f"is_python_script(): {is_python_script()}")
    print(f"\nCurrent Build Checks // Based on hasattr(sys,..) and getattr(sys,..)")
    print("------------------------------")
    print(f"in_repl(): {in_repl()}")
    print(f"as_frozen(): {as_frozen()}")
    print(f"as_pyinstaller(): {as_pyinstaller()}")
    print("\nOperating System Checks // Based on platform.system()")
    print("------------------------------")
    print(f"on_termux(): {on_termux()}")
    print(f"on_windows(): {on_windows()}")
    print(f"on_apple(): {on_apple()}")
    print(f"on_linux(): {on_linux()}")
    print(f"on_ish_alpine(): {on_ish_alpine()}")
    print(f"on_android(): {on_android()}")
    print(f"on_freebsd(): {on_freebsd()}")
    print("\nCapability Checks")
    print("-------------------------")
    print(f"tkinter_is_available(): {tkinter_is_available()}")
    print(f"matplotlib_is_available_for_gui_plotting(): {matplotlib_is_available_for_gui_plotting()}")
    print(f"matplotlib_is_available_for_headless_image_export(): {matplotlib_is_available_for_headless_image_export()}")
    print(f"web_browser_is_available(): {web_browser_is_available()}")
    print(f"interactive_terminal_is_available(): {interactive_terminal_is_available()}")

if __name__ == "__main__":
    main()
    #run_cli()
