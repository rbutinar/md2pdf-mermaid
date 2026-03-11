#!/usr/bin/env python3
"""
Build helper for md2pdf standalone executable.

Usage: python scripts/build.py
"""

import os
import platform
import subprocess
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    os.chdir(ROOT_DIR)

    print(f"Building md2pdf standalone executable...")
    print(f"  Platform: {platform.system()} {platform.machine()}")
    print(f"  Python:   {sys.version}")
    print()

    # Run PyInstaller
    result = subprocess.run(
        [sys.executable, "-m", "PyInstaller", "md2pdf.spec", "--clean", "--noconfirm"],
        cwd=ROOT_DIR,
    )
    if result.returncode != 0:
        print("\nBuild failed!", file=sys.stderr)
        return 1

    # Find the output binary
    exe_name = "md2pdf.exe" if platform.system() == "Windows" else "md2pdf"
    exe_path = os.path.join(ROOT_DIR, "dist", exe_name)

    if not os.path.exists(exe_path):
        print(f"\nError: Expected output not found at {exe_path}", file=sys.stderr)
        return 1

    # Report size
    size_mb = os.path.getsize(exe_path) / (1024 * 1024)
    print(f"\nBuild successful!")
    print(f"  Output: {exe_path}")
    print(f"  Size:   {size_mb:.1f} MB")

    # Verify
    print(f"\nVerifying...")
    result = subprocess.run([exe_path, "--version"], capture_output=True, text=True, timeout=30)
    if result.returncode == 0:
        print(f"  Version: {result.stdout.strip()}")
    else:
        print(f"  Warning: --version check failed", file=sys.stderr)
        if result.stdout.strip():
            print(f"  stdout: {result.stdout.strip()}", file=sys.stderr)
        if result.stderr.strip():
            print(f"  stderr: {result.stderr.strip()}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
