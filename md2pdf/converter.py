#!/usr/bin/env python3
"""
Markdown to PDF Converter
Professional PDF generation from Markdown with Mermaid diagram support
"""

import os
import re
import tempfile
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Preformatted, Image
)
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT

try:
    from .mermaid import render_mermaid_to_png, is_playwright_available
    MERMAID_AVAILABLE = True
except ImportError:
    MERMAID_AVAILABLE = False
    def is_playwright_available():
        return False


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


def convert_markdown_to_pdf(markdown_text, output_path, title="Document",
                            enable_mermaid=True):
    """
    Convert Markdown text to PDF

    Args:
        markdown_text: Markdown content as string
        output_path: Path to output PDF file
        title: Document title
        enable_mermaid: Enable Mermaid diagram rendering (default: True)

    Returns:
        dict with keys:
            - success: True if successful, False otherwise
            - mermaid_count: Number of Mermaid diagrams found
            - mermaid_rendered: Number of Mermaid diagrams successfully rendered
            - playwright_available: Whether Playwright is available
    """

    # Parse markdown
    elements = parse_markdown(markdown_text)

    # Track Mermaid diagrams
    mermaid_count = sum(1 for elem_type, _ in elements if elem_type == 'mermaid')
    mermaid_rendered = 0
    playwright_available = is_playwright_available()

    # Create PDF
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )

    styles = getSampleStyleSheet()

    # Custom styles
    styles.add(ParagraphStyle(
        name='CustomH1',
        parent=styles['Heading1'],
        fontSize=20,
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
        textColor=colors.HexColor('#555555'),
        spaceAfter=8,
        spaceBefore=8
    ))

    styles.add(ParagraphStyle(
        name='CustomCode',
        parent=styles['Code'],
        fontSize=7,
        fontName='Courier',
        backgroundColor=colors.HexColor('#f8f8f8'),
        borderWidth=1,
        borderColor=colors.HexColor('#dddddd'),
        borderPadding=8,
        leftIndent=8,
        rightIndent=8
    ))

    story = []
    temp_files = []  # Track temporary files for cleanup

    for elem_type, content in elements:
        if elem_type == 'h1':
            story.append(Paragraph(content, styles['CustomH1']))

        elif elem_type == 'h2':
            story.append(Paragraph(content, styles['CustomH2']))

        elif elem_type == 'h3':
            story.append(Paragraph(content, styles['CustomH3']))

        elif elem_type == 'h4':
            story.append(Paragraph(content, styles['Heading4']))

        elif elem_type == 'p':
            # Handle inline formatting
            # Escape XML special characters first
            content = content.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            # Apply markdown formatting
            content = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', content)
            content = re.sub(r'`(.+?)`', r'<font face="courier" color="#666666">\1</font>', content)
            story.append(Paragraph(content, styles['Normal']))

        elif elem_type == 'list':
            story.append(Paragraph(f"• {content}", styles['Normal']))

        elif elem_type == 'numlist':
            story.append(Paragraph(f"  {content}", styles['Normal']))

        elif elem_type == 'mermaid':
            # Render Mermaid diagram as image
            if enable_mermaid and MERMAID_AVAILABLE and playwright_available:
                try:
                    # Create temporary file for PNG
                    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
                        tmp_path = tmp_file.name
                    temp_files.append(tmp_path)

                    # Render Mermaid
                    if render_mermaid_to_png(content, tmp_path, width=1400, height=1000):
                        # Insert image in PDF
                        img = Image(tmp_path, width=16*cm, height=10*cm, kind='proportional')
                        story.append(img)
                        story.append(Spacer(1, 0.3*cm))
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
            for i in range(0, len(formatted_lines), MAX_LINES):
                chunk = formatted_lines[i:i+MAX_LINES]
                code_text = '\n'.join(chunk)
                story.append(Preformatted(code_text, styles['CustomCode']))
                if i + MAX_LINES < len(formatted_lines):
                    story.append(Spacer(1, 0.1*cm))

        elif elem_type == 'table':
            # Parse table
            table_data = []
            for line in content:
                if '---' in line or '===' in line:
                    continue
                cells = [cell.strip() for cell in line.split('|') if cell.strip()]
                if cells:
                    table_data.append(cells)

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

        elif elem_type == 'hr':
            story.append(Spacer(1, 0.3*cm))
            story.append(Paragraph('<hr/>', styles['Normal']))
            story.append(Spacer(1, 0.3*cm))

        elif elem_type == 'space':
            story.append(Spacer(1, 0.2*cm))

    # Build PDF
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
