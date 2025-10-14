#!/usr/bin/env python3
"""
Command-line interface for md2pdf
"""

import argparse
import sys
from pathlib import Path
from .converter import convert_markdown_to_pdf


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Convert Markdown to PDF with Mermaid diagram rendering",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  md2pdf document.md                    # Convert to document.pdf
  md2pdf doc.md -o report.pdf          # Custom output name
  md2pdf doc.md --no-mermaid           # Disable Mermaid rendering
  md2pdf doc.md --title "My Report"   # Custom title

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
        "-v", "--version",
        action="version",
        version="md2pdf 1.0.0"
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
        if args.no_mermaid:
            print("  (Mermaid rendering disabled)")

        result = convert_markdown_to_pdf(
            markdown_content,
            output_path,
            title=title,
            enable_mermaid=not args.no_mermaid
        )

        # Success
        output_size_kb = Path(output_path).stat().st_size / 1024
        print(f"[OK] PDF created: {output_path} ({output_size_kb:.1f} KB)")

        # Show Mermaid info if applicable
        if result['mermaid_count'] > 0:
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
