"""
pyhabitat.web

Reusable helpers for launching local web applications.

Typical usage
-------------

    from http.server import ThreadingHTTPServer
    from pyhabitat.web import (
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
import urllib.error

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

        except urllib.error.HTTPError:
            # Server answered.
            return True


        except (
            urllib.error.URLError,
            TimeoutError,
            ConnectionError,
        ):
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
    termux_launcher = shutil.which("termux-open-url"):
    if on_termux() and termux_launcher:

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

    edge = shutil.which("microsoft-edge")
    if on_wsl() and edge: #edge:
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
    linux_launcher = shutil.which("xdg-open")
    if on_linux() and linux_launcher:

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
                "Timed out after %.1fs waiting for %s",
                timeout,
                url,
            )

    thread = threading.Thread(
        target=worker,
        daemon=True,
        name=f"launch-browser-when-ready: {url}",
    )

    thread.start()

    return thread
