# Changelog

All notable changes to this project will be documented in this file.

The format is (read: strives to be) based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

---

## [1.0.11] - 2025-10-20

### Breaking Change:
- **Function Rename**: The file-opening utility function open_text_file_in_default_app() has been renamed to open_text_file_for_editing(). This change accurately reflects the function's behavior in constrained environments (Termux, iSH), where it explicitly enforces the use of the nano editor rather than relying on the user's system default.

### Features & Improvements:
- **Platform Robustness**: Ensured that both the nano text editor and the dos2unix utility are explicitly installed and available in the Termux and iSH Alpine environments before attempting to open a text file.

- **Line Ending Safety**: Confirmed the execution of the dos2unix line-ending conversion on all Unix-like platforms (Linux, macOS, Termux, iSH) to prevent issues when using console editors.

---

## [1.0.9] - 2025-10-20

### Added
- **Folding**: The README now utilizes detail and summary tags to appear more concise and readable.

### Breaking Change
- **Function name**: Renamed `is_interactive_terminal()` to `interactive_terminal_is_available()`. This ensures consistent naming across all capability checks (as opposed to OS identity checks). Call sites must be updated.