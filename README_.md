# pyhabitat 🧭

**Lightweight Python library for accurate build & environment introspection**

Stop writing fragile `sys.platform` / env-var soup.  
`pyhabitat` gives clean, reliable answers to:

- Which OS / mobile environment am I on?  
- Am I frozen (PyInstaller), zipapp, pipx, normal script…?  
- Can I actually pop up a GUI window here?

Strong detection for **Termux**, **iSH**, **WSL**, **Pydroid**, etc.

[→ GitHub](https://github.com/City-of-Memphis-Wastewater/pyhabitat)

<p align="center">
  <img src="https://raw.githubusercontent.com/City-of-Memphis-Wastewater/pyhabitat/main/assets/pyhabitat-ico-alpha.png" width="180">
</p>

## Quick Install

```bash
pip install pyhabitat
```

## Core Questions Answered

```python
import pyhabitat as ph

ph.on_termux()          # True in Termux (Android)
ph.on_ish_alpine()      # True in iSH (iOS)
ph.on_wsl()             # True in WSL/WSL2
ph.as_frozen()          # True for PyInstaller / cx_Freeze / etc.
ph.is_pipx()            # True when run from pipx-installed tool
ph.tkinter_is_available()           # Can we open real GUI windows?
ph.matplotlib_is_available_for_gui_plotting()  # Interactive plots ok?
```

## Main Detection Groups

### OS & Special Environments

```python
on_windows / on_apple / on_linux / on_freebsd
on_wsl / on_termux / on_ish_alpine / on_android / on_pydroid
in_repl
```

### Build / Packaging State

Accepts optional `path=` (defaults to `sys.argv[0]`)

```python
as_frozen / as_pyinstaller
is_python_script / is_pipx / is_pyz
is_elf / is_windows_portable_executable / is_macos_executable
is_msix
```

### Capabilities

```python
tkinter_is_available()
matplotlib_is_available_for_gui_plotting(termux_has_gui=False)
matplotlib_is_available_for_headless_image_export()
interactive_terminal_is_available()
web_browser_is_available()
```

### Handy Utilities

```python
ph.edit_textfile("config.toml")           # opens in default editor / nano
ph.show_system_explorer()                 # opens current folder in explorer/finder/etc
ph.interp_path()                          # path to current python interpreter
ph.report()                               # print nice summary of everything
```

## Quick Wins / Typical Use Cases

```python
# Adaptive plotting strategy
if ph.matplotlib_is_available_for_gui_plotting(termux_has_gui=True):
    # interactive window
    plt.show()
else:
    # save to file
    plt.savefig("result.png")

# Different help text / behavior in mobile environments
if ph.on_termux() or ph.on_ish_alpine():
    print("Running in mobile Linux — some features limited")
```

Run the built-in report:

```bash
python -m pyhabitat
# or
import pyhabitat; pyhabitat.report()
```

## Motivation

We build tools that actually run usefully on phones (Termux and iSH), laptops, servers, and distribution in the app store — without dozens of brittle platform checks.

Made with ❤️ by people who want their CLIs **work** everywhere, their builds to jump through all the hoops, and their GUIs to know when to stay home.

MIT licensed • Contributions welcome for new environments!
