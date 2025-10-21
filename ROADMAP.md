# Roadmap md2pdf-mermaid

This document outlines the planned features and improvements for md2pdf-mermaid.

## Recently Completed

### v1.3.1 (2025-10-21) - Patch Release ✅
- [x] Extended emoji removal to cover Miscellaneous Technical symbols (⏰, ⏱️, ⏲️)
- [x] Fixed Unicode range 0x2300-0x23FF handling in `remove_emoji()`

### v1.3.0 (2025-10-21) ✅
- [x] Mermaid theme support (5 themes: default, neutral, dark, forest, base)
- [x] Mermaid quality/resolution control (--mermaid-scale flag)
- [x] Automatic emoji removal for PDF compatibility
- [x] Hyperlink handling (convert to plain text)
- [x] Fixed Mermaid diagram sizing and quality issues

### v1.2.0 (2025-10-20) ✅
- [x] Full Unicode/UTF-8 support with automatic font detection
- [x] Customizable font selection (Arial, DejaVu, Helvetica, custom TTF)
- [x] Bold and inline code formatting in lists
- [x] Full-width Mermaid diagrams

### v1.1.0 (2025-10-20) ✅
- [x] Page numbering in PDF footer
- [x] Page size options (A4, A3, Letter)
- [x] Page orientation options (Portrait, Landscape)

## Future Versions

## Version 1.4.0 (Planned)

### Custom Mermaid Themes
- [ ] `--mermaid-theme dark|forest|neutral|default` - Built-in theme support
- [ ] `--mermaid-theme-file custom.css` - Custom theme CSS file support
- [ ] Theme preview in documentation

**Rationale**: Different diagram themes for different documentation styles (dark mode docs, corporate themes, etc.)

### Page Customization
- [ ] `--page-size A4|Letter|A3|A5` - Standard page sizes
- [ ] `--orientation portrait|landscape` - Page orientation
- [ ] `--margins "top,right,bottom,left"` - Custom margins in mm/inches
- [ ] `--header` and `--footer` - Custom headers/footers

**Rationale**: Professional PDF output requires control over page formatting

### Custom Styling
- [ ] `--style custom.yaml` - YAML-based style configuration
- [ ] Support for custom fonts
- [ ] Color scheme customization
- [ ] Code block syntax highlighting themes

**Rationale**: Brand consistency and corporate documentation requirements

### Batch Processing
- [ ] `md2pdf docs/*.md --output-dir pdfs/` - Process multiple files
- [ ] `--recursive` - Process directories recursively
- [ ] Progress bar for multiple files
- [ ] `--watch` mode for auto-regeneration

**Rationale**: Efficient workflow for documentation projects with many files

### Table of Contents
- [ ] `--toc` - Auto-generate table of contents
- [ ] `--toc-depth 1|2|3` - Control TOC depth
- [ ] `--toc-title "Custom Title"` - Custom TOC title
- [ ] Clickable TOC links in PDF

**Rationale**: Essential for long documentation and reports

### Hyperlink Support
- [ ] Clickable hyperlinks in PDF (internal anchors)
- [ ] External URL links
- [ ] Cross-references between sections
- [ ] Automatic link styling

**Rationale**: Currently hyperlinks are removed for readability. Full support requires ReportLab anchor implementation for professional interactive PDFs.

## Version 1.2.0 (Future)

### Performance Improvements
- [ ] Parallel Mermaid diagram rendering
- [ ] Diagram caching for repeated conversions
- [ ] Incremental updates (only changed diagrams)
- [ ] Memory optimization for large documents

### Advanced Mermaid Support
- [ ] Interactive diagrams (if PDF supports)
- [ ] Diagram scaling options
- [ ] High-DPI rendering for print quality
- [ ] SVG fallback option

### Export Formats
- [ ] HTML export with embedded diagrams
- [ ] DOCX support (Microsoft Word)
- [ ] EPUB for e-readers
- [ ] Multi-format batch export

### Integration Features
- [ ] GitHub Actions integration examples
- [ ] GitLab CI templates
- [ ] Pre-commit hooks
- [ ] API for programmatic use

## Version 2.0.0 (Long-term)

### Templating System
- [ ] Document templates (reports, articles, books)
- [ ] Custom layouts
- [ ] Multi-column support
- [ ] Advanced typography

### Collaboration Features
- [ ] Metadata support (author, version, date)
- [ ] Change tracking in generated PDFs
- [ ] Diff visualization between versions

### Enterprise Features
- [ ] Digital signatures
- [ ] Watermarks
- [ ] Password protection
- [ ] Compliance modes (PDF/A, PDF/X)

## Community Requests

Track feature requests from users:
- [ ] TBD based on GitHub issues

## Notes

- Versions are tentative and may change based on community feedback
- Breaking changes will follow semantic versioning (major version bump)
- Security and bug fixes take priority over new features
