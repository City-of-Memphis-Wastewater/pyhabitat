# Changelog

All notable changes to this project will be documented in this file.

The format is (read: strives to be) based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

---

## [1.1.38] - 2026-02-11
### Added:
- environment.get_interp_shebang(), for use in identifying the python interpreter, like for the -p flag in shiv/zipapp.
- Use get_interp_shebang() in build_pyz.py

### Changed:
- Remove bump-my-version. Too many dependencies. While it wouldn't necessarily trickle into my dependency tree, it is too risky for something so basic.

---

## [1.1.33] - 2026-01-26
### Fixed:
- Removed VERSION from .gitignore. Wow, what a wild adventure in debugging that resulted in a full CI refactor.


---

## [1.1.29] - 2026-01-26
### Added:
- Use `bump-my-version` and add section to pyproject.toml

### Fixed:
- Troubleshoot version numbering

---

## [1.1.27] - 2026-01-26
### Added:
- `is_in_git_repo()` adjusting to be tri-state (to return None if git is not installed or otherwise cannot be called with subprocess.run())

### Changed:
- versioning now uses src/pyhabitat/VERSION as king, the source of truth, or first importlib if pyhabitat is installed. 

---

## [1.1.26] - 2026-01-21
### Added:
- `is_in_git_repo()` command added to environment.py;

### Removed:
- Get rid of errors in pyproject.toml: long description of markdown file, author, and author-email

---

## [1.1.24] - 2026-01-19
### Fixed:
- Use functools.lru_cache to add backport functionality for 3.7, @cache

---

## [1.1.23] - 2026-01-18
### Fixed:
- in tkinter_is_available(), return False if on_linux() and not os.environ.get("DISPLAY").

---

## [1.1.22] - 2026-01-18
### BREAKING
- `os_apple()` → `on_macos()`
- The old version of on_apple() would be true if on_ish_alpine(); os_macos() does not do this.

---

## [1.1.21] - 2026-01-17
### Fixed:
- Add missing comma in __all__ list in enviroment.py
- Remove duplicate keyword section in pyproject.toml.

---

## [1.1.19] - 2026-01-17
### Internal:
- Demonstrate Git Actions

---

## [1.1.18] - 2026-01-16
### Fixed:
- Logic chain was broken by an erroneous if that should have been an elif.

---

## [1.1.17] - 2026-01-16
### Fixed:
- In show_system_explorer(), correct Path and str order of conversion for that it doesnt trip. Default to None and allow str or Path as inputs.

### Internal:
- We are finally building.

---

## [1.1.16] - 2026-01-16
### Fixed:
- Alter the sanity check in build.yml to test each of the build artifacts with the --debug flag, rather than trying to reference the nonexistent whl, now that we no longer use uv build.


---

## [1.1.15] - 2026-01-16
### Fixed:
In build_pyz.py, because we have a nested export folder, we need: DIST_DIR.mkdir(exist_ok=True) -> DIST_DIR.mkdir(parents=True, exist_ok=True)

---

## [1.1.14] - 2026-01-16
### Fixed:
- Separate build.yml and publish.yml; PyPI really wanted to check the dist/ folder for everything.

---

## [1.1.13] - 2026-01-16
### Fixed:
- Ensure that PyPI publish does not try to validate the PYZ or the EXE, use dist/zipapp/ and dist/onefile/
- Ensure that build_executiable.py PyInstaller call knows where to send the output, with the `--distpath` flag.

---

## [1.1.11] - 2026-01-16
### Fixed:
- clean() -> clean_build_folder(), and repositioned, in build_executable.py

---

## [1.1.10] - 2026-01-16
### Fixed:
- publish.yml needs some love for how uv is leveraged; be consistent and use `uv sync --group dev`.

---

## [1.1.9] - 2026-01-16
### Added:
- environment.show_system_explorer(). Migrated from the pdflinkcheck package.
- Dev dependencies
- pyproject.toml details
- Logo :)

### Changed:
- publish.yml now leverages uv and also builds the EXE and PYZ and then uploads the artifacts to the release.

---

## [1.1.8] - 2026-01-15
### Changed:
- Make edit_textfile() always use system notepad for msix packages
- If dos2unix fails on termux, fall back to installing and then running, in edit_textfile(). Before, it tried to install every time.
- If dos2unix and nano fails on ish-alpine-ios, fall back to installing and then running, in edit_textfile(). Before, it tried to install every time.

---

## [1.1.7] - 2026-01-13
### Fixed:
- Updated version_info.py so that non-pyhabitat pyproject.toml files can be used to identify the version of pyhabitat.
- Improve version_info.get_package_name() to leverage the PIP_PACKAGE_NAME if pyproject.toml is not found.

---

## [1.1.6] - 2026-01-12
- Simplify environment.edit_textfile(). Now it will only use the surefire opening tools os.startfile, and if that files (very rare) notepad.exe. Remove the bloat of explicitly listing common third party editors; these will never hit anyways, and are brittle. Ensure that Exceptions will print.
- Ensure path resolutions for windows in edit_texfile(), for safe useage from an MSIX package.

