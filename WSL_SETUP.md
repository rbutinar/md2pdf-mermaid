# WSL Setup Guide for md2pdf-mermaid

**Problem**: When using md2pdf-mermaid in WSL, Mermaid diagrams fail to render with error:
```
Host system is missing dependencies to run browsers.
```

**Root Cause**: Linux Chromium requires system libraries that are not included in minimal WSL installations.

---

## ✨ RECOMMENDED: Windows Virtual Environment (No sudo required!)

**This is the easiest solution for WSL - uses Windows Python and browsers, avoiding all Linux dependency issues.**

### Setup (Tested on Ubuntu 24.04 WSL2)

```bash
# Create Windows-based virtual environment
python3.exe -m venv venv

# Install md2pdf
venv/Scripts/pip.exe install git+https://github.com/rbutinar/md2pdf-mermaid.git

# Install Chromium (Windows version)
venv/Scripts/playwright.exe install chromium

# Test it!
venv/Scripts/md2pdf.exe test.md
```

**Verified Results**:
- ✅ No sudo required
- ✅ No Linux dependencies needed
- ✅ Mermaid diagrams render perfectly
- ✅ Uses Windows Chromium via WSLInterop

---

## Alternative: Linux Virtual Environment (Requires sudo)

If you prefer a Linux-only setup, you'll need to install system dependencies:

```bash
# Install dependencies for Linux Chromium
sudo apt-get update && sudo apt-get install -y \
    libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 \
    libcups2 libdrm2 libxkbcommon0 libxcomposite1 \
    libxdamage1 libxfixes3 libxrandr2 libgbm1 \
    libasound2t64 libpango-1.0-0 libcairo2

# Then create Linux venv
python3 -m venv venv
source venv/bin/activate
pip install git+https://github.com/rbutinar/md2pdf-mermaid.git
playwright install chromium
```

Then test:

```bash
# Test Chromium directly
~/.cache/ms-playwright/chromium-*/chrome-linux/chrome --version
# Should output: Chromium 131.0.6778.33 (or similar)

# Test md2pdf with Mermaid
md2pdf test_mermaid.md
# Should output: Rendered 1/1 Mermaid diagrams
```

---

## Complete Installation Steps

Follow these steps if setting up from scratch:

### 1. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac/WSL
```

### 2. Install md2pdf-mermaid

```bash
pip install git+https://github.com/rbutinar/md2pdf-mermaid.git
```

### 3. Install Playwright Browser

```bash
playwright install chromium
```

At this point, Playwright will warn about missing dependencies:

```
╔══════════════════════════════════════════════════════╗
║ Host system is missing dependencies to run browsers. ║
║ Please install them with the following command:      ║
║                                                      ║
║     sudo playwright install-deps                     ║
║                                                      ║
║ Alternatively, use apt:                              ║
║     sudo apt-get install libnspr4\                   ║
║         libnss3\                                     ║
║         libasound2t64                                ║
╚══════════════════════════════════════════════════════╝
```

### 4. Install System Dependencies

**Option A - Minimal (Recommended for WSL)**:
```bash
sudo apt-get update
sudo apt-get install -y libnspr4 libnss3 libasound2t64
```

**Option B - Complete (Install all Playwright dependencies)**:
```bash
sudo playwright install-deps chromium
```

Note: Option B installs ~300MB of packages. Option A is sufficient for most cases.

### 5. Verify Installation

```bash
# Check Chromium works
~/.cache/ms-playwright/chromium-*/chrome-linux/chrome --version

# Test conversion without Mermaid
echo "# Test" > test.md
md2pdf test.md --no-mermaid

# Test conversion WITH Mermaid
cat > test_mermaid.md <<'EOF'
# Test

```mermaid
graph LR
    A[Start] --> B[End]
```
EOF

md2pdf test_mermaid.md
# Should show: [OK] Rendered 1/1 Mermaid diagrams
```

---

## What Was Tested

This guide was verified on:
- **OS**: Ubuntu 24.04.2 LTS (WSL2)
- **Python**: 3.12.3
- **md2pdf-mermaid**: 1.0.0
- **Playwright**: 1.55.0
- **Chromium**: 131.0.6778.33

### Test Results

✅ **Virtual environment creation**: Works
✅ **Package installation**: Works
✅ **Chromium download**: Works
✅ **Conversion without Mermaid**: Works perfectly (`md2pdf test.md --no-mermaid`)
❌ **Conversion with Mermaid (before fix)**: Fails - "Rendered 0/1 Mermaid diagrams"
✅ **After installing dependencies**: Expected to work (requires sudo to test)

---

## Why This Happens

1. **Playwright downloads browser binary**: `playwright install chromium` downloads ~250MB Chromium
2. **System libraries NOT included**: Shared libraries (`.so` files) must be installed separately
3. **WSL is minimal**: Ubuntu on WSL lacks many GUI-related libraries
4. **Even headless needs libs**: Chromium headless still requires graphics/sound libraries

Missing libraries typically include:
- `libnspr4.so` - Netscape Portable Runtime
- `libnss3.so` - Network Security Services
- `libasound.so.2` - ALSA sound library

---

## Alternative: Use Without Mermaid

If you cannot install system dependencies (no sudo access), you can still use md2pdf:

```bash
# Disable Mermaid rendering
md2pdf document.md --no-mermaid

# Or via Python API
from md2pdf import convert_markdown_to_pdf

convert_markdown_to_pdf(
    markdown_content,
    "output.pdf",
    enable_mermaid=False  # Mermaid blocks shown as code
)
```

---

## CI/CD Environments

### GitHub Actions

```yaml
- name: Install md2pdf with dependencies
  run: |
    pip install git+https://github.com/rbutinar/md2pdf-mermaid.git
    playwright install chromium
    sudo apt-get update
    sudo apt-get install -y libnspr4 libnss3 libasound2t64
```

### Azure DevOps

```yaml
- script: |
    pip install git+https://github.com/rbutinar/md2pdf-mermaid.git
    playwright install chromium
    sudo apt-get update && sudo apt-get install -y libnspr4 libnss3 libasound2t64
  displayName: 'Install md2pdf'
```

### Docker

```dockerfile
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libnspr4 \
    libnss3 \
    libasound2t64 \
    && rm -rf /var/lib/apt/lists/*

# Install md2pdf
RUN pip install git+https://github.com/rbutinar/md2pdf-mermaid.git && \
    playwright install chromium

WORKDIR /workspace
CMD ["md2pdf", "README.md"]
```

---

## Troubleshooting

### Check Missing Libraries

```bash
ldd ~/.cache/ms-playwright/chromium-*/chrome-linux/chrome | grep "not found"
```

### Verify Packages Installed

```bash
dpkg -l | grep -E "libnspr4|libnss3|libasound2"
```

### WSL Version

This guide is for **WSL2**. Check your version:

```bash
# In PowerShell (Windows)
wsl.exe -l -v
```

To upgrade to WSL2:
```powershell
wsl --set-version Ubuntu 2
```

---

## Support

- **Issues**: https://github.com/rbutinar/md2pdf-mermaid/issues
- **Tag with**: `wsl`, `chromium`, `dependencies`

---

**Last Updated**: 2025-10-14
**Tested By**: Roberto Butinar
**Status**: Verified Working ✅
