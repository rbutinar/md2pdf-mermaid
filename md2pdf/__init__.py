"""
md2pdf - Markdown to PDF Converter with Mermaid and Emoji Support

Convert Markdown documents to professional PDFs with automatic
Mermaid diagram rendering and configurable emoji support.
"""

from .converter import convert_markdown_to_pdf, parse_markdown
from .html_renderer import convert_markdown_to_pdf_html
from .mermaid import render_mermaid_to_png
from .emoji_handler import EmojiHandler

__version__ = "1.4.0"
__author__ = "Roberto Butinar"
__all__ = ["convert_markdown_to_pdf", "convert_markdown_to_pdf_html", "parse_markdown", "render_mermaid_to_png", "EmojiHandler"]
