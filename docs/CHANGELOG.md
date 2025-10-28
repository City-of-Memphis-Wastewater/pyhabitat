# Changelog

All notable changes to this project will be documented in this file.

The format is (read: strives to be) based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).


---

## [1.0.31] - 2025-10-28

### Added:
- In user_darrin_deyoung(), add logic to enable manual setting
of env var  `export USER_DARRIN_DEYOUNG=True` to enable testing.
- Default to empty string if env var USER_DARRIN_DEYOUNG is not found.

### Fixed:
- interactive_terminal_is_available() false negative resolved by using "exit 0" for can_spawn_shell() test rather than "echo hello".
- Implement section in can_read_input() to do microsoft specific check with msvcrt.kbhit().
- Change order of interactive_terminal_is_available() so that not (sys.stdin.isatty() and sys.stdout.isatty()) returns False quickly.
- Remove license classifer from from pyproject.toml, as per PEP 621/639. Keep dedicated license line.

---

## [1.0.30] - 2025-10-25

### Active
- Better solution in main() or run_cli() or __main__() to handle new window quick closure.
- is_binary() and is_ascii()

### Fixed:
-  False negative corrected in interactive_terminal_is_availsble(): 
Suppress use of can_read_input() in check for interactivr_terminal_is_available(), 
because a non-boolean is involved, and I don't understand the select library.
 The function should  already be sufficient for our purposes at this time, though checking for reading accurately is desired. 

---

## [1.0.29] - 2025-10-25

###  BREAKING:
- Move files back into pyhabitat directory, but keep __main__.py in root. 
- For building, .build.sh copies files to pyhabitat-build dir and keep this relative organization - there is a pyhabitat-build/pyhabitat/ directory.

### Running:
- In development, run code with:
    - python .
    - python . --help
    - python . on_termux
- PYZ:
    - python ./pyhabitat-1.0.29.pyz --list
    
---

## [1.0.28] - 2025-10-25

### Fixed:
- 'import __init__ as pyhabitat' in cli.py to enable --list and command for.pyz.
---

## [1.0.27] - 2025-10-25

### BREAKING:
- All files from ./pyhabitat migrated to root.

### Fixed:
- PYZ file should now not fail because it tries to.import explicitly from the pyhabitat dir

### Added:
- build.sh isolates the zipapp build from the .git and .github dirs.

---

## [1.0.26] - 2025-10-25

### Fixed:
- Exit with return after each CLI subcommand, to precent entire report from also printing and burying the single intent.
---

## [1.0.25] - 2025-10-25

### Fixed:
- Bool check for text match in user_darrin_deyoung() should be "==" instead of "!="

---

## [1.0.24] - 2025-10-25

### Added:
- Add functions user_darrin_deyoung() for checking if the computer is a windows demo unit. 
- Add functions can_spawn_shell() and can_read_input(), for more rigorous interactive console checking beyond the existing TTY check.
- (Try to) make all funcrions individually available through the CLI based on argparse.
- Implement globals _CAN_READ_INPUT and _CAN_SPAWN_SHELL to capture boolean on the first run of these functions to avoid repetitive checking and overhead - use override_known arg to allow user to recheck within the same session.
- Add .pyz check at the bottom of main(), to stay open after report; this is non rigprous but fine for testing


---

## [1.0.22] – 2025-10-24

### Fixed:
- Ensure magic_bytes is not None before checking string. This was a consciis choice to be explicit on both ends about None rather than b'' indicating that an empty string eas found. also wrap the whole thing in try except just for safety. is_windows_portable_executable().

---

## [1.0.21] – 2025-10-22

### Fixed:
- Fix erroneous comment character in environment.py. 
- Redundant logic hanging on after return in is_pipx().
- Improved is_pipx() print statements to be more aesthetic and useful.
- Improve string handling in is_pipx() by added variable pipx_venv_base_str.
- Return None rther than False for no match from read_magic_bytes. This is now reflected in the output type hinting. 

### Added:
- Add build phase to publish.yaml for assurance.
- Add caller checking as a guard in _check_executable_path() to avoid recusrive loops with is_pipx().
- Add version flag to CLI.

---

## [1.0.20] – 2025-10-22

### Fixed
- Improve stability of on_wsl() - testing revealed permission denied issues for /prove/version/ which did not handle gracefully.

---

## [1.0.19] – 2025-10-22

### Added
- `read_magic_bytes()`: Consolidates existing logic for inspecting executable magic bytes.
- `suppress_debugging` argument in path/executable check functions (e.g., `is_elf()`, `is_pyz()`) to optionally suppress debug logging.
- New debug messages for interpreter path checks, including its relation to the pipx virtual environment base.
- **New Functions**: `on_wsl()` and `on_pydroid()`.
- `main()` now reports `on_wsl()` and `on_pydroid()` status for improved environment visibility.

