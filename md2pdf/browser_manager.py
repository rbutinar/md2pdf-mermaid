#!/usr/bin/env python3
"""
Browser Manager for md2pdf standalone executables.

Handles lazy detection and download of Chromium for PyInstaller-bundled binaries.
When running as a normal Python package, defers to standard Playwright behavior.
"""

import os
import sys
import subprocess
import platform


def is_frozen():
    """Check if running as a PyInstaller bundle."""
    return getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')


def get_browser_cache_dir():
    """Get platform-appropriate cache directory for browser binaries.

    Returns the first existing browser path found, or the default cache location.
    """
    # Check standard Playwright locations first (reuse existing installs)
    standard_paths = []
    home = os.path.expanduser("~")

    system = platform.system()
    if system == "Darwin":
        standard_paths.append(os.path.join(home, "Library", "Caches", "ms-playwright"))
        default_cache = os.path.join(home, "Library", "Caches", "md2pdf", "playwright")
    elif system == "Windows":
        local_app = os.environ.get("LOCALAPPDATA", os.path.join(home, "AppData", "Local"))
        standard_paths.append(os.path.join(local_app, "ms-playwright"))
        default_cache = os.path.join(local_app, "md2pdf", "playwright")
    else:  # Linux and others
        xdg_cache = os.environ.get("XDG_CACHE_HOME", os.path.join(home, ".cache"))
        standard_paths.append(os.path.join(xdg_cache, "ms-playwright"))
        default_cache = os.path.join(xdg_cache, "md2pdf", "playwright")

    # If PLAYWRIGHT_BROWSERS_PATH is already set, respect it
    if os.environ.get("PLAYWRIGHT_BROWSERS_PATH"):
        return os.environ["PLAYWRIGHT_BROWSERS_PATH"]

    # Check standard locations for existing browser installs
    for path in standard_paths:
        if os.path.isdir(path) and _has_chromium(path):
            return path

    return default_cache


def _has_chromium(browsers_path):
    """Check if a Chromium installation exists in the given path."""
    if not os.path.isdir(browsers_path):
        return False
    for entry in os.listdir(browsers_path):
        if entry.startswith("chromium"):
            return True
    return False


def is_browser_installed():
    """Check if Chromium is available for Playwright."""
    cache_dir = get_browser_cache_dir()
    return _has_chromium(cache_dir)


def install_browser():
    """Download and install Chromium using Playwright's driver.

    Streams output so the user sees download progress.
    """
    cache_dir = get_browser_cache_dir()
    os.makedirs(cache_dir, exist_ok=True)

    env = os.environ.copy()
    env["PLAYWRIGHT_BROWSERS_PATH"] = cache_dir

    print(f"\nChromium browser not found. Downloading (~150 MB)...")
    print("This only happens once.\n")

    try:
        if is_frozen():
            # In frozen mode, find the Playwright driver inside the bundle
            _install_frozen(env)
        else:
            # Normal Python environment - use playwright CLI
            subprocess.run(
                [sys.executable, "-m", "playwright", "install", "chromium"],
                env=env,
                check=True,
            )

        print("\nChromium installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"\nError installing Chromium (exit code {e.returncode}).", file=sys.stderr)
        print("You can try manually: playwright install chromium", file=sys.stderr)
        raise SystemExit(1)
    except Exception as e:
        print(f"\nError installing Chromium: {e}", file=sys.stderr)
        raise SystemExit(1)


def _install_frozen(env):
    """Install browser when running from a PyInstaller bundle."""
    try:
        from playwright._impl._driver import compute_driver_executable
        driver_exec, driver_cli = compute_driver_executable()
        subprocess.run(
            [str(driver_exec), str(driver_cli), "install", "chromium"],
            env=env,
            check=True,
        )
    except (ImportError, Exception):
        # Fallback: locate node + cli.js inside _MEIPASS
        meipass = getattr(sys, '_MEIPASS', '')
        node_candidates = [
            os.path.join(meipass, "playwright", "driver", "node"),
            os.path.join(meipass, "playwright", "driver", "node.exe"),
        ]
        cli_candidates = [
            os.path.join(meipass, "playwright", "driver", "package", "cli.js"),
        ]

        node_path = next((p for p in node_candidates if os.path.exists(p)), None)
        cli_path = next((p for p in cli_candidates if os.path.exists(p)), None)

        if node_path and cli_path:
            subprocess.run(
                [node_path, cli_path, "install", "chromium"],
                env=env,
                check=True,
            )
        else:
            raise RuntimeError(
                "Could not locate Playwright driver in bundled executable. "
                "Please install Chromium manually: playwright install chromium"
            )


def ensure_browser():
    """Ensure Chromium is available, downloading if necessary.

    Call this before any Playwright-based rendering. Sets PLAYWRIGHT_BROWSERS_PATH
    so Playwright finds the browser.
    """
    cache_dir = get_browser_cache_dir()

    if _has_chromium(cache_dir):
        # Browser exists - make sure Playwright knows where it is
        os.environ["PLAYWRIGHT_BROWSERS_PATH"] = cache_dir
        return

    # Check standard locations one more time (in case get_browser_cache_dir
    # returned the default path but a standard install exists)
    if not is_frozen():
        # For non-frozen, Playwright usually finds its own browsers
        try:
            from playwright.sync_api import sync_playwright
            with sync_playwright() as p:
                # Quick check: can we launch Chromium?
                browser = p.chromium.launch(headless=True)
                browser.close()
                return
        except Exception:
            pass

    # Need to install
    install_browser()
    os.environ["PLAYWRIGHT_BROWSERS_PATH"] = cache_dir
