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
    """Check if Playwright is installed and a browser binary is available."""
    if not PLAYWRIGHT_AVAILABLE:
        return False
    # Verify that Chromium can actually be found
    try:
        from .browser_manager import is_browser_installed
        return is_browser_installed()
    except ImportError:
        # browser_manager not available (shouldn't happen, but be safe)
        return True


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
    # Using Mermaid v11 (latest stable version)
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
                }},
                securityLevel: 'loose'
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

            # Smart polling: Wait for valid dimensions (up to 5 seconds)
            # This allows simple diagrams to render quickly while giving complex ones time
            page.evaluate('''() => {
                return new Promise((resolve) => {
                    const svg = document.querySelector('#diagram svg');
                    const maxAttempts = 50;  // 50 attempts * 100ms = 5 seconds max
                    let attempts = 0;

                    const checkDimensions = () => {
                        attempts++;

                        // Try to get valid dimensions
                        let hasValidDimensions = false;
                        try {
                            const bbox = svg.getBBox();
                            if (bbox && bbox.width > 0 && bbox.height > 0 &&
                                !isNaN(bbox.width) && !isNaN(bbox.height)) {
                                hasValidDimensions = true;
                            }
                        } catch (e) {
                            // getBBox failed, try other methods
                        }

                        // Check viewBox as fallback
                        if (!hasValidDimensions) {
                            const viewBox = svg.getAttribute('viewBox');
                            if (viewBox) {
                                const parts = viewBox.split(/\\s+/);
                                if (parts.length >= 4) {
                                    const w = parseFloat(parts[2]);
                                    const h = parseFloat(parts[3]);
                                    if (w > 0 && h > 0 && !isNaN(w) && !isNaN(h)) {
                                        hasValidDimensions = true;
                                    }
                                }
                            }
                        }

                        // If we have valid dimensions or reached max attempts, resolve
                        if (hasValidDimensions || attempts >= maxAttempts) {
                            resolve();
                        } else {
                            // Check again in 100ms
                            setTimeout(checkDimensions, 100);
                        }
                    };

                    // Start checking after initial 500ms delay
                    setTimeout(checkDimensions, 500);
                });
            }''')

            # CRITICAL: Prepare SVG with proper viewBox (removes whitespace)
            # Then render to canvas at exact target dimensions
            svg_data = page.evaluate(f'''() => {{
                const svg = document.querySelector('#diagram svg');

                // Try multiple methods to get valid dimensions
                let naturalWidth, naturalHeight, bbox;

                // Method 1: Try getBBox() first
                try {{
                    bbox = svg.getBBox();
                    if (bbox && bbox.width > 0 && bbox.height > 0 &&
                        !isNaN(bbox.width) && !isNaN(bbox.height)) {{
                        naturalWidth = bbox.width;
                        naturalHeight = bbox.height;
                    }}
                }} catch (e) {{
                    console.log('getBBox failed:', e);
                }}

                // Method 2: Try SVG viewBox attribute
                if (!naturalWidth || !naturalHeight) {{
                    const viewBox = svg.getAttribute('viewBox');
                    if (viewBox) {{
                        const parts = viewBox.split(/\\s+/);
                        if (parts.length >= 4) {{
                            const w = parseFloat(parts[2]);
                            const h = parseFloat(parts[3]);
                            if (w > 0 && h > 0 && !isNaN(w) && !isNaN(h)) {{
                                naturalWidth = w;
                                naturalHeight = h;
                            }}
                        }}
                    }}
                }}

                // Method 3: Try SVG width/height attributes
                if (!naturalWidth || !naturalHeight) {{
                    const w = parseFloat(svg.getAttribute('width'));
                    const h = parseFloat(svg.getAttribute('height'));
                    if (w > 0 && h > 0 && !isNaN(w) && !isNaN(h)) {{
                        naturalWidth = w;
                        naturalHeight = h;
                    }}
                }}

                // Method 4: Try getBoundingClientRect()
                if (!naturalWidth || !naturalHeight) {{
                    const rect = svg.getBoundingClientRect();
                    if (rect && rect.width > 0 && rect.height > 0) {{
                        naturalWidth = rect.width;
                        naturalHeight = rect.height;
                    }}
                }}

                // Method 5: Use defaults as last resort
                if (!naturalWidth || naturalWidth <= 0 || isNaN(naturalWidth)) {{
                    naturalWidth = {width};
                }}
                if (!naturalHeight || naturalHeight <= 0 || isNaN(naturalHeight)) {{
                    naturalHeight = {height};
                }}

                const aspectRatio = naturalHeight / naturalWidth;

                // Calculate target dimensions (width * scale for quality)
                let targetWidth = {width} * {scale};
                let targetHeight = targetWidth * aspectRatio;

                // Limit maximum height to prevent very tall diagrams
                const maxHeight = 2400;  // Max height in pixels (fits in one PDF page)
                if (targetHeight > maxHeight) {{
                    targetHeight = maxHeight;
                    targetWidth = targetHeight / aspectRatio;
                }}

                // Set viewBox to content bounds (removes whitespace)
                // Only set if bbox has valid values
                if (bbox && bbox.width > 0 && bbox.height > 0 &&
                    !isNaN(bbox.width) && !isNaN(bbox.height)) {{
                    svg.setAttribute('viewBox', `${{bbox.x}} ${{bbox.y}} ${{bbox.width}} ${{bbox.height}}`);
                }}

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
