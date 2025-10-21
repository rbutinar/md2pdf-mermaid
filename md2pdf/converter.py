#!/usr/bin/env python3
"""
Markdown to PDF Converter
Professional PDF generation from Markdown with Mermaid diagram support
"""

import os
import re
import tempfile
from reportlab.lib.pagesizes import A4, A3, LETTER, landscape, portrait
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Preformatted, Image, PageBreak, Flowable, KeepTogether
)
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

try:
    from .mermaid import render_mermaid_to_png, is_playwright_available
    MERMAID_AVAILABLE = True
except ImportError:
    MERMAID_AVAILABLE = False
    def is_playwright_available():
        return False


def remove_emoji(text):
    """
    Remove emoji characters from text for PDF compatibility.

    ReportLab doesn't natively support color emoji fonts, so we remove them
    to keep the document clean and readable.

    Args:
        text: Input text that may contain emoji

    Returns:
        Text with emoji removed
    """
    if not text:
        return text

    result = []
    for char in text:
        codepoint = ord(char)

        # Check if character is an emoji (simplified heuristic)
        # Emoji are typically in ranges: 0x1F300-0x1F9FF, 0x2600-0x26FF, 0x2700-0x27BF
        # Also skip variation selectors (0xFE00-0xFE0F)
        is_emoji = (
            (codepoint >= 0x1F300 and codepoint <= 0x1F9FF) or  # Misc symbols and pictographs
            (codepoint >= 0x2600 and codepoint <= 0x26FF) or    # Misc symbols
            (codepoint >= 0x2700 and codepoint <= 0x27BF) or    # Dingbats
            (codepoint >= 0x1F600 and codepoint <= 0x1F64F) or  # Emoticons
            (codepoint >= 0x1F680 and codepoint <= 0x1F6FF) or  # Transport and map symbols
            (codepoint >= 0x2300 and codepoint <= 0x23FF) or    # Miscellaneous Technical (clocks, etc.)
            (codepoint >= 0xFE00 and codepoint <= 0xFE0F)       # Variation selectors
        )

        if not is_emoji:
            result.append(char)

    return ''.join(result)


def remove_hyperlinks(text):
    """
    Remove hyperlinks from markdown text, keeping only the link text.

    Converts [link text](url) -> link text
    Also handles reference-style links [link text][ref] -> link text

    This is a temporary solution until full hyperlink support is implemented.
    Hyperlinks in PDFs require more complex handling with ReportLab's anchor system.

    Args:
        text: Markdown text that may contain hyperlinks

    Returns:
        Text with hyperlinks removed, keeping only the displayed text
    """
    if not text:
        return text

    # Remove inline links [text](url)
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)

    # Remove reference-style links [text][ref]
    text = re.sub(r'\[([^\]]+)\]\[[^\]]+\]', r'\1', text)

    # Remove standalone reference links [text] that might be references
    # but only if they're followed by a colon (link definitions)
    text = re.sub(r'^\[([^\]]+)\]:\s*.*$', '', text, flags=re.MULTILINE)

    return text