### Changed
- Consolidated repeated interpreter and path-based checks in `main()`.
- Refined `is_pipx()` logging to clearly indicate whether the current interpreter resides somewhere within the pipx venv hierarchy (previously checked, now more transparent in debug output).
- Clarified debug messages for interpreter hierarchy:
  `Interpreter path resides somewhere within the pipx venv base hierarchy` — accurately reflects nested paths.

### Fixed
- Removed redundant debug outputs for magic bytes and path checks in `main()` when already logged.

---

## [1.0.18] - 2025-10-21
- Fixed debug log in `main()` to consistently show `Inspecting path: None` for `python -c` when `path=None`.
- Fixed `-c` handling in `main()` to set `script_path = None` when `sys.argv[0] == '-c'`.
- Restored debug statements by passing `debug=True` to check functions in `main()`.
- Added debug logging for `magic_bytes` in `is_elf`.
- Consolidated path resolution and checks into `_check_executable_path` helper.
- Fixed `pipx install` by ensuring local installation with `pipx install .`.
- Added CLI support with cli.py, changing __main__.py entirely, migrating main() to environment.py, and adding the necessary elements in pyroject.toml.

---

## [1.0.17] - 2025-10-21

BREAKING - Most all function names changed.

### Added:
- `__all__` in `environment.py` to explicitly list exported functions, matching `__init__.py`.
- `__main__.py` to enable `python -m pyhabitat` with an environment report.
- `main()` function exposed in `__init__.py` for REPL access (`ph.main()`).
- `in_repl()`: Detects Python interactive REPL using `sys.ps1`.
- `interp_path()`: Returns and optionally prints the Python interpreter path (`sys.executable`).
- `is_python_script(path=None)`: Checks if the script or specified path is a Python source file (.py), defaulting to `sys.argv[0]` with `Path.resolve()`. Useful for `python -m module` or `python script.py`.
- `README.md` usage example for running `main()` via `python -m pyhabitat` or in the REPL.
- `README.md` clarification that path-based functions (`is_pipx`, `is_macos_executable`, `is_elf`, `is_pyz`, `is_windows_portable_executable`) default to `sys.argv[0]` with `Path.resolve()` when `path=None`.

### Changed:
- Renamed functions for consistency:
  - `is_windows()` → `on_windows()`
  - `is_termux()` → `on_termux()`
  - `is_freebsd()` → `on_freebsd()`
  - `is_linux()` → `on_linux()`
  - `is_android()` → `on_android()`
  - `is_apple()` → `on_apple()`
  - `is_ish_alpine()` → `on_ish_alpine()`
  - `is_frozen()` → `as_frozen()`
  - `is_pyinstaller()` → `as_pyinstaller()`
  - `is_repl()` → `in_repl()`
- Implemented `Path.resolve()` for stable path handling in all path-based functions: `is_elf()`, `is_pyz()`, `is_python_script()`, `is_windows_portable_executable()`, `is_macos_executable()`, `is_pipx()`, `edit_textfile()`, `_run_dos2unix()`, `_check_if_zip()`.
- Updated `is_pyz()`: Fixed incomplete logic, renamed parameter to `path`, and ensured `bool` return.
- Updated `edit_textfile()`: Added REPL restriction check and updated docstring.
- Updated docstrings for path-based functions to clarify `Path.resolve()` and optional `path` parameter.
- Updated `README.md`: Added `is_pyz()`, fixed `in_repl()` typo, corrected `edit_textfile()` parameter, added `interp_path()`, `main()`, and `is_python_script()` usage examples, clarified path-based function descriptions with `termux_has_gui=True`, and specified that path-based functions check `sys.argv[0]` (e.g., `pyhabitat/__main__.py` for `python -m pyhabitat`, empty in REPL). Updated section names to match output ("Interpreter Checks", "Current Environment Check", "Current Build Checks", "Operating System Checks").
- Updated `__main__.py`: Aligned output format with user-provided output, added `is_windows_portable_executable`, `is_macos_executable`, `is_python_script`, and `is_python_script(interp_path())` to report, reorganized into "Interpreter Checks", "Current Environment Check", "Current Build Checks", and "Operating System Checks".### Added:
- `__all__` in `environment.py` to explicitly list exported functions, matching `__init__.py`.
- `__main__.py` to enable `python -m pyhabitat` with an environment report.
- `main()` function exposed in `__init__.py` for REPL access (`ph.main()`).
- `in_repl()`: Detects Python interactive REPL using `sys.ps1`.
- `interp_path()`: Returns and optionally prints the Python interpreter path (`sys.executable`).
- `is_python_script(path=None)`: Checks if the script or specified path is a Python source file (.py), defaulting to `sys.argv[0]` with `Path.resolve()`. Useful for `python -m module` or `python script.py`.
- `README.md` usage example for running `main()` via `python -m pyhabitat` or in the REPL.
- `README.md` clarification that path-based functions (`is_pipx`, `is_macos_executable`, `is_elf`, `is_pyz`, `is_windows_portable_executable`) default to `sys.argv[0]` with `Path.resolve()` when `path=None`.