---

## [1.1.2] - 2025-12-27
### Added
- More robust Windows file handling in environment.edit_textfile(), to handle commonly unassociated files like JSON. Default notepad.exe is the first in the try list, which will always succeed. So why have the other text editors in a try list? Documentation mostly, and maybe future work.

### Internal
- an old copy of environment.py was still active in the IDE and saved at a defunct path. This has been destroyed.

### Changed
- File naming: report.py -> reporting.py, to avoid a naming collision with reporting.report(), especially because __init__.py raising report() to the top level.

### Fixed:
- Instead of wildcard imports in reporting.py, use `from pyhabitat import environment as env` and then a `env.on_termux()` prefix, for example. 

---

## [1.1.1] - 2025-12-26
### Added
- Implemented a `src/` layout to improve package isolation and follow modern Python packaging best practices.
- Moved `__main__.py` into the package namespace to support `python -m pyhabitat` execution.
- Added a prioritized "Editor Ladder" to `edit_textfile` that favors lightweight standalone editors (gedit, mousepad, kate) over heavy IDEs (VS Code) to prevent workspace pollution.

### Changed
- Refactored `build_pyz.py` and `build_executable.py` to support the new `src/` directory structure.
- Enhanced `edit_textfile` logic to provide a robust fallback to `nano` when `xdg-open` or GUI editors are unavailable, preventing shell crashes in headless environments.
- Updated `pyproject.toml` to use `setuptools` find-package logic within the `src` directory.
    
### Fixed
- Resolved a "bad interpreter" error in WSL caused by CRLF-encoded Windows shims taking priority over Linux binaries.
- Corrected a PyInstaller argument ordering bug in the executable build script.    
- Suppressed `xdg-open` error noise when system-level mailcap rules or file associations are missing.

---

## [1.0.52] - 2025-12-10
### Added:
- Add SystemInfo to the pyhabitat.__init__

---

## [1.0.51] - 2025-12-10

### Added:
- `.github/workflows/docker.yml`

---

## [1.0.48] - 2025-12-09

### Fixed:
- Version checks had relied on read_text(), which is no good for binaries. 
- Ensure that a VERSION file is placed in the build/ directory, and referenced properly with `f"--add-data={version_file.resolve()}:."`

---


## [1.0.47] - 2025-12-09

### Fixed:
- Clean up spare imports from utils.
- Remove "GUI" as a keyword in the pyproject.toml.

### Removed:
- Remove the utils.py file after improving and migrating all contents to version_info.py.
- Remove build_pyz.ps1 and build_pyz.sh.


---

## [1.0.46] - 2025-12-09

### Changed:
- Alter get_package_version code to work in the [project] context.
- Migrate all version code to version_info.py

---

## [1.0.42] - 2025-11-27

### Changed:
- Alter build_executible.py to build .spec files in /build/ and to not inclue tkinter or matplotlib in the pyinstaller build.

---

## [1.0.42] - 2025-11-27

### Changed:
- Converted globals in environment.py nto functools.cache decorator, as the mechanism to prevent rechecking.
- Allow matplotlbit checks to be compatible with QtAgg or Gtk3Agg rather than forcing TkAgg.

### Added:
- can_spwan_shell_lite(). Supposedly it is a complete breakfast but we will see.
- `--clear-cache` arg added to CLI to forcibly clear the functools.cache elements.
- pyhabitat.environment.clear_all_caches(), which is called by the `--clear-cache` CLI flag. 

### Removed:
- can_read_input(). Why? It was malformed and not useful for contributing to the can_spawn_shell() check.

---

## [1.0.40] - 2025-11-24

### Fixed: 
- Added import of ./pyhabitat/system_info.py, ./pyhabitat/version_info.py, and ./pyhabitat/report.py to the files that are copied during the PYZ creation, for build_pyz.py and build_pyz.sh.
- This resolves the reference issues when running the PYZ.

---

## [1.0.38] - 2025-11-24

### Fixed:
- Nano fallback for on_linx() if xdg-open fails (like for WSL), in edit_textfile()

---

## [1.0.37] - 2025-11-10

### Added:
- Build guidance section in README.md for running `python -m build`, `python build_executable.py`, and `python build_pyz.py`.

### Fixed:
- Use get_version() in build_executible.py. 
- Ensure that ./dist/ is not destroyed for each run of build_executible.py and build_pyz.py
- Ensure proper library availability for report.py and for build_pyz.py, which were missing Path.

---

## [1.0.36] - 2025-11-10

### Added:
- Dedicated report.py file.
- build_executible.py

### Fixed:
- Report will stay open unless in_repl() or sys.flags.interactive.

---

## [1.0.35] - 2025-10-28

### Added:
- In user_darrin_deyoung(), add logic to enable manual setting
of env var  `export USER_DARRIN_DEYOUNG=True` to enable testing.
- Default to empty string if env var USER_DARRIN_DEYOUNG is not found.
- build_pyz.py file for building .pyz (use python -m build for .tar.gz and .whl)
- build.ps1 -> build_pyz.ps1, build.sh -> build_pyz.sh  

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
