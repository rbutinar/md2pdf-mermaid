# Getting Started with md2pdf-mermaid

Quick guide to start using md2pdf-mermaid in your projects.

---

## 📦 Installation

### Option 1: From Git Repository (Recommended)

```bash
# Install from GitHub/Azure DevOps
pip install git+https://github.com/rbutinar/md2pdf-mermaid.git

# Or install specific version
pip install git+https://github.com/rbutinar/md2pdf-mermaid.git@v1.0.0

# Install Playwright browser (required for Mermaid)
playwright install chromium
```

### Option 2: Local Development

```bash
# Clone repository
cd /path/to/md2pdf-mermaid

# Install in editable mode
pip install -e .

# Install Playwright browser
playwright install chromium
```

---

## 🚀 Quick Usage

### Command Line

```bash
# Convert a single file
md2pdf README.md

# Custom output name
md2pdf document.md -o report.pdf

# Custom title
md2pdf document.md --title "Project Documentation"

# Disable Mermaid (faster)
md2pdf document.md --no-mermaid

# Show help
md2pdf --help
```

### Python Code

```python
from md2pdf import convert_markdown_to_pdf

# Read markdown
with open("document.md", "r") as f:
    markdown = f.read()

# Convert to PDF
convert_markdown_to_pdf(
    markdown,
    "output.pdf",
    title="My Document",
    enable_mermaid=True
)
```

---

## 📋 Using in Your Projects

### Add to requirements.txt

```txt
# requirements.txt
md2pdf-mermaid @ git+https://github.com/rbutinar/md2pdf-mermaid.git@v1.0.0
```

### Add to setup.py

```python
setup(
    name="your-project",
    install_requires=[
        "md2pdf-mermaid @ git+https://github.com/rbutinar/md2pdf-mermaid.git@v1.0.0",
    ],
)
```

### Add to pyproject.toml

```toml
[project]
dependencies = [
    "md2pdf-mermaid @ git+https://github.com/rbutinar/md2pdf-mermaid.git@v1.0.0",
]
```

---

## 🔧 Configuration in Project

### Create Conversion Script

Save as `scripts/generate_pdfs.py`:

```python
#!/usr/bin/env python3
"""Generate PDFs from project documentation"""

from pathlib import Path
from md2pdf import convert_markdown_to_pdf

# Files to convert
docs = [
    "README.md",
    "docs/GUIDE.md",
    "docs/API.md",
]

for doc_file in docs:
    path = Path(doc_file)
    if not path.exists():
        print(f"Skip {doc_file} (not found)")
        continue

    # Convert
    with open(path, "r") as f:
        content = f.read()

    output_path = path.with_suffix(".pdf")
    convert_markdown_to_pdf(content, str(output_path), title=path.stem)

    print(f"✓ Created {output_path}")
```

Run with:
```bash
python scripts/generate_pdfs.py
```

---

## 🐳 Docker Integration

### Dockerfile

```dockerfile
FROM python:3.11-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    wget gnupg \
    && rm -rf /var/lib/apt/lists/*

# Install md2pdf
RUN pip install git+https://github.com/rbutinar/md2pdf-mermaid.git

# Install Playwright browser
RUN playwright install chromium --with-deps

WORKDIR /workspace

# Convert markdown files
CMD ["md2pdf", "README.md"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  pdf-generator:
    build: .
    volumes:
      - ./docs:/workspace
    command: md2pdf /workspace/README.md
```

---

## 🔄 CI/CD Integration

### GitHub Actions

`.github/workflows/generate-pdfs.yml`:

```yaml
name: Generate PDFs

on:
  push:
    paths:
      - 'docs/**/*.md'
      - 'README.md'

jobs:
  generate-pdfs:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install md2pdf
        run: |
          pip install git+https://github.com/rbutinar/md2pdf-mermaid.git
          playwright install chromium

      - name: Generate PDFs
        run: |
          md2pdf README.md
          md2pdf docs/GUIDE.md -o docs/GUIDE.pdf

      - name: Upload PDFs
        uses: actions/upload-artifact@v3
        with:
          name: documentation-pdfs
          path: |
            README.pdf
            docs/*.pdf
```

