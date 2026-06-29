"""
pyhabitat.web

Reusable helpers for launching local web applications.

Typical usage
-------------

    from http.server import ThreadingHTTPServer
    from pyhabitat.launch_web import (
        find_open_port,
        launch_browser_when_ready,
    )

    port = find_open_port(8000)

    with ThreadingHTTPServer(("127.0.0.1", port), Handler) as httpd:

        url = f"http://127.0.0.1:{port}/"

        launch_browser_when_ready(url)

        httpd.serve_forever()

The browser is only opened after the server is actually responding,
avoiding arbitrary sleep() delays and startup race conditions.
"""

from __future__ import annotations

import logging
import os
import shutil
import socket
import subprocess
import threading
import time
import urllib.request
import webbrowser

from .environment import on_wsl, on_termux, on_linux

logger = logging.getLogger(__name__)

__all__ = [
    'launch_browser_when_ready',
    'find_open_port',
]

# ----------------------------------------------------------------------
# Port utilities
# ----------------------------------------------------------------------

def find_open_port(
    start: int = 8000,
    host: str = "127.0.0.1",
) -> int:
    """
    Return the first available TCP port at or above ``start``.
    """

    port = start

    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.bind((host, port))
                return port
            except OSError:
                port += 1


# ----------------------------------------------------------------------
# HTTP readiness
# ----------------------------------------------------------------------

def wait_until_http_ready(
    url: str,
    *,
    timeout: float = 5.0,
    poll_interval: float = 0.1,
) -> bool:
    """
    Wait until an HTTP endpoint responds.

    Returns
    -------
    bool
        True if the endpoint became responsive before timeout.
    """

    deadline = time.monotonic() + timeout

    while time.monotonic() < deadline:

        try:
            with urllib.request.urlopen(url, timeout=1):
                return True

        except Exception:
            time.sleep(poll_interval)

    return False


# ----------------------------------------------------------------------
# Browser launching
# ----------------------------------------------------------------------

def launch_browser(url: str) -> bool:
    """
    Open a URL using the best available launcher.

    Returns
    -------
    bool
        True if a launch command was successfully started.
    """

    #
    # Termux
    #

    if on_termux(): # shutil.which("termux-open-url"):

        try:
            subprocess.Popen(
                ["termux-open-url", url],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

            return True

        except Exception:
            logger.exception("termux-open-url failed")

    #
    # WSL / Windows Edge
    #

    
    if on_wsl(): #edge:
        edge = shutil.which("microsoft-edge")
        env = os.environ.copy()
        env["CHROME_LOG_LEVEL"] = "3"

        try:
            subprocess.Popen(
                [
                    edge,
                    url,
                    "--no-first-run",
                    "--quiet",
                    "--disable-gpu",
                    "--disable-software-rasterizer",
                    "--disable-sync",
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                env=env,
                start_new_session=True,
            )

            return True

        except Exception:
            logger.exception("microsoft-edge failed")

    #
    # Linux desktop
    #

    if on_linux(): #shutil.which("xdg-open"):

        try:
            subprocess.Popen(
                ["xdg-open", url],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

            return True

        except Exception:
            logger.exception("xdg-open failed")

    
    #
    # Generic Python fallback
    #

    try:
        webbrowser.open_new_tab(url)
        return True

    except Exception:
        logger.exception("webbrowser failed")
        return False


# ----------------------------------------------------------------------
# Combined helper
# ----------------------------------------------------------------------

def launch_browser_when_ready(
    url: str,
    *,
    timeout: float = 5.0,
    poll_interval: float = 0.1,
) -> threading.Thread:
    """
    Launch a daemon thread which waits for an HTTP server to become
    responsive before opening the user's browser.

    This function returns immediately.

    Parameters
    ----------
    url
        URL to poll and eventually open.

    timeout
        Maximum time to wait.

    poll_interval
        Delay between connection attempts.

    Returns
    -------
    threading.Thread
        The daemon thread performing the wait.
    """

    def worker():

        if wait_until_http_ready(
            url,
            timeout=timeout,
            poll_interval=poll_interval,
        ):

            logger.debug("Server ready: %s", url)

            launch_browser(url)

        else:

            logger.warning(
                "Timed out waiting for server: %s",
                url,
            )

    thread = threading.Thread(
        target=worker,
        daemon=True,
        name="launch-browser-when-ready",
    )

    thread.start()

    return thread
