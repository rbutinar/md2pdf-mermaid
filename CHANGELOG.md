# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned for Future Versions
- Custom Mermaid themes (dark, forest, neutral)
- Batch processing with `md2pdf docs/*.md --output-dir pdfs/`
- Table of contents auto-generation
- Custom CSS injection via YAML configuration

See [ROADMAP.md](ROADMAP.md) for detailed feature planning and long-term vision.

## [1.1.0] - 2025-10-20

### Added
- **Page numbering** in PDF footer (centered at bottom of each page)
  - Enabled by default
  - Can be disabled with `--no-page-numbers` flag
- **Page size options**: A4, A3, Letter
  - Use `--page-size` flag (default: a4)
- **Page orientation options**: Portrait, Landscape
  - Use `--orientation` flag (default: portrait)

### Technical
- New `get_page_size()` function to handle page dimensions
- Updated `add_page_number()` to work with any page size
- CLI now supports `--page-size`, `--orientation`, and `--no-page-numbers` flags
- Version updated to 1.1.0

## [1.0.1] - 2025-10-20

### Fixed
- Bold formatting (`**text**`) in table cells now renders correctly in PDF
- Previously, `**` markers were displayed literally instead of being converted to bold text
- Table cells now support the same inline markdown formatting as paragraphs (bold and inline code)

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

### Documentation
- WSL (Windows Subsystem for Linux) setup guide
- PyPI package publication
- Comprehensive README with examples

---

## Version Links

[Unreleased]: https://github.com/rbutinar/md2pdf-mermaid/compare/v1.1.0...HEAD
[1.1.0]: https://github.com/rbutinar/md2pdf-mermaid/compare/v1.0.1...v1.1.0
[1.0.1]: https://github.com/rbutinar/md2pdf-mermaid/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/rbutinar/md2pdf-mermaid/releases/tag/v1.0.0