### Azure DevOps

`azure-pipelines.yml`:

```yaml
trigger:
  paths:
    include:
      - docs/**/*.md
      - README.md

pool:
  vmImage: 'ubuntu-latest'

steps:
- task: UsePythonVersion@0
  inputs:
    versionSpec: '3.11'

- script: |
    pip install git+https://github.com/rbutinar/md2pdf-mermaid.git
    playwright install chromium
  displayName: 'Install dependencies'

- script: |
    md2pdf README.md
    md2pdf docs/GUIDE.md -o docs/GUIDE.pdf
  displayName: 'Generate PDFs'

- task: PublishBuildArtifacts@1
  inputs:
    pathToPublish: '$(Build.SourcesDirectory)'
    artifactName: 'documentation'
```

---

## 🎯 Examples

### Example 1: Documentation for Client

```python
from md2pdf import convert_markdown_to_pdf

# Project documentation
files = [
    ("README.md", "Project Overview"),
    ("docs/ARCHITECTURE.md", "System Architecture"),
    ("docs/DEPLOYMENT.md", "Deployment Guide"),
]

for md_file, title in files:
    with open(md_file) as f:
        content = f.read()

    pdf_file = md_file.replace('.md', '_CLIENT.pdf')
    convert_markdown_to_pdf(content, pdf_file, title=title)

    print(f"✓ {pdf_file}")
```

### Example 2: Batch Conversion

```python
from pathlib import Path
from md2pdf import convert_markdown_to_pdf

# Convert all markdown in docs/
for md_file in Path("docs").rglob("*.md"):
    with open(md_file) as f:
        content = f.read()

    pdf_file = md_file.with_suffix(".pdf")
    convert_markdown_to_pdf(
        content,
        str(pdf_file),
        title=md_file.stem
    )

    print(f"✓ {pdf_file}")
```

### Example 3: Custom Workflow

```python
from md2pdf import parse_markdown, convert_markdown_to_pdf

# Read and modify markdown
with open("template.md") as f:
    content = f.read()

# Add dynamic content
content += f"\n\n## Generated: {datetime.now()}\n"
content += f"\nVersion: {get_version()}\n"

# Convert
convert_markdown_to_pdf(content, "report.pdf", title="Weekly Report")
```

---

## 📝 Tips

1. **Version Pinning**: Always pin to a specific version in production
   ```txt
   md2pdf-mermaid @ git+https://...@v1.0.0
   ```

2. **Cache Playwright**: In CI/CD, cache Playwright browser to speed up builds

3. **Parallel Conversion**: Use multiprocessing for batch conversions

4. **Fallback Mode**: Test with `--no-mermaid` if Playwright causes issues

5. **File Size**: PDFs with many Mermaid diagrams can be 200-300 KB

---

## 🆘 Troubleshooting

### Package Not Found

```bash
# Verify package is accessible
pip install git+https://github.com/rbutinar/md2pdf-mermaid.git --dry-run
```

### Chromium Installation Failed

```bash
# Force reinstall
playwright install --force chromium

# Or install system-wide
sudo apt-get install chromium-browser
```

### Import Error

```python
# Make sure package is installed
import sys
print(sys.path)

# Try reinstalling
pip uninstall md2pdf-mermaid
pip install git+https://github.com/rbutinar/md2pdf-mermaid.git
```

---

## 🔗 Next Steps

- Read full documentation: [README.md](README.md)
- Check examples: [TEST_DOCUMENT.md](TEST_DOCUMENT.md)
- Report issues: https://github.com/rbutinar/md2pdf-mermaid/issues

---

**Happy Converting!** 🎉
