# pyhabitat 🧭

## A Robust Environment and Build Introspection Library for Python

**`pyhabitat`** is a focused, lightweight library designed to accurately and securely determine the execution context of a running Python script. It provides definitive checks for the Operating System (OS), common container/emulation environments (Termux, iSH), build states (PyInstaller, pipx), and the availability of GUI backends (Matplotlib, Tkinter).

Stop writing verbose `sys.platform` and environment variable checks. Instead, use **`pyhabitat`** to implement architectural logic in your code.

## 🚀 Features

  * **Definitive Environment Checks:** Accurate detection for Windows, macOS (Apple), Linux, FreeBSD, Android (general), Termux, and iSH (iOS Alpine).
  * **GUI Availability:** Rigorous, cached checks to determine if the environment supports a graphical popup window (Tkinter/Matplotlib TkAgg) or just headless image export (Matplotlib Agg).
  * **Build/Packaging Detection:** Reliable detection of standalone executables built by tools like PyInstaller, and, crucially, correct identification and exclusion of pipx-managed virtual environments.
  * **Executable Type Inspection:** Uses file magic numbers (ELF and MZ) to confirm if the running script is a monolithic, frozen binary (non-pipx).

## 📦 Installation

```bash
pip install pyhabitat
```

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

## 📚 API Reference

All functions are Boolean checks and are cached after the first call (except for functions that take arguments, like matplotlib\_is\_available\_for\_gui\_plotting).

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

### Capabilities

| Function | Description |
| :--- | :--- |
| `tkinter_is_available()` | Checks if Tkinter is imported and can successfully create a window. |
| `matplotlib_is_available_for_gui_plotting(termux_has_gui=False)` | Checks for Matplotlib and its TkAgg backend, required for interactive plotting. |
| `matplotlib_is_available_for_headless_image_export()` | Checks for Matplotlib and its Agg backend, required for saving images without a GUI. |
| `is_interactive_terminal()` | Checks if standard input and output streams are connected to a TTY (allows safe use of interactive prompts). |

## 🤝 Contributing

Contributions are welcome\! If you find an environment or build system that is not correctly detected (e.g., a new container or a specific bundler), please open an issue or submit a pull request with the relevant detection logic.

## 📄 License

This project is licensed under the MIT License. See the LICENSE file for details.