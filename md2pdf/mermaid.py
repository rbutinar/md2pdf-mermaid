#!/usr/bin/env python3
"""
Mermaid Diagram Renderer
Converts Mermaid diagrams to PNG images using Playwright
"""

import os

# Check if Playwright is available
PLAYWRIGHT_AVAILABLE = False
try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    pass


def is_playwright_available():
    """Check if Playwright is installed and browsers are available"""
    return PLAYWRIGHT_AVAILABLE


def render_mermaid_to_png(mermaid_code, output_path, width=1400, height=1000):
    """
    Render a Mermaid diagram to PNG

    Args:
        mermaid_code: Mermaid code (string)
        output_path: Path to output PNG file
        width: Image width in pixels (default 1400px)
        height: Image height in pixels (default 1000px)

    Returns:
        True if successful, False otherwise
    """

    if not PLAYWRIGHT_AVAILABLE:
        return False

    # HTML template with Mermaid.js from CDN
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script type="module">
            import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';
            mermaid.initialize({{
                startOnLoad: true,
                theme: 'default',
                flowchart: {{
                    useMaxWidth: false,
                    htmlLabels: true
                }}
            }});
        </script>
        <style>
            body {{
                margin: 0;
                padding: 20px;
                background: white;
                display: flex;
                justify-content: center;
                align-items: center;
            }}
            #diagram {{
                max-width: {width}px;
            }}
        </style>
    </head>
    <body>
        <div id="diagram" class="mermaid">
{mermaid_code}
        </div>
    </body>
    </html>
    """

    try:
        with sync_playwright() as p:
            # Use Chromium headless
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={'width': width, 'height': height})

            # Load HTML with Mermaid
            page.set_content(html_template)

            # Wait for Mermaid to render
            page.wait_for_selector('#diagram svg', timeout=15000)

            # Wait a bit more for stabilization
            page.wait_for_timeout(1000)

            # Take screenshot of just the SVG element (not the full page)
            svg_element = page.query_selector('#diagram svg')
            svg_element.screenshot(path=output_path)

            browser.close()
            return True

    except Exception as e:
        print(f"Error rendering Mermaid: {e}")
        return False
