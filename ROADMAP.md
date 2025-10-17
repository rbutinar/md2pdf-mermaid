# Roadmap md2pdf-mermaid

This document outlines the planned features and improvements for md2pdf-mermaid.

## Version 1.1.0 (Planned)

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
