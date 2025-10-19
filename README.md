# pyhabitat 🧭

## A Robust Environment and Build Introspection Library for Python

**`pyhabitat`** is a focused, lightweight library designed to accurately and securely determine the execution context of a running Python script. It provides definitive checks for the Operating System (OS), common container/emulation environments (Termux, iSH), build states (PyInstaller, pipx), and the availability of GUI backends (Matplotlib, Tkinter).

Stop writing verbose `sys.platform` and environment variable checks. Instead, use **`pyhabitat`** to implement architectural logic in your code.

This library is especially useful for leveraging Python in mobile environments, namely `Termux` on Andoird and `iSH` on iOS, which have particular limitations and require special consideration. For example, localhost plotting is a common work-around when `matplotlib` is not available, and web-based interfaces are useful when `tkinter` is not available.

Another key goals is to facilitate the orchestration of wider system installation for `pipx` CLI tools for additonal touch points, like addition to context menus and widgets.  

## 🚀 Features

  * **Definitive Environment Checks:** Rigorous checks catered to Termux and iSH (iOS Alpine). Accurate, typical modern detection for Windows, macOS (Apple), Linux, FreeBSD, Android.
  * **GUI Availability:** Rigorous, cached checks to determine if the environment supports a graphical popup window (Tkinter/Matplotlib TkAgg) or just headless image export (Matplotlib Agg).
  * **Build/Packaging Detection:** Reliable detection of standalone executables built by tools like PyInstaller, and, crucially, correct identification and exclusion of pipx-managed virtual environments, which also user binaries that could conflate the check.
  * **Executable Type Inspection:** Uses file magic numbers (ELF and MZ) to confirm if the running script is a monolithic, frozen binary (non-pipx).

## 📦 Installation

```bash
pip install pyhabitat
```
---

## 📚 API Reference

### OS and Environment

| Function | Description |
| :--- | :--- |
| `is_windows()` | Returns `True` on Windows. |
| `is_apple()` | Returns `True` on macOS (Darwin). |
| `is_linux()` | Returns `True` on Linux in general. |
| `is_termux()` | Returns `True` if running in the Termux Android environment. |
| `is_ish_alpine()` | Returns `True` if running in the iSH Alpine Linux iOS emulator. |
| `is_android()` | Returns `True` on any Android-based Linux environment. |

### Build and Packaging

| Function | Description |
| :--- | :--- |
| `is_frozen()` | Returns `True` if the script is running as a standalone executable (any bundler). |
| `is_pipx()` | Returns `True` if running from a pipx managed virtual environment. |
| `is_elf()` | Checks if the executable is an ELF binary (Linux standalone executable), excluding pipx. |
| `is_windows_portable_executable()` | Checks if the executable is a Windows PE binary (MZ header), excluding pipx. |
| `is_macos_executable()` | Checks if the executable is a macOS/Darwin Mach-O binary, excluding pipx. |

### Capabilities

| Function | Description |
| :--- | :--- |
| `tkinter_is_available()` | Checks if Tkinter is imported and can successfully create a window. |
| `matplotlib_is_available_for_gui_plotting(termux_has_gui=False)` | Checks for Matplotlib and its TkAgg backend, required for interactive plotting. |
| `matplotlib_is_available_for_headless_image_export()` | Checks for Matplotlib and its Agg backend, required for saving images without a GUI. |
| `is_interactive_terminal()` | Checks if standard input and output streams are connected to a TTY (allows safe use of interactive prompts). |
| `web_browser_is_available()` | Check if a web browser can be launched in the current environment (allows safe use of web-based prompts and localhost plotting). 	|

### Actions
| Function | Description |
| :--- | :--- |
| `open_text_file_in_default_app()` | Smoothly opens a text file for editing (for configuration editing prompted by a CLI flag). |

---

## 💻 Usage Examples

The module exposes all detection functions directly for easy access.

### 1\. Checking Environment and Build Type

```python
from pyhabitat import is_termux, is_windows, is_pipx, is_frozen

if is_pipx():
    print("Running inside a pipx virtual environment. This is not a standalone binary.")

elif is_frozen():
    print("Running as a frozen executable (PyInstaller, cx_Freeze, etc.).")

elif is_termux(): 
	# Expected cases: 
	#- pkg install python-numpy python-cryptography
    #- Avoiding matplotlib unless the user explicitly confirms that termux_has_gui=False in matplotlib_is_available_for_gui_plotting(termux_has_gui=False).
	#- Auto-selection of 'termux-open-url' and 'xdg-open' in logic.
	#- Installation on the system, like orchestrating the construction of Termux Widget entries in ~/.shortcuts.
    print("Running in the Termux environment on Android.")
    
elif is_windows():
    print("Running on Windows.")
```

### 2\. Checking GUI and Plotting Availability

Use these functions to determine if you can show an interactive plot or if you must save an image file.

```python
from pyhabitat import matplotlib_is_available_for_gui_plotting, matplotlib_is_available_for_headless_image_export

if matplotlib_is_available_for_gui_plotting():
    # We can safely call plt.show()
    print("GUI plotting is available! Using TkAgg backend.")
    import matplotlib.pyplot as plt
    plt.figure()
    plt.show()

elif matplotlib_is_available_for_headless_image_export():
    # We must save the plot to a file or buffer
    print("GUI unavailable, but headless image export is possible.")
    # Code to use 'Agg' backend and save to disk...
    
else:
    print("Matplotlib is not installed or the environment is too restrictive for plotting.")
```

### 3\. Text Editing

Use this function to smoothly open a text file for editing. 
Ideal use case: Edit a configuration file, if prompted by a CLI command like 'config --textedit'.

```python
open_text_file_in_default_app(filepath=Path('./config.json'))
```
---

## 🤝 Contributing

Contributions are welcome\! If you find an environment or build system that is not correctly detected (e.g., a new container or a specific bundler), please open an issue or submit a pull request with the relevant detection logic.

## 📄 License

This project is licensed under the MIT License. See the LICENSE file for details.