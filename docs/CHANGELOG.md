# Changelog

All notable changes to this project will be documented in this file.

The format is (read: strives to be) based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).


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