class HighQualityImage(Flowable):
    """Custom flowable for inserting high-resolution images without downsampling"""

    def __init__(self, img_path):
        Flowable.__init__(self)
        self.img_path = img_path

        # Open image to get dimensions
        from PIL import Image as PILImage
        pil_img = PILImage.open(img_path)
        self.img_width_px, self.img_height_px = pil_img.size
        self.aspect_ratio = self.img_height_px / self.img_width_px

        # Disable auto-rotation - let diagrams display in their natural orientation
        # Previous behavior: rotated images with aspect > 2.5, but this was confusing
        self.rotate_90 = False  # Never auto-rotate

        if self.rotate_90:
            # Swap dimensions for rotation
            self.img_width_px, self.img_height_px = self.img_height_px, self.img_width_px
            self.aspect_ratio = self.img_height_px / self.img_width_px

    def wrap(self, availWidth, availHeight):
        # Strategy: Maximize diagram size while respecting page boundaries
        # Use different strategies for horizontal vs vertical diagrams

        # Minimum height threshold: if available space is too small, request page break
        # This prevents diagrams from being squeezed into tiny remaining space at page bottom
        MIN_HEIGHT_CM = 8  # Minimum 8cm height for readable diagrams
        MIN_HEIGHT_PT = MIN_HEIGHT_CM * cm

        # If available height is too small, signal that we need more space
        # This will cause ReportLab to move the diagram to next page
        if availHeight < MIN_HEIGHT_PT:
            # Return very large dimensions to trigger page break
            return availWidth * 2, availHeight * 2

        # Maximum dimensions (leave margins)
        max_width = availWidth * 0.90   # 90% of width (5% margin each side)
        max_height = availHeight * 0.75  # 75% of height (allows more space for surrounding text)

        # Calculate constrained dimensions starting from width
        width_constrained = max_width
        height_constrained = width_constrained * self.aspect_ratio

        # If diagram is too tall (vertical diagrams), constrain by height instead
        if height_constrained > max_height:
            height_constrained = max_height
            width_constrained = height_constrained / self.aspect_ratio

        self.display_width = width_constrained
        self.display_height = height_constrained

        return self.display_width, self.display_height

    def draw(self):
        """Draw the image at full resolution directly to the canvas"""
        self.canv.saveState()
        try:
            if self.rotate_90:
                # Rotate 90 degrees clockwise around center
                # Move to center of where image will be
                center_x = self.display_width / 2
                center_y = self.display_height / 2

                # Translate to center, rotate, translate back
                self.canv.translate(center_x, center_y)
                self.canv.rotate(90)
                self.canv.translate(-center_y, -center_x)

                # Draw rotated (swap width/height)
                self.canv.drawImage(self.img_path, 0, 0,
                                   width=self.display_height, height=self.display_width,
                                   preserveAspectRatio=True, mask='auto')
            else:
                # Draw normally
                self.canv.drawImage(self.img_path, 0, 0,
                                   width=self.display_width, height=self.display_height,
                                   preserveAspectRatio=True, mask='auto')
        finally:
            self.canv.restoreState()


def parse_markdown(md_text):
    """
    Parse Markdown text into structured elements

    Args:
        md_text: Markdown content as string

    Returns:
        List of (type, content) tuples
    """
    lines = md_text.split('\n')
    elements = []

    in_code_block = False
    code_block_lines = []
    code_block_lang = None
    in_table = False
    table_lines = []

    for line in lines:
        # Code blocks
        if line.strip().startswith('```'):
            if in_code_block:
                # Closing code block
                if code_block_lang == 'mermaid':
                    elements.append(('mermaid', '\n'.join(code_block_lines)))
                else:
                    elements.append(('code', '\n'.join(code_block_lines)))
                code_block_lines = []
                code_block_lang = None
                in_code_block = False
            else:
                # Opening code block - detect language
                in_code_block = True
                lang = line.strip()[3:].strip()
                code_block_lang = lang if lang else None
            continue

        if in_code_block:
            code_block_lines.append(line)
            continue

        # Tables
        if '|' in line and line.strip():
            if not in_table:
                in_table = True
                table_lines = []
            table_lines.append(line)
            continue
        elif in_table:
            elements.append(('table', table_lines))
            table_lines = []
            in_table = False

        # Headers
        if line.startswith('# '):
            elements.append(('h1', line[2:].strip()))
        elif line.startswith('## '):
            elements.append(('h2', line[3:].strip()))
        elif line.startswith('### '):
            elements.append(('h3', line[4:].strip()))
        elif line.startswith('#### '):
            elements.append(('h4', line[5:].strip()))

        # Lists
        elif line.strip().startswith('- ') or line.strip().startswith('* '):
            elements.append(('list', line.strip()[2:]))
        elif re.match(r'^\d+\.\s', line.strip()):
            elements.append(('numlist', re.sub(r'^\d+\.\s', '', line.strip())))

        # Horizontal rule
        elif line.strip() in ['---', '***', '___']:
            elements.append(('hr', None))

        # Paragraph
        elif line.strip():
            elements.append(('p', line.strip()))

        # Empty line
        else:
            elements.append(('space', None))

    # Close any open table
    if in_table:
        elements.append(('table', table_lines))

    return elements


