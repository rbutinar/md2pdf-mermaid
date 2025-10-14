# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-10-14

### Added
- Initial release
- Markdown to PDF conversion with professional formatting
- Automatic Mermaid diagram rendering using Playwright
- CLI tool (`md2pdf` command)
- Python API for programmatic conversion
- Support for headers, tables, code blocks, lists
- Customizable styling with reportlab
- Fallback mode when Playwright unavailable
- Comprehensive documentation and examples

### Features
- Headers (H1-H4) with colored borders
- Tables with colored headers and alternating rows
- Code blocks with syntax highlighting
- Mermaid diagrams rendered as PNG images
- Inline formatting (bold, italic, code)
- Bullet and numbered lists
- Horizontal rules

### Technical
- Python 3.8+ support
- Playwright for Mermaid rendering
- Reportlab for PDF generation
- Automatic temp file cleanup
- Error handling and fallbacks
