# Standalone Executables

Pre-built standalone binaries that work without Python. Download, run, done.

---

## Download

Get the latest release from [GitHub Releases](https://github.com/rbutinar/md2pdf-mermaid/releases).

| Platform | Architecture | File | Size |
|----------|-------------|------|------|
| macOS | Apple Silicon (M1/M2/M3/M4) | `md2pdf-macos-arm64.tar.gz` | ~50-80 MB |
| macOS | Intel | `md2pdf-macos-x86_64.tar.gz` | ~50-80 MB |
| Linux | x86_64 | `md2pdf-linux-x86_64.tar.gz` | ~50-80 MB |
| Windows | x86_64 | `md2pdf-windows-x86_64.zip` | ~50-80 MB |

---

## Quick Install (macOS & Linux)

One-line installer that downloads the correct binary for your platform and installs it to `/usr/local/bin`:

```bash
curl -fsSL https://raw.githubusercontent.com/rbutinar/md2pdf-mermaid/master/scripts/install.sh | bash
```

After installation, `md2pdf` is available system-wide. Done!

---

## Manual Installation

### macOS (Apple Silicon)

```bash
# Download and extract
curl -L -o md2pdf.tar.gz https://github.com/rbutinar/md2pdf-mermaid/releases/latest/download/md2pdf-macos-arm64.tar.gz
tar xzf md2pdf.tar.gz

# Make executable (if needed)
chmod +x md2pdf

# Install to PATH (so you can run 'md2pdf' from anywhere)
sudo mv md2pdf /usr/local/bin/
```

**macOS Gatekeeper:** On first run, macOS may block the binary. To allow it:
1. Open **System Settings > Privacy & Security**
2. Scroll down and click **Allow Anyway** next to the md2pdf message
3. Or run: `xattr -d com.apple.quarantine md2pdf`

### macOS (Intel)

Same steps as above, but download `md2pdf-macos-x86_64.tar.gz`.

### Linux

```bash
# Download and extract
curl -L -o md2pdf.tar.gz https://github.com/rbutinar/md2pdf-mermaid/releases/latest/download/md2pdf-linux-x86_64.tar.gz
tar xzf md2pdf.tar.gz

# Make executable and install to PATH
chmod +x md2pdf
sudo mv md2pdf /usr/local/bin/
```

**Note:** On some minimal Linux installations, Chromium may need additional system libraries. If the browser download succeeds but rendering fails, install the dependencies:

```bash
# Debian/Ubuntu
sudo apt-get install -y libnss3 libatk1.0-0 libatk-bridge2.0-0 \
  libcups2 libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 \
  libxrandr2 libgbm1 libpango-1.0-0 libcairo2 libasound2

# Fedora/RHEL
sudo dnf install -y nss atk at-spi2-atk cups-libs libdrm \
  libxkbcommon libXcomposite libXdamage libXrandr mesa-libgbm \
  pango cairo alsa-lib
```

### Windows

1. Download `md2pdf-windows-x86_64.zip` from the [releases page](https://github.com/rbutinar/md2pdf-mermaid/releases)
2. Extract the zip file
3. Open a terminal (Command Prompt or PowerShell) in the extracted folder

```powershell
# Run directly
.\md2pdf.exe document.md

# Optional: add to PATH
# Move md2pdf.exe to a folder in your PATH, or add its folder to PATH:
# System Settings > Environment Variables > Path > Edit > New
```

**Windows Defender:** The executable may be flagged on first run. Click **More info > Run anyway** to allow it.

---

## First Run

The standalone binary does **not** bundle Chromium (~150 MB) to keep the download small. Chromium is automatically downloaded on first use:

```
$ ./md2pdf document.md
Converting document.md to PDF...

Chromium browser not found. Downloading (~150 MB)...
This only happens once.

Downloading Chromium 131.0.6778.33 - 154.2 MB [=========>    ] 62%
...
Chromium installed successfully.

  (Using HTML/Chromium engine - full emoji support)
[OK] PDF created: document.pdf (142.3 KB)
```

### Pre-download Chromium

To download Chromium before your first conversion (useful for offline setups):

```bash
./md2pdf --setup-browser
```

### Browser Cache Location

Chromium is cached per-platform and reused across runs:

| Platform | Cache Path |
|----------|-----------|
| macOS | `~/Library/Caches/md2pdf/playwright/` |
| Linux | `~/.cache/md2pdf/playwright/` |
| Windows | `%LOCALAPPDATA%\md2pdf\playwright\` |

If you already have Playwright installed (e.g., from a Python environment), md2pdf reuses the existing Chromium installation automatically.

---

## Usage

All CLI options work identically to the pip-installed version:

```bash
# Basic conversion
./md2pdf document.md

# Custom output name
./md2pdf document.md -o report.pdf

# Custom title
./md2pdf document.md --title "Project Report"

# Page size and orientation
./md2pdf document.md --page-size letter --orientation landscape

# High-quality Mermaid diagrams with custom theme
./md2pdf document.md --mermaid-scale 3 --mermaid-theme forest

# Use legacy ReportLab engine (no browser needed)
./md2pdf document.md --engine reportlab --no-mermaid

# Disable Mermaid rendering
./md2pdf document.md --no-mermaid

# Show version
./md2pdf --version

# Show all options
./md2pdf --help
```

### Using Without a Browser

The ReportLab engine works without Chromium for basic conversions (no emoji, no Mermaid diagrams):

```bash
./md2pdf document.md --engine reportlab --no-mermaid
```

---

## Building From Source

If you want to build the standalone executable yourself:

### Prerequisites

- Python 3.8+ (3.12 recommended)
- pip

### Build Steps

```bash
# Clone the repository
git clone https://github.com/rbutinar/md2pdf-mermaid.git
cd md2pdf-mermaid

# Install dependencies
pip install -e ".[dev]"

# Run the build script
python scripts/build.py
```

The executable is created at `dist/md2pdf` (or `dist/md2pdf.exe` on Windows).

### Build Script Details

`scripts/build.py` handles:
- Running PyInstaller with the `md2pdf.spec` configuration
- Verifying the output binary works (`--version` check)
- Reporting the final binary size

### Manual PyInstaller Build

If you prefer to run PyInstaller directly:

```bash
pip install pyinstaller>=6.0
pyinstaller md2pdf.spec --clean --noconfirm
```

### What Gets Bundled

| Component | Included | Size |
|-----------|----------|------|
| Python runtime | Yes | ~15 MB |
| md2pdf code | Yes | < 1 MB |
| Playwright driver (Node.js) | Yes | ~30 MB |
| ReportLab | Yes | ~5 MB |
| Markdown + Pillow | Yes | ~5 MB |
| **Chromium browser** | **No** | ~150 MB (downloaded on first run) |

---

## CI/CD: Automated Builds

The repository includes a GitHub Actions workflow (`.github/workflows/build-executables.yml`) that automatically builds executables for all platforms.

### Trigger

- **Automatic:** Push a version tag (e.g., `v1.4.4`)
- **Manual:** Run from the GitHub Actions tab (workflow_dispatch)

### Build Matrix

| Runner | Artifact |
|--------|----------|
| `macos-13` | `md2pdf-macos-x86_64` |
| `macos-14` | `md2pdf-macos-arm64` |
| `ubuntu-22.04` | `md2pdf-linux-x86_64` |
| `windows-latest` | `md2pdf-windows-x86_64` |

### Release

When triggered by a version tag, the workflow:
1. Builds all 4 platform binaries
2. Creates tar.gz (macOS/Linux) and zip (Windows) archives
3. Publishes a GitHub Release with all archives attached

---

## Troubleshooting

### "Chromium browser not found" on every run

The browser cache directory may not be writable. Check permissions:

```bash
# macOS
ls -la ~/Library/Caches/md2pdf/

# Linux
ls -la ~/.cache/md2pdf/
```

### macOS: "md2pdf can't be opened because Apple cannot check it for malicious software"

Remove the quarantine attribute:

```bash
xattr -d com.apple.quarantine md2pdf
```

Or allow it via System Settings > Privacy & Security.

### Linux: Browser crashes or rendering fails

Install the required system libraries for Chromium (see the [Linux installation section](#linux) above).

### Windows: "Windows protected your PC" (SmartScreen)

Click **More info**, then **Run anyway**. This happens because the executable is not code-signed.

### Executable won't start / crashes immediately

1. Ensure you downloaded the correct platform binary (ARM64 vs x86_64)
2. On macOS, check if Rosetta 2 is installed for Intel binaries: `softwareupdate --install-rosetta`
3. Try running from a terminal to see error messages

### Browser download fails (network/proxy)

Pre-download Chromium in an environment with internet access:

```bash
./md2pdf --setup-browser
```

If behind a proxy, set the standard proxy environment variables:

```bash
export HTTPS_PROXY=http://proxy.example.com:8080
./md2pdf --setup-browser
```

### "Permission denied" when running on Linux/macOS

```bash
chmod +x md2pdf
```

### Converting without internet (offline use)

1. Run `./md2pdf --setup-browser` once while connected to the internet
2. After that, all conversions work offline
3. Exception: Mermaid diagrams load Mermaid.js from a CDN. For fully offline Mermaid support, use the pip-installed version

---

## Comparison: Standalone vs pip Install

| Feature | Standalone | pip install |
|---------|-----------|-------------|
| Requires Python | No | Yes |
| Install complexity | Download + extract | `pip install` + `playwright install` |
| Executable size | ~50-80 MB | N/A (uses system Python) |
| First-run browser download | Yes (~150 MB) | Manual (`playwright install chromium`) |
| Auto-updates | No (re-download new version) | `pip install --upgrade` |
| Python API | No (CLI only) | Yes |
| All CLI features | Yes | Yes |
| Offline Mermaid | No (CDN) | No (CDN) |
