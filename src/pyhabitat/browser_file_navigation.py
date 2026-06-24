# src/pyhabitat/browser_file_navigation.py

from __future__ import annotations

import socket
import subprocess
import sys
from pathlib import Path
from typing import Optional


__all__ = [
    "find_free_port",
    "serve_directory",
]


# Cache the active server so repeated calls don't spawn duplicates.
_server: Optional[subprocess.Popen] = None
_server_port: Optional[int] = None
_server_root: Optional[Path] = None


def find_free_port(host: str = "127.0.0.1") -> int:
    """
    Find an available TCP port on the local machine.

    The returned port is suitable for immediately starting a server.
    """

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((host, 0))
        return sock.getsockname()[1]


def serve_directory(
    path: str | Path,
    *,
    host: str = "127.0.0.1",
    port: Optional[int] = None,
) -> str:
    """
    Serve a directory using Python's built-in HTTP server.

    Reuses an existing server if it is already serving the requested
    directory.

    Parameters
    ----------
    directory
        Directory to serve.
    host
        Interface to bind.
    port
        Optional fixed port. If omitted, a free port is chosen.

    Returns
    -------
    str
        URL of the directory browser.
    """

    global _server, _server_port, _server_root

    directory = path
    directory = Path(directory).expanduser().resolve()

    if not directory.is_dir():
        raise NotADirectoryError(directory)

    # Reuse an existing server if possible.
    if (
        _server is not None
        and _server.poll() is None
        and _server_root == directory
        and _server_port is not None
    ):
        return f"http://{host}:{_server_port}/"

    # Stop previous server.
    if _server is not None and _server.poll() is None:
        _server.terminate()
        try:
            _server.wait(timeout=2)
        except Exception:
            _server.kill()

    if port is None:
        port = find_free_port(host)

    _server = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "http.server",
            str(port),
            "--bind",
            host,
            "--directory",
            str(directory),
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )

    _server_root = directory
    _server_port = port

    return f"http://{host}:{port}/"