def get_page_size(size='a4', orientation='portrait'):
    """
    Get page size with specified orientation

    Args:
        size: Page size name ('a4', 'a3', 'letter')
        orientation: Page orientation ('portrait', 'landscape')

    Returns:
        Tuple of (width, height) for the page size
    """
    size_map = {
        'a4': A4,
        'a3': A3,
        'letter': LETTER
    }

    page_size = size_map.get(size.lower(), A4)

    if orientation.lower() == 'landscape':
        return landscape(page_size)
    else:
        return portrait(page_size)


def add_page_number(canvas, doc):
    """
    Add page number to the bottom center of each page

    Args:
        canvas: ReportLab canvas object
        doc: Document object
    """
    page_num = canvas.getPageNumber()
    text = f"Page {page_num}"
    canvas.saveState()
    canvas.setFont('Helvetica', 9)
    canvas.setFillColor(colors.HexColor('#666666'))
    # Use page width from canvas to center properly regardless of page size
    page_width = canvas._pagesize[0]
    canvas.drawCentredString(
        page_width / 2,  # x position (center of page)
        1.5 * cm,        # y position (bottom margin)
        text
    )
    canvas.restoreState()


def convert_markdown_to_pdf(markdown_text, output_path, title="Document",
                            enable_mermaid=True, page_numbers=True,
                            page_size='a4', orientation='portrait', font_name=None,
                            mermaid_scale=2, mermaid_theme='default'):
    """
    Convert Markdown text to PDF

    Args:
        markdown_text: Markdown content as string
        output_path: Path to output PDF file
        title: Document title
        enable_mermaid: Enable Mermaid diagram rendering (default: True)
        page_numbers: Enable page numbering in footer (default: True)
        page_size: Page size ('a4', 'a3', 'letter') (default: 'a4')
        orientation: Page orientation ('portrait', 'landscape') (default: 'portrait')
        font_name: Font to use (None=auto-detect, 'helvetica'=standard, 'arial'=Windows,
                   'dejavu'=Linux, or path to .ttf file) (default: None)
        mermaid_scale: Device scale factor for Mermaid rendering (default: 2)
                      Higher values produce sharper diagrams but larger files
                      Recommended: 2 (standard quality), 3 (high quality)

    Returns:
        dict with keys:
            - success: True if successful, False otherwise
            - mermaid_count: Number of Mermaid diagrams found
            - mermaid_rendered: Number of Mermaid diagrams successfully rendered
            - playwright_available: Whether Playwright is available
    """

    # Register UTF-8 fonts if available
    use_unicode_fonts = False
    unicode_font_name = None

    # Handle user-specified font
    if font_name and font_name.lower() == 'helvetica':
        # Use standard Helvetica fonts (no Unicode support)
        use_unicode_fonts = False
        unicode_font_name = None
    else:
        # Determine font sources to try
        if font_name:
            # User specified a font - try custom paths or specific font
            font_name_lower = font_name.lower()
            if font_name_lower == 'arial':
                font_attempts = [
                    ('Arial', 'C:\\Windows\\Fonts\\arial.ttf', 'C:\\Windows\\Fonts\\arialbd.ttf', 'C:\\Windows\\Fonts\\cour.ttf'),
                ]
            elif font_name_lower == 'dejavu':
                font_attempts = [
                    ('DejaVuSans', 'DejaVuSans.ttf', 'DejaVuSans-Bold.ttf', 'DejaVuSansMono.ttf'),
                ]
            elif font_name.endswith('.ttf'):
                # Custom TTF file path - assume user provides base name
                # User should provide path like "path/to/MyFont.ttf" and we'll derive bold/mono
                base_path = font_name.rsplit('.', 1)[0]
                font_attempts = [
                    ('CustomFont', font_name, f'{base_path}-Bold.ttf', f'{base_path}-Mono.ttf'),
                ]
            else:
                # Try as system font name
                font_attempts = [
                    (font_name, font_name + '.ttf', font_name + '-Bold.ttf', font_name + '-Mono.ttf'),
                ]
        else:
            # Auto-detect: try different font sources in order of preference
            font_attempts = [
                # DejaVu (Linux, sometimes Windows)
                ('DejaVuSans', 'DejaVuSans.ttf', 'DejaVuSans-Bold.ttf', 'DejaVuSansMono.ttf'),
                # Windows system fonts
                ('Arial', 'C:\\Windows\\Fonts\\arial.ttf', 'C:\\Windows\\Fonts\\arialbd.ttf', 'C:\\Windows\\Fonts\\cour.ttf'),
                # Alternative Windows path
                ('Arial', 'arial.ttf', 'arialbd.ttf', 'cour.ttf'),
            ]

        for font_family, regular, bold, mono in font_attempts:
            try:
                # Register individual fonts
                pdfmetrics.registerFont(TTFont(f'{font_family}', regular))
                pdfmetrics.registerFont(TTFont(f'{font_family}-Bold', bold))
                pdfmetrics.registerFont(TTFont(f'{font_family}-Mono', mono))

                # Register font family to enable automatic bold/italic switching
                from reportlab.pdfbase.pdfmetrics import registerFontFamily
                registerFontFamily(
                    font_family,
                    normal=font_family,
                    bold=f'{font_family}-Bold',
                    italic=font_family,  # Use regular for italic if not available
                    boldItalic=f'{font_family}-Bold'
                )

                use_unicode_fonts = True
                unicode_font_name = font_family
                break
            except:
                continue

    # Parse markdown
    elements = parse_markdown(markdown_text)

    # Track Mermaid diagrams
    mermaid_count = sum(1 for elem_type, _ in elements if elem_type == 'mermaid')
    mermaid_rendered = 0
    playwright_available = is_playwright_available()

    # Get page size with orientation
    final_pagesize = get_page_size(page_size, orientation)

    # Create PDF
    doc = SimpleDocTemplate(
        output_path,
        pagesize=final_pagesize,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )

    styles = getSampleStyleSheet()

    # Set default font based on Unicode support
    default_font = unicode_font_name if use_unicode_fonts else 'Helvetica'
    bold_font = f'{unicode_font_name}-Bold' if use_unicode_fonts else 'Helvetica-Bold'
    mono_font = f'{unicode_font_name}-Mono' if use_unicode_fonts else 'Courier'

    # Update base Normal style for Unicode support
    if use_unicode_fonts:
        styles['Normal'].fontName = default_font
        styles['Heading1'].fontName = bold_font
        styles['Heading2'].fontName = bold_font
        styles['Heading3'].fontName = bold_font
        styles['Heading4'].fontName = bold_font

    # Custom styles
    styles.add(ParagraphStyle(
        name='CustomH1',
        parent=styles['Heading1'],
        fontSize=20,
        fontName=bold_font,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=12,
        spaceBefore=12,
        borderWidth=2,
        borderColor=colors.HexColor('#3498db'),
        borderPadding=8
    ))

    styles.add(ParagraphStyle(
        name='CustomH2',
        parent=styles['Heading2'],
        fontSize=16,
        fontName=bold_font,
        textColor=colors.HexColor('#34495e'),
        spaceAfter=10,
        spaceBefore=10,
        borderWidth=1,
        borderColor=colors.HexColor('#95a5a6'),
        borderPadding=6
    ))

    styles.add(ParagraphStyle(
        name='CustomH3',
        parent=styles['Heading3'],
        fontSize=14,
        fontName=bold_font,
        textColor=colors.HexColor('#555555'),
        spaceAfter=8,
        spaceBefore=8
    ))

    styles.add(ParagraphStyle(
        name='CustomCode',
        parent=styles['Code'],
        fontSize=7,
        fontName=mono_font,
        backgroundColor=colors.HexColor('#f8f8f8'),
        borderWidth=1,
        borderColor=colors.HexColor('#dddddd'),
        borderPadding=8,
        leftIndent=8,
        rightIndent=8
    ))

    story = []
    temp_files = []  # Track temporary files for cleanup

    # Calculate available width for images (page width minus margins)
    available_width = final_pagesize[0] - doc.leftMargin - doc.rightMargin

    # Process elements with look-ahead for keeping titles with diagrams
    i = 0
    while i < len(elements):
        elem_type, content = elements[i]

        # Look ahead: if next non-space element is a mermaid diagram, group title with it
        # Skip over any 'space' elements when looking ahead
        next_idx = i + 1
        while next_idx < len(elements) and elements[next_idx][0] == 'space':
            next_idx += 1
        next_is_diagram = (next_idx < len(elements) and elements[next_idx][0] == 'mermaid')
        next_is_h3_or_h4 = (next_idx < len(elements) and elements[next_idx][0] in ['h3', 'h4'])

        # For H2, look even further ahead to see if there's H3/H4 + diagram pattern
        h2_has_nested_diagram = False
        nested_h_idx = None
        nested_diagram_idx = None
        if elem_type == 'h2' and next_is_h3_or_h4:
            # Found H2 → H3/H4, now check if H3/H4 → diagram
            nested_h_idx = next_idx
            check_idx = next_idx + 1
            while check_idx < len(elements) and elements[check_idx][0] == 'space':
                check_idx += 1
            if check_idx < len(elements) and elements[check_idx][0] == 'mermaid':
                h2_has_nested_diagram = True
                nested_diagram_idx = check_idx

        if elem_type == 'h1':
            content = remove_emoji(content)
            content = remove_hyperlinks(content)
            story.append(Paragraph(content, styles['CustomH1']))
            i += 1

        elif elem_type == 'h2' and h2_has_nested_diagram:
            # Keep H2 + H3/H4 + diagram together
            group = []
            content = remove_emoji(content)
            content = remove_hyperlinks(content)
            group.append(Paragraph(content, styles['CustomH2']))

            # Add the H3/H4 title
            nested_h_type, nested_h_content = elements[nested_h_idx]
            nested_h_content = remove_emoji(nested_h_content)
            nested_h_content = remove_hyperlinks(nested_h_content)
            nested_style = styles['CustomH3'] if nested_h_type == 'h3' else styles['Heading4']
            group.append(Paragraph(nested_h_content, nested_style))

            # Add the diagram
            diagram_type, diagram_content = elements[nested_diagram_idx]
            if enable_mermaid and MERMAID_AVAILABLE and playwright_available:
                try:
                    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
                        tmp_path_png = tmp_file.name
                    temp_files.append(tmp_path_png)

                    render_width = 1200
                    render_height = 1200

                    if render_mermaid_to_png(diagram_content, tmp_path_png, width=render_width, height=render_height, scale=mermaid_scale, theme=mermaid_theme):
                        group.append(Spacer(1, 0.3*cm))
                        img = HighQualityImage(tmp_path_png)
                        group.append(img)
                        group.append(Spacer(1, 0.5*cm))
                        mermaid_rendered += 1
                    else:
                        group.append(Paragraph("<i>Mermaid diagram (rendering failed)</i>", styles['Normal']))
                        group.append(Preformatted(diagram_content[:500], styles['CustomCode']))
                except Exception as e:
                    group.append(Paragraph(f"<i>Mermaid diagram (error: {str(e)})</i>", styles['Normal']))
            else:
                group.append(Preformatted(diagram_content, styles['CustomCode']))

            # Wrap in KeepTogether to prevent page breaks
            story.append(KeepTogether(group))
            # Skip past all processed elements
            i = nested_diagram_idx + 1

        elif elem_type == 'h2':
            content = remove_emoji(content)
            content = remove_hyperlinks(content)
            story.append(Paragraph(content, styles['CustomH2']))
            i += 1

        elif elem_type in ['h3', 'h4'] and next_is_diagram:
            # Keep title together with following diagram
            group = []
            content = remove_emoji(content)
            content = remove_hyperlinks(content)
            title_style = styles['CustomH3'] if elem_type == 'h3' else styles['Heading4']
            group.append(Paragraph(content, title_style))

            # Skip to the diagram (next_idx was calculated to skip over spaces)
            diagram_type, diagram_content = elements[next_idx]

            # Render diagram and add to group
            if enable_mermaid and MERMAID_AVAILABLE and playwright_available:
                try:
                    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
                        tmp_path_png = tmp_file.name
                    temp_files.append(tmp_path_png)

                    render_width = 1200
                    render_height = 1200

                    if render_mermaid_to_png(diagram_content, tmp_path_png, width=render_width, height=render_height, scale=mermaid_scale, theme=mermaid_theme):
                        group.append(Spacer(1, 0.3*cm))
                        img = HighQualityImage(tmp_path_png)
                        group.append(img)
                        group.append(Spacer(1, 0.5*cm))
                        mermaid_rendered += 1
                    else:
                        group.append(Paragraph("<i>Mermaid diagram (rendering failed)</i>", styles['Normal']))
                        group.append(Preformatted(diagram_content[:500], styles['CustomCode']))
                except Exception as e:
                    group.append(Paragraph(f"<i>Mermaid diagram (error: {str(e)})</i>", styles['Normal']))
            else:
                group.append(Preformatted(diagram_content, styles['CustomCode']))

            # Wrap in KeepTogether to prevent page breaks between title and diagram
            story.append(KeepTogether(group))
            # Skip past the diagram (and any spaces in between)
            i = next_idx + 1

        elif elem_type == 'h3':
            content = remove_emoji(content)
            content = remove_hyperlinks(content)
            story.append(Paragraph(content, styles['CustomH3']))
            i += 1

        elif elem_type == 'h4':
            content = remove_emoji(content)
            content = remove_hyperlinks(content)
            story.append(Paragraph(content, styles['Heading4']))
            i += 1

        elif elem_type == 'p':
            # Handle inline formatting
            # Remove emoji first
            content = remove_emoji(content)
            # Remove hyperlinks
            content = remove_hyperlinks(content)
            # Escape XML special characters
            content = content.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            # Apply markdown formatting
            content = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', content)
            content = re.sub(r'`(.+?)`', r'<font face="courier" color="#666666">\1</font>', content)
            story.append(Paragraph(content, styles['Normal']))
            i += 1

        elif elem_type == 'list':
            # Handle inline formatting
            # Remove emoji first
            content = remove_emoji(content)
            # Remove hyperlinks
            content = remove_hyperlinks(content)
            # Escape XML special characters
            content = content.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            # Apply markdown formatting
            content = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', content)
            content = re.sub(r'`(.+?)`', r'<font face="courier" color="#666666">\1</font>', content)
            story.append(Paragraph(f"&#8226; {content}", styles['Normal']))
            i += 1

        elif elem_type == 'numlist':
            # Handle inline formatting
            # Remove emoji first
            content = remove_emoji(content)
            # Remove hyperlinks
            content = remove_hyperlinks(content)
            # Escape XML special characters
            content = content.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            # Apply markdown formatting
            content = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', content)
            content = re.sub(r'`(.+?)`', r'<font face="courier" color="#666666">\1</font>', content)
            story.append(Paragraph(f"  {content}", styles['Normal']))
            i += 1

        elif elem_type == 'mermaid':
            # Standalone mermaid diagram (no preceding title)
            # Render Mermaid diagram as ultra high-resolution PNG
            if enable_mermaid and MERMAID_AVAILABLE and playwright_available:
                try:
                    # Use PNG with VERY high resolution for crisp rendering
                    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
                        tmp_path_png = tmp_file.name
                    temp_files.append(tmp_path_png)

                    # Render Mermaid at high resolution for PDF clarity
                    # Target width for diagrams when displayed in PDF (in pixels)
                    # With mermaid_scale=2-3, final PNG will be: width * scale
                    # Example: 1200 * 2 = 2400px width for crisp rendering
                    render_width = 1200  # Base width, multiplied by scale factor in mermaid.py
                    render_height = 1200  # Base height for viewport

                    if render_mermaid_to_png(content, tmp_path_png, width=render_width, height=render_height, scale=mermaid_scale, theme=mermaid_theme):
                        # Use custom HighQualityImage flowable to preserve full resolution
                        # HighQualityImage will automatically size itself to fit available width
                        # Add spacing before and after for better visual separation
                        story.append(Spacer(1, 0.3*cm))  # Margin before diagram
                        img = HighQualityImage(tmp_path_png)
                        story.append(img)
                        story.append(Spacer(1, 0.5*cm))  # Margin after diagram
                        mermaid_rendered += 1
                    else:
                        # Fallback: show as code block
                        story.append(Paragraph("<i>Mermaid diagram (rendering failed)</i>", styles['Normal']))
                        story.append(Preformatted(content[:500], styles['CustomCode']))
                except Exception as e:
                    # Fallback on error
                    story.append(Paragraph(f"<i>Mermaid diagram (error: {str(e)})</i>", styles['Normal']))
            else:
                # Fallback: show as code block if Mermaid disabled or unavailable
                story.append(Preformatted(content, styles['CustomCode']))
            i += 1

        elif elem_type == 'code':
            # Code blocks with automatic chunking
            lines = content.split('\n')
            formatted_lines = []
            for line in lines:
                if len(line) > 95:
                    # Wrap long lines
                    formatted_lines.append(line[:95])
                    formatted_lines.append('  ' + line[95:])
                else:
                    formatted_lines.append(line)

            # Split into chunks for large code blocks
            MAX_LINES = 100
            for chunk_idx in range(0, len(formatted_lines), MAX_LINES):
                chunk = formatted_lines[chunk_idx:chunk_idx+MAX_LINES]
                code_text = '\n'.join(chunk)
                story.append(Preformatted(code_text, styles['CustomCode']))
                if chunk_idx + MAX_LINES < len(formatted_lines):
                    story.append(Spacer(1, 0.1*cm))
            i += 1

        elif elem_type == 'table':
            # Parse table
            table_data = []
            for line in content:
                if '---' in line or '===' in line:
                    continue
                cells = [cell.strip() for cell in line.split('|') if cell.strip()]
                if cells:
                    # Process markdown formatting in each cell
                    processed_cells = []
                    for cell in cells:
                        # Escape XML special characters first
                        cell = cell.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                        # Apply markdown formatting
                        cell = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', cell)
                        cell = re.sub(r'`(.+?)`', r'<font face="courier" color="#666666">\1</font>', cell)
                        # Convert to Paragraph for ReportLab to process formatting
                        processed_cells.append(Paragraph(cell, styles['Normal']))
                    table_data.append(processed_cells)

            if table_data:
                t = Table(table_data)
                t.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                    ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dddddd')),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')])
                ]))
                story.append(t)
            i += 1

        elif elem_type == 'hr':
            story.append(Spacer(1, 0.3*cm))
            story.append(Paragraph('<hr/>', styles['Normal']))
            story.append(Spacer(1, 0.3*cm))
            i += 1

        elif elem_type == 'space':
            story.append(Spacer(1, 0.2*cm))
            i += 1

        else:
            # Unknown element type, skip
            i += 1

    # Build PDF with page numbers
    if page_numbers:
        doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
    else:
        doc.build(story)

    # Cleanup temporary files
    for tmp_file in temp_files:
        try:
            os.unlink(tmp_file)
        except:
            pass

    return {
        'success': True,
        'mermaid_count': mermaid_count,
        'mermaid_rendered': mermaid_rendered,
        'playwright_available': playwright_available
    }
