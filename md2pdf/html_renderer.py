#!/usr/bin/env python3
"""
HTML-based PDF rendering with Playwright
Provides native emoji support through browser rendering
"""

import tempfile
import os
import re
import base64
from pathlib import Path
from typing import Optional, List, Tuple
import markdown


def _process_mermaid_diagrams(markdown_text: str) -> Tuple[str, List[str]]:
    """
    Find and render Mermaid diagrams, replace with <img> tags.

    Args:
        markdown_text: Markdown content with potential Mermaid blocks

    Returns:
        Tuple of (modified_markdown, list_of_temp_image_paths)
    """
    temp_images = []

    try:
        from .mermaid import render_mermaid_to_png, is_playwright_available

        if not is_playwright_available():
            # Playwright not available, return unchanged
            return markdown_text, temp_images

        # Find all Mermaid code blocks
        pattern = r'```mermaid\n(.*?)\n```'
        matches = list(re.finditer(pattern, markdown_text, re.DOTALL))

        # Process in reverse to maintain positions
        for match in reversed(matches):
            mermaid_code = match.group(1)

            # Create temporary PNG file
            tmp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
            tmp_path = tmp_file.name
            tmp_file.close()
            temp_images.append(tmp_path)

            # Render Mermaid to PNG
            # Use wider canvas but let height auto-calculate to avoid layout errors
            success = render_mermaid_to_png(
                mermaid_code, tmp_path,
                width=1400, height=2000, scale=2, theme='default'
            )

            if success:
                # Convert image to base64 for embedding
                with open(tmp_path, 'rb') as img_file:
                    img_data = base64.b64encode(img_file.read()).decode('utf-8')

                # Replace Mermaid block with inline image
                # Limit height to 75% of page height (matching ReportLab logic)
                # A4 page: 842pt height, minus 2cm margins (56.7pt each) = ~730pt
                # 75% of 730pt = ~547pt = 19.3cm = 728px at 96dpi
                max_height_px = 728  # Maximum height to fit on one page
                img_tag = f'<img src="data:image/png;base64,{img_data}" style="max-width: 90%; max-height: {max_height_px}px; width: auto; height: auto; display: block; margin: 20px auto; page-break-inside: avoid; object-fit: contain;" />'
                markdown_text = markdown_text[:match.start()] + img_tag + markdown_text[match.end():]
            else:
                # Keep as code block if rendering failed
                pass

    except ImportError:
        # Mermaid module not available
        pass
    except Exception as e:
        print(f"Warning: Failed to process Mermaid diagrams: {e}")

    return markdown_text, temp_images


def markdown_to_html(markdown_text: str, title: str = "Document",
                     enable_mermaid: bool = True) -> str:
    """
    Convert Markdown to HTML with proper styling for PDF.

    Args:
        markdown_text: Markdown content
        title: Document title
        enable_mermaid: Enable Mermaid diagram rendering

    Returns:
        Complete HTML document with CSS
    """
    # Pre-process Mermaid diagrams if enabled
    temp_images = []
    if enable_mermaid:
        markdown_text, temp_images = _process_mermaid_diagrams(markdown_text)

    # Convert markdown to HTML
    md = markdown.Markdown(extensions=[
        'extra',          # Tables, fenced code, etc.
        'codehilite',     # Syntax highlighting
        'toc',            # Table of contents
        'nl2br',          # Newlines to <br>
        'fenced_code',    # Fenced code blocks
    ])
    content_html = md.convert(markdown_text)

    # Create complete HTML document with nice styling
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        @page {{
            size: A4;
            margin: 2cm;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
                         "Helvetica Neue", Arial, sans-serif,
                         "Apple Color Emoji", "Segoe UI Emoji", "Noto Color Emoji";
            font-size: 11pt;
            line-height: 1.6;
            color: #333;
            max-width: 100%;
            margin: 0;
            padding: 0;
        }}

        h1 {{
            font-size: 24pt;
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 8px;
            margin-top: 24px;
            margin-bottom: 16px;
        }}

        h2 {{
            font-size: 18pt;
            color: #34495e;
            border-bottom: 1px solid #95a5a6;
            padding-bottom: 6px;
            margin-top: 20px;
            margin-bottom: 12px;
        }}

        h3 {{
            font-size: 14pt;
            color: #555;
            margin-top: 16px;
            margin-bottom: 10px;
        }}

        h4 {{
            font-size: 12pt;
            color: #666;
            margin-top: 14px;
            margin-bottom: 8px;
        }}

        p {{
            margin: 8px 0;
        }}

        ul, ol {{
            margin: 8px 0;
            padding-left: 24px;
        }}

        li {{
            margin: 4px 0;
        }}

        code {{
            background-color: #f8f8f8;
            border: 1px solid #ddd;
            border-radius: 3px;
            padding: 2px 6px;
            font-family: "Courier New", Courier, monospace;
            font-size: 10pt;
            color: #666;
        }}

        pre {{
            background-color: #f8f8f8;
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 12px;
            overflow-x: auto;
            margin: 12px 0;
        }}

        pre code {{
            background: none;
            border: none;
            padding: 0;
            font-size: 9pt;
        }}

        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 12px 0;
        }}

        th {{
            background-color: #3498db;
            color: white;
            font-weight: bold;
            padding: 10px;
            text-align: left;
            border: 1px solid #ddd;
        }}

        td {{
            padding: 8px;
            border: 1px solid #ddd;
        }}

        tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}

        blockquote {{
            border-left: 4px solid #3498db;
            padding-left: 16px;
            margin: 12px 0;
            color: #666;
            font-style: italic;
        }}

        hr {{
            border: none;
            border-top: 2px solid #eee;
            margin: 20px 0;
        }}

        a {{
            color: #3498db;
            text-decoration: none;
        }}

        a:hover {{
            text-decoration: underline;
        }}

        /* Emoji support - ensure they render properly */
        .emoji {{
            font-family: "Apple Color Emoji", "Segoe UI Emoji", "Noto Color Emoji", sans-serif;
        }}

        /* Page break handling */
        .page-break {{
            page-break-after: always;
        }}

        /* Print-specific styles */
        @media print {{
            body {{
                print-color-adjust: exact;
                -webkit-print-color-adjust: exact;
            }}
        }}
    </style>
