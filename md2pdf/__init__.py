"""
md2pdf - Markdown to PDF Converter with Mermaid Support

Convert Markdown documents to professional PDFs with automatic
Mermaid diagram rendering.
"""

from .converter import convert_markdown_to_pdf, parse_markdown
from .mermaid import render_mermaid_to_png

__version__ = "1.3.1"
__author__ = "Roberto Butinar"
__all__ = ["convert_markdown_to_pdf", "parse_markdown", "render_mermaid_to_png"]