### Changed:
- Renamed functions for consistency:
  - `is_windows()` → `on_windows()`
  - `is_termux()` → `on_termux()`
  - `is_freebsd()` → `on_freebsd()`
  - `is_linux()` → `on_linux()`
  - `is_android()` → `on_android()`
  - `is_apple()` → `on_apple()`
  - `is_ish_alpine()` → `on_ish_alpine()`
  - `is_frozen()` → `as_frozen()`
  - `is_pyinstaller()` → `as_pyinstaller()`
  - `is_repl()` → `in_repl()`
- Implemented `Path.resolve()` for stable path handling in all path-based functions: `is_elf()`, `is_pyz()`, `is_python_script()`, `is_windows_portable_executable()`, `is_macos_executable()`, `is_pipx()`, `edit_textfile()`, `_run_dos2unix()`, `_check_if_zip()`.
- Updated `is_pyz()`: Fixed incomplete logic, renamed parameter to `path`, and ensured `bool` return.
- Updated `edit_textfile()`: Added REPL restriction check and updated docstring.
- Updated docstrings for path-based functions to clarify `Path.resolve()` and optional `path` parameter.
- Updated `README.md`: Added `is_pyz()`, fixed `in_repl()` typo, corrected `edit_textfile()` parameter, added `interp_path()`, `main()`, and `is_python_script()` usage examples, clarified path-based function descriptions with `termux_has_gui=True`, and specified that path-based functions check `sys.argv[0]` (e.g., `pyhabitat/__main__.py` for `python -m pyhabitat`, empty in REPL). Updated section names to match output ("Interpreter Checks", "Current Environment Check", "Current Build Checks", "Operating System Checks").
- Updated `__main__.py`: Aligned output format with user-provided output, added `is_windows_portable_executable`, `is_macos_executable`, `is_python_script`, and `is_python_script(interp_path())` to report, reorganized into "Interpreter Checks", "Current Environment Check", "Current Build Checks", and "Operating System Checks".

---

## [1.0.16] - 2025-10-21

### BREAKING:
- **Rename function**: pyinstaller() -> is_pyinstaller()
- **Rename function**: open_text_file_for_editing() -> edit_textfile()

## Fix:
- Use try/except in edit_textfile() in case of failure (test: failed in Pydroid3)

## Mid-Refactor:
- I want a function like is_interp() or is_repl(). Possibly use Path(sys.executable).resolve(), rather than Path(sys.argv[0]).resolve()

---

## [1.0.15] - 2025-10-20

### Stability Fix:
- **Rectified Broken Function Reference:** All previous versions are considered broken. This is because check_if_zip() was still being referenced frpm pipeline. A line has been added to import zipfile, and the check_if_file() function has been duplicated locally as _check_if_file(). It has not been added to the available functions in __init__.py, because it only does what zipfile.is_zipfile(file_path) does.

---

## [1.0.13] - 2025-10-20

### Stability Fix:
- **Rectified Broken Function Transition:** Version 1.0.11 and 1.0.12 are considered broken and will be redacted due to an incomplete transition of the text editor launching function. The internal code for open_text_file_in_default_app() was not fully migrated to the new name, open_text_file_for_editing(), in the pyhabitat/__init__.py file, leading to runtime errors. This issue has been rectified in 1.0.13.

---

## [1.0.12] - 2025-10-20

### Stability Fix:
- **Rectified Broken Function Transition:** Version 1.0.11 is considered broken and will be redacted due to an incomplete transition of the environment check function. The internal code for is_interactive_terminal() was not fully migrated to the new name, interactive_terminal_is_available(), in the pyhabitat/__init__.py file, leading to runtime errors. This issue has been rectified in 1.0.12.

---

## [1.0.11] - 2025-10-20

### Breaking Change:
- **Function Rename**: The file-opening utility function open_text_file_for_editing() has been renamed to open_text_file_for_editing(). This change accurately reflects the function's behavior in constrained environments (Termux, iSH), where it explicitly enforces the use of the nano editor rather than relying on the user's system default.

### Features & Improvements:
- **Platform Robustness**: Ensured that both the nano text editor and the dos2unix utility are explicitly installed and available in the Termux and iSH Alpine environments before attempting to open a text file.

- **Line Ending Safety**: Confirmed the execution of the dos2unix line-ending conversion on all Unix-like platforms (Linux, macOS, Termux, iSH) to prevent issues when using console editors.

---

## [1.0.9] - 2025-10-20

### Added
- **Folding**: The README now utilizes detail and summary tags to appear more concise and readable.

### Breaking Change
- **Function name**: Renamed `is_interactive_terminal()` to `interactive_terminal_is_available()`. This ensures consistent naming across all capability checks (as opposed to OS identity checks). Call sites must be updated.