</head>
<body>
{content_html}
</body>
</html>"""

    return html


async def html_to_pdf_playwright(html_content: str, output_path: str,
                                 page_size: str = 'A4',
                                 orientation: str = 'portrait') -> bool:
    """
    Convert HTML to PDF using Playwright (Chromium).

    This provides native emoji support and excellent CSS rendering.

    Args:
        html_content: Complete HTML document
        output_path: Path to output PDF file
        page_size: Page size ('A4', 'A3', 'Letter')
        orientation: 'portrait' or 'landscape'

    Returns:
        True if successful, False otherwise
    """
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        print("Error: Playwright not available")
        return False

    try:
        # Create temporary HTML file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html',
                                        delete=False, encoding='utf-8') as f:
            f.write(html_content)
            html_path = f.name

        # Configure PDF options
        pdf_options = {
            'path': output_path,
            'format': page_size,
            'landscape': orientation.lower() == 'landscape',
            'print_background': True,
            'display_header_footer': True,
            'header_template': '<div></div>',  # Empty header
            'footer_template': '<div style="font-size: 9px; text-align: center; width: 100%; color: #666;"><span class="pageNumber"></span> / <span class="totalPages"></span></div>',
            'margin': {
                'top': '0.5cm',
                'right': '0.5cm',
                'bottom': '1.2cm',  # Increased for footer
                'left': '0.5cm'
            }
        }

        # Render with Playwright
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()

            # Load HTML file
            await page.goto(f'file://{os.path.abspath(html_path)}')

            # Wait for any dynamic content
            await page.wait_for_load_state('networkidle')

            # Generate PDF
            await page.pdf(**pdf_options)

            await browser.close()

        # Cleanup temporary file
        try:
            os.unlink(html_path)
        except:
            pass

        return True

    except Exception as e:
        print(f"Error converting HTML to PDF: {e}")
        import traceback
        traceback.print_exc()
        return False


def convert_markdown_to_pdf_html(markdown_text: str, output_path: str,
                                 title: str = "Document",
                                 page_size: str = 'A4',
                                 orientation: str = 'portrait',
                                 enable_mermaid: bool = True) -> dict:
    """
    Convert Markdown to PDF via HTML rendering (supports emoji!).

    This uses Playwright's Chromium browser for rendering, which provides
    native emoji support and excellent CSS compatibility.

    Args:
        markdown_text: Markdown content as string
        output_path: Path to output PDF file
        title: Document title
        page_size: Page size ('A4', 'A3', 'Letter')
        orientation: 'portrait' or 'landscape'

    Returns:
        dict with success status
    """
    try:
        # Convert Markdown to HTML
        html_content = markdown_to_html(markdown_text, title, enable_mermaid)

        # Use asyncio to run the async function
        import asyncio
        success = asyncio.run(html_to_pdf_playwright(
            html_content, output_path, page_size, orientation
        ))

        return {
            'success': success,
            'method': 'html_playwright',
            'emoji_support': True
        }

    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'method': 'html_playwright'
        }
