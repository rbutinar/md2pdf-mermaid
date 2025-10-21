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


def render_mermaid_to_png(mermaid_code, output_path, width=1400, height=1000, scale=2, theme='default'):
    """
    Render a Mermaid diagram to PNG

    Args:
        mermaid_code: Mermaid code (string)
        output_path: Path to output PNG file
        width: Image width in pixels (default 1400px)
        height: Image height in pixels (default 1000px)
        scale: Device scale factor for high-resolution rendering (default 2 = 2x resolution)
               Higher values = sharper images but larger file size
               Recommended: 2 for standard, 3 for very high quality

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
                theme: '{theme}',
                flowchart: {{
                    useMaxWidth: false,
                    htmlLabels: true
                }}
            }});
        </script>
        <style>
            body {{
                margin: 0;
                padding: 0;
                background: white;
            }}
            #diagram {{
                display: inline-block;
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
            # Use deviceScaleFactor=1 and scale dimensions in JavaScript instead
            # This avoids viewport scaling issues
            page = browser.new_page(viewport={
                'width': width * 2,  # Large viewport to accommodate scaled SVG
                'height': height * 2,
                'deviceScaleFactor': 1
            })

            # Load HTML with Mermaid
            page.set_content(html_template)

            # Wait for Mermaid to render
            page.wait_for_selector('#diagram svg', timeout=15000)

            # Wait a bit more for stabilization
            page.wait_for_timeout(1000)

            # CRITICAL: Prepare SVG with proper viewBox (removes whitespace)
            # Then render to canvas at exact target dimensions
            svg_data = page.evaluate(f'''() => {{
                const svg = document.querySelector('#diagram svg');

                // Get actual content bounding box
                const bbox = svg.getBBox();
                const naturalWidth = bbox.width;
                const naturalHeight = bbox.height;
                const aspectRatio = naturalHeight / naturalWidth;

                // Calculate target dimensions (width * scale for quality)
                const targetWidth = {width} * {scale};
                const targetHeight = targetWidth * aspectRatio;

                // Set viewBox to content bounds (removes whitespace)
                svg.setAttribute('viewBox', `${{bbox.x}} ${{bbox.y}} ${{bbox.width}} ${{bbox.height}}`);

                // Return dimensions for canvas rendering
                return {{
                    targetWidth: targetWidth,
                    targetHeight: targetHeight,
                    svgString: new XMLSerializer().serializeToString(svg)
                }};
            }}''')

            # Check if output should be SVG (based on file extension)
            if output_path.endswith('.svg'):
                # Save as SVG (vector format)
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(svg_data['svgString'])
            else:
                # Render SVG to canvas at exact target dimensions, then screenshot
                page.evaluate(f'''() => {{
                    const svgData = {svg_data};

                    // Create canvas with exact target dimensions
                    const canvas = document.createElement('canvas');
                    canvas.width = svgData.targetWidth;
                    canvas.height = svgData.targetHeight;
                    canvas.id = 'render-canvas';

                    // Clear diagram div and add canvas
                    const diagramDiv = document.querySelector('#diagram');
                    diagramDiv.innerHTML = '';
                    diagramDiv.appendChild(canvas);

                    // Draw SVG to canvas
                    const ctx = canvas.getContext('2d');
                    const img = new Image();
                    const svgBlob = new Blob([svgData.svgString], {{type: 'image/svg+xml;charset=utf-8'}});
                    const url = URL.createObjectURL(svgBlob);

                    return new Promise((resolve) => {{
                        img.onload = () => {{
                            ctx.drawImage(img, 0, 0, svgData.targetWidth, svgData.targetHeight);
                            URL.revokeObjectURL(url);
                            resolve();
                        }};
                        img.src = url;
                    }});
                }}''')

                # Wait for canvas rendering
                page.wait_for_timeout(500)

                # Screenshot the canvas element
                canvas_element = page.query_selector('#render-canvas')
                canvas_element.screenshot(path=output_path)

            browser.close()
            return True

    except Exception as e:
        print(f"Error rendering Mermaid: {e}")
        return False
