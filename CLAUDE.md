# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

md2pdf-mermaid is a Python CLI tool and library that converts Markdown to PDF with native emoji rendering and automatic Mermaid diagram support. Published on PyPI as `md2pdf-mermaid` (v1.4.3).

## Commands

```bash
# Install for development
pip install -e ".[dev]"
playwright install chromium

# Run CLI
md2pdf document.md
md2pdf document.md -o output.pdf --title "Report" --engine html

# Run all tests
pytest tests/

# Run a single test
pytest tests/nested_lists_test.py::TestParseMarkdownLists::test_flat_bullet_list -v

# Format / lint / typecheck
black md2pdf/
flake8 md2pdf/
mypy md2pdf/

# Build distribution
python -m build
```

## Architecture

Dual-engine design with a shared CLI entry point:

- **`cli.py`** — Entry point (`md2pdf` console script). Parses args, dispatches to the selected engine.
- **`html_renderer.py`** — Default engine. Converts markdown to HTML, renders to PDF via Playwright/Chromium. Native emoji support, no special handling needed.
- **`converter.py`** — Legacy ReportLab engine. Parses markdown into `(type, content)` tuples via `parse_markdown()`, builds PDF with ReportLab flowables. Uses `EmojiHandler` for emoji processing.
- **`mermaid.py`** — Renders Mermaid diagram code to PNG using Playwright + Mermaid.js v11. Smart dimension detection with multiple fallbacks (getBBox → viewBox → boundingClientRect).
- **`emoji_handler.py`** — Multi-strategy emoji processor (`auto`/`pilmoji`/`remove`/`keep`). Only used by the ReportLab engine.

### Processing pipelines

**HTML engine:** Markdown → normalize list indentation (4-space) → render Mermaid to base64 images → `markdown` lib → HTML → Playwright PDF

**ReportLab engine:** Markdown → `parse_markdown()` element list → render Mermaid to temp PNGs → build ReportLab Story → `SimpleDocTemplate.build()` → PDF

### Key patterns

- Graceful degradation: missing Playwright disables Mermaid with a warning rather than failing
- `HighQualityImage` (converter.py): custom ReportLab Flowable that preserves PNG resolution
- List indentation: stack-based dynamic nesting detection, HTML engine normalizes to 4-space
- Mermaid rendering polls up to 5s for SVG dimensions, uses canvas-based PNG export with configurable `deviceScaleFactor`

## Package exports (`__init__.py`)

`convert_markdown_to_pdf`, `convert_markdown_to_pdf_html`, `parse_markdown`, `render_mermaid_to_png`, `EmojiHandler`

## Standalone Executables

```bash
# Build standalone binary (requires pyinstaller)
python scripts/build.py

# Output: dist/md2pdf (or dist/md2pdf.exe on Windows)

# Pre-download browser for offline use
./dist/md2pdf --setup-browser
```

CI builds for macOS (ARM64 + Intel), Linux (x86_64), and Windows (x86_64) via `.github/workflows/build-executables.yml`. Triggered on version tags (`v*`) or manual dispatch. Creates GitHub Release with archives.

Key module: `browser_manager.py` — lazy Chromium download on first run for standalone builds.

## Release

Tag-based PyPI publishing via `.github/workflows/publish.yml`. Push a version tag (e.g., `v1.4.4`) to trigger. Same tag also triggers standalone executable builds.
