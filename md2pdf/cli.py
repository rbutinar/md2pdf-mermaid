#!/usr/bin/env python3
"""
Command-line interface for md2pdf
"""

import argparse
import sys
from pathlib import Path
from .converter import convert_markdown_to_pdf
from .html_renderer import convert_markdown_to_pdf_html
from . import __version__


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Convert Markdown to PDF with Mermaid diagram rendering",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  md2pdf document.md                           # Convert to document.pdf
  md2pdf doc.md -o report.pdf                 # Custom output name
  md2pdf doc.md --no-mermaid                  # Disable Mermaid rendering
  md2pdf doc.md --title "My Report"          # Custom title
  md2pdf doc.md --page-size letter           # Use Letter size
  md2pdf doc.md --orientation landscape      # Landscape orientation
  md2pdf doc.md --font arial                 # Use Arial font (Windows)
  md2pdf doc.md --font dejavu                # Use DejaVu font (Linux)
  md2pdf doc.md --emoji-strategy remove      # Remove emoji, keep symbols
  md2pdf doc.md --emoji-strategy pilmoji     # Colored emoji (requires pilmoji)
  md2pdf doc.md --engine html                # Full emoji support (HTML/Chromium)

For more information: https://github.com/rbutinar/md2pdf-mermaid
        """
    )

    parser.add_argument(
        "input",
        help="Input Markdown file"
    )
    parser.add_argument(
        "-o", "--output",
        help="Output PDF file (default: same name as input with .pdf extension)"
    )
    parser.add_argument(
        "--no-mermaid",
        action="store_true",
        help="Disable Mermaid rendering (fallback to code blocks)"
    )
    parser.add_argument(
        "--title",
        help="Document title (default: filename)"
    )
    parser.add_argument(
        "--page-size",
        choices=["a4", "a3", "letter"],
        default="a4",
        help="Page size (default: a4)"
    )
    parser.add_argument(
        "--orientation",
        choices=["portrait", "landscape"],
        default="portrait",
        help="Page orientation (default: portrait)"
    )
    parser.add_argument(
        "--no-page-numbers",
        action="store_true",
        help="Disable page numbering"
    )
    parser.add_argument(
        "--font",
        help="Font to use (auto=auto-detect, helvetica=standard, arial=Windows, dejavu=Linux, or path to .ttf file)"
    )
    parser.add_argument(
        "--mermaid-scale",
        type=int,
        default=2,
        choices=[1, 2, 3, 4],
        help="Mermaid diagram resolution scale (1=standard, 2=high quality, 3=very high, 4=ultra). Default: 2"
    )
    parser.add_argument(
        "--mermaid-theme",
        choices=["default", "neutral", "dark", "forest", "base"],
        default="default",
        help="Mermaid diagram color theme (default, neutral, dark, forest, base). Default: default"
    )
    parser.add_argument(
        "--emoji-strategy",
        choices=["auto", "pilmoji", "remove", "keep"],
        default="auto",
        help="Emoji rendering strategy: auto=try pilmoji then remove (default), pilmoji=colored images (requires pilmoji), remove=remove emoji keep symbols, keep=preserve all (needs font support)"
    )
    parser.add_argument(
        "--engine",
        choices=["html", "reportlab"],
        default="html",
        help="PDF rendering engine: html=full emoji support via Chromium (default), reportlab=legacy engine with advanced PDF features"
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"md2pdf {__version__}"
    )

    args = parser.parse_args()

    # Validate input file
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: File not found: {input_path}", file=sys.stderr)
        return 1

    # Determine output path
    output_path = args.output or str(input_path.with_suffix(".pdf"))

    # Determine title
    title = args.title or input_path.stem

    try:
        # Read markdown content
        with open(input_path, "r", encoding="utf-8") as f:
            markdown_content = f.read()

        # Convert to PDF
        print(f"Converting {input_path} to PDF...")
        if args.engine == 'html':
            print("  (Using HTML/Chromium engine - full emoji support)")
            if args.no_mermaid:
                print("  (Mermaid rendering disabled)")
            result = convert_markdown_to_pdf_html(
                markdown_content,
                output_path,
                title=title,
                page_size=args.page_size,
                orientation=args.orientation,
                enable_mermaid=not args.no_mermaid
            )
        else:
            if args.no_mermaid:
                print("  (Mermaid rendering disabled)")

            result = convert_markdown_to_pdf(
                markdown_content,
                output_path,
                title=title,
                enable_mermaid=not args.no_mermaid,
                page_numbers=not args.no_page_numbers,
                page_size=args.page_size,
                orientation=args.orientation,
                font_name=args.font if args.font and args.font.lower() != 'auto' else None,
                mermaid_scale=args.mermaid_scale,
                mermaid_theme=args.mermaid_theme,
                emoji_strategy=args.emoji_strategy
            )

        # Success
        output_size_kb = Path(output_path).stat().st_size / 1024
        print(f"[OK] PDF created: {output_path} ({output_size_kb:.1f} KB)")

        # Show Mermaid info if applicable (only for ReportLab engine)
        if result.get('mermaid_count', 0) > 0:
            if result['playwright_available'] and not args.no_mermaid:
                print(f"  [OK] Rendered {result['mermaid_rendered']}/{result['mermaid_count']} Mermaid diagrams")
            elif not result['playwright_available'] and not args.no_mermaid:
                print(f"\n⚠ Note: Found {result['mermaid_count']} Mermaid diagram(s) but Playwright is not available.")
                print("  Diagrams are shown as code blocks in the PDF.")
                print("\n  For full diagram rendering, install Playwright:")
                print("    playwright install chromium")
                print("  Then re-run the conversion.")

        return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
