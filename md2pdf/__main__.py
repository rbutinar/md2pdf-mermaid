"""Entry point for md2pdf when run as a module or PyInstaller bundle."""
from md2pdf.cli import main
import sys

if __name__ == "__main__":
    sys.exit(main())
