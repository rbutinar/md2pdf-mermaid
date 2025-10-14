# md2pdf-mermaid

**Professional Markdown to PDF converter with automatic Mermaid diagram rendering**

Convert your Markdown documentation to beautiful PDFs with:
- ✅ Professional formatting (headers, tables, code blocks)
- ✅ **Automatic Mermaid diagram rendering** (diagrams as PNG images)
- ✅ Syntax highlighting for code blocks
- ✅ Customizable styling
- ✅ CLI and Python API
- ✅ Fast and reliable

---

## 🚀 Quick Start

### Installation

```bash
# From Git repository
pip install git+https://github.com/rbutinar/md2pdf-mermaid.git

# Install Playwright browser (required for Mermaid rendering)
playwright install chromium
```

**WSL Users**: Use Windows Python to avoid dependency issues:
```bash
python3.exe -m venv venv  # Windows venv, no sudo needed!
venv/Scripts/pip.exe install git+https://github.com/rbutinar/md2pdf-mermaid.git
venv/Scripts/playwright.exe install chromium
```
See [WSL_SETUP.md](WSL_SETUP.md) for details.

### Command Line Usage

```bash
# Basic conversion
md2pdf document.md

# Custom output name
md2pdf document.md -o report.pdf

# Custom title
md2pdf document.md --title "Project Report"

# Disable Mermaid rendering (faster, text-only diagrams)
md2pdf document.md --no-mermaid
```

### Python API Usage

```python
from md2pdf import convert_markdown_to_pdf

# Read markdown file
with open("document.md", "r") as f:
    markdown_content = f.read()

# Convert to PDF
convert_markdown_to_pdf(
    markdown_content,
    "output.pdf",
    title="My Document"
)
```

---

## 📋 Features

### Markdown Support

- **Headers** (H1-H4) with colored borders
- **Bold**, *italic*, `inline code`
- Bullet lists and numbered lists
- Tables with colored headers
- Code blocks with syntax highlighting
- Horizontal rules
- **Mermaid diagrams** (rendered as images)

### Mermaid Diagrams

Automatically renders Mermaid diagrams as high-quality PNG images:

````markdown
```mermaid
graph LR
    A[Start] --> B[Process]
    B --> C[End]
    style A fill:#90EE90
    style C fill:#FFD700
```
````

**Becomes a visual diagram in the PDF!**

### PDF Styling

- A4 page size with 2cm margins
- Professional color scheme
- Tables with alternating row colors
- Code blocks with light gray background
- Headers with colored borders
- Optimized font sizes (10pt body, 7pt code)

---

## 🔧 Requirements

- Python 3.8+
- Chromium browser (via Playwright, ~250 MB)
- reportlab, playwright, pillow (installed automatically)

---

## 📚 Use Cases

### 1. Technical Documentation

Convert your project documentation to PDF for:
- Client deliverables
- Internal documentation
- Architecture diagrams (Mermaid)
- API documentation

### 2. Reports and Presentations

Create professional reports with:
- Data flow diagrams
- System architecture
- Process flowcharts
- Executive summaries

### 3. CI/CD Integration

Automatically generate PDFs in your pipeline:

```yaml
# GitHub Actions example
- name: Generate PDF Documentation
  run: |
    pip install git+https://github.com/rbutinar/md2pdf-mermaid.git
    playwright install chromium
    md2pdf README.md -o docs/README.pdf
```

---

## 💡 Advanced Usage

### Batch Conversion

```python
from md2pdf import convert_markdown_to_pdf
from pathlib import Path

# Convert all markdown files
for md_file in Path("docs").glob("*.md"):
    pdf_file = md_file.with_suffix(".pdf")

    with open(md_file, "r") as f:
        content = f.read()

    convert_markdown_to_pdf(content, str(pdf_file), title=md_file.stem)
    print(f"✓ Created {pdf_file}")
```

### Disable Mermaid Rendering

If Playwright is not available or you want faster conversion:

```python
convert_markdown_to_pdf(
    markdown_text,
    "output.pdf",
    enable_mermaid=False  # Diagrams shown as code blocks
)
```

### Custom Styling

The converter uses reportlab's styling system. You can modify styles by:

1. Fork the repository
2. Edit `md2pdf/converter.py`
3. Customize colors, fonts, sizes in the `convert_markdown_to_pdf()` function

---

## 🐛 Troubleshooting

### "Playwright not found" Error

```bash
# Install Playwright
pip install playwright

# Install Chromium browser
playwright install chromium
```

### "Permission denied" When Overwriting PDF

The PDF file is open in a viewer. Close it first, then try again.

### Mermaid Diagrams Not Rendering

1. Check Playwright is installed: `python -c "import playwright"`
2. Check Chromium is installed: `playwright install --force chromium`
3. Try disabling and re-enabling Mermaid: `md2pdf file.md --no-mermaid` (to verify other features work)

### WSL: "Host system is missing dependencies to run browsers"

**Best solution**: Use Windows Python instead of Linux Python (no sudo needed):

```bash
# Create Windows venv from WSL
python3.exe -m venv venv
venv/Scripts/pip.exe install git+https://github.com/rbutinar/md2pdf-mermaid.git
venv/Scripts/playwright.exe install chromium
venv/Scripts/md2pdf.exe document.md  # Works perfectly!
```

**Alternative** (requires sudo): Install Linux dependencies:
```bash
sudo apt-get install -y libnss3 libnspr4 libatk1.0-0 libgbm1 libasound2t64
```

See [WSL_SETUP.md](WSL_SETUP.md) for complete instructions.

### Large File Conversion Slow

Mermaid rendering takes ~10-15 seconds per diagram. For documents with many diagrams:
- Use `--no-mermaid` flag for faster preview
- Run conversion in background
- Consider caching rendered diagrams (future feature)

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

---

## 📝 License

MIT License - see LICENSE file for details

---

## 🔗 Related Projects

- [mermaid](https://mermaid.js.org/) - Diagram syntax
- [reportlab](https://www.reportlab.com/) - PDF generation
- [playwright](https://playwright.dev/) - Browser automation

---

## 📧 Support

- **Issues**: https://github.com/rbutinar/md2pdf-mermaid/issues
- **Documentation**: https://github.com/rbutinar/md2pdf-mermaid

---

## 🎯 Roadmap

- [ ] Support for more Mermaid diagram types
- [ ] Custom CSS themes
- [ ] Image embedding from URLs
- [ ] Table of contents generation
- [ ] Header/footer customization
- [ ] Multi-column layouts
- [ ] PDF metadata (author, keywords, etc.)

---

**Version**: 1.0.0
**Last Updated**: 2025-10-14
**Status**: Production Ready ✅
