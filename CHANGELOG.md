# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned for Future Versions
- Batch processing with `md2pdf docs/*.md --output-dir pdfs/`
- Table of contents auto-generation
- Custom CSS injection via YAML configuration
- Emoji rendering with color emoji fonts (future enhancement)

See [ROADMAP.md](ROADMAP.md) for detailed feature planning and long-term vision.

## [1.3.1] - 2025-10-21

### Fixed
- **Emoji removal for Miscellaneous Technical symbols** (⏰, ⏱️, ⏲️, etc.)
  - Added Unicode range 0x2300-0x23FF to `remove_emoji()` function
  - Previously, clock emoji (⏰) and similar technical symbols were converted to fallback characters (􀀀)
  - Now all technical symbols are cleanly removed from PDF output
  - Fixes issue where some emoji were not properly handled in v1.3.0

### Technical
- Extended `remove_emoji()` Unicode codepoint detection with range 0x2300-0x23FF (Miscellaneous Technical)
- This range includes: clock symbols, watch symbols, timer symbols, and other technical indicators

## [1.3.0] - 2025-10-21

### Added
- **Mermaid theme support** (`--mermaid-theme` CLI flag)
  - 5 color themes: `default`, `neutral`, `dark`, `forest`, `base`
  - Python API: `mermaid_theme` parameter
  - Themes applied during canvas-based rendering for consistent colors
- **Mermaid quality/resolution control** (`--mermaid-scale` CLI flag)
  - Scale factor 1-4 for diagram resolution (default: 2 = high quality)
  - Python API: `mermaid_scale` parameter
  - Higher scales produce crisper diagrams but take longer to render
- **Automatic emoji removal**
  - Emoji characters are automatically removed for PDF compatibility
  - ReportLab doesn't support color emoji fonts, so text is kept clean
  - Future enhancement: render emoji as inline images
- **Hyperlink handling**
  - Markdown hyperlinks `[text](url)` are now converted to plain text, keeping only the link text
  - Improves document readability in PDFs where links can cause rendering issues
  - Reference-style links and link definitions are also handled
  - Full clickable hyperlink support planned for future version (see ROADMAP.md)

### Fixed
- **Fixed Mermaid diagram sizing issues** - Canvas-based rendering ensures exact pixel dimensions
  - Previous versions had inconsistent whitespace around diagrams
  - Now uses forced canvas dimensions (2000x1400 at scale 2) for predictable sizing
  - Diagrams properly fill 90% of page width with consistent margins
- **Fixed Mermaid diagram quality** - High-resolution rendering (2x scale by default)
  - Previous versions sometimes produced low-quality or tiny diagrams
  - Canvas-based approach with deviceScaleFactor ensures crisp output
- **Improved diagram spacing** - Better margins around Mermaid diagrams
  - 0.3cm spacer before diagram
  - 0.5cm spacer after diagram
  - Prevents diagrams from cramming against surrounding text

### Changed
- **Breaking**: Emoji are now automatically removed from text
  - Previous behavior: Emoji rendered as boxes (□) or question marks (�)
  - New behavior: Emoji silently removed, keeping text clean and readable
  - Affects: Document titles, headers, paragraphs, lists, tables

### Technical
- Refactored `render_mermaid_to_png()` to use canvas-based rendering
- Added `mermaid_theme` and `mermaid_scale` parameters throughout conversion pipeline
- Added `remove_emoji()` function with Unicode codepoint range detection
- Added `remove_hyperlinks()` function to strip markdown link syntax while preserving text
- Theme configuration injected into Mermaid initialization code
- Canvas dimensions calculated as `base_width * scale, base_height * scale`
- Hyperlink removal applied to all text elements (headers, paragraphs, lists)

## [1.2.0] - 2025-10-20

### Added
- **Full Unicode/UTF-8 support** with automatic font detection
  - Auto-detects and loads Arial (Windows) or DejaVu (Linux) for Unicode support
  - Properly displays special characters: bullets (•), accented letters (è, à, ñ), emoji, and multilingual text
  - Font family registration enables bold/italic switching in Unicode fonts
- **Customizable font selection**
  - New `--font` CLI parameter: `arial`, `dejavu`, `helvetica`, or path to custom TTF file
  - New `font_name` parameter in Python API
  - Supports custom TTF font files
- **Bold and inline code formatting in lists**
  - Bullet and numbered lists now support `**bold**` and `` `inline code` `` formatting
  - Same markdown formatting support as regular paragraphs
- **Full-width Mermaid diagrams**
  - Diagrams now use entire page width (minus margins) for maximum readability
  - Increased rendering resolution from 1400x1000 to 2000x1400 for higher quality
  - Screenshot optimization: captures only SVG element, eliminating white space

### Fixed
- **Character encoding issues** - Bullet characters (•) and accented letters now display correctly instead of appearing as corrupted characters (â€¢, Ã¨)
- **Mermaid diagram sizing** - Diagrams are now significantly larger and more readable
- **Font rendering** - Bold text now renders correctly with Unicode fonts

### Technical
- Added `reportlab.pdfbase.ttfonts.TTFont` import for TrueType font support
- Implemented font family registration with `registerFontFamily()` for proper bold/italic support
- Dynamic font detection attempts multiple font sources in order of preference
- Added `available_width` calculation for full-page-width image rendering
- Modified Mermaid rendering to use `svg_element.screenshot()` instead of `page.screenshot(full_page=True)`
- Inline formatting (escape XML, apply bold/code regex) now applied to list items

### CLI
- Added `--font` parameter with options: `auto`, `arial`, `dejavu`, `helvetica`, or custom TTF path
- Updated help text and examples to show font selection usage

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

[Unreleased]: https://github.com/rbutinar/md2pdf-mermaid/compare/v1.3.1...HEAD
[1.3.1]: https://github.com/rbutinar/md2pdf-mermaid/compare/v1.3.0...v1.3.1
[1.3.0]: https://github.com/rbutinar/md2pdf-mermaid/compare/v1.2.0...v1.3.0
[1.2.0]: https://github.com/rbutinar/md2pdf-mermaid/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/rbutinar/md2pdf-mermaid/compare/v1.0.1...v1.1.0
[1.0.1]: https://github.com/rbutinar/md2pdf-mermaid/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/rbutinar/md2pdf-mermaid/releases/tag/v1.0.0
